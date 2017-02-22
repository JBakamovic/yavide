import sys
import os
import logging
import subprocess
import clang.cindex
from services.parser.ast_node_identifier import ASTNodeId

class ChildVisitResult(clang.cindex.BaseEnumeration):
    """
    A ChildVisitResult describes how the traversal of the children of a particular cursor should proceed after visiting a particular child cursor.
    """
    _kinds = []
    _name_map = None

    def __repr__(self):
        return 'ChildVisitResult.%s' % (self.name,)

ChildVisitResult.BREAK = ChildVisitResult(0) # Terminates the cursor traversal.
ChildVisitResult.CONTINUE = ChildVisitResult(1) # Continues the cursor traversal with the next sibling of the cursor just visited, without visiting its children.
ChildVisitResult.RECURSE = ChildVisitResult(2) # Recursively traverse the children of this cursor, using the same visitor and client data.

def default_visitor(child, parent, client_data):
    """Default implementation of AST node visitor."""

    return ChildVisitResult.CONTINUE.value

def traverse(self, client_data, client_visitor = default_visitor):
    """Traverse AST using the client provided visitor."""

    def visitor(child, parent, client_data):
        assert child != clang.cindex.conf.lib.clang_getNullCursor()
        child._tu = self._tu
        child.ast_parent = parent
        return client_visitor(child, parent, client_data)

    return clang.cindex.conf.lib.clang_visitChildren(self, clang.cindex.callbacks['cursor_visit'](visitor), client_data)

def get_children_patched(self, traversal_type = ChildVisitResult.CONTINUE):
    """
    Return an iterator for accessing the children of this cursor.
    This is a patched version of Cursor.get_children() but which is built on top of new traversal interface.
    See traverse() for more details.
    """

    def visitor(child, parent, children):
        children.append(child)
        return traversal_type.value

    children = []
    traverse(self, children, visitor)
    return iter(children)

"""
Monkey-patch the existing Cursor.get_children() with get_children_patched().
This is a temporary solution and should be removed once, and if, it becomes available in official libclang Python bindings.
New version provides more functionality (i.e. AST parent node) which is needed in certain cases.
"""
clang.cindex.Cursor.get_children = get_children_patched

def get_system_includes():
    output = subprocess.Popen(["g++", "-v", "-E", "-x", "c++", "-"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    pattern = ["#include <...> search starts here:", "End of search list."]
    output = str(output)
    return output[output.find(pattern[0]) + len(pattern[0]) : output.find(pattern[1])].replace(' ', '-I').split('\\n')

class ClangParser():
    def __init__(self):
        self.tunits = {}
        self.index = clang.cindex.Index.create()
        self.default_args = ['-x', 'c++', '-std=c++14'] + get_system_includes()

    def run(self, contents_filename, original_filename, compiler_args, project_root_directory):
        logging.info('Filename = {0}'.format(original_filename))
        logging.info('Contents Filename = {0}'.format(contents_filename))
        logging.info('Default args = {0}'.format(self.default_args))
        logging.info('User-provided compiler args = {0}'.format(compiler_args))
        logging.info('Compiler working-directory = {0}'.format(project_root_directory))
        try:
            # Parse the translation unit
            self.tunits[original_filename] = self.index.parse(
                path = contents_filename,
                args = self.default_args + compiler_args + ['-working-directory=' + project_root_directory],
                options = clang.cindex.TranslationUnit.PARSE_DETAILED_PROCESSING_RECORD # TODO CXTranslationUnit_KeepGoing?
            )

            # Inject new TU data member (list of AST nodes for given TU)
            self.tunits[original_filename].ast_node_list = []

            # Recursively visit all nodes
            self.__visit_all_nodes(self.tunits[original_filename].cursor, original_filename, contents_filename)

        except:
            logging.error(sys.exc_info()[0])

        logging.info("tunits: " + str(self.tunits))

    def get_diagnostics(self, filename):
        if filename in self.tunits:
            logging.info("get_diagnostics() for " + filename + " tunit: " + str(self.tunits[filename]))
            return self.tunits[filename].diagnostics
        return None

    def get_ast_node_list(self, filename):
        if filename in self.tunits:
            return self.tunits[filename].ast_node_list
        return []

    def get_ast_node_id(self, cursor):
        # We have to handle (at least) two different situations when libclang API will not give us enough details about the given cursor directly:
        #   1. When Cursor.TypeKind is DEPENDENT
        #       * Cursor.TypeKind happens to be set to DEPENDENT for constructs whose semantics may differ from one
        #         instantiation to another. These are called dependent names (see 14.6.2 [temp.dep] in C++ standard).
        #       * Example can be a call expression on non-instantiated function template, or even a reference to
        #         a data member of non-instantiated class template.
        #       * In this case we try to extract the right CursorKind by tokenizing the given cursor, selecting the
        #         right token and, depending on its position in the AST tree, return the right CursorKind information.
        #         See ClangParser.__extract_dependent_type_kind() for more details.
        #       * Similar actions have to be taken for extracting spelling and location for such cursors.
        #   2. When Cursor.Kind is OVERLOADED_DECL_REF
        #       * Cursor.Kind.OVERLOADED_DECL_REF basically identifies a reference to a set of overloaded functions
        #         or function templates which have not yet been resolved to a specific function or function template.
        #       * This means that token kind might be one of the following:
        #            Cursor.Kind.FUNCTION_DECL, Cursor.Kind.FUNCTION_TEMPLATE, Cursor.Kind.CXX_METHOD
        #       * To extract more information about the token we can use `clang_getNumOverloadedDecls()` to get how
        #         many overloads there are and then use `clang_getOverloadedDecl()` to get a specific overload.
        #       * In our case, we can always use the first overload which explains hard-coded 0 as an index.
        if cursor.type.kind == clang.cindex.TypeKind.DEPENDENT:
            return ClangParser.to_ast_node_id(ClangParser.__extract_dependent_type_kind(cursor))
        else:
            if cursor.referenced:
                if (cursor.referenced.kind == clang.cindex.CursorKind.OVERLOADED_DECL_REF):
                    if (ClangParser.__get_num_overloaded_decls(cursor.referenced)):
                        return ClangParser.to_ast_node_id(ClangParser.__get_overloaded_decl(cursor.referenced, 0).kind)
                return ClangParser.to_ast_node_id(cursor.referenced.kind)
            if (cursor.kind == clang.cindex.CursorKind.OVERLOADED_DECL_REF):
                if (ClangParser.__get_num_overloaded_decls(cursor)):
                    return ClangParser.to_ast_node_id(ClangParser.__get_overloaded_decl(cursor, 0).kind)
        return ClangParser.to_ast_node_id(cursor.kind)

    def get_ast_node_name(self, cursor):
        if cursor.type.kind == clang.cindex.TypeKind.DEPENDENT:
            return ClangParser.__extract_dependent_type_spelling(cursor)
        else:
            if (cursor.referenced):
                return cursor.referenced.spelling
            else:
                return cursor.spelling

    def get_ast_node_line(self, cursor):
        if cursor.type.kind == clang.cindex.TypeKind.DEPENDENT:
            return ClangParser.__extract_dependent_type_location(cursor).line
        return cursor.location.line

    def get_ast_node_column(self, cursor):
        if cursor.type.kind == clang.cindex.TypeKind.DEPENDENT:
            return ClangParser.__extract_dependent_type_location(cursor).column
        return cursor.location.column

    def map_source_location_to_type(self, original_filename, contents_filename, line, column):
        logging.info("Mapping source location to type for " + str(original_filename))

        if original_filename not in self.tunits:
            return ''

        cursor = clang.cindex.Cursor.from_location(
                    self.tunits[original_filename],
                    clang.cindex.SourceLocation.from_position(
                        self.tunits[original_filename],
                        clang.cindex.File.from_name(self.tunits[original_filename], contents_filename),
                        line,
                        column
                    )
                 )
        return cursor.type.spelling

    def get_definition(self, original_filename, contents_filename, line, column):
        if original_filename not in self.tunits:
            return None

        cursor = clang.cindex.Cursor.from_location(
                    self.tunits[original_filename],
                    clang.cindex.SourceLocation.from_position(
                        self.tunits[original_filename],
                        clang.cindex.File.from_name(self.tunits[original_filename], contents_filename),
                        line,
                        column
                    )
                 )
        return cursor.get_definition()

    def find_all_references(self, original_filename, contents_filename, line, column):
        if original_filename not in self.tunits:
            return []

        cursor = clang.cindex.Cursor.from_location(
                    self.tunits[original_filename],
                    clang.cindex.SourceLocation.from_position(
                        self.tunits[original_filename],
                        clang.cindex.File.from_name(self.tunits[original_filename], contents_filename),
                        line,
                        column
                    )
                 )

        references = []
        for tunit in self.tunits.itervalues():
            for ast_node in tunit.ast_node_list:
                if ast_node.spelling == cursor.spelling:
                    references.append(ast_node.location)
        return references

    def save_to_disk(self, root_dir):
        for filename, tunit in self.tunits.iteritems():
            directory = os.path.dirname(os.path.join(root_dir, filename[1:len(filename)]))
            if not os.path.exists(directory):
                os.makedirs(directory)
            logging.info('save_to_disk(): File = ' + os.path.join(root_dir, filename[1:len(filename)]))
            tunit.save(os.path.join(root_dir, filename[1:len(filename)]))

    def load_from_disk(self, root_dir):
        self.tunits.clear()
        for dirpath, dirs, files in os.walk(root_dir):
            for file in files:
                full_path = os.path.join(dirpath, file)
                logging.info('load_from_disk(): Full file path = ' + full_path)
                self.tunits[full_path[len(root_dir):]] = self.index.read(full_path)

    def drop_ast_node(self, filename):
        if filename in self.tunits:
            del self.tunits[filename]

    def drop_ast_node_list(self):
        self.tunits.clear()

    def dump_tokens(self, cursor):
        for token in cursor.get_tokens():
            logging.debug(
                '%-22s' % ('[' + str(token.extent.start.line) + ', ' + str(token.extent.start.column) + ']:[' + str(token.extent.end.line) + ', ' + str(token.extent.end.column) + ']') +
                '%-30s' % token.spelling +
                '%-40s' % str(token.kind) +
                '%-40s' % str(token.cursor.kind) +
                'Token.Cursor.Extent %-25s' % ('[' + str(token.cursor.extent.start.line) + ', ' + str(token.cursor.extent.start.column) + ']:[' + str(token.cursor.extent.end.line) + ', ' + str(token.cursor.extent.end.column) + ']') +
                'Cursor.Extent %-25s' % ('[' + str(cursor.extent.start.line) + ', ' + str(cursor.extent.start.column) + ']:[' + str(cursor.extent.end.line) + ', ' + str(cursor.extent.end.column) + ']'))

    def dump_ast_nodes(self, filename):
        if filename not in self.tunits:
            return

        logging.debug('%-12s' % '[Line, Col]' + '%-40s' % 'Spelling' + '%-40s' % 'Kind' + '%-40s' % 'Type.Spelling' +
                '%-40s' % 'Type.Kind' +
                '%-40s' % 'OverloadedDecl' + '%-40s' % 'NumOverloadedDecls' +
                '%-40s' % 'Referenced.Spelling' + '%-40s' % 'Referenced.Kind' +
                '%-40s' % 'Referenced.Type.Spelling' + '%-40s' % 'Referenced.Type.Kind' +
                '%-40s' % 'Referenced.ResultType.Spelling' + '%-40s' % 'Referenced.ResultType.Kind' +
                '%-40s' % 'Referenced.Canonical.Spelling' + '%-40s' % 'Referenced.Canonical.Kind' +
                '%-40s' % 'Referenced.SemanticParent.Spelling' + '%-40s' % 'Referenced.SemanticParent.Kind' +
                '%-40s' % 'Referenced.LexicalParent.Spelling' + '%-40s' % 'Referenced.LexicalParent.Kind')
        logging.debug('----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')

        for idx, cursor in enumerate(self.tunits[filename].ast_node_list):

            # if cursor.kind in [clang.cindex.CursorKind.CALL_EXPR, clang.cindex.CursorKind.MEMBER_REF_EXPR]:
            #    self.dump_tokens(cursor)

            logging.debug(
                '%-12s' % ('[' + str(cursor.location.line) + ', ' + str(cursor.location.column) + ']') +
                '%-40s' % str(cursor.spelling) +
                '%-40s' % str(cursor.kind) +
                '%-40s' % str(cursor.type.spelling) +
                '%-40s' % str(cursor.type.kind) +
                ('%-40s' % str(ClangParser.__get_overloaded_decl(cursor, 0).spelling) if (cursor.kind ==
                    clang.cindex.CursorKind.OVERLOADED_DECL_REF and ClangParser.__get_num_overloaded_decls(cursor)) else '%-40s' % '-') +
                ('%-40s' % str(ClangParser.__get_overloaded_decl(cursor, 0).kind) if (cursor.kind ==
                    clang.cindex.CursorKind.OVERLOADED_DECL_REF and ClangParser.__get_num_overloaded_decls(cursor)) else '%-40s' % '-') +
                ('%-40s' % str(cursor.referenced.spelling) if (cursor.referenced) else '%-40s' % '-') +
                ('%-40s' % str(cursor.referenced.kind) if (cursor.referenced) else '%-40s' % '-') +
                ('%-40s' % str(cursor.referenced.type.spelling) if (cursor.referenced) else '%-40s' % '-') +
                ('%-40s' % str(cursor.referenced.type.kind) if (cursor.referenced) else '%-40s' % '-') +
                ('%-40s' % str(cursor.referenced.result_type.spelling) if (cursor.referenced) else '%-40s' % '-') +
                ('%-40s' % str(cursor.referenced.result_type.kind) if (cursor.referenced) else '%-40s' % '-') +
                ('%-40s' % str(cursor.referenced.canonical.spelling) if (cursor.referenced) else '%-40s' % '-') +
                ('%-40s' % str(cursor.referenced.canonical.kind) if (cursor.referenced) else '%-40s' % '-') +
                ('%-40s' % str(cursor.referenced.semantic_parent.spelling) if (cursor.referenced and cursor.referenced.semantic_parent) else '%-40s' % '-') +
                ('%-40s' % str(cursor.referenced.semantic_parent.kind) if (cursor.referenced and cursor.referenced.semantic_parent) else '%-40s' % '-') +
                ('%-40s' % str(cursor.referenced.lexical_parent.spelling) if (cursor.referenced and cursor.referenced.lexical_parent) else '%-40s' % '-') +
                ('%-40s' % str(cursor.referenced.lexical_parent.kind) if (cursor.referenced and cursor.referenced.lexical_parent) else '%-40s' % '-'))

    def __visit_all_nodes(self, node, original_filename, contents_filename):
        for n in node.get_children():
            if n.location.file and n.location.file.name == contents_filename:
                self.tunits[original_filename].ast_node_list.append(n)
                self.__visit_all_nodes(n, original_filename, contents_filename)

    @staticmethod
    def __extract_dependent_type_kind(cursor):
        # For cursors whose CursorKind is MEMBER_REF_EXPR and whose TypeKind is DEPENDENT we don't get much information
        # from libclang API directly (i.e. cursor spelling will be empty).
        # Instead, we can extract such information indirectly by:
        #   1. Tokenizing the cursor
        #       * It will contain all the tokens that make up the MEMBER_REF_EXPR and therefore all the spellings, locations, extents, etc.
        #   2. Finding a token whose:
        #       * TokenKind is IDENTIFIER
        #       * CursorKind of a cursor that it corresponds to matches the MEMBER_REF_EXPR
        #       * Extent of a cursor that it corresponds to matches the extent of original cursor
        #   3. If CursorKind of original cursor AST parent is CALL_EXPR then we know that token found is CursorKind.CXX_METHOD
        #      If CursorKind of original cursor AST parent is not CALL_EXPR then we know that token found is CursorKind.FIELD_DECL
        assert cursor.type.kind == clang.cindex.TypeKind.DEPENDENT
        if cursor.kind == clang.cindex.CursorKind.MEMBER_REF_EXPR:
            if cursor.ast_parent and (cursor.ast_parent.kind == clang.cindex.CursorKind.CALL_EXPR):
                for token in cursor.get_tokens():
                    if (token.kind == clang.cindex.TokenKind.IDENTIFIER) and (token.cursor.kind == clang.cindex.CursorKind.MEMBER_REF_EXPR) and (token.cursor.extent == cursor.extent):
                        return clang.cindex.CursorKind.CXX_METHOD # We've got a function member call
            else:
                for token in cursor.get_tokens():
                    if (token.kind == clang.cindex.TokenKind.IDENTIFIER) and (token.cursor.kind == clang.cindex.CursorKind.MEMBER_REF_EXPR) and (token.cursor.extent == cursor.extent):
                        return clang.cindex.CursorKind.FIELD_DECL # We've got a data member
        return cursor.kind

    @staticmethod
    def __extract_dependent_type_spelling(cursor):
        # See __extract_dependent_type_kind() for more details but in essence we have to tokenize the cursor and
        # return the spelling of appropriate token.
        assert cursor.type.kind == clang.cindex.TypeKind.DEPENDENT
        if cursor.kind == clang.cindex.CursorKind.MEMBER_REF_EXPR:
            for token in cursor.get_tokens():
                if (token.kind == clang.cindex.TokenKind.IDENTIFIER) and (token.cursor.kind == clang.cindex.CursorKind.MEMBER_REF_EXPR) and (token.cursor.extent == cursor.extent):
                    return token.spelling
        return cursor.spelling

    @staticmethod
    def __extract_dependent_type_location(cursor):
        # See __extract_dependent_type_kind() for more details but in essence we have to tokenize the cursor and
        # return the location of appropriate token.
        assert cursor.type.kind == clang.cindex.TypeKind.DEPENDENT
        if cursor.kind == clang.cindex.CursorKind.MEMBER_REF_EXPR:
            for token in cursor.get_tokens():
                if (token.kind == clang.cindex.TokenKind.IDENTIFIER) and (token.cursor.kind == clang.cindex.CursorKind.MEMBER_REF_EXPR) and (token.cursor.extent == cursor.extent):
                    return token.location
        return cursor.location

    @staticmethod
    def to_ast_node_id(kind):
        if (kind == clang.cindex.CursorKind.NAMESPACE):
            return ASTNodeId.getNamespaceId()
        if (kind in [clang.cindex.CursorKind.CLASS_DECL, clang.cindex.CursorKind.CLASS_TEMPLATE, clang.cindex.CursorKind.CLASS_TEMPLATE_PARTIAL_SPECIALIZATION]):
            return ASTNodeId.getClassId()
        if (kind == clang.cindex.CursorKind.STRUCT_DECL):
            return ASTNodeId.getStructId()
        if (kind == clang.cindex.CursorKind.ENUM_DECL):
            return ASTNodeId.getEnumId()
        if (kind == clang.cindex.CursorKind.ENUM_CONSTANT_DECL):
            return ASTNodeId.getEnumValueId()
        if (kind == clang.cindex.CursorKind.UNION_DECL):
            return ASTNodeId.getUnionId()
        if (kind == clang.cindex.CursorKind.FIELD_DECL):
            return ASTNodeId.getFieldId()
        if (kind == clang.cindex.CursorKind.VAR_DECL):
            return ASTNodeId.getLocalVariableId()
        if (kind in [clang.cindex.CursorKind.FUNCTION_DECL, clang.cindex.CursorKind.FUNCTION_TEMPLATE]):
            return ASTNodeId.getFunctionId()
        if (kind in [clang.cindex.CursorKind.CXX_METHOD, clang.cindex.CursorKind.CONSTRUCTOR, clang.cindex.CursorKind.DESTRUCTOR]):
            return ASTNodeId.getMethodId()
        if (kind == clang.cindex.CursorKind.PARM_DECL):
            return ASTNodeId.getFunctionParameterId()
        if (kind == clang.cindex.CursorKind.TEMPLATE_TYPE_PARAMETER):
            return ASTNodeId.getTemplateTypeParameterId()
        if (kind == clang.cindex.CursorKind.TEMPLATE_NON_TYPE_PARAMETER):
            return ASTNodeId.getTemplateNonTypeParameterId()
        if (kind == clang.cindex.CursorKind.TEMPLATE_TEMPLATE_PARAMETER):
            return ASTNodeId.getTemplateTemplateParameterId()
        if (kind == clang.cindex.CursorKind.MACRO_DEFINITION):
            return ASTNodeId.getMacroDefinitionId()
        if (kind == clang.cindex.CursorKind.MACRO_INSTANTIATION):
            return ASTNodeId.getMacroInstantiationId()
        if (kind in [clang.cindex.CursorKind.TYPEDEF_DECL, clang.cindex.CursorKind.TYPE_ALIAS_DECL]):
            return ASTNodeId.getTypedefId()
        if (kind == clang.cindex.CursorKind.NAMESPACE_ALIAS):
            return ASTNodeId.getNamespaceAliasId()
        if (kind == clang.cindex.CursorKind.USING_DIRECTIVE):
            return ASTNodeId.getUsingDirectiveId()
        if (kind == clang.cindex.CursorKind.USING_DECLARATION):
            return ASTNodeId.getUsingDeclarationId()
        return ASTNodeId.getUnsupportedId()

    # TODO Shall be removed once 'cindex.py' exposes it in its interface.
    @staticmethod
    def __get_num_overloaded_decls(cursor):
        return clang.cindex.conf.lib.clang_getNumOverloadedDecls(cursor)

    # TODO Shall be removed once 'cindex.py' exposes it in its interface.
    @staticmethod
    def __get_overloaded_decl(cursor, num):
        return clang.cindex.conf.lib.clang_getOverloadedDecl(cursor, num)
