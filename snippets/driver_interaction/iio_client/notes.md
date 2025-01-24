- https://ez.analog.com/adieducation/university-program/f/q-a/108205/plutosdr-minimal-tool-chain-for-c-compiling
- The example assumes that it is on the pluto by default https://ez.analog.com/adieducation/university-program/f/q-a/111671/pluto-to-pluto-data-link

# Building
## Xilinx toolchain
Xilinx toolchain is saved in
```bash
/tools/Xilinx/Vitis/2024.2/gnu/aarch32/lin/gcc-arm-linux-gnueabi/bin:$PATH
```


NOTE: this is a later toolchain than the one the userspace was compiled with, so we might have to install a different version of vivado.

Perhaps the best thing is to
- compile the firmware from source
    - https://github.com/analogdevicesinc/plutosdr-fw
- FLash the binary onto the pluto-sdr.

## Compiling firmware from source
Set 
- VIVADO_VERSION ?= 2023.2 (as specified in makefile)
- Make sure to install libmpc-dev (not specified in instructions)
    - This library allows for better handling of floating point errors.
- Make sure to install libidn11 according to the instruction linked in case of running on ubuntu >= 22.04 device.
    - https://askubuntu.com/questions/1477217/cant-install-libidn11-on-my-ubuntu-22-04

- Compiled firmware version v0.39-dirty.
- Put the zipfile acquired onto the mass storage device.
- Eject the device
- Wait until the user LED stops blinking.

## Cross-compiling
### iio-libs
We need to make sure we compile with the same iio-libs as the ones we have on our pluto-sdr.

Library version: 0.26
```bash
# iio_info --version
iio_info version: 0.26 (git tag:v0.26)
Libiio version: 0.26 (git tag: v0.26) backends: local xml ip usb serial
```

The local iiolib library version is: v0.25.

### Example attempt
When using this simple example:
- https://wiki.analog.com/university/tools/pluto/devs/embedded_code#set_up_your_linux_host

We come across the following error:
```bash
arm-linux-gnueabihf-gcc  --sysroot=$projects/rf_sdr_project/build_env/pluto-0.39.sysroot/ -std=gnu99 -g -o pluto_stream main.c -lpthread -liio -lm -Wall -Wextra
/tools/Xilinx/Vitis/2023.2/gnu/aarch32/lin/gcc-arm-linux-gnueabi/x86_64-petalinux-linux/usr/bin/arm-xilinx-linux-gnueabi/arm-xilinx-linux-gnueabi-ld.real: cannot find crtbeginS.o: No such file or directory
collect2.real: error: ld returned 1 exit status
```

It happens to be the case that one can't use the vitis toolchains anymore to build buildroot:
- https://ez.analog.com/adieducation/university-program/f/q-a/571929/plutosdr-stand-alone-apps-not-running-in-v0-37

after v0.36 since from then onwards there was a switch to uClibc sysroot instead of glibc sysrppt-

## Installing linaro toolchain



From the buildroot folder its visible that
- gcc-linaro-7.3.1-2018.05-x86_64_arm-linux-gnueabihf was used to compile the image.

So in the desired location:
```bash
sudo wget https://releases.linaro.org/components/toolchain/binaries/7.3-2018.05/arm-linux-gnueabihf/gcc-linaro-7.3.1-2018.05-i686_arm-linux-gnueabihf.tar.xz

sudo tar -xf gcc-linaro-7.3.1-2018.05-i686_arm-linux-gnueabihf.tar.xz
```

And add the toolchain to your path.

Then perform 

```bash
# PLUTOSDR_TOOLCHAIN/aarch64-linux-gnu-gcc  --sysroot=$PLUTOSDR_SYSROOT -std=gnu99 -g -o pluto_stream main.c -lpthread -liio -lm -Wall -Wextra

pluto-0.39.sysroot/usr/lib/crt1.o: error adding symbols: File in wrong format
collect2: error: ld returned 1 exit status
```


And even when trying the example from the analog-devices website, we get the following result for a simple main.c:

```bash
 $PLUTOSDR_TOOLCHAIN/arm-linux-gnueabihf-gcc -mfloat-abi=hard  --sysroot=$PLUTOSDR_SYSROOT -std=gnu99 -g -o pluto_stream main.c -lpthread -liio -lm -Wall -Wextra
```

Note: previously a wrong path was given here, make sure the path to sysroot is in fact correct


For the actual example:

```bash
$PLUTOSDR_TOOLCHAIN/arm-linux-gnueabihf-gcc -mfloat-abi=hard  --sysroot=$PLUTOSDR_SYSROOT -std=gnu99 -g -o pluto_stream ad9361-iiostream.c -lpthread -liio -lm -Wall -Wextra
```
Which outputs the correct file.

# Transferring the files onto the pluto
Use the command:
```bash
sudo scp -O ads9361_libiio_txrx.bin  root@192.168.2.1:/tmp/
```

Afterwards transfer data back using the command
```bash
sudo scp -O root@192.168.2.1:/tmp/data/* $PWD/data/
```

Important is to specify -O to make sure there's reverse-compatibility with the client's version of scp / ssh.