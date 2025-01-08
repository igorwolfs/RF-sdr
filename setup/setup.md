# Connecting to the device
When connecting the device shows up as:

```bash
enx00e022ac8ac0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet6 fe80::6f21:3291:39f9:8d75  prefixlen 64  scopeid 0x20<link>
        ether 00:e0:22:ac:8a:c0  txqueuelen 1000  (Ethernet)
        RX packets 2  bytes 374 (374.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 5  bytes 1244 (1.2 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

```

## Connecting through ssh

The bash connection is:
```bash
ssh root@192.168.2.1
```

The username by default is "root", the password by default is "analog"

# Updating firmware
```bash
# iio_attr -u ip:192.168.2.1 -C fw_version
fw_version: v0.32
```

To check all devices do:
```
iio_readdev -S
```

# Building firmware
https://github.com/analogdevicesinc/plutosdr-fw

```bash
 sudo apt-get install git build-essential fakeroot libncurses5-dev libssl-dev ccache
 sudo apt-get install dfu-util u-boot-tools device-tree-compiler libssl1.0-dev mtools
 sudo apt-get install bc python cpio zip unzip rsync file wget
 git clone --recursive https://github.com/analogdevicesinc/plutosdr-fw.git
 cd plutosdr-fw
 export VIVADO_SETTINGS=/opt/Xilinx/Vivado/2021.2/settings64.sh
 make
```

# Checking USB / Ethernet bandwidth

- The pluto-SDR itself has 20 MHz of bandwidth.
- The USB itself is limited to about 4 MS/s

## Using the command

### Command
- iio_readdev -u ip:192.168.2.1 -b 100000 cf-ad9361-lpc | pv > /dev/null

Shows
- a throughput of about 17-19 MiB/s.
- bandwidth check shows around 5.1 MHz

- iio_readdev -u usb:3.5.5 -b 100000 cf-ad9361-lpc | pv > /dev/null
- a throughput of about 25 MiB/s 
- bandwidth check shows around 6.7 MHz

The main thing here is the buffer-size. It needs to be an integer amount of the pluto internal buffers. It can also be set using the iio-libs:
- https://ez.analog.com/adieducation/university-program/f/q-a/533760/pluto-sdr-number-of-buffer

### Explanation
- iio_readdev -u <device_name> -b <buffer_size> <device_name>
- |: pipe operator -> pass output from one command through as input to the next.
- pv: piper viewer: shows the progress of the data flowing through pipe
- /dev/null: linux null device discarding anything it receives
- cf-ad9361-lpc: core-fpga-AD9361-low-pin-count device
