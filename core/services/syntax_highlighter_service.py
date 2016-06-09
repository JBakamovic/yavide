import logging
import time
from yavide_service import YavideService
from services.syntax_highlighter.syntax_highlighter import VimSyntaxHighlighter
from services.syntax_highlighter.tag_identifier import TagIdentifier
from common.yavide_utils import YavideUtils

class SyntaxHighlighter(YavideService):
    def __init__(self, server_queue, yavide_instance):
        YavideService.__init__(self, server_queue, yavide_instance)
        self.output_directory = "/tmp"
        self.tag_id_list = [
            TagIdentifier.getClassId(),
            TagIdentifier.getClassStructUnionMemberId(),
            TagIdentifier.getEnumId(),
            TagIdentifier.getEnumValueId(),
            TagIdentifier.getExternFwdDeclarationId(),
            TagIdentifier.getFunctionDefinitionId(),
            TagIdentifier.getFunctionPrototypeId(),
            TagIdentifier.getLocalVariableId(),
            TagIdentifier.getMacroId(),
            TagIdentifier.getNamespaceId(),
            TagIdentifier.getStructId(),
            TagIdentifier.getTypedefId(),
            TagIdentifier.getUnionId(),
            TagIdentifier.getVariableDefinitionId()
        ]
        self.syntax_highlighter = VimSyntaxHighlighter(self.tag_id_list, self.output_directory)
        logging.info("tag_id_list = {0}.".format(self.tag_id_list))

    def run_impl(self, filename):
        start = time.clock()
        self.syntax_highlighter.generate_vim_syntax_file(filename)
        end = time.clock()
        logging.info("Generating vim syntax for '{0}' took {1}.".format(filename, end-start))
        YavideUtils.call_vim_remote_function(self.yavide_instance, "Y_SrcCodeHighlighter_Apply('" + filename + "')")

