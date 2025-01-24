# Firmware
## IIO-drivers
The iio-drivers are defined in linux/drivers/iio/
- ad9361.c
- ..

Defining an attribute happens through 
- IIO_DEVICE_ATTR which contains (in order) the attribute-name (appearing in the file), the octal file-permissions (sysfs), getter, setter, addr (attribute passed to getter-setter)


### Modifying the existing firmware
The big issue with modifying the pluto-image and building it again is that it takes loads of time. So first thing we do is find a way to reduce the time it takes to build the whole image:
- https://github.com/daniestevez/pluto-firmware-modifications

# Examples