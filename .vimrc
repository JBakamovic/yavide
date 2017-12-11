"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" 	Description: Yavide entry point (startup file)
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Yavide runtime path (root directory)
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
let g:YAVIDE_ROOT_DIRECTORY = expand('<sfile>:p:h')

let g:yavide_configuration_files = [
\                   'core/.core.vimrc',
\                   'config/.user_settings.vimrc',
\                   'core/.api.vimrc',
\                   'core/services/vim/builder/builder.vimrc',
\                   'core/services/vim/clang_format/clang_format.vimrc',
\                   'core/services/vim/clang_tidy/clang_tidy.vimrc',
\                   'core/services/vim/source_code_model/diagnostics/diagnostics.vimrc',
\                   'core/services/vim/source_code_model/go_to_definition/go_to_definition.vimrc',
\                   'core/services/vim/source_code_model/go_to_include/go_to_include.vimrc',
\                   'core/services/vim/source_code_model/indexer/indexer.vimrc',
\                   'core/services/vim/source_code_model/semantic_syntax_highlight/semantic_syntax_highlight.vimrc',
\                   'core/services/vim/source_code_model/type_deduction/type_deduction.vimrc',
\                   'core/.editor.vimrc',
\                   'core/.plugins.vimrc',
\                   'core/.globals.vimrc',
\                   'core/.autocommands.vimrc',
\                   'core/.commands.vimrc',
\]

for file in g:yavide_configuration_files
    execute('source ' . g:YAVIDE_ROOT_DIRECTORY . '/' . file)
endfor

