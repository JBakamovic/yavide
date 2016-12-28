import sys
import argparse
import logging
from services.syntax_highlighter.token_identifier import TokenIdentifier
from services.syntax_highlighter.ctags_tokenizer import CtagsTokenizer
from services.syntax_highlighter.clang_tokenizer import ClangTokenizer

# TODO remove this once 'Unsupported token id' message is removed
import clang.cindex

class VimSyntaxHighlighter:
    def __init__(self, output_syntax_file):
        self.output_syntax_file = output_syntax_file

    def generate_vim_syntax_file_from_clang(self, filename, compiler_args, project_root_directory):
        # Generate the tokens
        tokenizer = ClangTokenizer()
        tokenizer.run(filename, compiler_args, project_root_directory)

        # Build Vim syntax highlight rules
        vim_syntax_element = ['call clearmatches()\n']
        token_list = tokenizer.get_token_list()
        for token in token_list:
            token_id = tokenizer.get_token_id(token)
            if token_id != TokenIdentifier.getUnsupportedId():
                highlight_rule = self.__tag_id_to_vim_syntax_group(token_id) + " " + tokenizer.get_token_name(token)
                vim_syntax_element.append(
                    "call matchaddpos('" +
                    str(self.__tag_id_to_vim_syntax_group(token_id)) +
                    "', [[" +
                    str(tokenizer.get_token_line(token)) +
                    ", " +
                    str(tokenizer.get_token_column(token)) +
                    ", " +
                    str(len(tokenizer.get_token_name(token))) +
                    "]], -1)" +
                    "\n"
                )
            else:
                logging.debug("Unsupported token id: [{0}, {1}]: {2} '{3}'".format(token.location.line, token.location.column, token.kind, tokenizer.get_token_name(token)))

        # Write Vim syntax file
        vim_syntax_file = open(self.output_syntax_file, "w")
        vim_syntax_file.writelines(vim_syntax_element)

        # Write some debug information
        tokenizer.dump_token_list()

    def generate_vim_syntax_file_from_ctags(self, filename):
        # Generate the tags
        output_tag_file = "/tmp/yavide_tags"
        tokenizer = CtagsTokenizer(output_tag_file)
        tokenizer.run(filename)

        # Generate the vim syntax file
        tags_db = None
        try:
            tags_db = open(output_tag_file)
            # Build Vim syntax highlight rules
            vim_highlight_rules = set()
            for line in tags_db:
                if not tokenizer.is_header(line):
                    highlight_rule = self.__tag_id_to_vim_syntax_group(tokenizer.get_token_id(line)) + " " + tokenizer.get_token_name(line)
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
        if tag_identifier == TokenIdentifier.getNamespaceId():
            return "yavideCppNamespace"
        if tag_identifier == TokenIdentifier.getNamespaceAliasId():
            return "yavideCppNamespaceAlias"
        if tag_identifier == TokenIdentifier.getClassId():
            return "yavideCppClass"
        if tag_identifier == TokenIdentifier.getStructId():
            return "yavideCppStructure"
        if tag_identifier == TokenIdentifier.getEnumId():
            return "yavideCppEnum"
        if tag_identifier == TokenIdentifier.getEnumValueId():
            return "yavideCppEnumValue"
        if tag_identifier == TokenIdentifier.getUnionId():
            return "yavideCppUnion"
        if tag_identifier == TokenIdentifier.getFieldId():
            return "yavideCppField"
        if tag_identifier == TokenIdentifier.getLocalVariableId():
            return "yavideCppLocalVariable"
        if tag_identifier == TokenIdentifier.getFunctionId():
            return "yavideCppFunction"
        if tag_identifier == TokenIdentifier.getMethodId():
            return "yavideCppMethod"
        if tag_identifier == TokenIdentifier.getFunctionParameterId():
            return "yavideCppFunctionParameter"
        if tag_identifier == TokenIdentifier.getTemplateTypeParameterId():
            return "yavideCppTemplateTypeParameter"
        if tag_identifier == TokenIdentifier.getTemplateNonTypeParameterId():
            return "yavideCppTemplateNonTypeParameter"
        if tag_identifier == TokenIdentifier.getTemplateTemplateParameterId():
            return "yavideCppTemplateTemplateParameter"
        if tag_identifier == TokenIdentifier.getMacroDefinitionId():
            return "yavideCppMacroDefinition"
        if tag_identifier == TokenIdentifier.getMacroInstantiationId():
            return "yavideCppMacroInstantiation"
        if tag_identifier == TokenIdentifier.getTypedefId():
            return "yavideCppTypedef"
        if tag_identifier == TokenIdentifier.getUsingDirectiveId():
            return "yavideCppUsingDirective"
        if tag_identifier == TokenIdentifier.getUsingDeclarationId():
            return "yavideCppUsingDeclaration"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename",                                                       help="source code file to generate the source code highlighting for")
    parser.add_argument("output_syntax_file",                                             help="resulting Vim syntax file")
    args = parser.parse_args()
    args_dict = vars(args)

    vimHighlighter = VimSyntaxHighlighter(args.output_syntax_file)
    vimHighlighter.generate_vim_syntax_file_from_clang(args.filename, [''])
 
if __name__ == "__main__":
    main()

