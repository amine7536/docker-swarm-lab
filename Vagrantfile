# -*- mode: ruby -*-
# vi: set ft=ruby :

ENV["LC_ALL"] = "en_US.UTF-8"
BOX="ubuntu/xenial64"


Vagrant.configure("2") do |config|

  config.hostmanager.enabled = true
  config.hostmanager.manage_host = true
  config.hostmanager.ignore_private_ip = false
  config.hostmanager.include_offline = true

  # Swarm Manager
  config.vm.define "manager" do |manager|
    manager.vm.box = BOX

    manager.vm.provider "vmware_fusion" do |v|
      v.vmx["memsize"] = "1024"
      v.vmx["numvcpus"] = "2"
    end

    manager.vm.provider :virtualbox do |v|
      v.customize ["modifyvm", :id, "--memory", 1024]
      v.customize ["modifyvm", :id, "--cpus", 2]
    end


    manager.vm.hostname = "manager.lab.local.dev"
    manager.vm.network :private_network, ip: "10.0.40.10"
    manager.hostmanager.aliases = "manager"
    
    manager.vm.provision "shell", path: "./provision/docker.sh"
    manager.vm.provision "shell", path: "./provision/manager.sh"
      
  end
  
  # Swarm Worker
  config.vm.define "worker1" do |worker1|
    worker1.vm.box = BOX

    worker1.vm.provider "vmware_fusion" do |v|
      v.vmx["memsize"] = "512"
      v.vmx["numvcpus"] = "2"
    end

    worker1.vm.provider :virtualbox do |v|
      v.customize ["modifyvm", :id, "--memory", 512]
      v.customize ["modifyvm", :id, "--cpus", 2]
    end

    worker1.vm.host_name = "worker1.lab.local.dev"
    worker1.vm.network "private_network", ip: "10.0.40.101"
    worker1.hostmanager.aliases = "worker1"

    worker1.vm.provision "shell", path: "./provision/docker.sh"    

  end

end
