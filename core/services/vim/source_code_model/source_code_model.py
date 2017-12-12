import logging
from common.yavide_utils import YavideUtils
from services.service_plugin import ServicePlugin
from services.vim.source_code_model.indexer.indexer import VimIndexer
from services.vim.source_code_model.semantic_syntax_highlight.syntax_generator import VimSyntaxGenerator
from services.vim.source_code_model.diagnostics.quickfix_diagnostics import VimQuickFixDiagnostics
from services.vim.source_code_model.type_deduction.type_deduction import VimTypeDeduction
from services.vim.source_code_model.go_to_definition.go_to_definition import VimGoToDefinition
from services.vim.source_code_model.go_to_include.go_to_include import VimGoToInclude

class VimSourceCodeModel(ServicePlugin):
    def __init__(self, yavide_instance):
        self.yavide_instance = yavide_instance
        self.indexer = VimIndexer(self.yavide_instance)
        self.semantic_syntax_higlight = VimSyntaxGenerator(self.yavide_instance, "/tmp/yavideSyntaxFile.vim")
        self.diagnostics = VimQuickFixDiagnostics(self.yavide_instance)
        self.type_deduction = VimTypeDeduction(self.yavide_instance)
        self.go_to_definition = VimGoToDefinition(self.yavide_instance)
        self.go_to_include = VimGoToInclude(self.yavide_instance)

    def startup_callback(self, success, payload):
        project_root_directory, compiler_args_filename = payload[0], payload[1]
        YavideUtils.call_vim_remote_function(self.yavide_instance, "Y_SrcCodeModel_StartCompleted()")
        logging.info("SourceCodeModel configured with: project root directory='{0}', compiler args='{1}'".format(project_root_directory, compiler_args_filename))

    def shutdown_callback(self, success, payload):
        reply_with_callback = bool(payload)
        if reply_with_callback:
            YavideUtils.call_vim_remote_function(self.yavide_instance, "Y_SrcCodeModel_StopCompleted()")

    def __call__(self, success, args, payload):
        source_code_model_service_id = int(payload[0])
        if source_code_model_service_id == 0:
            self.indexer(success, args, payload)
        elif source_code_model_service_id == 1:
            self.semantic_syntax_higlight(success, args, payload)
        elif source_code_model_service_id == 2:
            self.diagnostics(success, args, payload)
        elif source_code_model_service_id == 3:
            self.type_deduction(success, args, payload)
        elif source_code_model_service_id == 4:
            self.go_to_definition(success, args, payload)
        elif source_code_model_service_id == 5:
            self.go_to_include(success, args, payload)
        else:
            logging.error('Invalid source code model service id!')
