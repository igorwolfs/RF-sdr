# Radio Receiver / Transmitter
- Link: https://www.electronicdesign.com/technologies/analog/adc/article/21804630/high-speed-rf-sampling-adc-boosts-bandwidth-dynamic-range

## Receiver
1. LNA
2. Mixer
3. Analog filter (configurable)
4. ADC
5. 128-tap FIR (finite impulse response filter)
6. Manual / automatic gain control, dc offset, quadrature correction.
7. Resulting I and Q signals are passed to the digital baseband processor.


### Superheterodyne vs direct conversion vs RF sampling
**Superheterodyne**

- Takes in incoming RF signal.
- Downconverts with a mixer to lower intermediate frequency.
- This leads to a lower sampling-rate requirement.

CON:
- requires many filters and circuits
- Requires a local oscillator which adds phase noise and jitter
- Image issues (https://www.viksnewsletter.com/p/the-image-problem-in-rf-receiver)

**Direct Conversion Receiver**

- LO (Local oscillator) frequency is equal to the incoming signal frequency.
- This leads to a difference IF (intermediate frequency) of zero.
    - This is called a zero IF receiver
- RF signal is down-converted directly to baseband.

PRO:
- Less circuits and filters needed.
- No image-problem 


## Transmitter
1. Accepts 12-bit (I / Q), (Real / Imaginary) samples.
2. Runs it through a 128-tap FIR, interpolation filters, DAC, analog filters, and power amplifier
3. PLL's inside the AD9363 provide clocks and oscillators for receive and transmit channels.


# FPGA
- Xilinx Zynq AP SOC contains
    - Single core ARM Cortex-A9
    - 28 nm Artix-7 PML
    - Common peripherals (USB, SPI, etc..)


# libiio
## Purpose
It's a user-space library that makes it easier to interact with linux industrial drivers.
Device examples are ADC, DAC, accelerometers, IMU's, ..

## Checking the API
The API is exposed through sysfs at
- /sys/bus/iio/devices/*

This is the lowest possible way to interact with the devices on the plutosdr.

Which for the pluto-sdr becomes
```bash
# pwd
/sys/bus/iio/devices

# ls
iio:device0  iio:device1  iio:device2  iio:device3

# ls iio\:device1
dev                        in_voltage0_vccint_raw     in_voltage2_vccbram_scale  in_voltage5_vccoddr_raw    in_voltage7_vrefn_scale    power
events                     in_voltage0_vccint_scale   in_voltage3_vccpint_raw    in_voltage5_vccoddr_scale  in_voltage8_raw            sampling_frequency
in_temp0_offset            in_voltage1_vccaux_raw     in_voltage3_vccpint_scale  in_voltage6_vrefp_raw      in_voltage8_scale          subsystem
in_temp0_raw               in_voltage1_vccaux_scale   in_voltage4_vccpaux_raw    in_voltage6_vrefp_scale    name                       uevent
in_temp0_scale             in_voltage2_vccbram_raw    in_voltage4_vccpaux_scale  in_voltage7_vrefn_raw      of_node
```

For channels:
- in/out: indicates the direction of the channel
- Number: indicates the channel
- vrefn / vccbram / ..: alias name
- raw: parameter name

Depending on the name of the device and the device folder, we can
- Identify the IIO devices
- Identify the channel
- Identify attributes of the channel
- ..

iio_devices have 
- an iio_buffer (for passing data in or out)
- a debug-attribute (to )

## Where can it run

- An embedded linux system including IIO drivers.
- PC running a linux distribution connected to an embedded system through
    - USB
    - Serial
    - Network

## Library structure
- Local: interface through sysf virtual filesystem
- Network, USB: interface through iiod server (iiod server should for this purpose be installed on the computer)
- XML: interfacing through XML file
- Serial: interfacing with tiny-iiod through serial link

## The C-language API
### iio:context

- iio_context (instance of the library)
    - Can have 0 or many devices
    - Each device can have 1 buffer and 0 or many channels
- Library: https://analogdevicesinc.github.io/libiio/master/libiio/group__Context.html

1. iio_create_scan_context(NULL, 0)
2. You can get the info of the context to get more info.
3. Once you have more info you can delete the context-object.

There's various ways to create and delete contexts, examples can be found in the video / documentation.

**Navigation through context**

See examples to go through all channels of each device, and through the context.

**Sampling samples from a device**

There are several functions for that, check examples.
- Enable the channel
- Create an IO buffer
- Call IO buffer refill to get a new set of samples
- Destroy the IO buffer after use

You can access samples using
- A for-loop
- A callback

## LibIIO Bindings
It can be used
- Directly in C++
- Python (iio.py)
- C# 

Can be found in the analog-devices repo.

Other bindings (third party) exist in
- Rust: rust-industrial-io
- Node.js: node-iio
- GNU Radio: gr-iio

### GNU Radio module
- iio_device_source and iio_device_sink-IIO blocks can be used to 

## Libiio extra tools
- iio_info: allows you to get info about an iio-device: iio_info -u ip:192.168..2.1
- iio_attr: allows you to read and write iio attributes
- iio_writedev: allows you to write samle from an iio-device
- iio_reg: allows you to read or write spi / i2c registers in an iio-device
    - This is a really good way to debug and work on drivers.


## pyadi-iio
Can be install using pip install pyadi-iio.


# Resources:
- https://wiki.analog.com/software/linux/docs/iio/iio