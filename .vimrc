" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" 	VIM Configuration File
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" 	Description: Configuration file optimized for C/C++ development" 	
"
"	Requirements:
"		Vim v7.4		(http://www.vim.org)
"		Exuberant Ctags	(http://ctags.sourceforge.net)
"		Powerline Fonts	(https://github.com/Lokaltog/powerline-fonts)
"		Git				(http://git-scm.com)
"
"	Feature:							Implemented by:							Website:
"			Project explorer 				(NERDTree plugin)						https://github.com/scrooloose/nerdtree
"			Session manager 				(Session plugin)						https://github.com/xolox/vim-session
"			Building						(Vim-integrated)						http://www.vim.org
"			Auto-completion					(Clang-complete plugin)					https://github.com/Rip-Rip/clang_complete
"			Code navigation					(Exuberant Ctags)						http://ctags.sourceforge.net/
"			Tab completion					(SuperTabs plugin)						https://github.com/ervandew/supertab
"			Code outline 					(Tagbar plugin)							https://github.com/majutsushi/tagbar
"			Statusbar/Tabbar				(Airline plugin)						https://github.com/bling/vim-airline
"			Switch hdr & impl				(A plugin)								https://github.com/vim-scripts/a.vim
"			Switch to file					(A plugin)								https://github.com/vim-scripts/a.vim
"			Parenthesis auto-complete		(Auto-close plugin)						https://github.com/Townk/vim-autoclose
"			Find and replace				(Vim-integrated)						http://www.vim.org
"			Grep integration				(Vim-integrated)						http://www.vim.org
"			Code snippets					(UltiSnips plugin)						https://github.com/SirVer/ultisnips
"			SCM integration					(Vim-fugitive plugin)					https://github.com/tpope/vim-fugitive.git
"			Highlight occurences			(Vim-integrated)						http://www.vim.org
"			Code comments					(NERDCommenter plugin)					https://github.com/scrooloose/nerdcommenter
"			Plugin manager					(Pathogen plugin)						https://github.com/tpope/vim-pathogen
"
" 	Author: 
"			Jusufadis Bakamovic
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Core settings
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
source /opt/yavide/.core.vimrc

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" User-configurable settings
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
source /opt/yavide/.user_settings.vimrc

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Editor settings
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
source /opt/yavide/.editor.vimrc

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Plugins
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
source /opt/yavide/.plugins.vimrc

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function: 	UpdateCTags()
" Description:	Starts generation of ctags in currently selected node in NERDTree
" Dependency:	NERDTree, ctags exuberant
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function UpdateCTags()
    let curNodePath = g:NERDTreeFileNode.GetSelected().path.str()
	exec ':!ctags -R --c++-kinds=+p --fields=+iaS --extra=+q -f ' . curNodePath . '/tags ' . curNodePath
endfunction

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function: 	UpdateCScope()
" Description:	Starts generation of cscope in currently selected node in NERDTree
" Dependency:	NERDTree, cscope
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function UpdateCScope()
    let curNodePath = g:NERDTreeFileNode.GetSelected().path.str()
	exec ':!find ' . curNodePath . ' -iname "*.c" -o -iname "*.cpp" -o -iname "*.h" -o -iname "*.hpp" -o -iname "*.java" > ' . curNodePath . '/' . 'cscope.files'
	exec ':!cscope -q -R -b -i ' . curNodePath . '/' . 'cscope.files'
endfunction

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function: 	MyMake()
" Description:	Runs the Makefile and opens up the quickfix window afterwards
" Dependency:	None
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function MyMake()
	:make! | copen
endfunction
:command Make :call MyMake()

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function: 	MyCppCheck()
" Description:	Runs the cppcheck on given path
" Dependency:	cppcheck
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! MyCppCheck(path, ...)
	let additional_args = ''
	if a:0 != 0
		let additional_args = a:1
		let i = 2
		while i <= a:0
		    execute "let additional_args = additional_args . \" \" . a:" . i
		    let i = i + 1
		endwhile
    endif

    let mp=&makeprg
    let &makeprg = 'cppcheck --enable=all --force --quiet --template=gcc ' . additional_args . ' ' . a:path
	exec "make!"
    let &makeprg=mp
endfunction
:command -nargs=* -complete=file CppCheck :call MyCppCheck(".", <f-args>)
:command -nargs=* -complete=file CppCheckBuf :call MyCppCheck("%", <f-args>)

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function: 	StripTrailingWhitespaces()
" Description:	Strips trailing whitespaces from current buffer
" Dependency:	None
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! <SID>StripTrailingWhitespaces()
    " Preparation: save last search, and cursor position.
    let _s=@/
    let l = line(".")
    let c = col(".")
    " Do the business:
    %s/\s\+$//e
    " Clean up: restore previous search history, and cursor position
    let @/=_s
    call cursor(l, c)
endfunction
autocmd FileType c,cpp,java autocmd BufWritePre <buffer> :call <SID>StripTrailingWhitespaces()

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Function: 	GoToBuffer()
" Description:	Switches to the next/previous buffer but ignores 'quickfix' windows
" Dependency:	None
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function GoToBuffer(bGoToNext)
let cmd = a:bGoToNext == 1 ? ":bnext" : ":bprevious"
exec cmd
if &buftype ==# 'quickfix'
	exec cmd
endif
endfunction
:command -nargs=1 -complete=file GoToNextBuffer :call GoToBuffer(1)
:command -nargs=1 -complete=file GoToPreviousBuffer :call GoToBuffer(0)

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Keyboard mappings
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
nmap <C-o> :OpenSession<CR>|"											Open session
nmap <C-e> :SaveSession<CR>|" 											Save session

map <C-f> :promptfind<CR>|" 											Open find dialog
map <C-r> :promptrepl<CR>|" 											Open find and replace dialog

nmap <C-s> <ESC>:w<CR>|" 												Save current buffer (normal mode)
imap <C-s> <ESC>:w<CR>i|" 												Save current buffer (insert mode)
nnoremap <C-c> :bp<bar>sp<bar>bn<bar>bd<CR>|"							Close current buffer (without killing the window!)
map <C-Tab> :GoToNextBuffer()<CR>|"										Go to next buffer
map <C-S-Tab> :GoToPreviousBuffer()<CR>|"								Go to previous buffer
nnoremap <C-Down> <C-e>|"												Scroll buffer by one line (down)
nnoremap <C-Up> <C-y>|"													Scroll buffer by one line (up)

nnoremap <C-a> ggVG|"													Select all
vnoremap <C-X> "+x|"													Cut
vnoremap <C-C> "+y|"													Copy
nnoremap <C-V> "+gP|"													Paste
nnoremap <C-z> u|"														Undo

nmap <F3> :IH<CR>|"														Switch to file under cursor
imap <F3> <ESC>:IH<CR>i|"
nmap <F4> :A<CR>|"														Switch between header/source
imap <F4> <ESC>:A<CR>i|"
nmap <S-F4> :AV<CR>|"													Switch between header/source in a vertical split
imap <S-F4> <ESC>:AV<CR>i|"
nmap <F12> :tjump <C-R><C-W> <CR>|"										Goto definition (but show a list in case of multiple definitions)
imap <F12> :tjump <C-R><C-W> <CR>|"
nmap <S-F12> :vsp <CR>:tjump <C-R><C-W> <CR>|"							Goto definition in a vertical split
imap <S-F12> :vsp <CR>:tjump <C-R><C-W> <CR>|"
nmap <C-LeftMouse> :tjump <C-R><C-W> <CR>|"								Goto definition (but show a list in case of multiple definitions)
imap <C-LeftMouse> :tjump <C-R><C-W> <CR>|"
nmap <F5> :call UpdateCTags()<CR>|"										Create/update ctags in currently selected NODETree directory
nmap <F6> :call UpdateCScope()<CR>|"									Create/update cscope in currently selected NODETree directory

nmap <F7> :call MyMake()<CR>|"											Build using :make (in insert mode exit to command mode, save and compile)
imap <F7> <ESC>:w<CR>:call MyMake()<CR>|"
nmap <S-F7> :make clean<CR>|"											Build using :make clean all
imap <S-F7> <ESC>:w<CR>:make clean<CR>|"

" The following maps all invoke one of the following cscope search types:
"
"   's'   symbol: find all references to the token under cursor
"   'g'   global: find global definition(s) of the token under cursor
"   'c'   calls:  find all calls to the function name under cursor
"   't'   text:   find all instances of the text under cursor
"   'e'   egrep:  egrep search for the word under cursor
"   'f'   file:   open the filename under cursor
"   'i'   includes: find files that include the filename under cursor
"   'd'   called: find functions that function under cursor calls
nmap <C-\>s :cs find s <C-R>=expand("<cword>")<CR><CR>
nmap <C-\>g :cs find g <C-R>=expand("<cword>")<CR><CR>
nmap <C-\>c :cs find c <C-R>=expand("<cword>")<CR><CR>
nmap <C-\>t :cs find t <C-R>=expand("<cword>")<CR><CR>
nmap <C-\>e :cs find e <C-R>=expand("<cword>")<CR><CR>
nmap <C-\>f :cs find f <C-R>=expand("<cfile>")<CR><CR>
nmap <C-\>i :cs find i ^<C-R>=expand("<cfile>")<CR>$<CR>
nmap <C-\>d :cs find d <C-R>=expand("<cword>")<CR><CR>

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" User-defined commands
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function MyLayoutRefresh()
	:NERDTree
	:Tagbar
endfunction
:command LayoutRefresh :call MyLayoutRefresh()
