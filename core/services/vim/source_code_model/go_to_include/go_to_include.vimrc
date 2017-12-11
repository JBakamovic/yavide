" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function:     Y_SrcCodeNavigation_GoToInclude()
" Description:  Fetches the filename which include directive corresponds to on the given (current) line.
" Dependency:
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_SrcCodeNavigation_GoToInclude()
    if g:project_service_src_code_model['services']['go_to_include']['enabled']
        let l:current_buffer = expand('%:p')

        " If buffer contents are modified but not saved, we need to serialize contents of the current buffer into temporary file.
        let l:contents_filename = l:current_buffer
        if getbufvar(bufnr('%'), '&modified')
            let l:contents_filename = '/tmp/tmp_' . expand('%:t') 
            call Y_Utils_SerializeCurrentBufferContents(l:contents_filename)
        endif
        call Y_SrcCodeModel_Run(g:project_service_src_code_model['services']['go_to_include']['id'], [l:contents_filename, l:current_buffer, line('.')])
    endif
endfunction

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function:     Y_SrcCodeNavigation_GoToIncludeCompleted()
" Description:  Opens the filename which corresponds to the include directive.
" Dependency:
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_SrcCodeNavigation_GoToIncludeCompleted(filename)
    if a:filename != ''
        execute('edit ' . a:filename)
    endif
endfunction

