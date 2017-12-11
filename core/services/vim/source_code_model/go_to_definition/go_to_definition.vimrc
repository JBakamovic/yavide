" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function:     Y_SrcCodeNavigation_GoToDefinition()
" Description:  Jumps to the definition of a symbol under the cursor.
" Dependency:
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_SrcCodeNavigation_GoToDefinition()
    if g:project_service_src_code_model['services']['go_to_definition']['enabled']
        let l:current_buffer = expand('%:p')

        " If buffer contents are modified but not saved, we need to serialize contents of the current buffer into temporary file.
        let l:contents_filename = l:current_buffer
        if getbufvar(bufnr('%'), '&modified')
            let l:contents_filename = '/tmp/tmp_' . expand('%:t') 
            call Y_Utils_SerializeCurrentBufferContents(l:contents_filename)
        endif
        call Y_SrcCodeModel_Run(g:project_service_src_code_model['services']['go_to_definition']['id'], [l:contents_filename, l:current_buffer, line('.'), col('.')])
    endif
endfunction

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function:     Y_SrcCodeNavigation_GoToDefinitionCompleted()
" Description:  Jumps to the definition found.
" Dependency:
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_SrcCodeNavigation_GoToDefinitionCompleted(filename, line, column)
    if a:filename != ''
        if expand('%:p') != a:filename
            execute('edit ' . a:filename)
        endif
        call cursor(a:line, a:column)
    endif
endfunction

