# Yocto and Raspberry Pi

The following repositories were developed for the deliverables:

## meta-tec layer
This contains the rgb2yuv-c, rgb2yuv-intrinsics recipes and meta-tec image.

Just calling `bitbake tec-image` in your workspace after adding this layer is
enough to build the Raspberry Pi image with our recipes and camera usage enabled.

git@github.com:jeosadn/meta-tec.git

## rgb2yuv-c package
This package builds and deploys rgb2yuv-c using autotools.

git@github.com:jeosadn/rgb2yuv-c.git

## rgb2yuv-intrinsics package
This package builds and deploys rgb2yuv-intrinsics using autotools.

As this requires NEON, it is not possible to build it for a local machine.

git@github.com:jeosadn/rgb2yuv-c.git


## meta-local workspace
This contains the workspace that imports the layers and builds the images
(You probably have a local version of this and don't need it. If you do, take
care to update the hardcoded paths)
