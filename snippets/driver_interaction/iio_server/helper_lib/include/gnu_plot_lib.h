#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>


void plot_init(int xmin, int xmax, int ymin, int ymax, const char* name, FILE **pipe);
void plot(FILE *pipe, float *data_, size_t size_);
void plot_close(FILE *pipe);