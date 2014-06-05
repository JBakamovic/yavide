" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" 	VIM Configuration File
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" 	Description: Configuration file optimized for C/C++ development" 	
"
"	Requirements:
"		Vim v7.4		(http://www.vim.org)
"		Exuberant Ctags	(http://ctags.sourceforge.net)
"		LLVM v3.4		(llvm.org/releases/download.html)
"		Silver Searcher	(https://github.com/ggreer/the_silver_searcher)
"		Powerline Fonts	(https://github.com/Lokaltog/powerline-fonts)
"		Git				(http://git-scm.com)
"
"	Feature:							Implemented by:							Website:
"			Project explorer 				(NERDTree plugin)						https://github.com/scrooloose/nerdtree
"			Session manager 				(Session plugin)						https://github.com/xolox/vim-session
"			Building						(Vim-integrated)						http://www.vim.org
"			Auto-completion Variant 1		(Clang-complete plugin)					https://github.com/Rip-Rip/clang_complete
"			Auto-completion	Variant 2		(YouCompleteMe plugin)					https://github.com/Valloric/YouCompleteMe
"			Auto-completion Variant 3		(YouCompleteMe plugin fork)				https://github.com/oblitum/YouCompleteMe
"			Code navigation					(Exuberant Ctags)						http://ctags.sourceforge.net/
"			Tab completion					(SuperTabs plugin)						https://github.com/ervandew/supertab
"			Class outline 					(Tagbar plugin)							https://github.com/majutsushi/tagbar
"			Statusbar/Tabbar				(Airline plugin)						https://github.com/bling/vim-airline
"			Switch hdr & impl				(A plugin)								https://github.com/vim-scripts/a.vim
"			Switch to file					(A plugin)								https://github.com/vim-scripts/a.vim
"			Parenthesis auto-complete		(Auto-close plugin)						https://github.com/Townk/vim-autoclose
"			Find and replace				(Vim-integrated)						http://www.vim.org
"			Grep integration				(Grep plugin)							https://github.com/yegappan/grep
"			Code snippets					(UltiSnips plugin)						https://github.com/SirVer/ultisnips
"			SCM integration					(Git plugin)							https://github.com/motemen/git-vim
"			Highlight occurences			(Vim-integrated)						http://www.vim.org
"			Code comments					(NERDCommenter plugin)					https://github.com/scrooloose/nerdcommenter
"			Fuzzy search					(CtrlP plugin)							https://github.com/kien/ctrlp.vim
"			Syntax check on-the-fly 		(YCM)									https://github.com/Valloric/YouCompleteMe
"			Plugin manager					(Pathogen plugin)						https://github.com/tpope/vim-pathogen
"
" 	Author: 
"			Jusufadis Bakamovic
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" User-defined variables
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
let myvar_libclang_location = "/usr/lib/llvm-3.4/lib"				" Set the correct location of libclang.so
let myvar_ycm_extra_conf_file = "/opt/yavide/.ycm_extra_conf.py"	" Set the path to the YCM configuration file
																	" Applicable only when YCM is employed
let myvar_use_ycm_plugin = 0										" 1 for YouCompleteMe, 
																	" 0 for clang-complete autocompletion plugin
let myvar_use_ctrlp_ag_engine = 1									" 1 to make CtrlP use a Silver Searcher,
																	" 0 to use the default one from Vim (globpath())


" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Runtimepath customization
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" set default 'runtimepath' (without ~/.vim folders)
let &runtimepath = printf('%s/vimfiles,%s,%s/vimfiles/after', $VIM, $VIMRUNTIME, $VIM)

" what is the name of the directory containing this file?
let s:portable = expand('<sfile>:p:h')

" add the directory to 'runtimepath'
let &runtimepath = printf('%s,%s,%s/after', s:portable, &runtimepath, s:portable)


" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" General settings
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
autocmd! bufwritepost .vimrc source %								" Auto reload .vimrc when changed, this avoids reopening vim
filetype plugin on													" Turn on the filetype plugin
set enc=utf-8														" Set UTF-8 encoding
set fenc=utf-8
set termencoding=utf-8
set nocompatible													" Disable vi compatibility (emulation of old bugs)
set tags=./tags;													" Begin searching for the 'tags' file starting from the directory of currently opened file
set autoindent														" Use indentation of previous line
set smartindent														" Use intelligent indentation for C
set tabstop=4        												" Tab width is 4 spaces					
set shiftwidth=4     												" Indent also with 4 spaces
set expandtab        												" Expand tabs to spaces
set textwidth=120													" Wrap lines at 120 chars. 80 is somewaht antiquated with nowadays displays.
let mapleader = ","													" Define ',' is leader key
syntax on															" Turn syntax highlighting on
set hlsearch														" Highlight all search results
set number															" Turn line numbers on
set showmatch														" Highlight matching braces
set comments=sl:/*,mb:\ *,elx:\ */									" Intelligent comments
set wildmode=longest:full											" Use intelligent file completion like in the bash
set wildmenu
set hidden															" Allow changeing buffers without saving them
if has("gui_running")												" GUI Vim settings
    colorscheme wombat												" Set the color scheme
	set guifont=DejaVu\ Sans\ Mono\ for\ Powerline\ 9				" Set the nice Powerline font so Airline could make use of it
  	set lines=999 columns=999										" Run maximized
else																" Console Vim settings
    set t_Co=256													" Set the color scheme
    colorscheme wombat256											
	if exists("+lines")												" Run maximized
		set lines=50
	endif
	if exists("+columns")
		set columns=100
	endif
endif
if has("win32")														" Make backspace working on Windows
    set bs=2
endif


" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Try not to pollute working directory with ~, *.swp, *.un~ files
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
if !isdirectory("/opt/yavide/.tmp")
    call mkdir("/opt/yavide/.tmp", "p")
endif
if !isdirectory("/opt/yavide/.tmp/.backup")
    call mkdir("/opt/yavide/.tmp/.backup", "p")
endif
if !isdirectory("/opt/yavide/.tmp/.swp")
    call mkdir("/opt/yavide/.tmp/.swp", "p")
endif
if !isdirectory("/opt/yavide/.tmp/.undo")
    call mkdir("/opt/yavide/.tmp/.undo", "p")
endif
set backupdir=/opt/yavide/.tmp/.backup//
set directory=/opt/yavide/.tmp/.swp//
set undodir=/opt/yavide/.tmp/.undo//


" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" YouCompleteMe vs. clang_complete plugin setup
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
set completeopt=menu,menuone											" Complete options (disable preview scratch window, longest removed to aways show menu)
set pumheight=20														" Limit popup menu height
let g:pathogen_disabled = []
if myvar_use_ycm_plugin
	call add(g:pathogen_disabled, 'clang_complete')						" Make sure we disable loading clang_complete plugin
	let g:ycm_global_ycm_extra_conf = myvar_ycm_extra_conf_file			" Path to the ycm configuration file
	"let g:ycm_min_num_of_chars_for_completion = 99						" Comment-out to disable identifier completion
	let g:ycm_filetype_whitelist = {'c' : 1, 'cpp' : 1}					" Limit the YCM scope *only* to filetypes listed here (add more if you like or comment it out to work on all files)
	let g:ycm_error_symbol = 'X'
	let g:ycm_warning_symbol = '!'
else
	call add(g:pathogen_disabled, 'YouCompleteMe')						" Make sure we disable loading YouCompleteMe plugin
	let g:clang_use_library = 1											" Use libclang directly
	let g:clang_library_path = myvar_libclang_location					" Path to the libclang on the system
	let g:clang_complete_auto = 1										" Run autocompletion immediatelly after ->, ., ::
	let g:clang_complete_copen = 1										" Open quickfix window on error
	let g:clang_periodic_quickfix = 0									" Turn-off periodic updating of quickfix window (g:ClangUpdateQuickFix() does the same)
	let g:clang_snippets = 1											" Enable function args autocompletion
	let g:clang_snippets_engine = 'ultisnips'							" Use UltiSnips engine for function args autocompletion (works better for me)
	"let g:clang_snippets_engine = 'clang_complete'						" Use clang_complete engine for function args autocompletion (didn't work so well)
	"let g:clang_trailing_placeholder = 1								" Relevant only when clang_complete engine is used
	set concealcursor = vin												" Configure various parameters relevant to function args autocompletion
	set conceallevel = 2												" 
	let g:clang_conceal_snippets = 1									" 
	"let g:clang_hl_errors = 0											" Turn-off error highlighting
	"let g:clang_complete_patterns = 1									" (Does not work for me) Turn-on autocompletion for language constructs (i.e. loops)
	"let g:clang_complete_macros = 1
endif


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
let g:SuperTabDefaultCompletionType='<c-x><c-u><c-p>'					" Set the default completion type
"let g:SuperTabDefaultCompletionType = 'context'						" You can play with these settings as well but they didn't work well for me
"let g:SuperTabCompletionContexts = ['s:ContextText', 's:ContextDiscover']
"let g:SuperTabLongestHighlight=1
"let g:SuperTabLongestEnhanced=1


" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Session plugin
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
let g:session_autoload = 'yes'											" Automatically load previous session
let g:session_autosave = 'yes'											" Automatically save current session
let g:session_default_to_last = 1										" Open last active session
let g:session_directory = expand('<sfile>:p:h') . "/sessions"			" Store session information where '.vimrc' is stored


" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Git plugin
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"set statusline=%{GitBranch()}


" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Airline plugin
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
set laststatus=2
let g:airline_powerline_fonts = 1										" Use Powerline fonts to show beautiful symbols
let g:airline#extensions#tabline#enabled = 1							" Display tab bar with buffers
if ! has('gui_running')													" Fix the timout when leaving insert mode (see http://usevim.com/2013/07/24/powerline-escape-fix)
  set ttimeoutlen=10
  augroup FastEscape
    autocmd!
    au InsertEnter * set timeoutlen=0
    au InsertLeave * set timeoutlen=10
  augroup END
endif


" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" CtrlP plugin
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"let g:ctrlp_working_path_mode = 'ra'									" 
let g:ctrlp_match_window = 'bottom,order:btt,min:1,max:10,results:15'	" Setup the results window position and dimensions
let g:ctrlp_by_filename = 1												" Rather search by filenames only
let g:ctrlp_lazy_update = 50											" Update the matching window 50ms after user has stopped typing
if myvar_use_ctrlp_ag_engine
	let g:ctrlp_user_command = 'ag %s -l --nocolor -g ""'				" Use rather external tool (Silver Searcher) to obtain the results
else
	let g:ctrlp_max_files = 0											" Set no limit to maximum number of files to scan
	"let g:ctrlp_max_depth = 80											" Set directory recursion depth (default is 40)
	set wildignore+=*.exe,*.so,*.a,*.dll,*.o,*.bin,*.img,*.hex,*.fw		" Ignore particular directories and filetypes
	let g:ctrlp_custom_ignore = {										" 
	    \ 'dir': '\v[\/]\.(git|hg|svn|bzr)$',							" .git, .svn, .hg, .bzr
	    \ 'file': '\v\.(exe|so|a|dll|o|bin|img|hex|fw)$',				" .exe, .so, .a, .dll, .o, .bin, .img, .hex, .fw
		"\ 'link': 'SOME_BAD_SYMBOLIC_LINKS',
	    \ }
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
" Function: 	CreateTags()
" Description:	Starts generation of ctags in currently selected node in NERDTree
" Dependency:	NERDTree, ctags exuberant
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function CreateTags()
    let curNodePath = g:NERDTreeFileNode.GetSelected().path.str()
	exec ':!ctags -R --c++-kinds=+p --fields=+iaS --extra=+q -f ' . curNodePath . '/tags ' . curNodePath
endfunction


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
map <C-Tab> :bnext<CR>|"												Go to next buffer
map <C-S-Tab> :bprevious<CR>|"											Go to previous buffer
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
nmap <F5> :call CreateTags()<CR>|"										Create/update ctags in currently selected NODETree directory

nmap <F7> :make<CR>|"													Build using :make (in insert mode exit to command mode, save and compile)
imap <F7> <ESC>:w<CR>:make<CR>|"
nmap <S-F7> :make clean all<CR>|"										Build using :make clean all
imap <S-F7> <ESC>:w<CR>:make clean all<CR>|"

