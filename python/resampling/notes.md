# Rational resample (up-sampling followed by down-samling)

Changes the sample-rate of a discrete time sampled signal.

E.g.: from 
- f1 = 8000 samples / second
to
- f2 = 12000 sample / second

12 / 8 = 3 / 2

So
1. Up-sample by a factor of 3
    - insert N-1 (N=3) zeros between each samples
    - pass the signal through an ideal LP filter with normalized bandwidth 1/N compared to nyquist bandwidth
2. Down-sample by a factor of 2
    - pass the signal through a LP filter with normalized bandwidth (1/D) (D=2) compared to the nyquist bandiwdth
    - Decimate the signal by a factor of D (so keep only every Dth sample)

Instead of using 2 LP filter we can do it with one
1. Insert N-1 zeros between each sample
2. Run through low-pass filter with bandwidth of B=min(1/N, 1/D)
3. Decimate signal by factor of D