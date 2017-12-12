from server.server import Server
from services.vim.clang_format.clang_format import VimClangFormat
from services.vim.clang_tidy.clang_tidy import VimClangTidy
from services.vim.builder.builder import VimBuilder
from services.vim.source_code_model.source_code_model import VimSourceCodeModel

def get_server_instance(msg_queue, args):
    vim_instance = args
    return Server(
        msg_queue,
        VimSourceCodeModel(vim_instance),
        VimBuilder(vim_instance),
        VimClangFormat(vim_instance),
        VimClangTidy(vim_instance)
    )
