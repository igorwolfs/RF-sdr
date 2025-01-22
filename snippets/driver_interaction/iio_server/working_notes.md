# Parallel transmit and receiving
- Transmitting and receiving works in C-libiio libraries in non-cyclical mode in some cases.
    - We saw this in the case where receiving worked for only the seventh plot for some reason.
- Transmitting and receiving works in pyadi cyclically
    - We saw this in our pyadi code

For some reason however we can't seem to receive what we think we send with direct libiio in C.
