# Install DNSMASQ
sudo apt-get -y install dnsmasq
sudo cp /vagrant/dnsmasq.pix.lab.conf /etc/dnsmasq.d/.
sudo cp /vagrant/resolv.dnsmasq.conf /etc/.
sudo cp /vagrant/resolv.dnsmasq.conf /etc/resolv.conf
sudo systemctl restart dnsmasq