" --------------------------------------------------------------------------------------------------------------------------------------
"
"   SOURCE CODE DIAGNOSTICS API
"
" --------------------------------------------------------------------------------------------------------------------------------------
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function:     Y_SrcCodeDiagnostics_Run()
" Description:  Triggers the source code diagnostics for current buffer.
" Dependency:
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_SrcCodeDiagnostics_Run()
    if g:project_service_src_code_model['services']['diagnostics']['enabled']
        let l:current_buffer = expand('%:p')

        " If buffer contents are modified but not saved, we need to serialize contents of the current buffer into temporary file.
        let l:contents_filename = l:current_buffer
        if getbufvar(bufnr('%'), '&modified')
            let l:contents_filename = '/tmp/tmp_' . expand('%:t') 
            call Y_Utils_SerializeCurrentBufferContents(l:contents_filename)
        endif
        call Y_SrcCodeModel_Run(g:project_service_src_code_model['services']['diagnostics']['id'], [l:contents_filename, l:current_buffer])
    endif
endfunction

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function:     Y_SrcCodeDiagnostics_Apply()
" Description:  Populates the quickfix window with source code diagnostics.
" Dependency:
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_SrcCodeDiagnostics_Apply(diagnostics)
    call setloclist(0, a:diagnostics, 'r')
    redraw
endfunction

