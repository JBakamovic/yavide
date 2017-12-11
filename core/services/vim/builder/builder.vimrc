" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function:     Y_ProjectBuilder_Start()
" Description:  Starts the project builder background service.
" Dependency:
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_ProjectBuilder_Start()
    let args = [g:project_root_directory, g:project_env_build_command]
    call Y_ServerStartService(g:project_service_project_builder['id'], args)
endfunction

function! Y_ProjectBuilder_StartCompleted()
    let g:project_service_project_builder['started'] = 1
endfunction

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function:     Y_ProjectBuilder_Stop()
" Description:  Stops the project builder background service.
" Dependency:
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_ProjectBuilder_Stop(subscribe_for_shutdown_callback)
    call Y_ServerStopService(g:project_service_project_builder['id'], a:subscribe_for_shutdown_callback)
endfunction

function! Y_ProjectBuilder_StopCompleted()
    let g:project_service_project_builder['started'] = 0
endfunction

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function:     Y_ProjectBuilder_Run()
" Description:  Triggers the build for current project.
" Dependency:
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_ProjectBuilder_Run(...)
    if g:project_service_project_builder['started']
        let args = [g:project_env_build_command]
        if a:0 != 0
            let args = a:1
            let i = 2
            while i <= a:0
                execute "let args = args . \" \" . a:" . i
                let i = i + 1
            endwhile
        endif
        call setqflist([])
        call Y_ServerSendServiceRequest(g:project_service_project_builder['id'], args)
    endif
endfunction

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function:     Y_ProjectBuilder_Apply()
" Description:  Apply the results of source code highlighting for given filename.
" Dependency:
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_ProjectBuilder_Apply(filename)
    execute('cgetfile '.a:filename)
    execute('copen')
    redraw
endfunction

