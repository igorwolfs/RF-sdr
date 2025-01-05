# Buying
- JTAG compatible stuff to interface directly with the Xilinx FPGA
    - Buy 1.27 mm pin connectors
    - Solder them to the pluto-sdr jtag connector
- u.fl. connectors (female and male) to work with the adalm pluto

# Programming
- Check to what extent you can program the FPGA without an actual connection (so using the existing linux kernel on the device.)
- Launch the IIO-server on your laptop and try to get some data from the adalm pluto.
    - Try to access everything first using the gr-iio (GNU-radio) package, the iio_device_source and iio_device_sink-packages.
    - Use the configuration to: Choose a context, Enable channels, Set buffer size ..
- Try decoding a gnss signal from the adalm pluto and get the full actual messages