#include "csv_writer.h"
#include <iostream>
#include <chrono>
#include <ctime>
#include <cstring>

#include <fstream>
#include <string>
#include <filesystem>



void save_as_csv(uint32_t* buffer, int size_t, char* filename)
{   
    // ***************** TIME HEADER AND FILE CREATION ***************************
    std::time_t save_time = std::chrono::system_clock::to_time_t(std::chrono::system_clock::now());
    std::tm *time_info = std::localtime(&save_time);
    char *save_time_str = std::ctime(&save_time);
    std::ostringstream oss;

    char fname[50] = "";
    sprintf(fname, "h2data_%d%02d%02d-%02d%02d%02d.csv",time_info->tm_year + 1900 , time_info->tm_mon + 1, time_info->tm_mday, time_info->tm_hour, time_info->tm_min, time_info->tm_sec);
    
    int flen = strlen(fname);
    // Check if the folder exists
    if (!std::filesystem::exists(SAVE_FOLDER))
    {
        // Try to create the folder
        if (std::filesystem::create_directory(SAVE_FOLDER))
        {
            printf("Folder created: %s", SAVE_FOLDER);
        }
        else
        {
            std::cerr << "Error: Could not create folder " << SAVE_FOLDER << std::endl;
        }
    }
    else
    {
        printf("Folder %s exists\r\n", SAVE_FOLDER);
    }

    // Open the file using the provided filename
    char file_path[100] = "";
    sprintf(file_path, "%s/%s", SAVE_FOLDER, fname);
    printf("file name: %s\r\n", file_path);
    std::ofstream file(file_path);


    // Check if the file is open
    if (!file.is_open())
    {
        printf("Error: Unable to open file \r\n");
        return;
    }

    // ***************** DATA HEADER AND WRITING ***************************
    // Write the buffer to the file, comma-separated
    double t_step = 1.0/((double)RX_TX_SAMPLING_RATE)
    file << "time (ms), I, Q\r\n";
    int n_samples = (int) bufflen / (BUFFER_ELEMENT_SIZE);

    // From 0 -> bufflen in terms of timesteps
    for (int i = 0; i < bufflen; i++)
    {
        int16_t ipart = (int16_t)((buffer[i] & 0xffff0000) >> 16);
        int16_t qpart = (int16_t)(buffer[i] & 0xffff);
        file << (double)t_step * (double)i << ", " << ipart << ", " << qpart << "\r\n";
    }


    // Close the file
    file.close();

    printf("Data successfully saved to %s", fname);
}