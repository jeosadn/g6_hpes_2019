#                                               -*- Autoconf -*-
# Process this file with autoconf to produce a configure script.

AC_PREREQ([2.69])
AC_INIT([memcheck], [1.0], [g6@tec.com])
AC_CONFIG_SRCDIR([src/memcheck.c])
AC_CONFIG_AUX_DIR([build-aux])
AM_INIT_AUTOMAKE

LT_INIT

# Checks for programs.
AC_PROG_CC

# Checks for libraries.

# Checks for header files.
AC_CHECK_HEADERS([stdlib.h string.h sys/time.h unistd.h])

# Checks for typedefs, structures, and compiler characteristics.

# Checks for library functions.
AC_CHECK_FUNCS([gettimeofday])

AC_OUTPUT(Makefile lib/Makefile src/Makefile)
