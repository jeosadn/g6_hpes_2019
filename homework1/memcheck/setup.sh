#!/bin/sh

aclocal
automake --add-missing
autoconf
./configure
make
make install
