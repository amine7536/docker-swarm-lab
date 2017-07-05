# Join cluster
sudo docker swarm join --token $(cat /vagrant/swarm.token) 10.0.40.10:2377
