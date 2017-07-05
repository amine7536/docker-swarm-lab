# Swam Lab

## Stack 
- Ubuntu 16.04
- Docker Swarm
- Docker Flow (reverse proxy)
- DNSMasq

- Start everything :

```bash
$> vagrant up --provider virtualbox
Bringing machine 'manager' up with 'virtualbox' provider...
Bringing machine 'worker1' up with 'virtualbox' provider...
==> manager: Importing base box 'ubuntu/xenial64'...
==> manager: Matching MAC address for NAT networking...
==> manager: Checking if box 'ubuntu/xenial64' is up to date...
```

- Check lab Swam status

```bash
root@manager:~# docker node ls
ID                            HOSTNAME            STATUS              AVAILABILITY        MANAGER STATUS
kbukcmh4chcqpz5vf642ilxu1 *   manager             Ready               Active              Leader
y5u7dw2egf7vq4kwptrugc4qz     worker1             Ready               Active
```

- Manager IP : 10.0.40.10
- Worder IP : 10.0.40.101

It's a very basic cluster with only 1 Manager and 1 Worker.
The Swarm cluster is configured to use http://proxy.dockerflow.com/ as front facing reverse proxy. Docker flow proxy listen on changes to the list of service and updates its configuration accordingly.

```bash
root@manager:~# docker service list
ID                  NAME                MODE                REPLICAS            IMAGE                                       PORTS
isz3c3buhl06        proxy               replicated          1/1                 vfarcic/docker-flow-proxy:latest            *:80->80/tcp,*:443->443/tcp
yzy42jup59ku        swarm-listener      replicated          1/1                 vfarcic/docker-flow-swarm-listener:latest
```

Docker flow listens on port 80 (port 443 is not working needs to provide certificats)
DNSMasq is configured on the `manager` host to manage domain `*.pix.lab`.

```bash
$> host myservice.pix.lab
myservice.pix.lab has address 10.0.40.10
```

Tips: you can add 10.0.40.10 as a resolver on your workstation to access the services hosted on this lab.

