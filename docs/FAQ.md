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

4. The following error occurs: `E319: Sorry, the command is not available in this version: python import sys, vim`
  * This error can occur if your version of `vim` is not compiled with `python` support. One can easily check this by running `vim --version`.
  * Instance of `vim` deployed on `Ubuntu 16.04` for example does not have compiled in the `python` support. To fix the issue on this Ubuntu system one can run the following commands:
    * `sudo apt install vim-gnome-py2`
    * `sudo update-alternatives --set vim /usr/bin/vim.gnome-py2`
    * `sudo update-alternatives --set gvim /usr/bin/vim.gnome-py2`
