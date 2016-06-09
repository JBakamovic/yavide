" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Core variables
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
let g:YAVIDE_CONFIG_DIRECTORY         = g:YAVIDE_ROOT_DIRECTORY . '/' . 'config'
let g:YAVIDE_CORE_DIRECTORY           = g:YAVIDE_ROOT_DIRECTORY . '/' . 'core'

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Runtimepath customization
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Setup the default 'runtimepath' (without ~/.vim folders)
let &runtimepath = printf('%s/vimfiles,%s,%s/vimfiles/after', $VIM, $VIMRUNTIME, $VIM)

" Utilize Pathogen to handle the Yavide runtime directories
execute('source ' . g:YAVIDE_ROOT_DIRECTORY . '/core/external/vim-pathogen/autoload/pathogen.vim')
execute pathogen#infect(
\    g:YAVIDE_ROOT_DIRECTORY                                   . '/' . '{}',
\    g:YAVIDE_ROOT_DIRECTORY . '/' . 'colors'                  . '/' . '{}',
\    g:YAVIDE_ROOT_DIRECTORY . '/' . 'config'                  . '/' . '{}',
\    g:YAVIDE_ROOT_DIRECTORY . '/' . 'core'                    . '/' . '{}',
\    g:YAVIDE_ROOT_DIRECTORY . '/' . 'core' . '/' . 'common'   . '/' . '{}',
\    g:YAVIDE_ROOT_DIRECTORY . '/' . 'core' . '/' . 'external' . '/' . '{}',
\    g:YAVIDE_ROOT_DIRECTORY . '/' . 'core' . '/' . 'indexer'  . '/' . '{}',
\    g:YAVIDE_ROOT_DIRECTORY . '/' . 'core' . '/' . 'syntax'   . '/' . '{}',
\    g:YAVIDE_ROOT_DIRECTORY . '/' . 'core' . '/' . 'server'   . '/' . '{}',
\    g:YAVIDE_ROOT_DIRECTORY . '/' . 'core' . '/' . 'ui'       . '/' . '{}'
\)

" Setup the runtime path for Python modules
python import sys, vim
python sys.path.append(vim.eval('g:YAVIDE_CORE_DIRECTORY'))

