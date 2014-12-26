" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Session management
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
nmap 		<C-s>n 			:YavideSessionNew<CR>|"								New session
nmap 		<C-s>o 			:YavideSessionOpen<CR>|"							Open session
nmap		<C-s>c			:YavideSessionClose<CR>|"							Close session
nmap 		<C-s>s 			:YavideSessionSave<CR>|"							Save session
nmap 		<C-s>d 			:YavideSessionDelete<CR>|"							Delete session

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Search tools
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
map 		<C-f> 			:YavidePromptFind<CR>|"								Open find dialog
map 		<C-h> 			:YavidePromptFindAndReplace<CR>|"					Open find and replace dialog

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Buffer management
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
nmap 		<C-s> 			<ESC>:YavideBufferSave<CR>|"						Save current buffer (normal mode)
imap 		<C-s> 			<ESC>:YavideBufferSave<CR>i|"						Save current buffer (insert mode)
nnoremap 	<C-c> 			:YavideBufferClose<CR>|"							Close current buffer (without killing the window!)
map 		<C-s-Tab> 		:YavideBufferPrev<CR>|"								Go to previous buffer
map 		<C-Tab> 		:YavideBufferNext<CR>|"								Go to next buffer
nnoremap 	<C-Down> 		:YavideBufferScrollDown<CR>|"						Scroll buffer by one line (down)
nnoremap 	<C-Up> 			:YavideBufferScrollUp<CR>|"							Scroll buffer by one line (up)

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Buffer editing
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
nnoremap 	<C-a> 			ggVG|"												Select all
vnoremap 	<C-x> 			"+x|"												Cut
vnoremap 	<C-c> 			"+y|"												Copy
nnoremap 	<C-v> 			"+gP|"												Paste
nnoremap	<C-z> 			u|"													Undo

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Source code navigation
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
nmap 		<F3> 			:YavideSrcNavOpenFile<CR>|"							Open file under the cursor
imap 		<F3> 			<ESC>:YavideSrcNavOpenFile<CR>i|"
nmap 		<F4> 			:YavideSrcNavSwitchBetweenHeaderImpl<CR>|"			Switch between header/source
imap 		<F4> 			<ESC>YavideSrcNavSwitchBetweenHeaderImpl<CR>i|"
nmap 		<S-F4> 			:YavideSrcNavSwitchBetweenHeaderImplVSplit<CR>|"	Switch between header/source in a vertical split
imap 		<S-F4> 			<ESC>:YavideSrcNavSwitchBetweenHeaderImplVSplit<CR>i|"
nmap 		<F12> 			:YavideSrcNavGoToDefinition<CR>|"					Goto definition
imap 		<F12> 			:YavideSrcNavGoToDefinition<CR>|"
nmap 		<C-LeftMouse> 	:YavideSrcNavGoToDefinition<CR>|"
imap 		<C-LeftMouse> 	:YavideSrcNavGoToDefinition<CR>|"
nmap 		<S-F12> 		:vsp <CR>:YavideSrcNavGoToDefinition<CR>|"			Goto definition in a vertical split
imap 		<S-F12> 		:vsp <CR>:YavideSrcNavGoToDefinition<CR>|"
nmap 		<C-\>s 			:YavideSrcNavFindAllReferences<CR>|"				Find all references to the token under the cursor
nmap 		<C-\>g 			:YavideSrcNavFindGlobalDefinitions<CR>|"			Find global definition(s) of token under the cursor
nmap 		<C-\>c			:YavideSrcNavFindAllCallers<CR>|"					Find all functions calling the function under the cursor
nmap 		<C-\>d 			:YavideSrcNavFindAllCallees<CR>|"					Find all functions called by the function under the cursor
nmap 		<C-\>i 			:YavideSrcNavFindAllIncludes<CR>|"					Find all files that include the filename under the cursor
nmap 		<C-\>t 			:YavideSrcNavFindAllInstancesOfText<CR>|"			Find all instances of the text under cursor
nmap 		<C-\>e 			:YavideSrcNavEGrepSearch<CR>|"						Search for the word under the cursor using 'egrep'

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Source code parser
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
nmap 		<F5> 			:YavideSrcParserGenerateCxxTags<CR>|"				Create/update ctags in currently opened project
nmap 		<F6> 			:YavideSrcParserGenerateCScope<CR>|"				Create/update cscope in currently opened project

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Build process
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
nmap 		<F7> 			:YavideBuildRunMake release<CR>|"					Start build in 'release' mode
imap 		<F7> 			<ESC>:w<CR>:YavideBuildRunMake release<CR>|"
nmap 		<S-F7> 			:YavideBuildRunMake debug<CR>|"						Start build in 'debug' mode
imap 		<S-F7> 			<ESC>:w<CR>:YavideBuildRunMake debug<CR>|"
nmap 		<F8> 			:YavideBuildRunMake clean<CR>|"						Clean build
imap 		<F8> 			<ESC>:w<CR>:YavideBuildRunMake clean<CR>|"

