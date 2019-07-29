#!/bin/sh

rm -rf aclocal.m4 autom4te.cache build-aux/ libtool \
      config.log config.status configure log.txt \
      lib/Makefile lib/Makefile.in Makefile \
      Makefile.in src/Makefile src/Makefile.in \
      lib/libmemcheck.la src/memcheck src/memcheck.o \
      lib/libmemcheck_la-libmemcheck.lo lib/libmemcheck_la-libmemcheck.o
