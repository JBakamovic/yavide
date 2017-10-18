# Contents
* [Changes](#changes)
* [Installation](#installation)
* [Usage](#usage)
* [Screenshots](#screenshots)
* [Features](#features)
* [Credits](#credits)
* [FAQ](#faq)

# Changes
* 12th of February, 2017
    * Implemented [type deduction](docs/services_framework.md#type-deduction) service.
        * A mouse cursor hover over source code will give details about the underlying constructs (i.e. data types, function signatures, etc.).
* 10th of February, 2017
    * Implemented Clang-based [fixits & diagnostics](docs/services_framework.md#fixits-and-diagnostics) service.
    * Implemented mechanism which enables sharing the same AST within multiple services:
        * E.g. Once the AST is built, semantic syntax highlighting and Clang fixits services
          will be able to share the same AST.
        * This will be especially important when more heavy-weight Clang-based services will
          come into play, such as indexer and auto-completion engine.
    * Refactored server-side code to decouple editor-specific integrations from the core implementation of services.
* 19th of January, 2017
    * Polished some rough edges around syntax highlighting:
        * Implemented support for handling a set of overloaded functions or function templates (CursorKind.OVERLOADED_DECL_REF expressions)
        * Implemented support for handling dependent types (TypeKind.DEPENDENT expressions)
        * Implemented non-intrusive patch for clang.cindex enabling more flexible AST traversal
* 28th of December, 2016
    * Implemented Clang-based source code [syntax highlighting](docs/services_framework.md#syntax-highlighting) service
      (run `cd <yavide_install_dir>/colors/yaflandia && git pull` to get required colorscheme changes)
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
* Source code syntax highlighting based on `libclang`
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
* NERDCommenter (https://github.com/scrooloose/nerdcommenter)
* NERDTree (https://github.com/scrooloose/nerdtree)
* SuperTab (https://github.com/ervandew/supertab)
* Tagbar (https://github.com/majutsushi/tagbar)
* UltiSnips (https://github.com/SirVer/ultisnips)
* vim-airline (https://github.com/bling/vim-airline)
* vim-autoclose (https://github.com/Townk/vim-autoclose)
* vim-fugitive (https://github.com/tpope/vim-fugitive)
* vim-gitgutter (https://github.com/airblade/vim-gitgutter)
* vim-multiple-cursors (https://github.com/terryma/vim-multiple-cursors)
* vim-pathogen (https://github.com/tpope/vim-pathogen)

# FAQ
See [FAQ](docs/FAQ.md).

