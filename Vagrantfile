# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
    # All Vagrant configuration is done here. The most common configuration
    # options are documented and commented below. For a complete reference,
    # please see the online documentation at vagrantup.com.

    # Every Vagrant virtual environment requires a box to build off of.
    config.vm.box = "django-base"
    config.vm.box_url = "http://blitz-vagrant.s3.amazonaws.com/django-base.box"

    ## Networking
    config.vm.network :forwarded_port, guest: 8000, host: 8000 # local dev
    config.vm.network :forwarded_port, guest: 5432, host: 5432 # postgresql
    
    config.ssh.forward_agent = true
    config.vm.synced_folder "cloudseed/current/srv/", "/srv/"
    config.vm.synced_folder "./", "/var/www/"
    

    ## Install Saltstack GitFS requirements
    config.vm.provision :shell, :inline => "sudo apt-get update"
    config.vm.provision :shell, :inline => "sudo apt-get install python-dev git-core python-setuptools -y"
    config.vm.provision :shell, :inline => "sudo easy_install GitPython"

    ## Salt:
    config.vm.provision :salt do |salt|
        salt.run_highstate = true
        salt.install_master = true
        salt.master_config = "cloudseed/current/salt/master"
        salt.minion_config = "cloudseed/current/vagrant/minion"
        salt.minion_key = "cloudseed/current/vagrant/minion.pem"
        salt.minion_pub = "cloudseed/current/vagrant/minion.pub"
        salt.seed_master = {minion: "cloudseed/current/vagrant/minion.pub"}
        salt.verbose = true
        
        salt.install_type = "git"
        salt.install_args = "v0.17.0"
        salt.bootstrap_options = "-D -F"
        end

end