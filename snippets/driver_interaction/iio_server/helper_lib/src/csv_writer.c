#include "csv_writer.h"


#include <stdio.h>
#include <time.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>




void save_as_csv(uint32_t* buffer, int64_t buflen, char* filename)
{   
    // ***************** TIME HEADER AND FILE CREATION ***************************
    time_t rawtime;
    struct tm * timeinfo;
    time ( &rawtime );
    timeinfo = localtime ( &rawtime );
    printf ( "Current local time and date: %d:%d:%d", timeinfo->tm_sec, timeinfo->tm_min, timeinfo->tm_hour );

    int flen = strlen(filename);

    // Check if the folder exists
    struct stat st = {0};
    if (stat(SAVE_FOLDER, &st) == -1) {
        mkdir(SAVE_FOLDER, 0700);
        printf("Folder created: %s", SAVE_FOLDER);
    }
    else
    {
        printf("Folder %s exists\r\n", SAVE_FOLDER);

    }

    // Open the file using the provided filename
    char file_path[100] = "";
    sprintf(file_path, "%s/%s", SAVE_FOLDER, filename);
    printf("file name: %s\r\n", file_path);
    
    FILE *fpt;
    fpt = fopen(file_path, "w+");

    // Check if the file is open
    if (!fpt)
    {
        printf("Error: Unable to open file \r\n");
        return;
    }

    // ***************** DATA HEADER AND WRITING ***************************
    // Write the buffer to the file, comma-separated
    double t_step = 1000.0/((double)RX_TX_SAMPLING_RATE);

    fprintf(fpt,"time (ms), I, Q\r\n");

    int n_samples = (int) buflen / (BUFFER_ELEMENT_SIZE);

    // From 0 -> bufflen in terms of timesteps
    for (int i = 0; i < n_samples; i++)
    {
        int16_t ipart = (int16_t)((buffer[i] & 0xffff0000) >> 16);
        int16_t qpart = (int16_t)(buffer[i] & 0xffff);
        fprintf(fpt,"%.9f, %hd, %hd\r\n", (double)t_step * (double)i, ipart, qpart);
    }


    // Close the file
    fclose(fpt);

    printf("Data successfully saved to %s", filename);
}