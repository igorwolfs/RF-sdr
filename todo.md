# Programming
- Check to what extent you can program the FPGA without an actual connection (so using the existing linux kernel on the device.)
- Launch the IIO-server on your laptop and try to get some data from the adalm pluto.
    - Try to access everything first using the gr-iio (GNU-radio) package, the iio_device_source and iio_device_sink-packages.
    - Use the configuration to: Choose a context, Enable channels, Set buffer size ..
- Try decoding a gnss signal from the adalm pluto and get the full actual messages
    - Use the ADI library
    - Then try it using the iio library
    - Then try it directly accessing the peripheral drivers (if possible)


# Program the fpga through jtag
- solder 1.27 mm on your pluto

## Access using peripheral drivers
- Check what happens on the libiio-driver side in the build-project

# Check
- https://github.com/timcardenuto/testPlutoSDR
    - Adding your own project to buildroot

# Check
- What exactly does the FPGA do inside the plutoSDR?
- Which pins are interfacing with the hard-logic in the device?
- Experiment with the Arty-s7 to get a grasp on simple verilog, before moving on to the plutosdr-firmware.