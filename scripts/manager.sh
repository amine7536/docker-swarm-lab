
# Init Swarm
sudo docker swarm init --advertise-addr 10.0.40.10:2377 | grep SWMTKN | awk '{print $5}' > /vagrant/swarm.token

# Create proxy overlay network
sudo docker network create --driver overlay proxy

# Create apps overlay network
sudo docker network create --driver overlay apps

# Create listener for new Swarm service
docker service create --name swarm-listener \
--network proxy \
--mount "type=bind,source=/var/run/docker.sock,target=/var/run/docker.sock" \
-e DF_NOTIFY_CREATE_SERVICE_URL=http://proxy:8080/v1/docker-flow-proxy/reconfigure \
-e DF_NOTIFY_REMOVE_SERVICE_URL=http://proxy:8080/v1/docker-flow-proxy/remove \
--constraint 'node.role==manager' \
vfarcic/docker-flow-swarm-listener

# Create proxy service
docker service create --name proxy \
-p 80:80 \
-p 443:443 \
--network proxy \
-e MODE=swarm \
-e LISTENER_ADDRESS=swarm-listener \
vfarcic/docker-flow-proxy

# Use DNSMasq on worker1 as DNS
sudo apt-get -y remove resolvconf
sudo cp /vagrant/resolv.dnsmasq.conf /etc/resolv.conf