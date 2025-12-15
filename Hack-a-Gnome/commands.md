**whoami**:

```
<br>root<br><br>
```

**ps aux**:

```
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.1  0.0 1075516 15204 ?        Ssl  16:22   0:07 /app/gnome_cancontroller
root        20  0.0  0.0   4364  3200 ?         S    16:22   0:00 bash -c /usr/sbin/sshd -D & node server.js 2>&1 > /tmp/node.log
root        21  0.0  0.0  15436  8704 ?         S    16:22   0:00 sshd: /usr/sbin/sshd -D [listener] 0 of 10-100 startups
root        22  0.0  0.3 705148 56564 ?         Sl   16:22   0:00 node server.js
root        59  0.0  0.0      0     0 ?         Z    16:31   0:00 [timeout] <defunct>
root        72  0.0  0.0      0     0 ?         Z    16:43   0:00 [timeout] <defunct>
root        77  0.0  0.0      0     0 ?         Z    16:44   0:00 [timeout] <defunct>
root       120  0.0  0.0   2892   996 ?         S    17:33   0:00 /bin/sh -c ps aux
root       121  0.0  0.0   7064  1572 ?         R    17:33   0:00 ps aux
```

**uname -a**:

```
Linux ca3f5d486148 6.1.0-40-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.153-1 (2025-09-20) x86_64 x86_64 x86_64 GNU/Linux
```

**ss -ntlp**:

```
State   Recv-Q  Send-Q  Local Address:Port    Peer Address:Port   Process
LISTEN  0       4096    127.0.0.11:39239       0.0.0.0:*           -
LISTEN  0       128     0.0.0.0:22             0.0.0.0:*           users:(("sshd",pid=22,fd=3))
LISTEN  0       128     [::]:22                [::]:*              users:(("sshd",pid=22,fd=4))
LISTEN  0       511     *:3000                 *:*                 users:(("node",pid=23,fd=18))
```

**echo $PATH**:

```
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
```

**hostname**:

```
3fd0d769ea40
```

**ifconfig**:

```
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
    inet 172.18.0.7  netmask 255.255.0.0  broadcast 172.18.255.255
    ether f2:d3:f5:a2:d3:be  txqueuelen 0  (Ethernet)
    RX packets 76  bytes 15087 (15.0 KB)
    RX errors 0  dropped 0  overruns 0  frame 0
    TX packets 54  bytes 32188 (32.1 KB)
    TX errors 0  dropped 0  overruns 0  carrier 0  collisions 0

gcan0: flags=193<UP,RUNNING,NOARP>  mtu 72
    unspec 00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00
    txqueuelen 1000  (UNSPEC)
    RX packets 1423  bytes 2704 (2.7 KB)
    RX errors 0  dropped 0  overruns 0  frame 0
    TX packets 1423  bytes 2704 (2.7 KB)
    TX errors 0  dropped 0  overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
    inet 127.0.0.1  netmask 255.0.0.0
    inet6 ::1  prefixlen 128  scopeid 0x10<host>
    loop  txqueuelen 1000  (Local Loopback)
    RX packets 8  bytes 625 (625.0 B)
    RX errors 0  dropped 0  overruns 0  frame 0
    TX packets 8  bytes 625 (625.0 B)
    TX errors 0  dropped 0  overruns 0  carrier 0  collisions 0
```