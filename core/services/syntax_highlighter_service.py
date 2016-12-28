import logging
import time
from yavide_service import YavideService
from services.syntax_highlighter.syntax_highlighter import VimSyntaxHighlighter
from common.yavide_utils import YavideUtils

class SyntaxHighlighter(YavideService):
    def __init__(self, server_queue, yavide_instance):
        YavideService.__init__(self, server_queue, yavide_instance)
        self.output_syntax_file = "/tmp/yavideSyntaxFile.vim"
        self.syntax_highlighter = VimSyntaxHighlighter(self.output_syntax_file)

    def run_impl(self, args):
        contents_filename = str(args[0])
        original_filename = str(args[1])
        compiler_args = list(str(args[2]).split())
        project_root_directory = str(args[3])
        start = time.clock()
        self.syntax_highlighter.generate_vim_syntax_file_from_clang(contents_filename, compiler_args, project_root_directory)
        end = time.clock()
        logging.info("Generating vim syntax for '{0}' took {1}.".format(original_filename, end-start))
        YavideUtils.call_vim_remote_function(self.yavide_instance, "Y_SrcCodeHighlighter_Apply('" + original_filename + "'" + ", '" + self.output_syntax_file + "')")
