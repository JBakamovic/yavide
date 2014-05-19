==================================================================================================================================
											Vim Configuration
==================================================================================================================================


----------------------------------------------------------------------------------------------------------------------------------
# Contents
----------------------------------------------------------------------------------------------------------------------------------
* Requirements
* Plugins
* Installation
* Features
* Usage
* Project workspace setup
* Auto-completion
* Fuzzy search
* Known issues
* TODO


----------------------------------------------------------------------------------------------------------------------------------
# Requirements
----------------------------------------------------------------------------------------------------------------------------------
* Vim 7.4
  * http://www.vim.org
* Exuberant Ctags
  * http://ctags.sourceforge.net
* LLVM 3.4
  * http://llvm.org/releases/download.html
* Git
  * http://git-scm.com
* Silver Searcher
  * https://github.com/ggreer/the_silver_searcher
* Powerline Fonts
  * https://github.com/Lokaltog/powerline-fonts


----------------------------------------------------------------------------------------------------------------------------------
# Plugins
----------------------------------------------------------------------------------------------------------------------------------
This configuration utilizes heavy usage of Vi plugins. Otherwise, this setup would not be possible. Here is the list of plugins 
currently integrated:
* NERDTree
  * Tree-like project browser
  * https://github.com/scrooloose/nerdtree
* Session
  * Session manager for handling projects/workspaces
  * https://github.com/xolox/vim-session
* Clang_complete
  * auto-completion
  * https://github.com/Rip-Rip/clang_complete
* YouCompleteMe
  * auto-completion + syntax checking
  * https://github.com/Valloric/YouCompleteMe
* YouCompleteMeFork
  * auto-completion + syntax checking + argument auto-completion
  * https://github.com/oblitum/YouCompleteMe
* SuperTab
  * tab completion + argument auto-completion
  * https://github.com/ervandew/supertab
* Tagbar
  * code outlining
  * https://github.com/majutsushi/tagbar
* Airline
  * support for tabs + enhanced status bar
  * https://github.com/bling/vim-airline
* A
  * switcher between header and implementation + jumping to a file
  * https://github.com/vim-scripts/a.vim
* Auto-close
  * parenthesis auto-complete ("()", "[]", "{}")
  * https://github.com/Townk/vim-autoclose
* NERDCommenter
  * code commenting
  * https://github.com/scrooloose/nerdcommenter
* CtrlP
  * fuzzy search
  * https://github.com/kien/ctrlp.vim
* Grep
  * grep search providing interactive UI to walk through the results
  * https://github.com/yegappan/grep
* UltiSnips
  * code snippets
  * https://github.com/SirVer/ultisnips
* Git
  * Git client
  * https://github.com/motemen/git-vim
* Pathogen
  * package manager
  * https://github.com/tpope/vim-pathogen

Should you want to tweak the existing configuration or learn what additional features these plugins offer, please feel free to 
consult its documentation for more details. This is not by any means an exhaustive configuration.


----------------------------------------------------------------------------------------------------------------------------------
# Installation
----------------------------------------------------------------------------------------------------------------------------------
1. Vim
  * `sudo apt-get install vim-gnome` 	(for GNOME-based desktops like Unity)
  * `sudo apt-get install vim-gtk` 		(for XFCE-, LXDE-, KDE-based desktops)
2. `cd vim-ide`
3. `./install.sh` (do **NOT** run as `sudo`)
4. Wait and hope it will finish successfuly :)


----------------------------------------------------------------------------------------------------------------------------------
# Features
----------------------------------------------------------------------------------------------------------------------------------
* Bundled and tweaked for C/C++ development
* Tree-like project browser
* Session manager for handling projects/workspaces
* Build tools integration (i.e. make)
* Syntax checking on-the-fly (only when YCM plugin is employed)
* Source code auto-completion
* Source code navigation
* Source code outlining
* Source code commenting
* Source code occurence highlighting
* Switching between header and implementation
* Switching to a file under the cursor
* Parenthesis auto-complete
* Code snippets
* Grep search (interactive-mode)
* Fuzzy search
* Search dialog
* Search and replace dialog
* Bash shell integration
* Git client integration
* Tab completion
* Enhanced statusbar/tabbar
* Plugin manager


----------------------------------------------------------------------------------------------------------------------------------
# Usage
----------------------------------------------------------------------------------------------------------------------------------

## Workspace handling
----------------------------------------------------------------------------------------------------------------------------------
* `Ctrl-o`				Open the session
* `Ctrl-e`				Save the session

## Buffer handling
----------------------------------------------------------------------------------------------------------------------------------
* `Ctrl-c`				Close buffer
* `Ctrl-Tab`			Go to next buffer
* `Ctrl-Shift-Tab`		Go to previous buffer
* `Ctrl-Down`			Scroll buffer by one line (down)
* `Ctrl-Up`				Scroll buffer by one line (up)

## Window handling
----------------------------------------------------------------------------------------------------------------------------------
* `Ctrl-w + c`			Close the current window
* `Ctrl-w + <Arrow>`	Navigate through windows
* `Ctrl-w + s`			Split the window horizontally
* `Ctrl-w + v`			Split the window vertically

## Tab handling
----------------------------------------------------------------------------------------------------------------------------------
* `Ctrl-PgDn`			Go to next tab
* `Ctrl-PgUp`			Go to previous tab

## Build
----------------------------------------------------------------------------------------------------------------------------------
* `F7`					Build using :make
* `Shift-F7`			Clean build using :make clean all

## Code navigation
----------------------------------------------------------------------------------------------------------------------------------
* `F3`					Open file under the cursor
* `F4`					Switch between header and corresponding implementation file
* `Shift-F4`			Switch between header/implementation in a vertically splitted window
* `F5`					Create/update ctags in currently selected tree-explorer directory (be cautious to select the root dir first!)
* `F12`					Goto definition (but open a dialog to choose from if multiple definitions exist!)
* `Shift-F12`			Goto definition in a vertically splitted window
* `Ctrl-LeftMouse`		Goto definition (but open a dialog to choose from if multiple definitions exist!)
* `Ctrl-RightMouse`		Jump back from definition
* `Ctrl-t`				Jump back from definition

## Editor
----------------------------------------------------------------------------------------------------------------------------------
* `a`					Enter the insert mode (append after cursor)
* `i`					Enter the insert mode (insert before cursor)
* `Shift-v`				Enter the visual mode (line mode)
* `v`					Enter the visual mode (character mode)
* `Ctrl-s`				Save currently opened file
* `Ctrl-a`				Select all
* `Ctrl-x`				Cut
* `Ctrl-c`				Copy
* `Ctrl-v`				Paste
* `Ctrl-z`				Undo
* `Shift-s`				Delete the whole line
* `*`					Highlight occurences of word under the cursor
* `Shift-LeftMouse`		Highlight occurences of word under the cursor
* `,cA`					Insert comment at the current line
* `,cc`					Comment the selected line/block
* `,cs`					Comment the selected line/block (other style)
* `,cu`					Uncomment the selected line/block

## Search
----------------------------------------------------------------------------------------------------------------------------------
* `Ctrl-f`				Open find dialog
* `Ctrl-r`				Open find and replace dialog
* `Ctrl-p`				Run CtrlP fuzzy search
* `:Grep`				Run grep on provided input
* `:GrepBuffer`			Run grep on current buffer
* `:Rgrep`				Run rgrep on provided input

## Misc
----------------------------------------------------------------------------------------------------------------------------------
* `:sh`					Enter the bash shell
* `:make`				Start the build process in current directory


----------------------------------------------------------------------------------------------------------------------------------
# Project workspace setup
----------------------------------------------------------------------------------------------------------------------------------
* Open GVim
* Using the NERDTree, with your mouse and/or keyboard navigate to the root directory of your project
* Press `C` to enter the directory
* Issue `:SaveSession <arbitrary_name_of_the_session>` to save the session with corresponding name
* To make sure that it works exit GVim
* Open GVim again
* Press `Ctrl-o` to open the session
* If there is > 1 session available, session manager will let you select the one you want (by entering the number for session)
* Otherwise it will just open the last used session
* Every setting regarding the NERDTree root directory, window layout, previously opened tabs, buffers, etc. should be as in the last time


----------------------------------------------------------------------------------------------------------------------------------
# Auto-completion
----------------------------------------------------------------------------------------------------------------------------------
This feature is provided by 3 different plugins:
* `Clang_complete`
* `YouCompleteMe`
* `YouCompleteMe` fork (defaults over original `YouCompleteMe` in the installation)

To avoid problems, no more than 1 plugin should be running at the same time. Therefore, to select one of the mechanisms, 
one should use pre-defined variables located at top of the `.vimrc` file:
* `use_ycm_plugin`
  * set this variable to 1 if you should want to use the YouCompleteMe plugin
  * otherwise, when set to 0 (default), `clang_complete` plugin will be used

At the time of writing, best results I have observed with clang_complete plugin. Hence, it is a default.
YouCompleteMe plugin works well with C++ files, whereas it has problems with C files. Function arguments are not being 
recognized (displayed in a small bubble window) until user enters the OmniComplete mode (by pressing the `Ctrl-space`). This is 
quite unhandy.

Another problem that YouCompleteMe has is the auto-completion of function/method arguments. This is solved by the fork of 
YouCompleteMe plugin but still suffers from the same C-file problem mentioned previously.

Clang_complete seems not to have these kind of problems, or at least I have not observed them.

Moreover, YouCompleteMe requires an additional configuration file to be tweaked on per-project basis. An example of this file 
providing a starting point can be found at `.ycm_extra_conf.py`. To learn how to configure it, consult the official 
YouCompleteMe documentation.


----------------------------------------------------------------------------------------------------------------------------------
# Fuzzy search
----------------------------------------------------------------------------------------------------------------------------------
Search engine that fuzzy search (CtrlP plugin) utilizes by default is the one from Vi (`globpath()`). This mechanism seems to be 
rather slow for big projects. One of the causes is probably interpreted Vimscript language that it is written in. Authors of the 
plugin were aware enough of that fact so they have provided means to run external mechanism if needed. That's where 
Silver Searcher comes in. It is implemented in C language and therefore provides much better performance.
To enable it one should use pre-defined variable located at top of the `.vimrc` file:
* `use_ctrlp_ag_engine`
  * set this variable to 1 (default) if you should want to use the `Silver Searcher`
  * otherwise, when set to 0, Vi mechanism will be used


----------------------------------------------------------------------------------------------------------------------------------
# Known issues
----------------------------------------------------------------------------------------------------------------------------------
Layout sometimes can become screwed up due to some command and/or plugin. This oftenly results in loss of a tree explorer and/or 
tag list. To restore it:
* Kill any empty windows that may have appeared (give focus to the window and press `Ctrl-w c`)
* Switch to some existing buffer (`Ctrl-Tab`)
* If tree explorer is missing, enter `:NERDTree`
* If tag list is missing, enter `:Tagbar`
* Adjust the size of the windows
* `:SaveSession`

----------------------------------------------------------------------------------------------------------------------------------
# TODO
----------------------------------------------------------------------------------------------------------------------------------
* Doc generation (i.e. Doxygen)
* CScope integration
* Syntastic syntax checking on-the-fly
* Debugging
* Code folding
* Spell check


