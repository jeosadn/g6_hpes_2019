/*

This program will numerically compute the integral of

                  4/(1+x*x)

from 0 to 1.

History: Written by Tim Mattson, 11/99.

*/
#include <omp.h>
#include <stdio.h>
static long num_steps = 100000000;
double step;
int main() {
   int i;
   double x, pi, sum = 0.0;
   double start_time, run_time;

   step = 1.0 / (double)num_steps;

   start_time = omp_get_wtime();

   // Con el pragma teams se crea un conjunto de equipos, donde cada equipo
   // tiene un hilo maestro. num_teams define la cantidad de equipos a crear.
   #pragma omp target teams num_teams(3) map(sum,x)

   // Con el pragma distribute se distrubuyen las iteraciones del ciclo for
   // dentro de cada equipo. El pragma parallel for permite paralelizar la
   // ejecucion dentro de cada equipo.
   #pragma omp distribute parallel for reduction(+:sum)
   for (i = 1; i <= num_steps; i++) {
      x = (i - 0.5) * step;
      sum = sum + 4.0 / (1.0 + x * x);
   }

   pi = step * sum;
   run_time = omp_get_wtime() - start_time;
   printf("pi with %ld steps is %lf in %lf seconds\n", num_steps, pi, run_time);
}
