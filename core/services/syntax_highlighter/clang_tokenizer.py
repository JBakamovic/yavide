import sys
import logging
import clang.cindex
from services.syntax_highlighter.token_identifier import TokenIdentifier

class ClangTokenizer():
    def __init__(self):
        self.filename = ''
        self.token_list = []
        self.index = clang.cindex.Index.create()

    def run(self, filename):
        self.filename = filename
        self.token_list = []
        logging.info('Filename = {0}'.format(self.filename))
        translation_unit = self.index.parse(self.filename, ['-x', 'c++', '-std=c++14',
            '-I', '/usr/bin/../lib64/clang/3.8.0/include',
            '-I', '/usr/include',
            '-I', '/usr/bin/../lib/gcc/x86_64-redhat-linux/6.2.1/../../../../include/c++/6.2.1',
            '-I', '/usr/bin/../lib/gcc/x86_64-redhat-linux/6.2.1/../../../../include/c++/6.2.1/x86_64-redhat-linux',
            '-I', '/usr/bin/../lib/gcc/x86_64-redhat-linux/6.2.1/../../../../include/c++/6.2.1/backward',
            '-I', '/usr/local/include'])
#            ])

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
            if n.location.file and n.location.file.name == self.filename:
                self.token_list.append(n)
                self.__visit_all_nodes(n)

    @staticmethod
    def to_token_id(kind):
        if (kind in [clang.cindex.CursorKind.NAMESPACE, clang.cindex.CursorKind.NAMESPACE_REF]):
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
            return TokenIdentifier.getClassStructUnionMemberId()
        if (kind in [clang.cindex.CursorKind.VAR_DECL, clang.cindex.CursorKind.PARM_DECL, clang.cindex.CursorKind.TEMPLATE_TYPE_PARAMETER, clang.cindex.CursorKind.TEMPLATE_NON_TYPE_PARAMETER]):
            return TokenIdentifier.getLocalVariableId()
        #if (kind == clang.cindex.CursorKind.):
        #    return TokenIdentifier.getVariableDefinitionId()
        if (kind in [clang.cindex.CursorKind.FUNCTION_DECL, clang.cindex.CursorKind.FUNCTION_TEMPLATE]):
            return TokenIdentifier.getFunctionPrototypeId()
        if (kind == clang.cindex.CursorKind.CXX_METHOD):
            return TokenIdentifier.getFunctionPrototypeId()
        #if (kind == clang.cindex.CursorKind.):
        #    return TokenIdentifier.getFunctionDefinitionId()
        #if (kind == clang.cindex.CursorKind.PREPROCESSING_DIRECTIVE):
        #    return TokenIdentifier.getMacroId()
        if (kind == clang.cindex.CursorKind.TYPEDEF_DECL):
            return TokenIdentifier.getTypedefId()
        #if (kind == clang.cindex.CursorKind.):
        #    return TokenIdentifier.getExternFwdDeclarationId()
        return TokenIdentifier.getUnsupportedId()

#print 'Includes: '
#file_inclusion_list = tu.get_includes()
#for finc in file_inclusion_list:
#    print "Source: ", finc.source, " Location: ", finc.location, " Include: ", finc.include

