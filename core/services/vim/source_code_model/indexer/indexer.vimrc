" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function:     Y_SrcCodeIndexer_RunOnSingleFile()
" Description:  Runs indexer on a single file.
" Dependency:
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_SrcCodeIndexer_RunOnSingleFile()
    if g:project_service_src_code_model['services']['indexer']['enabled']
        let l:current_buffer = expand('%:p')

        " If buffer contents are modified but not saved, we need to serialize contents of the current buffer into temporary file.
        let l:contents_filename = l:current_buffer
        if getbufvar(bufnr('%'), '&modified')
            let l:contents_filename = '/tmp/tmp_' . expand('%:t') 
            call Y_Utils_SerializeCurrentBufferContents(l:contents_filename)
        endif
        call Y_SrcCodeModel_Run(g:project_service_src_code_model['services']['indexer']['id'], [0x0, l:contents_filename, l:current_buffer])
    endif
endfunction

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function:     Y_SrcCodeIndexer_RunOnSingleFileCompleted()
" Description:  Running indexer on a single file completed.
" Dependency:
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_SrcCodeIndexer_RunOnSingleFileCompleted()
endfunction

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function:     Y_SrcCodeIndexer_RunOnDirectory()
" Description:  Runs indexer on a whole directory.
" Dependency:
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_SrcCodeIndexer_RunOnDirectory()
    if g:project_service_src_code_model['services']['indexer']['enabled']
        echomsg 'Indexing on ' . g:project_root_directory . ' started ... It may take a while if it is run for the first time.'
        call Y_SrcCodeModel_Run(g:project_service_src_code_model['services']['indexer']['id'], [0x1])
    endif
endfunction

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function:     Y_SrcCodeIndexer_RunOnDirectoryCompleted()
" Description:  Running indexer on a directory completed.
" Dependency:
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_SrcCodeIndexer_RunOnDirectoryCompleted()
    echomsg 'Indexing run on ' . g:project_root_directory . ' completed.'
endfunction

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function:     Y_SrcCodeIndexer_DropSingleFile()
" Description:  Drops index for given file from the indexer.
" Dependency:
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_SrcCodeIndexer_DropSingleFile(filename)
    if g:project_service_src_code_model['services']['indexer']['enabled']
        call Y_SrcCodeModel_Run(g:project_service_src_code_model['services']['indexer']['id'], [0x2, a:filename])
    endif
endfunction

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function:     Y_SrcCodeIndexer_DropSingleFileCompleted()
" Description:  Dropping single file from indexing results completed.
" Dependency:
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_SrcCodeIndexer_DropSingleFileCompleted()
endfunction

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function:     Y_SrcCodeIndexer_DropAll()
" Description:  Drops all of the indices from the indexer.
" Dependency:
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_SrcCodeIndexer_DropAll()
    if g:project_service_src_code_model['services']['indexer']['enabled']
        call Y_SrcCodeModel_Run(g:project_service_src_code_model['services']['indexer']['id'], [0x3, v:true])
    endif
endfunction

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function:     Y_SrcCodeIndexer_DropAllCompleted()
" Description:  Dropping all indices from indexing results completed.
" Dependency:
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_SrcCodeIndexer_DropAllCompleted()
endfunction

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function:     Y_SrcCodeIndexer_DropAllAndRunOnDirectory()
" Description:  Drops the index database and runs indexer again (aka reindexing operation)
" Dependency:
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_SrcCodeIndexer_DropAllAndRunOnDirectory()
    if g:project_service_src_code_model['services']['indexer']['enabled']
        call Y_SrcCodeModel_Run(g:project_service_src_code_model['services']['indexer']['id'], [0x3, v:true])
        call Y_SrcCodeModel_Run(g:project_service_src_code_model['services']['indexer']['id'], [0x1])
    endif
endfunction

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function:     Y_SrcCodeIndexer_FindAllReferences()
" Description:  Finds project-wide references of a symbol under the cursor.
" Dependency:
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! Y_SrcCodeIndexer_FindAllReferences()
    if g:project_service_src_code_model['services']['indexer']['enabled']
        call Y_SrcCodeModel_Run(g:project_service_src_code_model['services']['indexer']['id'], [0x10, expand('%:p'), line('.'), col('.')])
    endif
endfunction

function! Y_SrcCodeIndexer_FindAllReferencesCompleted(references)
python << EOF
import vim
with open(vim.eval('a:references'), 'r') as f:
    vim.eval("setqflist([" + f.read() + "], 'r')")
EOF
    execute('copen')
    redraw
endfunction

