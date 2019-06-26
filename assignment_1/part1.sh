#!/bin/sh

#Downloading requirements
if false; then
   wget "https://github.com/torvalds/linux/archive/v5.1.tar.gz"
   wget "ftp://ftp.denx.de/pub/u-boot/u-boot-2016.11.tar.bz2"
   wget "https://busybox.net/downloads/busybox-1.30.0.tar.bz2"
   #The linaro toolchain can be installed via apt, no need for download.
fi

#All dependencies install
if false; then
   sudo apt-get install 'g++-arm-linux-gnueabihf' qemu-system-arm libncurses-dev flex bison libssl-dev device-tree-compiler
fi

#Compiling uboot
if false; then
   tar xf u-boot-2016.11.tar.bz2
   cd u-boot-2016.11
   make vexpress-ca9x4-defconfig
   make all CROSS_COMPILE=arm-linux-gnueabihf-
   cp u-boot ../.
   cd ..
   qemu-system-arm -machine vexpress-a9 -nographic -no-reboot -kernel u-boot
   #Looks like uboot is compiled and qemu can run it at this point.
fi

#Compiling linux
if false; then
   tar xf v5.1.tar.gz
   cd linux-5.1
   make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- defconfig #This step is interactive, configure whatever
   make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- all #Compilation takes ~2hours, fails in stage2 but zImage is done
   cp arch/arm/boot/zImage ../.

   #Due to the error, hand-compile the dtb file
   sed -i 's/#include/\/include\//' ./arch/arm/boot/dts/vexpress-v2p-ca9.dts
   dtc -O dtb -o ../vexpress-v2p-ca9.dtb ./arch/arm/boot/dts/vexpress-v2p-ca9.dts
   cd ../

   #This QEMU command stalls
   qemu-system-arm -machine vexpress-a9 -nographic -no-reboot -kernel zImage -dtb vexpress-v2p-ca9.dtb -cpu cortex-a9 -m 512M
   qemu-system-arm -machine vexpress-a9 -nographic            -kernel zImage -dtb vexpress-v2p-ca9.dtb -cpu cortex-a9 -m 512M
fi

#Compiling busybox
if false; then
   cd bussybox-1.30.0/
   make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- defconfig #default config
   make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- menuconfig #Settings -> Build -> enable static linking
   make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- install
fi

