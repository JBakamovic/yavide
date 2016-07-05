# Contents
* [FAQ](#faq)

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

