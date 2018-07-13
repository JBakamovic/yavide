" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" AutoCommands
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
augroup yavide_layout_mgmt_group
    autocmd!
    autocmd FileType                qf           wincmd J
augroup END

augroup yavide_editor_group
    autocmd!
    autocmd FileType                c,cpp,java   autocmd BufWritePre <buffer> :call Y_Buffer_StripTrailingWhitespaces()
augroup END

