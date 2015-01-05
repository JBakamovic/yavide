#!/bin/bash
# yavide installation script

#####################################################################################################
# Settings
#####################################################################################################
print_error_and_exit(){
	echo "Please provide the system name you're running."
	echo "Currently supported ones are:"
	echo -e "\t'ubuntu'"
	echo -e "\t'debian'"
	echo -e "\t'opensuse'"
	echo -e "\t'centos'"
	exit
}

YAVIDE_IDE_ROOT="/opt/yavide"
if [ ! -z $1 ]; then
	if [ $1 == "ubuntu" ] || [ $1 == "debian" ]; then
		PACKAGE_MANAGER="apt-get"
		PACKAGE_MANAGER_INSTALL="apt-get install"
		PACKAGE_MANAGER_UPDATE="apt-get update"
	elif [ $1 == "opensuse" ]; then
		PACKAGE_MANAGER="zypper"
		PACKAGE_MANAGER_INSTALL="zypper install"
		PACKAGE_MANAGER_UPDATE="zypper update"
	elif [ $1 == "centos" ]; then
		PACKAGE_MANAGER="yum"
		PACKAGE_MANAGER_INSTALL="yum install"
		PACKAGE_MANAGER_UPDATE="yum update"
	else
		print_error_and_exit
	fi
else
	print_error_and_exit
fi

#####################################################################################################
# Plugins
#####################################################################################################

# Nerdtree
PLUGINS="$PLUGINS https://github.com/scrooloose/nerdtree"

# Session
PLUGINS="$PLUGINS https://github.com/xolox/vim-session"
PLUGINS="$PLUGINS https://github.com/xolox/vim-misc.git"

# Clang_complete
PLUGINS="$PLUGINS https://github.com/Rip-Rip/clang_complete"

# Cscope
CSCOPE_PLUGIN="http://cscope.sourceforge.net/cscope_maps.vim"
CSCOPE_AUTOLOAD_PLUGIN="http://vim.sourceforge.net/scripts/download_script.php?src_id=14884"

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
# Root password needed for some operations
#####################################################################################################
CURRENT_USER=`whoami`
echo -n "Enter the password for $CURRENT_USER: "
stty_orig=`stty -g` # save original terminal setting.
stty -echo          # turn-off echoing.
read passwd         # read the password
stty $stty_orig     # restore terminal setting.

#####################################################################################################
# Check and install the prerequisites
#####################################################################################################

# Install required packages
echo "$passwd" | sudo -S $PACKAGE_MANAGER_UPDATE
echo "$passwd" | sudo -S $PACKAGE_MANAGER_INSTALL ctags cscope git wget libpcre3 libpcre3-dev
[ -d $/home/$USER/.fonts ] | echo "$passwd" | sudo -S mkdir /home/$USER/.fonts
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
echo "$passwd" | sudo -S cp .vimrc $YAVIDE_IDE_ROOT
echo "$passwd" | sudo -S cp -R sessions $YAVIDE_IDE_ROOT/sessions

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
echo "Installing cscope ..."
echo "----------------------------------------------------------------------------"
cd $YAVIDE_IDE_ROOT/bundle/
echo "$passwd" | sudo -S mkdir cscope && cd cscope
echo "$passwd" | sudo -S mkdir plugin && cd plugin
echo "$passwd" | sudo -S wget $CSCOPE_PLUGIN
echo "$passwd" | sudo -S wget $CSCOPE_AUTOLOAD_PLUGIN -O autoload_cscope.vim

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

