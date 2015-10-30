import sys
import shlex
import re
import logging
import os.path
from sets import Set
from subprocess import call
from syntax.syntax_highlighter.tag_identifier import TagIdentifier

# TODO class TagSanitizer:
#           def extract(self):
#
#      etc.
#

class TagGenerator():
    def __init__(self, root_directory, tag_type, tag_db_path, sanitized_tag_db_path):
        self.root_directory = root_directory
        self.tag_type = tag_type
        self.tag_db_path = tag_db_path
        self.sanitized_tag_db_path = sanitized_tag_db_path

    def run(self):
        self.__generate_tag_db()
        self.__extract()

    def get_sanitized_tag_db_path(self):
        return self.sanitized_tag_db_path

    def delete_tag_db(self):
        # TODO
        return

    def __extract(self):
        if os.path.exists(self.tag_db_path):
            with open(self.tag_db_path) as f:
                lines = f.readlines()
                symbol = Set()
                for l in lines:
                    if not l.startswith("!_TAG_"): # ignore the ctags tag file information
                        #if not "access:private" in l: # only take into account tags which are not declared as private/protected
                        #    if not "access:protected" in l:
                        #        if not "~" in l[0][0]: # we don't want destructors to be in the list
                        symbol.add(re.split(r'\t+', l)[0])
                out = open(self.sanitized_tag_db_path, "w")
                out.write("\n".join(symbol))
        else:
            logging.error("Non-existing filename or directory '{0}'.".format(self.tag_db_path))

    def __generate_tag_db(self):
        if os.path.exists(self.root_directory):
            cmd  = 'ctags --languages=C++ --fields=a --extra=-fq ' + '--c++-kinds=' + self.tag_type  + ' -f ' + self.tag_db_path + ' -R ' + self.root_directory
            logging.info("Generating the db: '{0}'".format(cmd))
            call(shlex.split(cmd))
        else:
            logging.error("Non-existing directory '{0}'.".format(self.root_directory))
   
class NamespaceTagManager(TagGenerator):
    def __init__(self, root_directory):
        TagGenerator.__init__(self, root_directory, "n", "/tmp/tags-namespace", "/tmp/tags-namespace-processed")

class ClassTagManager(TagGenerator):
    def __init__(self, root_directory):
        TagGenerator.__init__(self, root_directory, "c", "/tmp/tags-class", "/tmp/tags-class-processed")

class StructTagManager(TagGenerator):
    def __init__(self, root_directory):
        TagGenerator.__init__(self, root_directory, "s", "/tmp/tags-struct", "/tmp/tags-struct-processed")

class EnumTagManager(TagGenerator):
    def __init__(self, root_directory):
        TagGenerator.__init__(self, root_directory, "g", "/tmp/tags-enum", "/tmp/tags-enum-processed")

class EnumValueTagManager(TagGenerator):
    def __init__(self, root_directory):
        TagGenerator.__init__(self, root_directory, "e", "/tmp/tags-enum-value", "/tmp/tags-enum-value-processed")

class UnionTagManager(TagGenerator):
    def __init__(self, root_directory):
        TagGenerator.__init__(self, root_directory, "u", "/tmp/tags-union", "/tmp/tags-union-processed")

class ClassStructUnionMemberTagManager(TagGenerator):
    def __init__(self, root_directory):
        TagGenerator.__init__(self, root_directory, "m", "/tmp/tags-class-struct-union-member", "/tmp/tags-class-struct-union-member-processed")

class LocalVariableTagManager(TagGenerator):
    def __init__(self, root_directory):
        TagGenerator.__init__(self, root_directory, "l", "/tmp/tags-local-variable", "/tmp/tags-local-variable-processed")

class VariableDefinitionTagManager(TagGenerator):
    def __init__(self, root_directory):
        TagGenerator.__init__(self, root_directory, "v", "/tmp/tags-variable", "/tmp/tags-variable-processed")

class FunctionPrototypeTagManager(TagGenerator):
    def __init__(self, root_directory):
        TagGenerator.__init__(self, root_directory, "p", "/tmp/tags-func-proto", "/tmp/tags-func-proto-processed")

class FunctionDefinitionTagManager(TagGenerator):
    def __init__(self, root_directory):
        TagGenerator.__init__(self, root_directory, "f", "/tmp/tags-func", "/tmp/tags-func-processed")

class MacroTagManager(TagGenerator):
    def __init__(self, root_directory):
        TagGenerator.__init__(self, root_directory, "d", "/tmp/tags-macro", "/tmp/tags-macro-processed")

class TypedefTagManager(TagGenerator):
    def __init__(self, root_directory):
        TagGenerator.__init__(self, root_directory, "t", "/tmp/tags-typedef", "/tmp/tags-typedef-processed")

class ExternForwardDeclarationTagManager(TagGenerator):
    def __init__(self, root_directory):
        TagGenerator.__init__(self, root_directory, "x", "/tmp/tags-extern-fwd", "/tmp/tags-extern-fwd-processed")

class TagManagerFactory():
    @staticmethod
    def getTagManager(programming_language, tag_identifier, filename):
        if (programming_language == 'Cxx'):
            if tag_identifier == TagIdentifier.getNamespaceId():
                return NamespaceTagManager(filename) 
            if tag_identifier == TagIdentifier.getClassId():
                return ClassTagManager(filename) 
            if tag_identifier == TagIdentifier.getStructId():
                return StructTagManager(filename)
            if tag_identifier == TagIdentifier.getEnumId():
                return EnumTagManager(filename)
            if tag_identifier == TagIdentifier.getEnumValueId():
                return EnumValueTagManager(filename)
            if tag_identifier == TagIdentifier.getUnionId():
                return UnionTagManager(filename)
            if tag_identifier == TagIdentifier.getClassStructUnionMemberId():
                return ClassStructUnionMemberTagManager(filename)
            if tag_identifier == TagIdentifier.getLocalVariableId():
                return LocalVariableTagManager(filename)
            if tag_identifier == TagIdentifier.getVariableDefinitionId():
                return VariableDefinitionTagManager(filename)
            if tag_identifier == TagIdentifier.getFunctionPrototypeId():
                return FunctionPrototypeTagManager(filename)
            if tag_identifier == TagIdentifier.getFunctionDefinitionId():
                return FunctionDefinitionTagManager(filename)
            if tag_identifier == TagIdentifier.getMacroId():
                return MacroTagManager(filename) 
            if tag_identifier == TagIdentifier.getTypedefId():
                return TypedefTagManager(filename)
            if tag_identifier == TagIdentifier.getExternFwdDeclarationId():
                return ExternForwardDeclarationTagManager(filename)
        else:
            return None

