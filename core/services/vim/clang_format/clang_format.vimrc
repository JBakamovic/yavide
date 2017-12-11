" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function:     Y_SrcCodeFormatter_Start()
" Description:  Starts the source code formatting background service.
" Dependency:
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_SrcCodeFormatter_Start()
    let l:configFile = g:project_root_directory . '/' . g:project_env_src_code_format_config
    call Y_ServerStartService(g:project_service_src_code_formatter['id'], l:configFile)
endfunction

function! Y_SrcCodeFormatter_StartCompleted()
    let g:project_service_src_code_formatter['started'] = 1
endfunction

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function:     Y_SrcCodeFormatter_Stop()
" Description:  Stops the source code formatting background service.
" Dependency:
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_SrcCodeFormatter_Stop(subscribe_for_shutdown_callback)
    call Y_ServerStopService(g:project_service_src_code_formatter['id'], a:subscribe_for_shutdown_callback)
endfunction

function! Y_SrcCodeFormatter_StopCompleted()
    let g:project_service_src_code_formatter['started'] = 0
endfunction

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function:     Y_SrcCodeFormatter_Run()
" Description:  Triggers the formatting on current buffer.
" Dependency:
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_SrcCodeFormatter_Run()
    if g:project_service_src_code_formatter['started']
        if filereadable(g:project_root_directory . '/' . g:project_env_src_code_format_config)
            let l:current_buffer = expand('%:p')
            call Y_ServerSendServiceRequest(g:project_service_src_code_formatter['id'], l:current_buffer)
        endif
    endif
endfunction

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function:     Y_SrcCodeFormatter_Apply()
" Description:  Apply the results of source code formatting for given filename.
" Dependency:
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_SrcCodeFormatter_Apply(filename)
    let l:current_buffer = expand('%:p')
    if l:current_buffer == a:filename
        execute('e')
    endif
endfunction

