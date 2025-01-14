
#include <float.h>
#include "calc.h"
void min_f32(float *buffer, int sample_count, float* ret)
{
    float min_temp = FLT_MAX;
    // Declare minimum variable equal to max_float
	for (int i=0; i<sample_count; i++)
	{
		if (buffer[i] < min_temp)
		{
			min_temp = buffer[i];
		}
	}
    // iterate over all variables in buffer
    // If variable is smaller than just declared, set equal to that variable
	*ret = min_temp;
}

void max_f32(float *buffer, int sample_count, float* ret)
{
    float max_temp = -FLT_MAX;
    // Declare minimum variable equal to max_float
	for (int i=0; i<sample_count; i++)
	{
		if (buffer[i] > max_temp)
		{
			max_temp = buffer[i];
		}
	}
	*ret = max_temp;
}
