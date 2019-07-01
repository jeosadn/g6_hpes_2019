# Yocto and Raspberry Pi

The following repositories were developed for the deliverables:

## meta-tec layer
This contains the rgb2yuv-c, rgb2yuv-intrinsics recipes and meta-tec image.

Just calling `bitbake tec-image` in your workspace after adding this layer is
enough to build the Raspberry Pi image with our recipes and camera usage enabled.

The rgb2yuv-\* recipes deploy to the following locations:
* `/usr/bin/rgb2yuv-*` for the binaries, and
* `/usr/share/rgb2yuv-*/` for the documentation.

`git@github.com:jeosadn/meta-tec.git`

https://github.com/jeosadn/meta-tec

## rgb2yuv-c package
This package builds and deploys rgb2yuv-c using autotools, to
`/usr/local/bin/rgb2yuv-c` and `/usr/local/share/doc/rgb2yuv-c/`

`git@github.com:jeosadn/rgb2yuv-c.git`

https://github.com/jeosadn/rgb2yuv-c

## rgb2yuv-intrinsics package
This package builds and deploys rgb2yuv-intrinsics using autotools, to
`/usr/local/bin/rgb2yuv-intrinsics` and `/usr/local/share/doc/rgb2yuv-intrinsics/`

As this requires NEON, it is not possible to build it for a local machine.

`git@github.com:jeosadn/rgb2yuv-intrinsics.git`

https://github.com/jeosadn/rgb2yuv-intrinsics


## meta-local workspace
This contains the workspace that imports the layers and builds the images
(You probably have a local version of this and don't need it. If you do, take
care to update the hardcoded paths)

`git@github.com:jeosadn/meta-local.git`

https://github.com/jeosadn/meta-local
