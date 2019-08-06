#define _GNU_SOURCE

#include <dlfcn.h>
#include <stdio.h>

void __attribute__ ((destructor)) finMemCheck(void);

static void *(*real_malloc)(size_t);
static void *(*real_free)(void *);
static int allocCnt = 0;
static int freeCnt = 0;

void finMemCheck(void) {
  int diff = allocCnt - freeCnt;
  printf("\n\tAnalysis finished!\n\tMemory allocations: %d\n\tMemory free: %d\n\tTotal memory leaks found: %d\n\n",allocCnt, freeCnt, diff);
}

void *malloc(size_t size)
{
  allocCnt=allocCnt+1;
  void* p = NULL;
  real_malloc = dlsym(RTLD_NEXT, "malloc");
  p = real_malloc(size);
  return p;
}

void free(void* ptr) {
  freeCnt=freeCnt+1;
  real_free = dlsym(RTLD_NEXT, "free");
  real_free(ptr);
}
