sudo apt-get update
sudo apt-get install -y language-pack-en
# Python Pip Fabric ...
sudo apt-get install -y python-pip python-dev build-essential
sudo apt-get install -y libssl-dev libffi-dev python-dev
sudo apt-get install -y libxslt-dev libxml2-dev
sudo apt-get install -y mkisofs
sudo apt-get install -y git
sudo pip install virtualenv
sudo pip install fabric
sudo pip install jinja2

# Install Pix-Cli to manage services
cd /vagrant/pix-cli && pip install -e .[test]