#!/bin/bash

apt-get update

echo "Add repository for installing PostgreSQL 9.4..."
sudo add-apt-repository "deb https://apt.postgresql.org/pub/repos/apt 14.04-pgdg main"
sudo add-apt-repository "deb https://apt.postgresql.org/pub/repos/apt/ trusty-pgdg main"
wget --quiet -O - https://postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt-get update

echo "Installing dependencies..."
apt-get install -y wget nginx python3.4 python3.4-dev git postgresql-9.4 postgresql-contrib-9.4
echo "Done!"

echo "Installing pip3..."
cd /home/vagrant/
wget https://bootstrap.pypa.io/get-pip.py
python3.4 get-pip.py
rm /home/vagrant/get-pip.py
echo "Done!"

echo "Install Python libs..."
pip3 install -r /opt/.provision/requirements/vagrant.txt
echo "Done!"

echo "Configuring bulavka application..."
mkdir -p /etc/bulavka/
cp /opt/.provision/bulavka.conf /etc/bulavka/bulavka.conf
chown -R "root:root" /etc/bulavka/
echo "Done!"

echo "Preparing logging destination for bulavka application..."
mkdir -p /var/log/bulavka
touch /var/log/bulavka/application.log
chown -R "vagrant:vagrant" /var/log/bulavka
echo "Done!"

echo "Preparing destination for publicly shared data..."
mkdir -p /opt/apps/spa_request_handler/media
chown -R "vagrant:vagrant" /opt/apps/spa_request_handler/media
mkdir -p /opt/apps/spa_request_handler/static
chown -R "vagrant:vagrant" /opt/apps/spa_request_handler/static
echo "Done!"

echo "Run collector tornado..."
nohup python3 /opt/apps/spa_request_handler/application.py --debug &
echo "Done!"

echo "Configuring nginx..."
mkdir -p /etc/nginx/sites-available /etc/nginx/sites-enabled
cp /opt/.provision/nginx.conf /etc/nginx/nginx.conf
cp /opt/.provision/app.nginx /etc/nginx/sites-available/bulavka && \
    ln -fs /etc/nginx/sites-available/bulavka /etc/nginx/sites-enabled/bulavka
echo "Done!"

echo "Start & Enable nginx..."
/etc/init.d/nginx start
echo "Done!"
