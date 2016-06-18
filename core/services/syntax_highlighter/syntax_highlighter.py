import sys
import argparse
import logging
from services.syntax_highlighter.tag_identifier import TagIdentifier
from services.syntax_highlighter.tag_generator import TagGenerator

class VimSyntaxHighlighter:
    def __init__(self, tag_id_list, output_syntax_file):
        self.tag_id_list = tag_id_list
        self.output_syntax_file = output_syntax_file
        self.output_tag_file = "/tmp/yavide_tags"

    def generate_vim_syntax_file(self, filename):
        # Generate the tags
        tag_generator = TagGenerator(self.tag_id_list, self.output_tag_file)
        tag_generator.run(filename)

        # Generate the vim syntax file
        tags_db = None
        try:
            tags_db = open(self.output_tag_file)
            # Build Vim syntax highlight rules
            vim_highlight_rules = set()
            for line in tags_db:
                if not tag_generator.is_header(line):
                    highlight_rule = self.__tag_id_to_vim_syntax_group(tag_generator.get_tag_id(line)) + " " + tag_generator.get_tag_name(line)
                    vim_highlight_rules.add(highlight_rule)

            vim_syntax_element = []
            for rule in vim_highlight_rules:
                vim_syntax_element.append("syntax keyword " + rule + "\n")

            # Write syntax file
            vim_syntax_file = open(self.output_syntax_file, "w")
            vim_syntax_file.writelines(vim_syntax_element)
        finally:
            if tags_db is not None:
                tags_db.close()

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
    parser.add_argument("output_syntax_file",                                             help="resulting Vim syntax file")
    args = parser.parse_args()
    args_dict = vars(args)

    tag_id_list = list()
    for key, value in args_dict.iteritems():
        if value == True:
            tag_id_list.append(key)

    vimHighlighter = VimSyntaxHighlighter(tag_id_list, args.output_syntax_file)
    vimHighlighter.generate_vim_syntax_file(args.filename)
 
if __name__ == "__main__":
    main()

