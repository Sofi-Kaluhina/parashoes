# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"


options = {
    :network_ip => ENV['BULAVKA_VAGRANT_NETWORK_IP'] || "10.11.12.11",
    :port_ssh => Integer(ENV['BULAVKA_VAGRANT_PORT_SSH'] || 2201),
    :port_http => Integer(ENV['BULAVKA_VAGRANT_PORT_HTTP'] || 8081),
    :port_pg => Integer(ENV['BULAVKA_VAGRANT_PORT_PG'] || 5433),
    :vm_memory => Integer(ENV['BULAVKA_VAGRANT_MEMORY'] || 512),
}


Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
    config.vbguest.iso_path = "http://download.virtualbox.org/virtualbox/5.0.16/VBoxGuestAdditions_5.0.16.iso"
    config.hostsupdater.remove_on_suspend = true

    config.vm.box = "ubuntu/trusty64"
    config.vm.box_version = "14.04"

    config.ssh.shell = "bash -c 'BASH_ENV=/etc/profile exec bash'"

    config.vm.define "bulavka" do |node|
        node.vm.hostname = "bulavka"
        node.vm.network :private_network, ip: options[:network_ip]

        node.vm.network :forwarded_port,
            guest: 22,
            host: options[:port_ssh],
            id: "ssh",
            auto_correct: true
        node.vm.network :forwarded_port,
            guest: 8080,
            host: options[:port_http],
            id: "http"
        node.vm.network :forwarded_port,
            guest: 5432,
            host: options[:port_pg],
            id: "pg"

        node.vm.synced_folder "./apps", "/opt/apps",
            сreate: true,
            group: "vagrant",
            owner: "vagrant"
        node.vm.synced_folder "./.provision", "/opt/.provision",
            сreate: true,
            group: "vagrant",
            owner: "vagrant"

        node.vm.provider :virtualbox do |vb|
            vb.gui = false
        #    vb.customize [
        #        "modifyvm", :id,
        #        "--name", "vagrant-bulavka-ubuntu",
        #        "--memory", options[:vm_memory],
        #        "--natdnshostresolver1", "on",
        #        "--longmode", "on",
        #    ]
        end

        node.vm.provision "shell", path: "./.provision/bootstrap.sh"
    end
end
