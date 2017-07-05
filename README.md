# Swam Lab

## Stack 
- Ubuntu 16.04
- Docker Swarm
- Docker Flow (reverse proxy)
- DNSMasq

## Getting Started :

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
#
root@manager:~# docker network ls
NETWORK ID          NAME                DRIVER              SCOPE
j9v6g1k6hrnr        apps                overlay             swarm
4f2b5036adb1        bridge              bridge              local
0a226554a5be        docker_gwbridge     bridge              local
e57ec38a3afd        host                host                local
accgl5jfp3yf        ingress             overlay             swarm
6285fcd5ce67        none                null                local
2qz13hz13ga5        proxy               overlay             swarm
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


## Build a branch

A Python based CLI `pix-cli` is provided and already installed on the manager to help build and run the micorservices usint the Feature-Branch workflow

### Build a branch

```bash
# On the manager
$> pix-cli svc:build <micro svc name> --branch <feature branch name>
```

Example :

```bash
$> pix svc:build ms1 --branch my-feature
INFO: Pushing feature branch: my-feature for Service: ms1
INFO: Building docker image ms1:my-feature
INFO: Checkout branch my-feature
INFO: Using Dockerfile /vagrant/ms1/Dockerfile
Sending build context to Docker daemon  8.192kB
Step 1/7 : FROM ruby:2.1.5
 ---> 4c5360a232bd
Step 2/7 : WORKDIR /usr/src/app
 ---> Using cache
 ---> 99702d2e00cc
Step 3/7 : COPY Gemfile* ./
 ---> Using cache
```

### Run the Microservice

```bash
# On the manager
$> pix-cli svc:run <micro svc name> --branch <feature branch name>
```

Example :

```bash
pix svc:run ms1 --branch my-feature
INFO: Running feature branch: my-feature for Service: ms1
/vagrant/ms1/Dockerfile
/vagrant/ms1
ms1:my-feature
my-feature-ms1
my-feature-ms1.pix.lab
```

The CLI will run the command :

```
docker service create --name my-feature-ms1 \
        -e MS_URL=http://new-branch-ms2.pix.lab  \
        --network apps \
        --network proxy \
        --label com.df.notify=true \
        --label com.df.distribute=true \
        --label com.df.servicePath=/ \
        --label com.df.serviceDomain=my-feature-ms1.pix.lab \
        --label com.df.port=8080 \
        ms1:my-feature
```

This will run the service and register the configuration on Docker Flow proxy to respond on the vhosts `my-feature-ms1.pix.lab`

### Check it's working

- ms1 :

```bash
$> curl -sv http://my-feature-ms1.pix.lab
curl -sv http://my-feature-ms1.pix.lab
* Rebuilt URL to: http://my-feature-ms1.pix.lab/
*   Trying 10.0.40.10...
* Connected to my-feature-ms1.pix.lab (10.0.40.10) port 80 (#0)
> GET / HTTP/1.1
> Host: my-feature-ms1.pix.lab
> User-Agent: curl/7.47.0
> Accept: */*
>

Hello, world. I'm OK"
```

- ms2 :

```bash
$> curl -sv http://my-feature-ms2.pix.lab
```


# Todo :
- Adding configuration files
- Env file for each microservice
- Unit Tests
...