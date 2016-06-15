import sys
import shlex
import logging
import os.path
from subprocess import call
from services.syntax_highlighter.tag_identifier import TagIdentifier

class TagGenerator():
    def __init__(self, tag_id_list, tag_db_path):
        self.tag_id_list = tag_id_list
        self.tag_db_path = tag_db_path

    def run(self, path):
        self.__generate_ctags_db(path)

    def is_header(self, tag_line):
        if tag_line.startswith("!_TAG_"): # ctags tag file header
            return True
        else:
            return False

    def get_tag_id(self, tag_line):
        s = tag_line.split()
        if s:
            return CtagsTagGenerator.to_tag_id(s[len(s)-1])
        else:
            return ""

    def get_tag_name(self, tag_line):
        s = tag_line.split()
        if s:
            return s[0]
        else:
            return ""

    def __generate_ctags_db(self, path):
        if os.path.exists(path):
            cmd = 'ctags --languages=C,C++ --fields=K --extra=-fq ' + '--c++-kinds=' + self.__tag_id_list_to_ctags_kinds_list() + ' -f ' + self.tag_db_path + ' '
            if os.path.isdir(path):
                cmd += '-R '
            cmd += path
            logging.info("Generating the db: '{0}'".format(cmd))
            call(shlex.split(cmd))
        else:
            logging.error("Non-existing path '{0}'.".format(path))

    def __tag_id_list_to_ctags_kinds_list(self):
        ctags_kind_list = ''
        for tag_id in self.tag_id_list:
            ctags_kind_list += CtagsTagGenerator.from_tag_id(tag_id)
        return ctags_kind_list

class CtagsTagGenerator():
    @staticmethod
    def to_tag_id(kind):
        if (kind == "namespace"):
            return TagIdentifier.getNamespaceId()
        if (kind == "class"):
            return TagIdentifier.getClassId()
        if (kind == "struct"):
            return TagIdentifier.getStructId()
        if (kind == "enum"):
            return TagIdentifier.getEnumId()
        if (kind == "enumerator"):
            return TagIdentifier.getEnumValueId()
        if (kind == "union"):
            return TagIdentifier.getUnionId()
        if (kind == "member"):
            return TagIdentifier.getClassStructUnionMemberId()
        if (kind == "local"):
            return TagIdentifier.getLocalVariableId()
        if (kind == "variable"):
            return TagIdentifier.getVariableDefinitionId()
        if (kind == "prototype"):
            return TagIdentifier.getFunctionPrototypeId()
        if (kind == "function"):
            return TagIdentifier.getFunctionDefinitionId()
        if (kind == "macro"):
            return TagIdentifier.getMacroId()
        if (kind == "typedef"):
            return TagIdentifier.getTypedefId()
        if (kind == "externvar"):
            return TagIdentifier.getExternFwdDeclarationId()

    @staticmethod
    def from_tag_id(tag_id):
        if tag_id == TagIdentifier.getNamespaceId():
            return "n"
        if tag_id == TagIdentifier.getClassId():
            return "c"
        if tag_id == TagIdentifier.getStructId():
            return "s"
        if tag_id == TagIdentifier.getEnumId():
            return "g"
        if tag_id == TagIdentifier.getEnumValueId():
            return "e"
        if tag_id == TagIdentifier.getUnionId():
            return "u"
        if tag_id == TagIdentifier.getClassStructUnionMemberId():
            return "m"
        if tag_id == TagIdentifier.getLocalVariableId():
            return "l"
        if tag_id == TagIdentifier.getVariableDefinitionId():
            return "v"
        if tag_id == TagIdentifier.getFunctionPrototypeId():
            return "p"
        if tag_id == TagIdentifier.getFunctionDefinitionId():
            return "f"
        if tag_id == TagIdentifier.getMacroId():
            return "d"
        if tag_id == TagIdentifier.getTypedefId():
            return "t"
        if tag_id == TagIdentifier.getExternFwdDeclarationId():
            return "x"

