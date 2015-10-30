import sys
import argparse
import os.path
from syntax.syntax_highlighter.tag_identifier import TagIdentifier
from syntax.syntax_highlighter.tag_generator import TagManagerFactory

class VimSyntaxTag:
    def __init__(self, tag_id, tag_manager_instance):
        self.tag_id = tag_id
        self.tag_manager_instance = tag_manager_instance

    def get_instance(self):
        return self.tag_manager_instance

    def get_id(self):
        return self.tag_id


class VimSyntaxHighlighter:
    def __init__(self, tag_id_list, file_to_be_highlighted, output_directory):
        self.file_to_be_highlighted = file_to_be_highlighted
        self.output_directory = output_directory
        self.tag_manager_list = list()
        self.__instantiate_syntax_tag_manager_list(tag_id_list)

    def generate_vim_syntax_file(self):
        for tag_manager in self.tag_manager_list:
            tag_manager.get_instance().run()
            with open(tag_manager.get_instance().get_sanitized_tag_db_path()) as tag_db:
                vim_highlight_rules = []
                for tag in tag_db.readlines():
                    highlight_rule = "syntax keyword " + self.__tag_id_to_vim_syntax_group(tag_manager.get_id()) + " " + tag
                    vim_highlight_rules.append(highlight_rule)
                generated_vim_syntax_file = os.path.join(self.output_directory, self.__tag_id_to_vim_syntax_group(tag_manager.get_id()) + ".vim")
                vim_syntax_file = open(generated_vim_syntax_file, "w")
                vim_syntax_file.writelines(vim_highlight_rules)
   
    def __instantiate_syntax_tag_manager_list(self, tag_id_list):
        for tag_id in tag_id_list:
            self.tag_manager_list.append(
                    VimSyntaxTag(
                        tag_id, 
                        TagManagerFactory.getTagManager("Cxx", tag_id, self.file_to_be_highlighted)
                    )
            )

    def __tag_id_to_vim_syntax_group(self, tag_identifier):
        if tag_identifier == TagIdentifier.getNamespaceId():
            return "yavideCppNamespace"
        if tag_identifier == TagIdentifier.getClassId():
            return "yavideCppClass"
        if tag_identifier == TagIdentifier.getStructId():
            return "yavideCppStructure"
        if tag_identifier == TagIdentifier.getEnumId():
            return "yavideCppEnum"
        if tag_identifier == TagIdentifier.getEnumValueId():
            return "yavideCppEnumValue"
        if tag_identifier == TagIdentifier.getUnionId():
            return "yavideCppUnion"
        if tag_identifier == TagIdentifier.getClassStructUnionMemberId():
            return "yavideCppClassStructUnionMember"
        if tag_identifier == TagIdentifier.getLocalVariableId():
            return "yavideCppLocalVariable"
        if tag_identifier == TagIdentifier.getVariableDefinitionId():
            return "yavideCppVariableDefinition"
        if tag_identifier == TagIdentifier.getFunctionPrototypeId():
            return "yavideCppFunctionPrototype"
        if tag_identifier == TagIdentifier.getFunctionDefinitionId():
            return "yavideCppFunctionDefinition"
        if tag_identifier == TagIdentifier.getMacroId():
            return "yavideCppMacro"
        if tag_identifier == TagIdentifier.getTypedefId():
            return "yavideCppTypedef"
        if tag_identifier == TagIdentifier.getExternFwdDeclarationId():
            return "yavideCppExternForwardDeclaration"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n",       "--" + TagIdentifier.getNamespaceId(),                help="enable namespace highlighting",                       action="store_true")
    parser.add_argument("-c",       "--" + TagIdentifier.getClassId(),                    help="enable class highlighting",                           action="store_true")
    parser.add_argument("-s",       "--" + TagIdentifier.getStructId(),                   help="enable struct highlighting",                          action="store_true")
    parser.add_argument("-e",       "--" + TagIdentifier.getEnumId(),                     help="enable enum highlighting",                            action="store_true")
    parser.add_argument("-ev",      "--" + TagIdentifier.getEnumValueId(),                help="enable enum values highlighting",                     action="store_true")
    parser.add_argument("-u",       "--" + TagIdentifier.getUnionId(),                    help="enable union highlighting",                           action="store_true")
    parser.add_argument("-cusm",    "--" + TagIdentifier.getClassStructUnionMemberId(),   help="enable class/union/struct member highlighting",       action="store_true")
    parser.add_argument("-lv",      "--" + TagIdentifier.getLocalVariableId(),            help="enable local variable highlighting",                  action="store_true")
    parser.add_argument("-vd",      "--" + TagIdentifier.getVariableDefinitionId(),       help="enable variable definition highlighting",             action="store_true")
    parser.add_argument("-fp",      "--" + TagIdentifier.getFunctionPrototypeId(),        help="enable function declaration highlighting",            action="store_true")
    parser.add_argument("-fd",      "--" + TagIdentifier.getFunctionDefinitionId(),       help="enable function definition highlighting",             action="store_true")
    parser.add_argument("-t",       "--" + TagIdentifier.getTypedefId(),                  help="enable typedef highlighting",                         action="store_true")
    parser.add_argument("-m",       "--" + TagIdentifier.getMacroId(),                    help="enable macro highlighting",                           action="store_true")
    parser.add_argument("-efwd",    "--" + TagIdentifier.getExternFwdDeclarationId(),     help="enable extern & forward declaration highlighting",    action="store_true")
    parser.add_argument("filename",                                                       help="source code file to generate the source code highlighting for")
    parser.add_argument("output_directory",                                               help="directory where the generated Vim syntax file will be stored")
    args = parser.parse_args()
    args_dict = vars(args)

    tag_id_list = list()
    for key, value in args_dict.iteritems():
        if value == True:
            tag_id_list.append(key)

    vimHighlighter = VimSyntaxHighlighter(tag_id_list, args.filename, args.output_directory)
    vimHighlighter.generate_vim_syntax_file()
 
if __name__ == "__main__":
    main()

