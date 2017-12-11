function! Y_SrcCodeTypeDeduction_Run()
    if g:project_service_src_code_model['services']['type_deduction']['enabled']
        " Execute requests only on non-special, ordinary buffers. I.e. ignore NERD_Tree, Tagbar, quickfix and alike.
        " In case of non-ordinary buffers, buffer may not even exist on a disk and triggering the service does not
        " any make sense then.
        if getbufvar(v:beval_bufnr, "&buftype") == ''
            let l:current_buffer = fnamemodify(bufname(v:beval_bufnr), ':p')

            " If buffer contents are modified but not saved, we need to serialize contents of the current buffer into temporary file.
            let l:contents_filename = l:current_buffer
            if getbufvar(bufnr('%'), '&modified')
                let l:contents_filename = '/tmp/tmp_' . expand('%:t') 
                call Y_Utils_SerializeCurrentBufferContents(l:contents_filename)
            endif
            call Y_SrcCodeModel_Run(g:project_service_src_code_model['services']['type_deduction']['id'], [l:contents_filename, l:current_buffer, v:beval_lnum, v:beval_col])
        endif
    endif
    return ''
endfunction

function! Y_SrcCodeTypeDeduction_Apply(deducted_type)
    if exists('*balloon_show')
        if a:deducted_type != ''
            call balloon_show(a:deducted_type)
        endif
    else
        echo a:deducted_type
    endif
endfunction

