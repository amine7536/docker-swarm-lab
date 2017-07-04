sudo apt-get -y remove docker docker-engine docker.io
sudo apt-get update
sudo apt-get -y install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs)  stable"
sudo apt-get update
sudo apt-get -y install docker-ce


# sudo apt-get update
# sudo apt-get install -y language-pack-en
# # Python Pip Fabric ...
# sudo apt-get install -y python-pip python-dev build-essential
# sudo apt-get install -y libssl-dev libffi-dev python-dev
# sudo apt-get install -y libxslt-dev libxml2-dev
# sudo apt-get install -y mkisofs
# sudo apt-get install -y git
# sudo pip install virtualenv
# sudo pip install fabric
# sudo pip install jinja2
