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
