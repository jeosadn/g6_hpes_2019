#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h> /* for pid_t */
#include <sys/wait.h> /* for wait */

int menu(int argc, char **argv, char **PATH, int *exit){
   int authors = 0;
   int help = 0;
   *PATH = NULL;
   *exit = 1;

   int opt;

   while ((opt = getopt(argc, argv, "p:ha")) != -1) {

      switch (opt) {
         case 'h':
            help = 1;
            break;
         case 'a':
            authors = 1;
            break;
         case 'p':
            *PATH = optarg;
            break;
         case '?':
            printf("unknown option: %c\n", optopt);
            break;
      }
   }

   printf("\n");
   printf("  __  __                 ____ _               _\n");
   printf(" |  \\/  | ___ _ __ ___  / ___| |__   ___  ___| | __\n");
   printf(" | |\\/| |/ _ \\ '_ ` _ \\| |   | '_ \\ / _ \\/ __| |/ /\n");
   printf(" | |  | |  __/ | | | | | |___| | | |  __/ (__|   <\n");
   printf(" |_|  |_|\\___|_| |_| |_|\\____|_| |_|\\___|\\___|_|\\_\\\n");
   printf("\n");

   if (authors) {
      printf("Authors: Boris Altamirano - Daniel Jimenez - Jose Andres Pacheco\n\n");
   }

   if (help) {
      printf("Memchecker help.\n");
      printf("Options: \n\t -a \t\t Displays authors names. \n\t -h \t\t Displays this menu. \n");
      printf("\t -p 'program' \t Path to program to analyze. \n\n");
   }

   if (*PATH != NULL) {
      printf("Using program: %s.\n", *PATH);
      *exit = 0;
   }

   if (*PATH == NULL && !(authors || help)) {
      printf("Error: no program specified. Use -h for help\n\n");
      return 1;
   } else {
      return 0;
   }
}

int main (int argc, char **argv)
{
   char *PATH;
   int exit;

   if (menu(argc, argv, &PATH, &exit)) {
      return 1;
   }

   if (exit) {
      return 0;
   }

   printf("Analyzing program: %s.\n", PATH);

   pid_t pid=fork();
   if (pid==0) {
     putenv("LD_PRELOAD=/usr/local/lib/libmemcheck.so");
     execl(PATH,PATH,NULL);
   }

   return 0;
}
