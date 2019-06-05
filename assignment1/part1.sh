#!/bin/sh

#Downloading requirements
if false; then
   wget "https://github.com/torvalds/linux/releases/tag/v5.1"
   wget "ftp://ftp.denx.de/pub/u-boot/u-boot-2016.11.tar.bz2"
   wget "https://busybox.net/downloads/busybox-1.30.0.tar.bz2"
   #The linaro toolchain can be installed via apt, no need for download.
fi

#Compiling uboot
if false; then
   tar xf u-boot-2016.11.tar.bz2
   cd u-boot-2016.11
   make ./vexpress-ca9x4-defconfig
   sudo apt-get install 'g++-arm-linux-gnueabihf'
   make all CROSS_COMPILE=arm-linux-gnueabihf-
   sudo apt install qemu-system-arm
   qemu-system-arm -machine vexpress-a9 -nographic -no-reboot -kernel u-boot
   #Looks like uboot is compiled and qemu can run it at this point.
fi

#Compiling linux
if false; then
   sudo apt install libncurses-dev flex bison libssl-dev
   make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- menuconfig #This step is interactive, configure whatever
   make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- all
   #At this point compilation ran for ~2 hours and then failed
fi

