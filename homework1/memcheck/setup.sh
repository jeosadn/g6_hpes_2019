#!/bin/sh

autoreconf -i
aclocal
automake --add-missing
autoconf
./configure
make
make install
