#!/bin/bash

echo "Welcome to SDN Project MM DM FLR"
echo "Select the topology:"
printf "Press [\e[1;92mS\e[0m] to get SINGLE topo.\n"
printf "Press [\e[1;92mL\e[0m] to get LINEAR topo.\n"
printf "Press [\e[1;92mT\e[0m] to get TORUS topo.\n"
printf "Press [\e[1;92mA\e[0m] to get TREE topo.\n"
read -p "" selection

case "$selection" in
    [Ss])
        topology=single
        read -p "Select n° of hosts: " host
        echo "topology: $topology with $host hosts"
        topo_params="$topology,$host"
        ;;
    [Ll])
        topology=linear
        read -p "Select n° of switches: " switch
        echo "topology: $topology with $switch switches"
        topo_params="$topology,$switch"
        ;;
    [Tt])
        topology=torus
        read -p "Select the length and the breadth (recommended 3): " length
        breadth=$length
        echo "topology: $topology with length $length and breadth $breadth"
        topo_params="$topology,$length,$breadth"
        ;;
    [Aa])
        topology=tree
        read -p "Select the depth: " depth
        read -p "Select the fanout: " fanout
        echo "topology: $topology with depth $depth and fanout $fanout"
        topo_params="$topology,$depth,$fanout"
        ;;
    *)
        echo "Error, select one of the above options."
        exit 1
        ;;
esac

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

echo "sudo mn --topo $topo_params --controller=remote"
screen -d -m bash -c "sudo mn --topo $topo_params --controller=remote"

echo "Starting ryu-controller..."
cd /home/comnetsemu/Backend-SDN/ryu_app
screen -d -m bash -c "ryu-manager --observe-links ryu.app.simple_switch_13 ryu.app.gui_topology.gui_topology"

echo "Active screens: "
screen -list
sudo screen -list

echo "Pulling frontend: "
cd /var/www/html
sudo git pull

echo "Finish! Go to: http://localhost:8000"
    