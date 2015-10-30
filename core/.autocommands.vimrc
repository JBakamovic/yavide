" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" AutoCommands
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
augroup yavide_environment_mgmt_group
    autocmd!
    autocmd VimEnter                *                           call Y_Env_Init()
    autocmd VimLeave                *                           call Y_Env_Deinit()
augroup END

augroup yavide_src_parser_group
    autocmd!
    autocmd BufEnter                *.java                      exec 'set tags='.g:project_java_tags
    autocmd BufEnter                *.cpp,*.cc,*.c,*.h,*.hpp    exec 'set tags='.g:project_cxx_tags
augroup END

augroup yavide_src_highlight_group
    autocmd BufEnter                *.cpp,*.cc,*.c,*.h,*.hpp    call Y_CodeHighlight_Run()
    autocmd BufWritePost            *.cpp,*.cc,*.c,*.h,*.hpp    call Y_CodeHighlight_Run()
augroup END

augroup yavide_layout_mgmt_group
    autocmd!
    autocmd FileType                qf                          wincmd J
augroup END

augroup yavide_editor_group
    autocmd!
    autocmd FileType                c,cpp,java                  autocmd BufWritePre <buffer> :call Y_Buffer_StripTrailingWhitespaces()
augroup END

