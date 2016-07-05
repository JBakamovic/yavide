# Contents
* [Changes](#changes)
* [Installation](#installation)
* [Usage](#usage)
* [Screenshots](#screenshots)
* [Features](#features)
* [Credits](#credits)
* [FAQ](#faq)

# Changes
* 1st of July, 2016
    * Implemented new generic client-server (async) [framework](docs/services_framework.md#framework) which enables dispatching any kind of operations to run in a separate 
      non-blocking background processes (so called [services](docs/services_framework.md#services)) and upon whose completion results can be reported back to the server ('Yavide').
    * Implemented 4 new services on top of the new async framework:
        * On-the-fly source code [syntax highlighting](docs/services_framework.md#syntax-highlighting) service.
        * On-the-fly source code [indexing](docs/services_framework.md#indexing) service.
        * Clang-based source code [auto-formatting](docs/services_framework.md#auto-formatting) service.
        * [Project builder](docs/services_framework.md#project-builder) service.

# Installation
See [Installation guide](docs/INSTALL.md).

# Usage
See [Usage](docs/usage.md).

# Screenshots
![Yavide](https://raw.githubusercontent.com/wiki/JBakamovic/yavide/images/yavide_in_action.png)

See [some GIFs in action](docs/services_framework.md).

[More details ...](https://github.com/JBakamovic/yavide/wiki/Screenshots#how-it-looks-like)

# Features
* Bundled and tweaked for C/C++ development
* Project management
  * Create new projects or import existing code base into the new workspace
* Project explorer
  * Explore the project using a tree-view widget
* Project builder
  * Trigger your builds within the environment to run non-intrusively in background
* Class browser
  * Featuring an overview of symbols defined in current unit (i.e. macro, struct, class, method, namespace, etc.)
* Source code auto-completion
  * Backed by real C/C++ compiler back-end to ensure total correctness
* Source code navigation
  * Featuring a fully automated tag generation system which keeps the symbol database up-to-date
* Source code syntax highlighting
  * Providing more rich syntax highlighting support than the one provided originally by `Vim`
* Source code auto-formatting
  * `clang-formatter` support
* Source code static analysis
  * `Cppcheck` support
* Source code management client integration
  * Featuring integration of `Git` client
* Many more miscellaneous features like:
  * Parenthesis auto-complete
  * Context-aware ordinary text auto-complete
  * Multiple-selection editing support
  * Code snippets
  * Color schemes support

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
See [FAQ](docs/FAQ.md).

