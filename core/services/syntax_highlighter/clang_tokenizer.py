import sys
import logging
import subprocess
import clang.cindex
from services.syntax_highlighter.token_identifier import TokenIdentifier

def get_system_includes():
    output = subprocess.Popen(["clang", "-v", "-E", "-x", "c++", "-"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    pattern = ["#include <...> search starts here:", "End of search list."]
    output = str(output)
    return output[output.find(pattern[0]) + len(pattern[0]) : output.find(pattern[1])].replace(' ', '-I').split('\\n')

class ClangTokenizer():
    def __init__(self):
        self.source_filename = ''
        self.token_list = []
        self.index = clang.cindex.Index.create()
        self.default_args = ['-x', 'c++', '-std=c++14'] + get_system_includes()

    def run(self, source_filename, contents_modified_flag, contents):
        self.source_filename = source_filename
        self.token_list = []
        logging.info('Filename = {0}'.format(self.source_filename))
        logging.info('Args = {0}'.format(self.default_args))
        translation_unit = self.index.parse(
            path = self.source_filename,
            args = self.default_args,
            unsaved_files = [(source_filename, contents)] if contents_modified_flag else None,
            options = clang.cindex.TranslationUnit.PARSE_DETAILED_PROCESSING_RECORD
        )

        diag = translation_unit.diagnostics
        for d in diag:
            logging.info('Parsing error: ' + str(d))

        logging.info('Translation unit: '.format(translation_unit.spelling))
        self.__visit_all_nodes(translation_unit.cursor)

    def get_token_list(self):
        return self.token_list

    def get_token_id(self, token):
        if token.referenced:
            return ClangTokenizer.to_token_id(token.referenced.kind)
        return ClangTokenizer.to_token_id(token.kind)

    def get_token_name(self, token):
        if (token.referenced):
            return token.referenced.spelling
        else:
            return token.spelling

    def get_token_line(self, token):
        return token.location.line

    def get_token_column(self, token):
        return token.location.column

    def dump_token_list(self):
        for idx, token in enumerate(self.token_list):
            logging.debug(
                '%-12s' % ('[' + str(token.location.line) + ', ' + str(token.location.column) + ']') +
                '%-40s ' % str(token.spelling) +
                '%-40s ' % str(token.kind) +
                ('%-40s ' % str(token.referenced.spelling) if (token.kind.is_reference()) else '') +
                ('%-40s ' % str(token.referenced.kind) if (token.kind.is_reference()) else ''))  

    def __visit_all_nodes(self, node):
        for n in node.get_children():
            if n.location.file and n.location.file.name == self.source_filename:
                self.token_list.append(n)
                self.__visit_all_nodes(n)

    @staticmethod
    def to_token_id(kind):
        if (kind == clang.cindex.CursorKind.NAMESPACE):
            return TokenIdentifier.getNamespaceId()
        if (kind in [clang.cindex.CursorKind.CLASS_DECL, clang.cindex.CursorKind.CLASS_TEMPLATE, clang.cindex.CursorKind.CLASS_TEMPLATE_PARTIAL_SPECIALIZATION]):
            return TokenIdentifier.getClassId()
        if (kind == clang.cindex.CursorKind.STRUCT_DECL):
            return TokenIdentifier.getStructId()
        if (kind == clang.cindex.CursorKind.ENUM_DECL):
            return TokenIdentifier.getEnumId()
        if (kind == clang.cindex.CursorKind.ENUM_CONSTANT_DECL):
            return TokenIdentifier.getEnumValueId()
        if (kind == clang.cindex.CursorKind.UNION_DECL):
            return TokenIdentifier.getUnionId()
        if (kind == clang.cindex.CursorKind.FIELD_DECL):
            return TokenIdentifier.getFieldId()
        if (kind == clang.cindex.CursorKind.VAR_DECL):
            return TokenIdentifier.getLocalVariableId()
        if (kind in [clang.cindex.CursorKind.FUNCTION_DECL, clang.cindex.CursorKind.FUNCTION_TEMPLATE]):
            return TokenIdentifier.getFunctionId()
        if (kind in [clang.cindex.CursorKind.CXX_METHOD, clang.cindex.CursorKind.CONSTRUCTOR, clang.cindex.CursorKind.DESTRUCTOR]):
            return TokenIdentifier.getMethodId()
        if (kind == clang.cindex.CursorKind.PARM_DECL):
            return TokenIdentifier.getFunctionParameterId()
        if (kind == clang.cindex.CursorKind.TEMPLATE_TYPE_PARAMETER):
            return TokenIdentifier.getTemplateTypeParameterId()
        if (kind == clang.cindex.CursorKind.TEMPLATE_NON_TYPE_PARAMETER):
            return TokenIdentifier.getTemplateNonTypeParameterId()
        if (kind == clang.cindex.CursorKind.TEMPLATE_TEMPLATE_PARAMETER):
            return TokenIdentifier.getTemplateTemplateParameterId()
        if (kind == clang.cindex.CursorKind.MACRO_DEFINITION):
            return TokenIdentifier.getMacroDefinitionId()
        if (kind == clang.cindex.CursorKind.MACRO_INSTANTIATION):
            return TokenIdentifier.getMacroInstantiationId()
        if (kind in [clang.cindex.CursorKind.TYPEDEF_DECL, clang.cindex.CursorKind.TYPE_ALIAS_DECL]):
            return TokenIdentifier.getTypedefId()
        if (kind == clang.cindex.CursorKind.NAMESPACE_ALIAS):
            return TokenIdentifier.getNamespaceAliasId()
        if (kind == clang.cindex.CursorKind.USING_DIRECTIVE):
            return TokenIdentifier.getUsingDirectiveId()
        if (kind == clang.cindex.CursorKind.USING_DECLARATION):
            return TokenIdentifier.getUsingDeclarationId()
        return TokenIdentifier.getUnsupportedId()

