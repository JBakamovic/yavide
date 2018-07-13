# Contents
* [Requirements](#requirements)
* [Installation](#installation)

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

1. `cd ~/ && git clone --recursive https://github.com/JBakamovic/yavide.git`
2. `cd yavide && ./install.sh <install_directory>`
  * if `<install_directory>` is empty, installation path will be set to `/opt/yavide`
  * if `<install_directory>` is not empty, installation path will be set to `<install_directory>/yavide`
3. `sudo rm -R ~/yavide`
4. You can run `Yavide` by:
  * Double-clicking `yavide` icon from your `Desktop`
  * Typing in `yavide` in Unity/Gnome launcher
  * Picking `yavide` from classic start menu (`Programming` section)
  * Running it from the terminal by typing in `yavide`

If you experience any installation issues be sure to consult the [FAQ](FAQ.md) first.

