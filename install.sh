#!/bin/bash
# yavide installation script

#####################################################################################################
# Variables
#####################################################################################################
SYSTEM_PACKAGE_MANAGER=""
YAVIDE_IDE_ROOT="/opt/yavide"

#####################################################################################################
# Helper functions
#####################################################################################################
guess_system_package_manager(){
    if [ `which apt-get` != "" ]; then
        SYSTEM_PACKAGE_MANAGER="apt-get"
        SYSTEM_PACKAGE_MANAGER_INSTALL="apt-get install"
        SYSTEM_PACKAGE_MANAGER_UPDATE="apt-get update"
    elif [ `which zypper` != "" ]; then
        SYSTEM_PACKAGE_MANAGER="zypper"
        SYSTEM_PACKAGE_MANAGER_INSTALL="zypper install"
        SYSTEM_PACKAGE_MANAGER_UPDATE="zypper update"
    elif [ `which yum` != "" ]; then
        SYSTEM_PACKAGE_MANAGER="yum"
        SYSTEM_PACKAGE_MANAGER_INSTALL="yum install"
        SYSTEM_PACKAGE_MANAGER_UPDATE="yum update"
    elif [ `which pacman` != "" ]; then
        SYSTEM_PACKAGE_MANAGER="pacman"
        SYSTEM_PACKAGE_MANAGER_INSTALL="pacman -S"
        SYSTEM_PACKAGE_MANAGER_UPDATE="pacman -Syu"
    elif [ `which emerge` != "" ]; then
        SYSTEM_PACKAGE_MANAGER="emerge"
        SYSTEM_PACKAGE_MANAGER_INSTALL="emerge"
        SYSTEM_PACKAGE_MANAGER_UPDATE="emerge -uv world"
    fi
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
SCHEMES="$SCHEMES https://github.com/jeffreyiacono/vim-colors-wombat"
SCHEMES="$SCHEMES https://github.com/morhetz/gruvbox.git"

#####################################################################################################
# Identify the system package manager
#####################################################################################################
guess_system_package_manager
if [ -z $SYSTEM_PACKAGE_MANAGER ]; then
    echo "Identifying the system package manager failed. Currently supported ones are:
    'apt-get', 'zypper', 'yum', 'pacman', 'emerge'

Should you want to add support for new one, it should be easy enough to modify the
'guess_system_package_manager()' function which can be found in 'install.sh' script.

Alternatively, issue a support request on project homepage."
fi
echo "System package manager: '"$SYSTEM_PACKAGE_MANAGER"'"

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
echo "$passwd" | sudo -S $SYSTEM_PACKAGE_MANAGER_INSTALL ctags cscope git wget libpcre3 libpcre3-dev libyaml-dev python-pip
echo "$passwd" | sudo -S pip install watchdog
[ -d /home/$USER/.fonts ] | echo "$passwd" | sudo -S mkdir /home/$USER/.fonts
echo "$passwd" | sudo -S git clone https://github.com/Lokaltog/powerline-fonts.git /home/$USER/.fonts
fc-cache -vf /home/$USER/.fonts

#####################################################################################################
# Start the installation
#####################################################################################################

# Build the directory structure
[ -d $YAVIDE_IDE_ROOT ] || echo "$passwd" | sudo -S mkdir $YAVIDE_IDE_ROOT
[ -d $YAVIDE_IDE_ROOT/bundle ] || echo "$passwd" | sudo -S mkdir $YAVIDE_IDE_ROOT/bundle
[ -d $YAVIDE_IDE_ROOT/colors ] || echo "$passwd" | sudo -S mkdir $YAVIDE_IDE_ROOT/colors

# Copy the pre-configured stuff
echo "$passwd" | sudo -S cp yavide.desktop $YAVIDE_IDE_ROOT
echo "$passwd" | sudo -S cp yavide.desktop /home/$USER/Desktop
echo "$passwd" | sudo -S cp .*.vimrc .vimrc common.plugin *.py $YAVIDE_IDE_ROOT

# Try to setup the 'libclang' path automatically by searching for it in '/usr/lib*' system paths.
# In case multiple paths were found, the last one will be selected. Reasoning lays behind the fact
# that paths will be sorted alphabetically and selecting the last entry will make the script pick
# up the most recent version of the library. However, user is free to change the selection afterwards
# in configuration files. This is only to get the things going.
echo "Searching for 'libclang' paths ..."
declare -a libclang_paths
paths=`echo "$passwd" | sudo -S find /usr -type l -path "/usr/lib*/libclang.so"`
libclang_paths=( ${paths} )
echo "Found" ${#libclang_paths[@]} "'libclang' paths in total."
for (( i = 0; i < ${#libclang_paths[@]}; i++ ));
do
    echo ${libclang_paths[$i]}
done
libclang_selected=${libclang_paths[${#libclang_paths[@]}-1]}
echo "Selected 'libclang' is '"$libclang_selected"'"
echo "$passwd" | sudo -S sed -i '/let g:libclang_location/c\let g:libclang_location = "'${libclang_selected}'"' $YAVIDE_IDE_ROOT/.user_settings.vimrc

echo "\n"
echo "----------------------------------------------------------------------------"
echo "Installing plugins ..."
echo "----------------------------------------------------------------------------"
cd $YAVIDE_IDE_ROOT/bundle

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

echo "\n"
echo "----------------------------------------------------------------------------"
echo "Installing clang_complete ..."
echo "----------------------------------------------------------------------------"
cd $YAVIDE_IDE_ROOT/bundle/clang_complete
make install

echo "\n"
echo "----------------------------------------------------------------------------"
echo "Installing cppcheck ..."
echo "----------------------------------------------------------------------------"
cd $YAVIDE_IDE_ROOT/bundle/
echo "$passwd" | sudo -S mkdir cppcheck && cd cppcheck
echo "$passwd" | sudo -S mkdir download && cd download
echo "$passwd" | sudo -S wget http://sourceforge.net/projects/cppcheck/files/cppcheck/1.67/cppcheck-1.67.tar.bz2/download -O cppcheck.tar.bz2
echo "$passwd" | sudo -S tar xf cppcheck.tar.bz2 && cd cppcheck-1.67
echo "$passwd" | sudo -S make install SRCDIR=build CFGDIR=$YAVIDE_IDE_ROOT/bundle/cppcheck/cfg HAVE_RULES=yes
cd ../../
echo "$passwd" | sudo -S rm -r download

echo "----------------------------------------------------------------------------"
echo "Installing color schemes ..."
echo "----------------------------------------------------------------------------"
cd $YAVIDE_IDE_ROOT/colors

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

echo "----------------------------------------------------------------------------"
echo "Setting permissions ..."
echo "----------------------------------------------------------------------------"
echo "$passwd" | sudo -S chown $USER /home/$USER/Desktop/yavide.desktop
echo "$passwd" | sudo -S chown -R $USER $YAVIDE_IDE_ROOT

