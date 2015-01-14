# Contents
* [Introduction](#introduction)
* [Features](#features)
* [Requirements](#requirements)
* [Installation](#installation)
* [Usage](#usage)
* [Screenshots](#screenshots)
* [Credits](#credits)
* [FAQ](#faq)


# Introduction
Aim of this open-source project is to develop a fully-fledged IDE based on popular Vim editor reusing all of its features. Its powerful plugin 
engine will be used as an entry point towards the implementation of features normally found in other development environments and hopefully more.

Main goal will be to build an unified interface which will provide a common environment to develop code no matter what platform is targeted for. 
I.e.:
* `bare-metal`,
* `RTOS`,
* `embedded-Linux`,
* `Android`,
* `desktop`,
* etc.

Development for such a platforms is usually done in very specialized IDEs which:
* mostly put focus on development for a particular platform 
* do not support development for any other platform
* contain only a subset of features usually found in more advanced and mainstream IDEs 
* are not that easily extensible
* are not free
* etc.

Not to mention that it gets pretty annoying to get used to a completely new environment each time your projects require you to develop
code for a different platform. This is a pretty common scenario if you work in dynamic environments.

Moreover, there is yet to be seen an IDE which can cope with a code base as large and as complex as Android. No IDE which has been set to 
that challenge recently was able to handle it. Usually, an IDE would crash at the very beginning during the source code import operation. 

What about projects (i.e. Android) containing source code written in multiple programming languages? IDEs present on the market usually 
provide support to import the source code of only a single programming language. This has a consequence of making the source code indexing service 
ignore all of the source code written in other programming languages and thus making impossible to use IDE features such as
`find symbol references` or `go to definition` to navigate through those parts of code. For example, one could easily imagine a project 
which features a middleware written in Java and all other platform-specific or performance-wise stuff written in some of the native 
programming languages such as C or C++. If one is employed in developing code for the whole stack, it would be very limiting to have IDE 
features working only for the source code type which has been selected during the import and/or project creation. This is an issue 
which has been already addressed by this IDE.

Besides multi-platform support, this IDE will also provide a complete development environment which will incorporate all elements of good 
software design including the integration of:
* test automation frameworks,
* code documenting tools,
* static analysis tools


# Features
* Bundled and tweaked for C/C++ development
* Project management 
  * Multiple project workspaces support
  * Various project types (`Generic`, `C`, `C++`, `Mixed`) support
* Project explorer
  * Tree-view support
* Class browser
  * Provides an overview of symbols defined in current file
  * i.e. macro, variable, function, struct, method, class, namespace, etc.
* Source code auto-completion
  * Utilizes `clang` engine
* Source code navigation
  * Open file under the cursor
  * Switch between header & implementation files
  * Go to declaration, go to definition
  * Find all references to the given symbol
  * Find all functions calling the given function
  * Find all functions called by the given function
  * Find all files that include the given filename
* Source code static analysis
  * `cppcheck` support
  * `Clang Static Analyzer` support to be added
* Build tools integration 
  * `GNU make` support
* SCM client integration
  * `git` support along with the side-column showing modifications in real-time
* Powerful search utilities
  * Search dialog
  * Search & replace dialog
  * `grep` in interactive mode
    * Enables easy navigation through the results
* Miscellaneous editor features
  * Highlight all occurrences
  * Parenthesis auto-complete
  * Context-aware text auto-complete
  * Multiple-selection editing support
  * Code snippets
* Bash shell integration
* Support for various color schemes
* Plugin manager


# Requirements
* Gnome version of Vim 7.3+ compiled with `python` support amongst other standard features like `clientserver`, `conceal`, `ctags` and alike.
* Python 2.x+
* GNU Make
* GNU GCC
* GNU G++
* Git
* `libclang.so`
* Internet connection

In `debian`-based distributions, one may install the requirements by running:
* `sudo apt-get update`
* `sudo apt-get install build-essential vim-gnome python2.7 git libclang-dev`


# Installation
Default installation path is set to `/opt/yavide`. Changing it is not currently supported but will be in future.

1. `cd ~/ && git clone https://github.com/JBakamovic/yavide.git`
2. `cd yavide && ./install.sh`
3. `sudo rm -R ~/yavide`

If you experience any installation issues be sure to consult the [FAQ](#faq) section first.

# Usage
Category                          | Shortcut                          | Description
--------------------------------- | --------------------------------- | ---------------------------------
**Project management**            |                                   |
                                  | `<Ctrl-s>n`	                      | Create new project
                                  | `<Ctrl-s>o`                       | Open project
                                  | `<Ctrl-s>c`                       | Close project
                                  | `<Ctrl-s>s`                       | Save project
                                  | `<Ctrl-s>d`                       | Delete project
**Buffer management**             |                                   |
                                  | `<Ctrl-c>`			              | Close current buffer
                                  | `<Ctrl-s>`                        | Save current buffer
                                  | `<Ctrl-Tab>`			          | Go to next buffer
                                  | `<Ctrl-Shift-Tab>`	              | Go to previous buffer
                                  | `<Ctrl-Down>`			          | Scroll buffer by one line (down)
                                  | `<Ctrl-Up>`			              | Scroll buffer by one line (up)
**Buffer modes**                  |                                   | 
                                  | `<ESC>`                           | Enter the `normal` mode
                                  | `<a>`					          | Enter the `insert` mode (append after cursor)
                                  | `<i>`					          | Enter the `insert` mode (insert before cursor)
                                  | `<Shift-v>`	                      |	Enter the `visual` mode (line mode)
                                  | `<v>`					          | Enter the `visual` mode (character mode)
**Buffer editing**                |                                   | 
                                  | `<Ctrl-a>`                        | Select all
                                  | `<Ctrl-x>`                        | Cut
                                  | `<Ctrl-c>`                        | Copy
                                  | `<Ctrl-v>`                        | Paste
                                  | `<Ctrl-z>`                        | Undo
                                  | `<Ctrl-r>`                        | Redo
                                  | `<Shift-s>`				          | Delete the whole line
                                  | `<*>` or `<Shift-LeftMouse>`      | Highlight all occurrences of text under the cursor
                                  | `<Ctrl-n>`                        | Start multiple-selection editing with the text under the cursor. Each consecutive press will highlight the next occurrence of selected text. After all occurrences have been marked, do the text editing with usual commands (`c`, `s`, `i`, `a`, etc.).
                                  | `<Ctrl-p>`                        | When in multiple-selection editing mode, one may press this key combination to remove the current occurrence and go back to the previous one.
                                  | `<Ctrl-x>`                        | When in multiple-selection editing mode, one may press this key combination to skip the current occurrence and go to the following one.
**Window management**             |                                   | 
                                  | `<Ctrl-w>c`			              | Close current window
                                  | `<Ctrl-w><Arrow>`	              | Navigate through windows using `<left>`, `<right>`, `<up>` & `<down>` arrows
                                  | `<Ctrl-w>s`			              | Create new horizontal window split
                                  | `<Ctrl-w>v`			              | Create new vertical window split
                                  | `<Ctrl-w>=`                       | Make split windows equal in size
**Search utilities**              |                                   |
                                  | `<Ctrl-f>`                        |	Open search dialog
                                  | `<Ctrl-h>`				          | Open search and replace dialog
                                  | `:grep <input>`		              | Run `grep` with provided `<input>`
**Source code commenting**        |                                   |
                                  | `<,cA>`				              | Insert comment at the current line
                                  | `<,cc>`				              | Comment the selected line/block
                                  | `<,cs>`				              | Comment the selected line/block (other style)
                                  | `<,cu>`				              | Uncomment the selected line/block
**Source code navigation**        |                                   |
                                  | `<F3>`				              | Open file under the cursor
                                  | `<F4>`				              | Switch between header & corresponding implementation file
                                  | `<Shift-F4>`			          | Switch between header & implementation (in a vertical split window)
                                  | `<F12>` or `<Ctrl-LeftMouse>`     | Goto definition of token under the cursor
                                  | `<Shift-F12>`			          | Goto definition of token under the cursor (in a vertical split window)
                                  | `<Ctrl-t>` or `<Ctrl-RightMouse>` | Jump back from definition
                                  | `<Ctrl-\>s`                       | Find all references to token under the cursor
                                  | `<Ctrl-\>g`                       | Find global definition(s) of token under the cursor
                                  | `<Ctrl-\>c`                       | Find all functions calling the function under the cursor
                                  | `<Ctrl-\>d`                       | Find all functions called by the function under the cursor
                                  | `<Ctrl-\>i`                       | Find all files that include the filename under the cursor
                                  | `<Ctrl-\>t`                       | Find all instances of the text under the cursor
                                  | `<Ctrl-\>e`                       | Search for the word under the cursor using `egrep`
**Source code parser**            |                                   | 
                                  | `<F5>`				              | Generate `ctags` for current project
                                  | `<F6>`                            | Generate `cscope` for current project
**Source code static analysis**   |                                   | 
                                  | `:YavideAnalyzerCppCheckBuf`      | Runs the `cppcheck` static analysis on current buffer
                                  | `:YavideAnalyzerCppCheck`         | Runs the `cppcheck` static analysis on whole project
**Build management**              |                                   | 
                                  | `<F7>`				              | Build project in `release` mode
                                  | `<Shift-F7>`                      | Build project in `debug` mode
                                  | `<F8>`			                  | Clean build
**SCM Git client**                |                                   | 
                                  | `:Gstatus`                        | Runs `git status`
                                  | `:Gcommit`                        | Runs `git commit`
                                  | `:Gmerge`                         | Runs `git merge`
                                  | `:Gpull`                          | Runs `git pull`
                                  | `:Gpush`                          | Runs `git push`
                                  | `:Gfetch`                         | Runs `git fetch`
                                  | `:Glog`                           | Runs `git log`
                                  | `:Gdiff`                          | Runs `git diff`
                                  | `:Gblame`                         | Runs `git blame`
**Misc**                          |                                   | 
                                  | `:YavideLayoutRefresh`            | Refresh the layout (opens up project explorer, class browser and clears up the `quickfix` window)
                                  | `:sh`					          | Enter the `bash` shell

# Screenshots

![Yavide](https://raw.githubusercontent.com/wiki/JBakamovic/yavide/images/yavide_in_action.png)
[More details ...](https://github.com/JBakamovic/yavide/wiki/Screenshots#how-it-looks-like)

# Credits
This is an alphabetically ordered list of third-party plugins currently utilized in the system:
* A (https://github.com/vim-scripts/a.vim)
* Clang_complete (https://github.com/Rip-Rip/clang_complete)
* NERDTree (https://github.com/scrooloose/nerdtree)
* NERDCommenter (https://github.com/scrooloose/nerdcommenter)
* SuperTab (https://github.com/ervandew/supertab)
* Tagbar (https://github.com/majutsushi/tagbar)
* vim-airline (https://github.com/bling/vim-airline)
* UltiSnips (https://github.com/SirVer/ultisnips)
* vim-autoclose (https://github.com/Townk/vim-autoclose)
* vim-fugitive (https://github.com/tpope/vim-fugitive)
* vim-gitgutter (https://github.com/airblade/vim-gitgutter)
* vim-multiple-cursors (https://github.com/terryma/vim-multiple-cursors)
* vim-pathogen (https://github.com/tpope/vim-pathogen)
* vim-session (https://github.com/xolox/vim-session)


# FAQ
1. Installation process does not complete all the steps successfully
  * Issues can arise when some required packages, like `libpcre3`, are named differently or 
    not even present in your distribution repository. Identify these packages and 
    install them manually.


