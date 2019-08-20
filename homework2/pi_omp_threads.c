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

   for (int j=0; j<4; j++){
      int i;
      double x, pi, sum = 0.0;
      double start_time, run_time;

      step = 1.0 / (double)num_steps;

      start_time = omp_get_wtime();

      // Con la funcion omp_set_num_threads se establece la cantidad de
      // hilos que se van a generar.
      omp_set_num_threads(j+1);

      // El pragma parallel indica que la siguiente porcion de codigo se
      // va a ejecutar en paralelo.
      #pragma omp parallel
      {
         // El pragma single indica que la siguiente instruccion se va
         // a ejecutar en un solo hilo.
         #pragma omp single
         printf(" num_threads = %d\n", omp_get_num_threads());

         // El pragma for reduction establece como se va a distribuir
         // el ciclo for en los diferentes hilos.
         #pragma omp for reduction(+ : sum)
         for (i = 1; i <= num_steps; i++) {
            x = (i - 0.5) * step;
            sum = sum + 4.0 / (1.0 + x * x);
         }
      }

      pi = step * sum;
      run_time = omp_get_wtime() - start_time;
      printf("pi with %ld steps is %lf in %lf seconds\n", num_steps, pi,
      run_time);
   }
}
