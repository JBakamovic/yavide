" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function:     Y_ClangTidy_Start()
" Description:  Starts the clang-tidy background service.
" Dependency:
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_ClangTidy_Start()
    let l:configFile = g:project_root_directory . '/' . g:project_env_clang_tidy_config
    call Y_ServerStartService(g:project_service_clang_tidy_checker['id'], [l:configFile, g:project_env_compilation_db_path])
endfunction

function! Y_ClangTidy_StartCompleted()
    let g:project_service_clang_tidy_checker['started'] = 1
endfunction

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function:     Y_ClangTidy_Stop()
" Description:  Stops the clang-tidy background service.
" Dependency:
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_ClangTidy_Stop(subscribe_for_shutdown_callback)
    call Y_ServerStopService(g:project_service_clang_tidy_checker['id'], a:subscribe_for_shutdown_callback)
endfunction

function! Y_ClangTidy_StopCompleted()
    let g:project_service_clang_tidy_checker['started'] = 0
endfunction

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function:     Y_ClangTidy_Run()
" Description:  Triggers the build for current project.
" Dependency:
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_ClangTidy_Run(apply_fixes)
    if g:project_service_clang_tidy_checker['started']
        if filereadable(g:project_root_directory . '/' . g:project_env_clang_tidy_config)
            let l:current_buffer = expand('%:p')
            call Y_ServerSendServiceRequest(g:project_service_clang_tidy_checker['id'], [l:current_buffer, a:apply_fixes])
        endif
    endif
endfunction

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function:     Y_ClangTidy_Apply()
" Description:  Display the results of clang-tidy.
" Dependency:
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_ClangTidy_Apply(clang_tidy_results_filename)
    execute('cgetfile '.a:clang_tidy_results_filename)
    execute('copen')
    redraw
endfunction

