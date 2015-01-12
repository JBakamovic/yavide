"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" 	Description: Yavide entry point (startup file)
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Yavide runtime path (root directory)
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
let g:YAVIDE_ROOT_DIRECTORY = expand('<sfile>:p:h')

let g:yavide_configuration_files = [
\                   '.core.vimrc',
\                   '.user_settings.vimrc',
\                   '.editor.vimrc',
\                   '.plugins.vimrc',
\                   '.api.vimrc',
\                   '.autocommands.vimrc',
\                   '.commands.vimrc',
\                   '.keyboard.vimrc'
\]

for file in g:yavide_configuration_files
    execute('source ' . g:YAVIDE_ROOT_DIRECTORY . '/' . file)
endfor

