import sys
import logging
import clang.cindex
from services.syntax_highlighter.tag_identifier import TagIdentifier

class ClangTokenizer():
    def __init__(self, tag_id_list):
        self.tag_id_list = tag_id_list
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
            return self.__to_tag_id(token.referenced.kind)
        return self.__to_tag_id(token.kind)

    def get_token_name(self, token):
        if (token.referenced):
            return token.referenced.spelling
        else:
            return token.spelling

    def __visit_all_nodes(self, node):
        for n in node.get_children():
            if n.location.file and n.location.file.name == self.filename:
                self.token_list.append(n)
                self.__visit_all_nodes(n)

    def __to_tag_id(self, kind):
        if (kind in [clang.cindex.CursorKind.NAMESPACE, clang.cindex.CursorKind.NAMESPACE_REF]):
            return TagIdentifier.getNamespaceId()
        if (kind in [clang.cindex.CursorKind.CLASS_DECL, clang.cindex.CursorKind.CLASS_TEMPLATE, clang.cindex.CursorKind.CLASS_TEMPLATE_PARTIAL_SPECIALIZATION]):
            return TagIdentifier.getClassId()
        if (kind == clang.cindex.CursorKind.STRUCT_DECL):
            return TagIdentifier.getStructId()
        if (kind == clang.cindex.CursorKind.ENUM_DECL):
            return TagIdentifier.getEnumId()
        if (kind == clang.cindex.CursorKind.ENUM_CONSTANT_DECL):
            return TagIdentifier.getEnumValueId()
        if (kind == clang.cindex.CursorKind.UNION_DECL):
            return TagIdentifier.getUnionId()
        if (kind == clang.cindex.CursorKind.FIELD_DECL):
            return TagIdentifier.getClassStructUnionMemberId()
        if (kind in [clang.cindex.CursorKind.VAR_DECL, clang.cindex.CursorKind.PARM_DECL, clang.cindex.CursorKind.TEMPLATE_TYPE_PARAMETER, clang.cindex.CursorKind.TEMPLATE_NON_TYPE_PARAMETER]):
            return TagIdentifier.getLocalVariableId()
        #if (kind == clang.cindex.CursorKind.):
        #    return TagIdentifier.getVariableDefinitionId()
        if (kind in [clang.cindex.CursorKind.FUNCTION_DECL, clang.cindex.CursorKind.FUNCTION_TEMPLATE]):
            return TagIdentifier.getFunctionPrototypeId()
        if (kind == clang.cindex.CursorKind.CXX_METHOD):
            return TagIdentifier.getFunctionPrototypeId()
        #if (kind == clang.cindex.CursorKind.):
        #    return TagIdentifier.getFunctionDefinitionId()
        #if (kind == clang.cindex.CursorKind.PREPROCESSING_DIRECTIVE):
        #    return TagIdentifier.getMacroId()
        if (kind == clang.cindex.CursorKind.TYPEDEF_DECL):
            return TagIdentifier.getTypedefId()
        #if (kind == clang.cindex.CursorKind.):
        #    return TagIdentifier.getExternFwdDeclarationId()
        return TagIdentifier.getUnsupportedId()

#print 'Includes: '
#file_inclusion_list = tu.get_includes()
#for finc in file_inclusion_list:
#    print "Source: ", finc.source, " Location: ", finc.location, " Include: ", finc.include

