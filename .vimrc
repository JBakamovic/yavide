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
" Code completion plugin
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
set completeopt=menu,menuone											" Complete options (disable preview scratch window, longest removed to aways show menu)
set pumheight=20														" Limit popup menu height
set concealcursor=inv													" Conceal in insert (i), normal (n) and visual (v) modes
set conceallevel=2														" Hide concealed text completely unless replacement character is defined
let g:clang_use_library = 1												" Use libclang directly
let g:clang_library_path = g:libclang_location							" Path to the libclang on the system
let g:clang_complete_auto = 1											" Run autocompletion immediatelly after ->, ., ::
let g:clang_complete_copen = 1											" Open quickfix window on error
let g:clang_periodic_quickfix = 0										" Turn-off periodic updating of quickfix window (g:ClangUpdateQuickFix() does the same)
let g:clang_snippets = 1												" Enable function args autocompletion, template parameters, ...
let g:clang_snippets_engine = 'ultisnips'								" Use UltiSnips engine for function args autocompletion (provides mechanism to jump over to the next argument)
"let g:clang_snippets_engine = 'clang_complete'							" Use clang_complete engine for function args autocompletion
let g:clang_conceal_snippets = 1										" clang_complete engine related setting
"let g:clang_trailing_placeholder = 1									" clang_complete engine related setting
"let g:clang_hl_errors = 0												" Turn-off error highlighting
"let g:clang_complete_patterns = 1										" (Does not work for me) Turn-on autocompletion for language constructs (i.e. loops)
"let g:clang_complete_macros = 1
"let g:clang_user_options='|| exit 0'									" Avoid freezing on offending code


" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" UltiSnips plugin
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
let g:UltiSnipsExpandTrigger="<tab>"
let g:UltiSnipsJumpForwardTrigger="<tab>"
let g:UltiSnipsJumpBackwardTrigger="<s-tab>"


" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" SuperTab plugin
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"let loaded_supertab = 1												" Uncomment the this line to disable the plugin
let g:SuperTabDefaultCompletionType='<c-x><c-u>'						" 'user' defined default completion type
let g:SuperTabDefaultCompletionType = 'context'							" 'context' defined default completion type
let g:SuperTabCompletionContexts = ['s:ContextText', 's:ContextDiscover']
let g:SuperTabLongestHighlight=1
let g:SuperTabLongestEnhanced=1


" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Session plugin
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
let g:session_autoload = 'yes'											" Automatically load previous session
let g:session_autosave = 'yes'											" Automatically save current session
let g:session_default_to_last = 1										" Open last active session
let g:session_directory = expand('<sfile>:p:h') . "/sessions"			" Store session information where '.vimrc' is stored


" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Airline plugin
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
set laststatus=2
let g:airline_powerline_fonts = 1										" Use Powerline fonts to show beautiful symbols
let g:airline_inactive_collapse = 0										" Do not collapse the status line while having multiple windows
let g:airline#extensions#tabline#enabled = 1							" Display tab bar with buffers
let g:airline#extensions#branch#enabled = 1								" Enable Git client integration
let g:airline#extensions#tagbar#enabled = 1								" Enable Tagbar integration
let g:airline#extensions#hunks#enabled = 1								" Enable Git hunks integration
if ! has('gui_running')													" Fix the timout when leaving insert mode (see http://usevim.com/2013/07/24/powerline-escape-fix)
  set ttimeoutlen=10
  augroup FastEscape
    autocmd!
    au InsertEnter * set timeoutlen=0
    au InsertLeave * set timeoutlen=10
  augroup END
endif


" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" NERDTree plugin
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
let g:NERDTreeMouseMode = 2												" Single-click to expand the directory, double-click to open the file
let g:NERDTreeShowHidden = 1											" Show hidden files

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Pathogen plugin
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
source /opt/yavide/bundle/vim-pathogen/autoload/pathogen.vim
execute pathogen#infect()


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
