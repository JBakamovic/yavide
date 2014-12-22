" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" AutoCommands
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
augroup yavide_session_mgmt_group
	autocmd!
	autocmd SessionLoadPost 	* 							call Y_Env_Setup()							" Load project specific settings
augroup END

augroup yavide_src_parser_group
	autocmd!
	autocmd BufEnter 			*.java 						exec 'set tags='.g:project_java_tags
	autocmd BufEnter 			*.cpp,*.c,*.h,*.cxx,*.cc	exec 'set tags='.g:project_cxx_tags
	autocmd FileType 			c,cpp						autocmd BufWritePost <buffer> call Y_SrcParser_UpdateCxxTags()
	autocmd FileType 			java						autocmd BufWritePost <buffer> call Y_SrcParser_UpdateJavaTags()
augroup END

augroup yavide_layout_mgmt_group
	autocmd!
	autocmd FileType 			qf 							wincmd J										" Make the quickfix window always appear at the bottom
augroup END

augroup yavide_editor_group
	autocmd!
	autocmd FileType 			c,cpp,java 					autocmd BufWritePre <buffer> :call Y_Buffer_StripTrailingWhitespaces()
augroup END

"autocmd! BufWritePost .vimrc source % " Reload '.vimrc' when modified

