" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function:     Y_SrcCodeModel_Start()
" Description:  Starts the source code model background service.
" Dependency:
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_SrcCodeModel_Start()
    " Enable balloon expressions if TypeDeduction service is enabled.
    if g:project_service_src_code_model['services']['type_deduction']['enabled']
        set ballooneval balloonexpr=Y_SrcCodeTypeDeduction_Run()
    endif
    call Y_ServerStartService(g:project_service_src_code_model['id'], [g:project_root_directory, g:project_env_compilation_db_path])
endfunction

function! Y_SrcCodeModel_StartCompleted()
    let g:project_service_src_code_model['started'] = 1
    call Y_SrcCodeIndexer_RunOnDirectory()
endfunction

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function:     Y_SrcCodeModel_Stop()
" Description:  Stops the source code model background service.
" Dependency:
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_SrcCodeModel_Stop(subscribe_for_shutdown_callback)
    call Y_ServerStopService(g:project_service_src_code_model['id'], a:subscribe_for_shutdown_callback)
endfunction

function! Y_SrcCodeModel_StopCompleted()
    let g:project_service_src_code_model['started'] = 0
endfunction

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function:     Y_SrcCodeModel_Run(service_id, args)
" Description:  Runs the specific service within the source code model (super)-service (i.e. syntax highlight, fixit, diagnostics, ...)
" Dependency:
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_SrcCodeModel_Run(service_id, args)
    if g:project_service_src_code_model['started']
        call insert(a:args, a:service_id)
        call Y_ServerSendServiceRequest(g:project_service_src_code_model['id'], a:args)
    endif
endfunction

