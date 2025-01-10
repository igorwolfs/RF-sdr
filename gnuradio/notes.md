# Good links

## Courses:
- https://pnsaeta.github.io/Learning_SDR/

# Blocks
## Repeat-block
Does upsampling, so makes each symbol last "Interpolation"-samples.
HOWEVER it does NOT keep the sampling rate the same, it increases the sampling rate in order to keep the bandwidth the same.
So given 20 symbols, an output sample rate of 1 kSamples and a repeat of 50 it should send exactly the 1kSamples per second expected.