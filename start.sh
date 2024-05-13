#!/bin/bash

echo "Active screens: "
screen -list

echo "Killing screens..."
sudo killall screen

echo "Result: "
screen -list

echo "Starting new screens"

echo "Starting node..."
cd /home/comnetsemu/Backend-SDN
screen -d -m bash -c "npm start"
sleep 5

echo "Starting mininet..."
cd /home/comnetsemu/Backend-SDN/ryu_app
sudo mn -c
screen -d -m bash -c "sudo mn --topo tree,3 --controller=remote"
sleep 5

echo "Starting ryu-controller..."
cd /home/comnetsemu/Backend-SDN/ryu_app
screen -d -m bash -c "ryu-manager --observe-links ryu.app.simple_switch ryu.app.gui_topology.gui_topology"


echo "Active screens: "
screen -list
sudo screen -list


echo "Pulling frontend: "
cd /var/www/html
sudo git pull

echo "Finish! Go to: https://localhost:8000"

