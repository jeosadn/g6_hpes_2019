#!/bin/sh

#Dependencies
if false; then
   #Yocto dependencies
   sudo apt install gawk wget git-core diffstat unzip texinfo gcc-multilib build-essential chrpath socat libsdl1.2-dev xterm nano

   #Extra dependencies
   sudo apt install autoconf libtool rpm

   #Python 2.7 is needed
   conda create -n py2 python=2.7

   #Manually enter the following command before building stuff
   conda activate py2
fi

# Build yocto
if false; then
   #Clone the repo (thud version)
   git clone -b thud git://git.yoctoproject.org/poky.git
   cd poky

   #Grab dependency meta layers
   git clone -b thud git://git.openembedded.org/meta-openembedded
   git clone -b thud https://github.com/meta-qt5/meta-qt5
   git clone -b thud git://git.yoctoproject.org/meta-raspberrypi

   #Clone tutorial meta layer
   git clone -b thud git://github.com/jumpnow/meta-rpi

   #Create meta-tec meta layer
   source oe-init-build-env ~/meta-tec

   #Copy config files #Careful with the paths! source above changed local dir
   cp meta-rpi/conf/local.conf.sample ~/meta-tec/conf/local.conf
      #Update MACHINE to raspberrypi2
      #Update EXTRA_USERS_PARAMS to use tec password
      #other defaults were left as-is

   cp meta-rpi/conf/bblayers.conf.sample ~/meta-tec/conf/bblayers.conf
      #Update paths to your actual meta layers

   #Now you can build (This will take multiple hours and use >50GB of disc space
   bitbake console-image

   #This took ~9 hours and produced a 17GB folder with images.
fi
