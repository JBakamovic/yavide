" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function:     Y_SrcCodeHighlighter_Run()
" Description:  Triggers the source code highlighting for current buffer.
" Dependency:
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_SrcCodeHighlighter_Run()
    if g:project_service_src_code_model['services']['semantic_syntax_highlight']['enabled']
        let l:current_buffer = expand('%:p')

        " If buffer contents are modified but not saved, we need to serialize contents of the current buffer into temporary file.
        let l:contents_filename = l:current_buffer
        if getbufvar(bufnr('%'), '&modified')
            let l:contents_filename = '/tmp/tmp_' . expand('%:t') 
            call Y_Utils_SerializeCurrentBufferContents(l:contents_filename)
        endif
        call Y_SrcCodeModel_Run(g:project_service_src_code_model['services']['semantic_syntax_highlight']['id'], [l:contents_filename, l:current_buffer])
    endif
endfunction

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function:     Y_SrcCodeHighlighter_Apply()
" Description:  Apply the results of source code highlighting for given filename.
" Dependency:
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_SrcCodeHighlighter_Apply(filename, syntax_file)
    let l:current_buffer = expand('%:p')
    if l:current_buffer == a:filename
        " Apply the syntax highlighting rules
        execute('source '.a:syntax_file)

        " Following command is a quick hack to apply the new syntax for
        " the given buffer. I haven't found any other more viable way to do it 
        " while keeping it fast & low on resources,
        execute(':redrawstatus')
    endif
endfunction

