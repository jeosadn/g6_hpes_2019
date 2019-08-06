#!/bin/sh

#Installation
if false; then
   sudo apt install valgrind
fi

#Execution
if true; then
   gcc -Wall -pedantic -g case1.c -o case1
   valgrind ./case1 2>&1 | tee Valgrind_case1.txt

   gcc -Wall -pedantic -g case2.c -o case2
   valgrind ./case2 2>&1 | tee Valgrind_case2.txt

   gcc -Wall -pedantic -g case3.c -o case3
   valgrind ./case3 2>&1 | tee Valgrind_case3.txt

   valgrind ./case4 2>&1 | tee Valgrind_case4.txt
fi

