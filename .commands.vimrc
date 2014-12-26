" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Session commands
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
:command! -nargs=0 -complete=file YavideSessionNew	 						:call Y_Session_New()
:command! -nargs=0 -complete=file YavideSessionOpen	 						:call Y_Session_Open()
:command! -nargs=0 -complete=file YavideSessionClose 						:call Y_Session_Close()
:command! -nargs=0 -complete=file YavideSessionSave	 						:call Y_Session_Save()
:command! -nargs=0 -complete=file YavideSessionDelete 						:call Y_Session_Delete()

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Layout commands
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
:command! -nargs=0 -complete=file YavideLayoutRefresh 						:call Y_Layout_Refresh()

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Search commands
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
:command! -nargs=0 -complete=file YavidePromptFind	 						:call Y_Prompt_Find()
:command! -nargs=0 -complete=file YavidePromptFindAndReplace				:call Y_Prompt_FindAndReplace()

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Buffer commands
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
:command! -nargs=0 -complete=file YavideBufferSave	 						:call Y_Buffer_Save()
:command! -nargs=0 -complete=file YavideBufferClose	 						:call Y_Buffer_Close()
:command! -nargs=0 -complete=file YavideBufferPrev	 						:call Y_Buffer_GoTo(0)
:command! -nargs=0 -complete=file YavideBufferNext	 						:call Y_Buffer_GoTo(1)
:command! -nargs=0 -complete=file YavideBufferScrollUp						:call Y_Buffer_Scroll(0)
:command! -nargs=0 -complete=file YavideBufferScrollDown					:call Y_Buffer_Scroll(1)

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Buffer editing commands
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
:command! -nargs=0 -complete=file YavideTextSelectAll 						:call Y_Text_SelectAll()
:command! -nargs=0 -complete=file YavideTextCut		 						:call Y_Text_Cut()
:command! -nargs=0 -complete=file YavideTextCopy		 					:call Y_Text_Copy()
:command! -nargs=0 -complete=file YavideTextPaste	 						:call Y_Text_Paste()
:command! -nargs=0 -complete=file YavideTextUndo		 					:call Y_Text_Undo()
:command! -nargs=0 -complete=file YavideTextRedo		 					:call Y_Text_Redo()

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Source code navigation commands
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
:command! -nargs=0 -complete=file YavideSrcNavOpenFile						:call Y_SrcNav_OpenFile()
:command! -nargs=0 -complete=file YavideSrcNavSwitchBetweenHeaderImpl		:call Y_SrcNav_SwitchBetweenHeaderImpl(0)
:command! -nargs=0 -complete=file YavideSrcNavSwitchBetweenHeaderImplVSplit :call Y_SrcNav_SwitchBetweenHeaderImpl(1)
:command! -nargs=0 -complete=file YavideSrcNavGoToDefinition				:call Y_SrcNav_GoToDefinition()
:command! -nargs=0 -complete=file YavideSrcNavFindAllReferences				:call Y_SrcNav_FindAllReferences()
:command! -nargs=0 -complete=file YavideSrcNavFindGlobalDefinitions			:call Y_SrcNav_FindGlobalDefinitions()
:command! -nargs=0 -complete=file YavideSrcNavFindAllCallers				:call Y_SrcNav_FindAllCallers()
:command! -nargs=0 -complete=file YavideSrcNavFindAllCallees				:call Y_SrcNav_FindAllCallees()
:command! -nargs=0 -complete=file YavideSrcNavFindAllIncludes				:call Y_SrcNav_FindAllIncludes()
:command! -nargs=0 -complete=file YavideSrcNavFindAllInstancesOfText		:call Y_SrcNav_FindAllInstancesOfText()
:command! -nargs=0 -complete=file YavideSrcNavEGrepSearch					:call Y_SrcNav_EGrepSearch()

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Source code parser commands
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
:command! -nargs=0 -complete=file YavideSrcParserGenerateJavaTags			:call Y_SrcParser_GenerateJavaTags()
:command! -nargs=0 -complete=file YavideSrcParserGenerateCxxTags			:call Y_SrcParser_GenerateCxxTags()
:command! -nargs=0 -complete=file YavideSrcParserGenerateCScope				:call Y_SrcParser_GenerateCScope(0)

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Source code static analysis commands
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
:command! -nargs=* -complete=file YavideAnalyzerCppCheck 					:call Y_Analyzer_RunCppCheck(".", <f-args>)
:command! -nargs=* -complete=file YavideAnalyzerCppCheckBuf 				:call Y_Analyzer_RunCppCheck("%", <f-args>)
:command! -nargs=* -complete=file YavideAnalyzerClangCheck 					:call Y_Analyzer_RunClangChecker("." <f-args>)

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Build commands
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
:command! -nargs=* -complete=file YavideBuildRunMake						:call Y_Build_RunMake(<f-args>)

