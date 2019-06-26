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
   git clone -b thud https://git.yoctoproject.org/poky.git
   cd poky

   #Grab dependency meta layers
   git clone -b thud https://git.openembedded.org/meta-openembedded
   git clone -b thud https://github.com/meta-qt5/meta-qt5
   git clone -b thud https://git.yoctoproject.org/git/meta-raspberrypi

   #Clone tutorial meta layer
   git clone -b thud https://github.com/jumpnow/meta-rpi

   #Create meta-tec meta layer
   source oe-init-build-env ~/meta-tec

   #Copy config files #Careful with the paths! source above changed local dir
   cp meta-rpi/conf/local.conf.sample ~/meta-tec/conf/local.conf
      #Update MACHINE to raspberrypi2
      #Update EXTRA_USERS_PARAMS to use tec password
      #other defaults were left as-is

   cp meta-rpi/conf/bblayers.conf.sample ~/meta-tec/conf/bblayers.conf
      #Update paths to your actual meta layers

   #Add recipes
   devtool add rg2yuv-c https://github.com/jeosadn/rgb2yuv-c.git
   devtool add rg2yuv-intrinsics https://github.com/jeosadn/rgb2yuv-intrinsics.git

   #Edit ~/meta-tec/workspace/recipes/rg2yuvc-*/rgb2yuv-*_git.bb
      #Change PV for 1.0
      #Change SRCREV for master

   #Edit ~/meta-tec/workspace/conf/layer.conf (note space in front of package name)
      #Add IMAGE_INSTALL_append = " rgb2yuv-c"
      #Add IMAGE_INSTALL_append = " rgb2yuv-intrinsics"

   #Before building, check the source paths in ~/meta-tec/workspace/appends/*.bbappend - These may have to be updated

   #When developing recipes, source code will be stored in ~/meta-tec/workspace/sources/* .
   #bitbake may not check for new commit from github, so be sure to update files here.
   #Finally, a sample image for dev is available at ~/meta-tec/samples/zelda_rgb24_w640_h480_rgba.rgb

   #Now you can build (This will take multiple hours and use >50GB of disc space
   bitbake console-image

   #This took ~9 hours and produced a 17GB folder with images.
   #Image is in tmp/work/raspberrypi2-poky-linux-gnueabi/console-image/1.0-r0/temp/

   #Now to copy the generated images to the sd card

   #cd to the meta-rpi helper scripts
   cd /home/jo/rendimiento/g6_hpes_2019/assignment1/poky/meta-rpi/scripts

   #Plug SD card, figure out device with command lsblk

   #Partition SD card
   sudo ./mk2parts.sh sdb

   #mount it
   sudo mkdir /media/card

   #Copy boot and root partitons
   export OETMP=/home/jo/meta-tec/tmp
   export MACHINE=raspberrypi2
   ./copy_boot.sh sdb
   ./copy_rootfs.sh sdb console
fi

#Boot raspberrypi, obtain test data
if false; then
   #Plug in power, keyboard, monitor, wifi, camera
   #Login with user root, pwd tec. Will ask to change password, used 12345

   #Configure camera
   mkdir /mnt/fat
   mount /dev/mmcblk0p1 /mnt/fat
   vi /mnt/fat/config.txt
      #start_x=1
      #gpu_mem=128
      #disable_camera_led=1   # optional for disabling the red LED on the camera
   reboot

   raspiyuv -w 640 -h 480 -bgr -o test_image
   #This command fails due to camera hardware. An image was downloaded from the internet
   #and converted to rgb using https://www.freefileconvert.com/png-rgb
fi

