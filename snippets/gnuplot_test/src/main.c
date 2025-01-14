#include "gnu_plot_lib.h"
#define NUM_POINTS 5

int main()
{

    FILE *pipe1_plot = NULL;
    FILE *pipe2_plot = NULL;

    // Initialize the pipes for two different gnuplot windows
    plot_init(-1, 6, -1, 6, "Graph 1", &pipe1_plot);
    plot_init(-1, 6, -1, 6, "Graph 2", &pipe2_plot);

    // Data to plot
    float xvals_[NUM_POINTS] = {1.0, 2.0, 3.0, 4.0, 5.0};
    float yvals_[NUM_POINTS] = {5.0 ,3.0, 1.0, 3.0, 5.0};
    float yvals_temp_1[NUM_POINTS] = {0};
    float yvals_temp_2[NUM_POINTS] = {0};

    // Main loop: update both plots
    for (int i = 0; i < 10; i++)
    {
        sleep(1);

        // Shift data for graph 1
        for (int j = 0; j < NUM_POINTS; j++)
        {
            yvals_temp_1[(j + i) % NUM_POINTS] = yvals_[j];
        }

        // Shift data for graph 2
        for (int j = 0; j < NUM_POINTS; j++)
        {
            yvals_temp_2[(j + i + 2) % NUM_POINTS] = yvals_[j];
        }

        // Plot data in both windows
        plot(pipe1_plot, yvals_temp_1, NUM_POINTS);
        plot(pipe2_plot, yvals_temp_2, NUM_POINTS);
    }

    // Close the gnuplot pipes
    plot_close(pipe1_plot);
    plot_close(pipe2_plot);

    return 0;
}