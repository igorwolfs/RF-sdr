#include <stdlib.h>
#include <stdio.h>
#include<unistd.h>

#define NUM_POINTS 5
#define NUM_COMMANDS 4
FILE *pipe1_plot=NULL;
FILE *pipe2_plot=NULL;

void plot_init(FILE* gnuplot_pipe, int xmin, int xmax, int ymin, int ymax, const char* name)
{
    // open persistent gnuplot window
    if (gnuplot_pipe != NULL)
    {
        printf("ERROR GNUPLOT INITIALIZED");
        return;
    }
    gnuplot_pipe = popen ("gnuplot -persistent", "w");
    // basic settings
    fprintf(gnuplot_pipe, "set title '%s'\n", name);
    fprintf(gnuplot_pipe, "set xrange [%d:%d]\n", xmin, xmax);
    fprintf(gnuplot_pipe, "set yrange [%d:%d]\n", ymin, ymax);
    fflush(gnuplot_pipe);
}
void plot(FILE *gnuplot_pipe, float *data_, size_t size_){
    // Plot command
    fprintf(gnuplot_pipe, "plot '-' with lines\n");
    for(size_t i=0; i<size_; ++i){
    fprintf(gnuplot_pipe, "%zu %f\n", i, data_[i]);
    }
    fprintf(gnuplot_pipe, "e\n");
    // refresh can probably be omitted
    fprintf(gnuplot_pipe, "refresh\n");
    
    fflush(gnuplot_pipe);          // Force data to be sent
}

void plot_close(FILE *gnuplot_pipe)
{
    pclose(gnuplot_pipe);
}

int main()
{
    // char * commandsForGnuplot[] = {"set title \"Random plot\"", 
    //     "set xrange [0:6]", 
    //     "set yrange [0:6]", 
    //     "plot 'data.temp'"};

    plot_init(pipe1_plot, -1, 6, -1, 6, "FloatSignal");
    plot_init(pipe2_plot, -1, 6, -1, 6, "FloatSignal");

    float xvals_[NUM_POINTS] = {1.0, 2.0, 3.0, 4.0, 5.0};
    float yvals_[NUM_POINTS] = {5.0 ,3.0, 1.0, 3.0, 5.0};
    float yvals_temp_1[NUM_POINTS] = {0};
    float yvals_temp_2[NUM_POINTS] = {0};

    for (int i=0; i<10; i++)
    {
        sleep(1);
        for (int j=0; j<NUM_POINTS; j++)
        {
            yvals_temp_1[(j+i)%NUM_POINTS] = yvals_[j];
            yvals_temp_2[(j+i+2)%NUM_POINTS] = yvals_[j];
        }
        plot(pipe1_plot, yvals_temp_1, NUM_POINTS);
        plot(pipe2_plot, yvals_temp_2, NUM_POINTS);
    }
    plot_close(pipe1_plot);
    plot_close(pipe2_plot);
    /*
    // Opens an interface that one can use to send commands as if they were typing into the gnuplot command line.  
     
    FILE * temp = fopen("data.temp", "w");

    // "The -persistent" keeps the plot open even after your C program terminates.
    FILE * gnuplotPipe = popen ("gnuplot -persistent", "w");
    // fprintf(gnuplotPipe, "plot '-' \n");
    int i;
    for (i=0; i < NUM_POINTS; i++)
    {
        fprintf(temp, "%lf %lf \n", xvals[i], yvals[i]); //Write the data to a temporary file
        // fprintf(gnuplotPipe, "%lf %lf\n", xvals[i], yvals[i]);
    }
    // fprintf(gnuplotPipe, "e");

    for (i=0; i < NUM_COMMANDS; i++)
    {
        fprintf(gnuplotPipe, "%s \n", commandsForGnuplot[i]); //Send commands to gnuplot one by one.
    }
    */
    return 0;
}