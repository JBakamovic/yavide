" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Editor settings
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
autocmd! bufwritepost .vimrc source %								" Auto reload .vimrc when changed, this avoids reopening vim
autocmd FileType qf wincmd J										" Make the quickfix window always appear at the bottom
filetype plugin indent on											" Turn on the filetype plugin
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
set nowrap															" Do not wrap lines
set textwidth=120													" Wrap lines at 120 chars. 80 is somewhat antiquated with nowadays displays.
let mapleader = ","													" Define ',' is leader key
syntax on															" Turn syntax highlighting on
set ignorecase
set smartcase
set incsearch
set hlsearch														" Highlight all search results
set number															" Turn line numbers on
set showmatch														" Highlight matching braces
set comments=sl:/*,mb:\ *,elx:\ */									" Intelligent comments
set wildmode=longest:full											" Use intelligent file completion like in the bash
set wildmenu
set hidden															" Allow changing buffers without saving them
set cul																" Highlight the current line
set backspace=2														" Backspace tweaks
set backspace=indent,eol,start
set smarttab
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

set nobackup
set nowritebackup
set noswapfile
