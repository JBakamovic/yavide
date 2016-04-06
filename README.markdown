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
This open-source project is about making a fully-fledged and modern IDE built on top of popular Vim editor. Already existing numerous features
found in Vim editor along with its powerful plugin engine will be used to carry out the features which can be found in more popular and
mainstream IDEs. In contrast, this IDE will additionally put focus on some specific requirements not being addressed by any other IDE.

## One to rule them all
Has it ever occurred to you to participate in a project(s) encompassing multiple platforms and/or technologies where each of them would impose a
requirement for specific development toolsets, such as different IDEs, toolchains, debuggers, build systems etc.? If it has, then you will
know how valuable would be to have a single and open-source product which could be utilized for whole such development. Why? There are numerous
reasons behind it but development targeting various platforms is usually done in very specialized, and very often commercial, IDEs which:
* mostly put focus on development for a particular platform
* do not support development for any other platform or provide a very limited support
* contain only a subset of features usually found in more advanced and mainstream IDEs
* are not easily extensible by the community
* are proprietary
* etc.

Having a standard and unified product would mitigate the aforementioned problems, but will also make you not to unnecessary waste your precious 
time by constantly re-learning the same tools. This is a pretty much common scenario if you are performing in dynamic work environment 
(i.e. short-term projects). So, one of the main goals of this project will be to build a single toolset which will provide an integrated 
environment to develop code no matter what platform is targeted for, such as:
* `bare-metal`,
* `RTOS`,
* `embedded-Linux`,
* `Android`,
* `desktop Linux, OS X, Windows, ...`

## Large-scale software
Moreover, there is yet to be seen an IDE which can cope with a code base as large and as complex as Android. This is what you definitely 
want to have if you do Android platform development. No IDE which has been set to that challenge was able to handle it. Be it Eclipse, 
Qt Creator or Codelite, each one of them would crash on a 64-bit Intel-i5 @2.5GHz machine with 12GB of RAM. Crash would always occur 
during the very basic operation: creating a new project and importing an existing Android source code. In either case, RAM would be 
eventually eaten up, probably by background source code indexing services, resulting in an application and/or system freeze.
This IDE will not get you into such problems.

## Mixed programming languages software
And what about projects such as Android containing source code written in multiple programming languages? IDEs present on the market, or
at least those that I am aware of, are usually able to handle single programming language per project. This in turn has a consequence of 
making the source code indexing service ignore all of the source code written in other programming languages and thus making impossible 
to utilize a whole lot of IDE features on such code (i.e. `find symbol references`, `go to definition`, `auto-complete` and alike).
To give you an example, one could easily imagine a project which features a middleware written in Java and all other platform-specific or 
performance-wise stuff written in some of the native programming languages such as C or C++. If one is employed in developing code for 
the whole stack, it would be very limiting to have IDE features working only for the subset of programming languages used in the project. 
This is a very important issue which has been genuinely addressed by this IDE.

## Good software design principles
Besides the aforementioned points, this IDE will also provide a complete development environment which will incorporate a programmers toolkit
which provides more seamless way to design better software. For example, it will integrate tools for:
* source code static analysis,
* unit-testing,
* source code management systems,
* docs generation

## Open-source at its finest
One may ask themselves is it really possible and realistic task to build a full-blown IDE in a reasonable time by a single developer? 
Thanks to the huge amount of open-source software which can be re-used and perfectly fitted into the IDE features, I think there is no 
space for doubt. Let me list just some of the open-source software this IDE relies on: `Vim`, `GNU GCC`, `Clang`, `GDB`, `LLDB`, 
`GNU Make`, `ctags`, `cscope`, `gtags`, `cppcheck`, `clang-analyzer`, `Git`, etc. Having in mind that open-source became a main driver
in nowadays technology advances, this list will only get bigger and better.


# Features
* Bundled and tweaked for C/C++ development
  * With plans to add support for Python & Java
* Project management & Project explorer
  * Featuring seamless project handling 
* Class browser
  * Featuring an overview of symbols defined in current unit 
    (i.e. macro, struct, class, method, namespace, etc.)
* Source code auto-completion
  * Featuring real C/C++ compiler back-end to ensure total correctness
* Source code navigation
  * Featuring a fully automated tag generation system running in background
    to ensure the best UI experience
* Source code static analysis
  * Featuring variety of tools to strengthen your code even more
* Source code management client integration
  * Featuring integration of `Git` client (and more to follow)
* Build tools
  * Featuring integration of `make` (and more to follow)
* Many more miscellaneous features like:
  * Syntax highlighting
  * Highlight all occurrences
  * Parenthesis auto-complete
  * Context-aware ordinary text auto-complete
  * Multiple-selection editing support
  * Code snippets
  * `grep` support
  * `bash` shell integration
  * Color schemes support


# Requirements
* Gnome version of Vim 7.3+ compiled with `python` support amongst other standard features like `clientserver`, `servername`, `conceal`, `ctags` and alike.
* Python 2.x+
* GNU Make
* GNU GCC
* GNU G++
* Git
* `libclang.so`
* Internet connection

In `fedora`-based distributions, one may install the requirements by running:
* `sudo dnf --refresh install @development-tools gvim python2 git clang-devel`

In `debian`-based distributions, one may install the requirements by running:
* `sudo apt-get update`
* `sudo apt-get install build-essential vim-gnome python2.7 git libclang-dev`


# Installation
Default installation path is set to `/opt/yavide`. To use different installation directory, provide it as a command line argument to `install.sh` script.

1. `cd ~/ && git clone https://github.com/JBakamovic/yavide.git`
2. `cd yavide && ./install.sh <install_directory>`
  * if `<install_directory>` is empty, installation path will be set to `/opt/yavide`
  * if `<install_directory>` is not empty, installation path will be set to `<install_directory>/yavide`
3. `sudo rm -R ~/yavide`

If you experience any installation issues be sure to consult the [FAQ](#faq) section first.


# Usage overview
Category                          | Shortcut                          | Description
--------------------------------- | --------------------------------- | ---------------------------------
**Project management**            |                                   |
                                  | `<Ctrl-s>n`                       | Create new project
                                  | `<Ctrl-s>i`                       | Import project with already existing code base
                                  | `<Ctrl-s>o`                       | Open project
                                  | `<Ctrl-s>c`                       | Close project
                                  | `<Ctrl-s>s`                       | Save project
                                  | `<Ctrl-s>d`                       | Delete project
**Buffer management**             |                                   |
                                  | `<Ctrl-c>`                        | Close current buffer
                                  | `<Ctrl-c-a>`                      | Close all buffers
                                  | `<Ctrl-Alt-c>`                    | Close all buffers but the current one
                                  | `<Ctrl-s>`                        | Save current buffer
                                  | `<Ctrl-Tab>`                      | Go to next buffer
                                  | `<Ctrl-Shift-Tab>`                | Go to previous buffer
                                  | `<Ctrl-Down>`                     | Scroll buffer by one line (down)
                                  | `<Ctrl-Up>`                       | Scroll buffer by one line (up)
**Buffer modes**                  |                                   | 
                                  | `<ESC>`                           | Enter the `normal` mode
                                  | `<a>`                             | Enter the `insert` mode (append after cursor)
                                  | `<i>`                             | Enter the `insert` mode (insert before cursor)
                                  | `<Shift-v>`                       | Enter the `visual` mode (line mode)
                                  | `<v>`                             | Enter the `visual` mode (character mode)
**Buffer editing**                |                                   | 
                                  | `<Ctrl-a>`                        | Select all
                                  | `<Ctrl-x>`                        | Cut
                                  | `<Ctrl-c>`                        | Copy
                                  | `<Ctrl-v>`                        | Paste
                                  | `<Ctrl-z>`                        | Undo
                                  | `<Ctrl-r>`                        | Redo
                                  | `<Shift-s>`                       | Delete the whole line
                                  | `<*>` or `<Shift-LeftMouse>`      | Highlight all occurrences of text under the cursor
                                  | `<Enter>`                         | Clear highlighted text occurences
                                  | `<Ctrl-n>`                        | Start multiple-selection editing with the text under the cursor. Each consecutive press will highlight the next occurrence of selected text. After all occurrences have been marked, do the text editing with usual commands (`c`, `s`, `i`, `a`, etc.).
                                  | `<Ctrl-p>`                        | When in multiple-selection editing mode, one may press this key combination to remove the current occurrence and go back to the previous one.
                                  | `<Ctrl-x>`                        | When in multiple-selection editing mode, one may press this key combination to skip the current occurrence and go to the following one.
**Window management**             |                                   | 
                                  | `<Ctrl-w>c`                       | Close current window
                                  | `<Ctrl-w><Arrow>`                 | Navigate through windows using `<left>`, `<right>`, `<up>` & `<down>` arrows
                                  | `<Ctrl-w>s`                       | Create new horizontal window split
                                  | `<Ctrl-w>v`                       | Create new vertical window split
                                  | `<Ctrl-w>=`                       | Make split windows equal in size
**Search utilities**              |                                   |
                                  | `<Ctrl-f>`                        | Open search dialog
                                  | `<Ctrl-h>`                        | Open search and replace dialog
                                  | `:grep <input>`                   | Run `grep` with provided `<input>`
**Source code commenting**        |                                   |
                                  | `<,cA>`                           | Insert comment at the current line
                                  | `<,cc>`                           | Comment the selected line/block
                                  | `<,cs>`                           | Comment the selected line/block (other style)
                                  | `<,cu>`                           | Uncomment the selected line/block
**Source code navigation**        |                                   |
                                  | `<F3>`                            | Open file under the cursor
                                  | `<F4>`                            | Switch between header & corresponding implementation file
                                  | `<Shift-F4>`                      | Switch between header & implementation (in a vertical split window)
                                  | `<F12>` or `<Ctrl-LeftMouse>`     | Goto definition of token under the cursor
                                  | `<Shift-F12>`                     | Goto definition of token under the cursor (in a vertical split window)
                                  | `<Ctrl-t>` or `<Ctrl-RightMouse>` | Jump back from definition
                                  | `<Ctrl-\>s`                       | Find all references to token under the cursor
                                  | `<Ctrl-\>g`                       | Find global definition(s) of token under the cursor
                                  | `<Ctrl-\>c`                       | Find all functions calling the function under the cursor
                                  | `<Ctrl-\>d`                       | Find all functions called by the function under the cursor
                                  | `<Ctrl-\>i`                       | Find all files that include the filename under the cursor
                                  | `<Ctrl-\>t`                       | Find all instances of the text under the cursor
                                  | `<Ctrl-\>e`                       | Search for the word under the cursor using `egrep`
**Source code static analysis**   |                                   | 
                                  | `:YavideAnalyzerCppCheckBuf`      | Runs the `cppcheck` static analysis on current buffer
                                  | `:YavideAnalyzerCppCheck`         | Runs the `cppcheck` static analysis on whole project
**Build management**              |                                   | 
                                  | `<F7>`                            | Build project in `release` mode
                                  | `<Shift-F7>`                      | Build project in `debug` mode
                                  | `<F8>`                            | Clean build
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
                                  | `:sh`                             | Enter the `bash` shell

# Screenshots

![Yavide](https://raw.githubusercontent.com/wiki/JBakamovic/yavide/images/yavide_in_action.png)
[More details ...](https://github.com/JBakamovic/yavide/wiki/Screenshots#how-it-looks-like)

# Credits
This is an alphabetically ordered list of third-party Vim plugins currently utilized in the system:
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


# FAQ
1. Installation process does not complete all the steps successfully.
  * Issues can arise when some required packages, like `libpcre3`, are named differently or 
    not even present in your distribution repository. Identify these packages and 
    install them manually.

2. Class browser does not show any symbols.
  * Check if `exuberant-ctags` have been correctly installed on the system.

3. Source code auto-complete does not work.
  * Check if `libclang` has been installed on the system.
  * Check if path to the `libclang.so` has been set properly in `.user_settings.vimrc`.
  * Check if `.clang_complete` contains valid entries (include directories) for your project.

