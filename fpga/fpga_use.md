# FPGA Usage overview
We try to firstly build each FPGA-component component separately, and figure out what the use of each one is.

In the Makefile we can find the makefile used to build all vhdl code.

Through makefile:
```sh
TARGET ?= pluto

bash -c "source $(VIVADO_SETTINGS) && make -C hdl/projects/$(TARGET) && cp hdl/projects/$(TARGET)/$(TARGET).sdk/system_top.xsa $@"
unzip -l $@ | grep -q ps7_init || cp hdl/projects/$(TARGET)/$(TARGET).srcs/sources_1/bd/system/ip/system_sys_ps7_0/ps7_init* build/
```


Simply calling in the pluto-project directory:
```bash
source $(VIVADO_SETTINGS) 
make
```
builds the files.
## axi_ad9361-module
- sources: https://wiki.analog.com/resources/fpga/docs/axi_ad9361



### SPI integration in verilog

### Which part of the fpga manages which part of the datastream?


### What exactly is the functinoality of the FPGA?

### How is this functionality referenced in the build-folder?


# Resources
List of IP cores and links to their functionality, as well as how to add extra modules to the FPGA:
- https://github.com/timcardenuto/testPlutoSDR

Integrating FIR filters into HDL design:
- https://wiki.analog.com/resources/fpga/docs/hdl/fmcomms2_fir_filt
