import sys
import shlex
import logging
import os.path
from subprocess import call
from services.parser.ast_node_identifier import ASTNodeId

class CtagsTokenizer():
    def __init__(self, tag_db_path):
        self.tag_db_path = tag_db_path

    def run(self, path):
        self.__generate_ctags_db(path)

    def is_header(self, tag_line):
        if tag_line.startswith("!_TAG_"): # ctags tag file header
            return True
        else:
            return False

    def get_token_id(self, tag_line):
        s = tag_line.split()
        if s:
            return CtagsTokenizer.to_token_id(s[len(s)-1])
        else:
            return ""

    def get_token_name(self, tag_line):
        s = tag_line.split()
        if s:
            return s[0]
        else:
            return ""

    def __generate_ctags_db(self, path):
        if os.path.exists(path):
            cmd = 'ctags --languages=C,C++ --fields=K --extra=-fq ' + '--c++-kinds=ncsgeumlvpfdtx' + ' -f ' + self.tag_db_path + ' '
            if os.path.isdir(path):
                cmd += '-R '
            cmd += path
            logging.info("Generating the db: '{0}'".format(cmd))
            call(shlex.split(cmd))
        else:
            logging.error("Non-existing path '{0}'.".format(path))

    @staticmethod
    def to_token_id(kind):
        if (kind == "namespace"):
            return ASTNodeId.getNamespaceId()
        if (kind == "class"):
            return ASTNodeId.getClassId()
        if (kind == "struct"):
            return ASTNodeId.getStructId()
        if (kind == "enum"):
            return ASTNodeId.getEnumId()
        if (kind == "enumerator"):
            return ASTNodeId.getEnumValueId()
        if (kind == "union"):
            return ASTNodeId.getUnionId()
        if (kind == "member"):
            return ASTNodeId.getClassStructUnionMemberId()
        if (kind == "local"):
            return ASTNodeId.getLocalVariableId()
        if (kind == "variable"):
            return ASTNodeId.getVariableDefinitionId()
        if (kind == "prototype"):
            return ASTNodeId.getFunctionPrototypeId()
        if (kind == "function"):
            return ASTNodeId.getFunctionDefinitionId()
        if (kind == "macro"):
            return ASTNodeId.getMacroId()
        if (kind == "typedef"):
            return ASTNodeId.getTypedefId()
        if (kind == "externvar"):
            return ASTNodeId.getExternFwdDeclarationId()
