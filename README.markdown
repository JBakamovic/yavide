# All development activities have been moved to [cxxd](https://github.com/JBakamovic/cxxd) and [cxxd-vim](https://github.com/JBakamovic/cxxd-vim) repositories. To keep up with the latest developments it is encouraged to use [cxxd-vim](https://github.com/JBakamovic/cxxd-vim) plugin. See first section of [FAQ](#faq) for more details.

# Contents
* [Changes](#changes)
* [Installation](#installation)
* [Usage](#usage)
* [Screenshots](#screenshots)
* [Features](#features)
* [Credits](#credits)
* [FAQ](#faq)

# Changes
* 13th of July, 2018
    * Core functionality has been extracted to separate repositories:
        * [cxxd](https://github.com/JBakamovic/cxxd), an implementation of C/C++ language server
        * [cxxd-vim](https://github.com/JBakamovic/cxxd-vim), a Vim frontend developed for `cxxd`
    * `Yavide` will include those as dependencies and will continue to function normally but
      **all development activity and focus is now moved to those projects** so in order to get
      more features and stability please start using them directly from your ordinary Vim config.
* 2nd of December, 2017
    * Implemented Clang-based [indexer](docs/services_framework.md#indexing)
    * Implemented Clang-based [find-all-references](docs/services_framework.md#find-all-references)
    * Implemented Clang-based [go-to-definition](docs/services_framework.md#go-to-definition)
    * Implemented Clang-based [go-to-include](docs/services_framework.md#go-to-include)
    * Implemented support for [clang-tidy](docs/services_framework.md#clang-tidy)
    * Implemented support for [JSON compilation databases](docs/services_framework.md#json-compilation-database)
    * Implemented translation-unit caching mechanisms
    * Various bugfixes and other smaller improvements
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
## Why development focus has been moved to [cxxd](https://github.com/JBakamovic/cxxd) and [cxxd-vim](https://github.com/JBakamovic/cxxd-vim)?
TL;DR Having separated one big monolithic `Yavide` repository into two separate ones (`cxxd` & `cxxd-vim`) brought us more modular, reusable, testable and flexible design. There are many many other advantages to this approach for all of them to be noted down here briefly but the important part now is that the frontend logic (e.g. UI implementation) is now separated from the backend implementation (C/C++ language server features). Both of these developments can now be driven separately and in parallel. Furthermore, `cxxd-vim` behaves like a real Vim plugin so you won't need to use hacky install scripts anymore but a regular way of installing just like for any other Vim plugin out there (e.g. Vundle). For many other details please have a look at respective repositories.

## Other questions
See [FAQ](docs/FAQ.md).

