# Install DNSMASQ
sudo apt-get -y install dnsmasq
cp /vagrant/dnsmasq.pix.lab.conf /etc/dnsmasq.d/.
sudo systemctl restart dnsmasq