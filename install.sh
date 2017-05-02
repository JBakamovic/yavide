#!/bin/bash
# yavide installation script

#####################################################################################################
# Variables
#####################################################################################################
SYSTEM_PACKAGE_MANAGER=""
SYSTEM_PACKAGE_TYPE=""
SYSTEM_PACKAGE_SET=""
YAVIDE_INSTALL_DIR_DEFAULT="/opt"
PIP_INSTALL_CMD="pip install"

#####################################################################################################
# Helper functions
#####################################################################################################
guess_system_package_manager(){
    if [ "`which dnf`" != "" ]; then
        SYSTEM_PACKAGE_MANAGER="dnf"
        SYSTEM_PACKAGE_TYPE="rpm"
        SYSTEM_PACKAGE_MANAGER_INSTALL="dnf -y install"
        SYSTEM_PACKAGE_MANAGER_UPDATE="dnf --refresh check-update"
    elif [ "`which apt-get`" != "" ]; then
        SYSTEM_PACKAGE_MANAGER="apt-get"
        SYSTEM_PACKAGE_TYPE="deb"
        SYSTEM_PACKAGE_MANAGER_INSTALL="apt-get -y install"
        SYSTEM_PACKAGE_MANAGER_UPDATE="apt-get update"
    elif [ "`which zypper`" != "" ]; then
        SYSTEM_PACKAGE_MANAGER="zypper"
        SYSTEM_PACKAGE_TYPE="rpm"
        SYSTEM_PACKAGE_MANAGER_INSTALL="zypper --non-interactive install"
        SYSTEM_PACKAGE_MANAGER_UPDATE="zypper refresh"
    elif [ "`which yum`" != "" ]; then
        SYSTEM_PACKAGE_MANAGER="yum"
        SYSTEM_PACKAGE_TYPE="rpm"
        SYSTEM_PACKAGE_MANAGER_INSTALL="yum -y install"
        SYSTEM_PACKAGE_MANAGER_UPDATE="yum check-update"
    elif [ "`which pacman`" != "" ]; then
        SYSTEM_PACKAGE_MANAGER="pacman"
        SYSTEM_PACKAGE_TYPE="archpkg"
        SYSTEM_PACKAGE_MANAGER_INSTALL="pacman --noconfirm -S"
        SYSTEM_PACKAGE_MANAGER_UPDATE="pacman -Syu"
    elif [ "`which emerge`" != "" ]; then
        SYSTEM_PACKAGE_MANAGER="emerge"
        SYSTEM_PACKAGE_TYPE="ebuild"
        SYSTEM_PACKAGE_MANAGER_INSTALL="emerge"
        SYSTEM_PACKAGE_MANAGER_UPDATE="emerge --sync"
        PIP_INSTALL_CMD="pip install --user"
    fi

    if [ $SYSTEM_PACKAGE_TYPE == "rpm" ]; then
        SYSTEM_PACKAGE_SET="gvim git wget pcre-devel python-pip python-devel clang-devel clang-libs"
    elif [ $SYSTEM_PACKAGE_TYPE == "deb" ]; then
        SYSTEM_PACKAGE_SET="vim-gnome git wget libpcre3 libpcre3-dev python-pip python-dev libclang-dev"
    elif [ $SYSTEM_PACKAGE_TYPE == "archpkg" || $SYSTEM_PACKAGE_TYPE == "ebuild" ]; then
        SYSTEM_PACKAGE_SET="gvim git wget pcre python-pip python clang"
    fi

    PIP_PACKAGE_SET="clang"
}

print_usage(){
    echo -e "Usage: './install.sh <directory>'"
    echo -e "Args:  <directory>"
    echo -e "           Optional argument defining installation directory. Default one is '"$YAVIDE_INSTALL_DIR_DEFAULT"'"
}

#####################################################################################################
# Plugins
#####################################################################################################

# Nerdtree
PLUGINS="$PLUGINS https://github.com/scrooloose/nerdtree"

# Clang_complete
PLUGINS="$PLUGINS https://github.com/Rip-Rip/clang_complete"

# SuperTab
PLUGINS="$PLUGINS https://github.com/ervandew/supertab"

# Tagbar
PLUGINS="$PLUGINS https://github.com/majutsushi/tagbar"

# Airline
PLUGINS="$PLUGINS https://github.com/bling/vim-airline"
PLUGINS="$PLUGINS https://github.com/vim-airline/vim-airline-themes"

# A
PLUGINS="$PLUGINS https://github.com/vim-scripts/a.vim"

# Auto-close
PLUGINS="$PLUGINS https://github.com/Townk/vim-autoclose"

# Multiple-cursors
PLUGINS="$PLUGINS https://github.com/terryma/vim-multiple-cursors.git"

# NERDCommenter
PLUGINS="$PLUGINS https://github.com/scrooloose/nerdcommenter"

# UltiSnips
PLUGINS="$PLUGINS https://github.com/SirVer/ultisnips"

# Git
PLUGINS="$PLUGINS https://github.com/tpope/vim-fugitive.git"
PLUGINS="$PLUGINS https://github.com/airblade/vim-gitgutter.git"

# Pathogen
PLUGINS="$PLUGINS https://github.com/tpope/vim-pathogen"

# Color schemes
SCHEMES="$SCHEMES https://github.com/JBakamovic/yaflandia.git"
SCHEMES="$SCHEMES https://github.com/jeffreyiacono/vim-colors-wombat"
SCHEMES="$SCHEMES https://github.com/morhetz/gruvbox.git"

#####################################################################################################
# Setup the installation directory
#####################################################################################################
YAVIDE_INSTALL_DIR=$YAVIDE_INSTALL_DIR_DEFAULT
if [ $# -eq 0 ]; then
    YAVIDE_INSTALL_DIR=$YAVIDE_INSTALL_DIR"/yavide"
    echo "Using default installation directory: '"$YAVIDE_INSTALL_DIR"'"
elif [ $# -eq 1 ]; then
    YAVIDE_INSTALL_DIR=${1%/}
    if [ ! -d $YAVIDE_INSTALL_DIR ]; then
        echo "Directory '"$YAVIDE_INSTALL_DIR"' does not exist."
        print_usage
        echo "Exiting ..."
        exit
    fi
    YAVIDE_INSTALL_DIR=$YAVIDE_INSTALL_DIR"/yavide"
    echo "Using user-defined installation directory: '"$YAVIDE_INSTALL_DIR"'"
else
    echo "Invalid number of arguments!"
    print_usage
    echo "Exiting ..."
    exit
fi

#####################################################################################################
# Identify the system package manager
#####################################################################################################
guess_system_package_manager
if [ -z $SYSTEM_PACKAGE_MANAGER ]; then
    echo "Identifying the system package manager failed. Currently supported ones are:
    'dnf', 'apt-get', 'zypper', 'yum', 'pacman', 'emerge'

Should you want to add support for new one, it should be easy enough to modify the
'guess_system_package_manager()' function which can be found in 'install.sh' script.

Alternatively, issue a support request on project homepage."
fi
echo "System package manager: '"$SYSTEM_PACKAGE_MANAGER"'"
echo "System package type: '"$SYSTEM_PACKAGE_TYPE"'"

#####################################################################################################
# Root password needed for some operations
#####################################################################################################
CURRENT_USER=`whoami`
echo -n "Enter the password for $CURRENT_USER: "
stty_orig=`stty -g` # save original terminal setting.
stty -echo          # turn-off echoing.
read passwd         # read the password
stty $stty_orig     # restore terminal setting.

#####################################################################################################
# Install dependencies
#####################################################################################################
echo "$passwd" | sudo -S $SYSTEM_PACKAGE_MANAGER_UPDATE
echo "$passwd" | sudo -S $SYSTEM_PACKAGE_MANAGER_INSTALL $SYSTEM_PACKAGE_SET
echo "$passwd" | sudo -S $PIP_INSTALL_CMD $PIP_PACKAGE_SET

mkdir -p $HOME/.fonts && git clone https://github.com/Lokaltog/powerline-fonts.git $HOME/.fonts
fc-cache -vf $HOME/.fonts

#####################################################################################################
# Start the installation
#####################################################################################################

# Yavide launcher file needs to be modified to reflect the destination directory selected in install process
sed -i '/^Exec=/ s\$\ -u '"$YAVIDE_INSTALL_DIR"'/.vimrc\' res/yavide.desktop

# Try to setup the 'libclang' path automatically by searching for it in '/usr/lib*' system paths.
# In case multiple paths were found, the last one will be selected. Reasoning lays behind the fact
# that paths will be sorted alphabetically and selecting the last entry will make the script pick
# up the most recent version of the library. However, user is free to change the selection afterwards
# in configuration files. This is only to get the things going.
echo "Searching for 'libclang' paths ..."
declare -a libclang_paths
paths=`find /usr -path "/usr/lib*/libclang.so"`
libclang_paths=( ${paths} )
echo "Found" ${#libclang_paths[@]} "'libclang' paths in total."
if [ ${#libclang_paths[@]} != 0 ]; then
	for (( i = 0; i < ${#libclang_paths[@]}; i++ ));
	do
		echo ${libclang_paths[$i]}
	done
	libclang_selected=${libclang_paths[${#libclang_paths[@]}-1]}
	echo "Selected 'libclang' is '"$libclang_selected"'"
	sed -i '/let g:libclang_location/c\let g:libclang_location = "'${libclang_selected}'"' config/.user_settings.vimrc
fi

# Build the destination directory and copy all of the relevant files
echo "$passwd" | sudo -S mkdir -p $YAVIDE_INSTALL_DIR
echo "$passwd" | sudo -S cp -R . $YAVIDE_INSTALL_DIR

# Make Yavide accessible via desktop shortcut
desktop=`echo $(xdg-user-dir DESKTOP)`
cp res/yavide.desktop $desktop

# Make Yavide accessible via 'Applications' menu and via application launcher
echo "$passwd" | sudo -S cp res/yavide.desktop /usr/share/applications

# Make Yavide accessible in terminal
yavide_alias=`grep -w "Exec" res/yavide.desktop | sed s/Exec=//`
echo "# Yavide alias" >> $HOME/.bashrc
echo "alias yavide=\""$yavide_alias"\"" >> $HOME/.bashrc

echo -e "\n"
echo "----------------------------------------------------------------------------"
echo "Installing plugins ..."
echo "----------------------------------------------------------------------------"
echo "$passwd" | sudo -S mkdir -p $YAVIDE_INSTALL_DIR/core/external && cd $YAVIDE_INSTALL_DIR/core/external

# Fetch/update the plugins
for URL in $PLUGINS; do
    # remove path from url
    DIR=${URL##*/}
    # remove extension from dir
    DIR=${DIR%.*}
    if [ -d $DIR  ]; then
        echo "Updating plugin $DIR..."
        cd $DIR
        echo "$passwd" | sudo -S git pull
        cd ..
    else
        echo "$passwd" | sudo -S git clone $URL $DIR
    fi
done

echo -e "\n"
echo "----------------------------------------------------------------------------"
echo "Installing clang_complete ..."
echo "----------------------------------------------------------------------------"
cd $YAVIDE_INSTALL_DIR/core/external/clang_complete
make install

echo -e "\n"
echo "----------------------------------------------------------------------------"
echo "Installing cppcheck ..."
echo "----------------------------------------------------------------------------"
cd $YAVIDE_INSTALL_DIR/core/external/
echo "$passwd" | sudo -S mkdir cppcheck && cd cppcheck
echo "$passwd" | sudo -S mkdir download && cd download
echo "$passwd" | sudo -S wget http://sourceforge.net/projects/cppcheck/files/cppcheck/1.67/cppcheck-1.67.tar.bz2/download -O cppcheck.tar.bz2
echo "$passwd" | sudo -S tar xf cppcheck.tar.bz2 && cd cppcheck-1.67
echo "$passwd" | sudo -S make install SRCDIR=build CFGDIR=$YAVIDE_INSTALL_DIR/core/external/cppcheck/cfg HAVE_RULES=yes
cd ../../
echo "$passwd" | sudo -S rm -r download

echo -e "\n"
echo "----------------------------------------------------------------------------"
echo "Installing color schemes ..."
echo "----------------------------------------------------------------------------"
echo "$passwd" | sudo -S mkdir -p $YAVIDE_INSTALL_DIR/colors && cd $YAVIDE_INSTALL_DIR/colors

# Fetch/update the color schemes
for URL in $SCHEMES; do
    # remove path from url
    DIR=${URL##*/}
    # remove extension from dir
    DIR=${DIR%.*}
    if [ -d $DIR  ]; then
        echo "Updating scheme $DIR..."
        cd $DIR
        echo "$passwd" | sudo -S git pull
        cd ..
    else
        echo "$passwd" | sudo -S git clone $URL $DIR
	fi
done

# Make symlinks to scheme files
echo "$passwd" | sudo -S ln -s `find . -wholename '*/colors/*.vim'` .

echo -e "\n"
echo "----------------------------------------------------------------------------"
echo "Setting permissions ..."
echo "----------------------------------------------------------------------------"
echo "$passwd" | sudo -S chown $USER $HOME/Desktop/yavide.desktop
echo "$passwd" | sudo -S chown -R $USER $YAVIDE_INSTALL_DIR

