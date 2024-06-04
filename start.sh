#!/bin/bash

echo "Welcome to sdn Project MM DM FLR"
echo "Select the topology:"
printf "Press [\e[1,92mS\e[0m] to get SINGLE topo.\n"
printf "Press [\e[1,92mL\e[0m] to get LINEAR topo.\n"
printf "Press [\e[1,92mT\e[0m] to get TORUS topo.\n"
printf "Press [\e[1,92mA\e[0m] to get TREE topo.\n"
read -p "" selection

if [ "$selection" == "S" ] || [ "$selection" == "s" ]; then
    topology=single
    echo "Select n° of host"
    read -p "" host
    echo "topology:$topology and $host of hosts"
elif [ "$selection" == "L" ] || [ "$selection" == "l" ]; then
    topology=linear
    echo "Select n° of switch:"
    read -p "" switch
    echo "topology:$topology and $switch"
elif [ "$selection" == "T" ] || [ "$selection" == "t" ]; then
    topology=torus
    echo "Select the lenght and the breadth(reccomended 3):"
    read -p "" lenght
    breadth=lenght
    echo "topology:$topology with lenght of $lenght and $breadth breadth"   
elif [ "$selection" == "A" ] || [ "$selection" == "a" ]; then
    topology=tree
    echo "Select the depht:"
    read -p "" depht
    echo "Select the fanout:"
    read -p "" fanout
    echo "topology:$topology and a fanout of $fanout"
else
    echo "Error, select one of the above options."
    exit 1
fi

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

if [ "$selection" == "S" ] || [ "$selection" == "s" ]; then
    echo "sudo mn --topo $topology,$host --controller=remote"
    screen -d -m bash -c "sudo mn --topo $topology,$host --controller=remote"
elif [ "$selection" == "L" ] || [ "$selection" == "l" ]; then
    echo "sudo mn --topo $topology,$switch --controller=remote"
    screen -d -m bash -c "sudo mn --topo $topology,$switch --controller=remote"
elif [ "$selection" == "T" ] || [ "$selection" == "t" ]; then
    echo "sudo mn --topo $topology,$lenght,$breadth --controller=remote"
    screen -d -m bash -c "sudo mn --topo $topology,$lenght,$breadth --controller=remote"
elif [ "$selection" == "A" ] || [ "$selection" == "a" ]; then
    echo "sudo mn --topo $topology,$depht,$fanout --controller=remote"
    screen -d -m bash -c "sudo mn --topo $topology,$depht,$fanout --controller=remote"
fi

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