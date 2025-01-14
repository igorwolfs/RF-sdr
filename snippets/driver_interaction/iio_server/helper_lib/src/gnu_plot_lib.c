#include "gnu_plot_lib.h"


// *******************************************************
// ****************** MULTI PLOT *************************
// *******************************************************

/**
 * Initializes the gnuplot pipe and window with the given settings.
 * This opens a single window and prepares it for multiple plots.
 */
void multiplot_init(int xmin, int xmax, int ymin, int ymax, const char* name, FILE **pipe)
{
    // Check if the pipe is already initialized
    if (*pipe != NULL)
    {
        printf("ERROR: GNUPLOT INITIALIZED\n");
        return;
    }

    // Open the gnuplot pipe
    *pipe = popen("gnuplot -persistent", "w");

    // Initialize the multiplot mode and set the layout
    fprintf(*pipe, "set multiplot layout 1,2 title 'Multiple Graphs'\n");

    // Basic settings for gnuplot
    fprintf(*pipe, "set title '%s'\n", name);
    fprintf(*pipe, "set xrange [%d:%d]\n", xmin, xmax);
    fprintf(*pipe, "set yrange [%d:%d]\n", ymin, ymax);
    fflush(*pipe);
}



/**
 * Plots data into the given gnuplot pipe.
 * Each plot is placed in one of the panels of the multiplot window.
 */
void multiplot(FILE *pipe, float *data_1, size_t size_1, float *data_2, size_t size_2)
{
    // Plot 1: First panel in the multiplot layout
    fprintf(pipe, "set title 'Graph 1'\n"); // Set title for the first plot
    fprintf(pipe, "plot '-' with lines\n");  // Plot data 1
    for (size_t i = 0; i < size_1; ++i)
    {
        fprintf(pipe, "%zu %f\n", i, data_1[i]);
    }
    fprintf(pipe, "e\n");
    fflush(pipe); // Ensure data is sent to gnuplot

    // Plot 2: Second panel in the multiplot layout
    fprintf(pipe, "set title 'Graph 2'\n"); // Set title for the second plot
    fprintf(pipe, "plot '-' with lines\n");  // Plot data 2
    for (size_t i = 0; i < size_2; ++i)
    {
        fprintf(pipe, "%zu %f\n", i, data_2[i]);
    }
    fprintf(pipe, "e\n");
    fflush(pipe); // Ensure data is sent to gnuplot
}

/**
 * Closes the gnuplot pipe and resets multiplot mode.
 */
void multiplot_close(FILE *pipe)
{
    // Finish multiplot mode and close the pipe
    fprintf(pipe, "unset multiplot\n");
    pclose(pipe);
}


// *******************************************************
// ***************** SINGLE PLOT *************************
// *******************************************************
/**
 * Initializes the gnuplot pipe and window with the given settings.
 * Each plot has its own separate window and settings.
 */
void plot_init(int xmin, int xmax, int ymin, int ymax, const char* name, FILE **pipe)
{
    // Check if the pipe is already initialized
    if (*pipe != NULL)
    {
        printf("ERROR: GNUPLOT INITIALIZED\n");
        return;
    }
    
    *pipe = popen("gnuplot -persistent", "w");
    
    // Basic settings for gnuplot
    fprintf(*pipe, "set title '%s'\n", name);
    fprintf(*pipe, "set xrange [%d:%d]\n", xmin, xmax);
    fprintf(*pipe, "set yrange [%d:%d]\n", ymin, ymax);
    fflush(*pipe);
}

/**
 * Plots data into the given gnuplot pipe.
 * Each pipe controls a separate gnuplot window.
 */
void plot(FILE *pipe, float *data_, size_t size_)
{
    // Issue plot command to gnuplot
    fprintf(pipe, "plot '-' with lines\n");
    for(size_t i = 0; i < size_; ++i)
    {
        fprintf(pipe, "%zu %f\n", i, data_[i]);
    }
    fprintf(pipe, "e\n");
    fflush(pipe); // Ensure data is sent to gnuplot
}

/**
 * Closes the gnuplot pipe.
 */
void plot_close(FILE *pipe)
{
    pclose(pipe);
}
