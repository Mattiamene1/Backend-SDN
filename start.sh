#!/bin/bash

echo "Welcome to sdn Project MM DM FLR"
echo "Select the topology:"
printf "Press [\e[1,92mS\e[0m] to get SINGLE topo.\n"
printf "Press [\e[1,92mR\e[0m] to get REVERSED topo.\n"
printf "Press [\e[1,92mL\e[0m] to get LINEAR topo.\n"
printf "Press [\e[1,92mT\e[0m] to get TORUS topo.\n"
printf "Press [\e[1,92mA\e[0m] to get TREE topo.\n"
read -p "" selection

if [ "$selection" == "S" ] || [ "$selection" == "s" ]; then
    topology=single
elif [ "$selection" == "R" ] || [ "$selection" == "r" ]; then
    topology=reversed
elif [ "$selection" == "L" ] || [ "$selection" == "l" ]; then
    topology=linear
elif [ "$selection" == "T" ] || [ "$selection" == "t" ]; then
    topology=torus
elif [ "$selection" == "A" ] || [ "$selection" == "a" ]; then
    topology=tree
else echo "Error,select one of the above"    

echo $topology

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

echo "Finish! Go to: http://localhost:8000"

