" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Runtimepath customization
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" set default 'runtimepath' (without ~/.vim folders)
let &runtimepath = printf('%s/vimfiles,%s,%s/vimfiles/after', $VIM, $VIMRUNTIME, $VIM)

" add Yavide root directory to 'runtimepath'
let &runtimepath = printf('%s,%s,%s/after', g:YAVIDE_ROOT_DIRECTORY, &runtimepath, g:YAVIDE_ROOT_DIRECTORY)

" Set Python runtime path
python import sys, vim
python sys.path.append(vim.eval('g:YAVIDE_ROOT_DIRECTORY'))

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Core variables
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
let g:YAVIDE_SOURCE_CODE_INDEXER      = g:YAVIDE_ROOT_DIRECTORY . '/' . 'yavide_indexer.py'
let g:YAVIDE_SOURCE_CODE_INDEXER_IF   = g:YAVIDE_ROOT_DIRECTORY . '/' . 'yavide_indexer_if.py'
let g:YAVIDE_SOURCE_CODE_INDEXER_PORT = 6000
let g:filesystem_separator = "/"

