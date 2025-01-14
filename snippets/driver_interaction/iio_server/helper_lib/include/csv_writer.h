#ifndef CSV_READ_WRITE_H
#define CSV_READ_WRITE_H

#define SAVE_FOLDER "../data"
#define BUFFER_ELEMENT_SIZE     32 // Size of individual bit size
#define RX_TX_SAMPLING_RATE     2.5e6

#include <stdint.h>
void save_as_csv(uint32_t *samples, int64_t buflen, char* filename);


#endif