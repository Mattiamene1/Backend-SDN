#!/bin/bash

# Start a new tmux session and run npm start in the Backend-SDN directory
tmux new-session -d -s Backend-SDN 'cd /Backend-SDN && npm start'

# Split the tmux window vertically and run mn command in the ryu-app directory
tmux split-window -v -t Backend-SDN 'cd /Backend-SDN/ryu-app && mn --topo tree,3 --controller=remote'

# Split the tmux window horizontally and run ryu-manager command in the ryu-app directory
tmux split-window -h -t Backend-SDN 'cd /Backend-SDN/ryu-app && ryu-manager --observe-links ryu.app.simple_switch ryu.app.gui_topology.gui_topology'

# Attach to the tmux session to view the terminals
tmux attach -t Backend-SDN


#cd /Backend-SDN
#screen
#npm start
#echo -en "\033[1;1H"

#cd /Backend-SDN/ryu-app
#screen
#mn --topo tree,3 --controller=remote
#echo -en "\033[1;1H"

#cd /Backend-SDN/ryu-app
#screen
#ryu-manager --observe-links ryu.app.simple_switch ryu.app.gui_topology.gui_topology
#echo -en "\033[1;1H"


#gnome-terminal --title="backend" --working-directory=~/Backend-SDN/ -- npm start

#gnome-terminal --title="mininet" --working-directory=~/Backend-SDN/ryu-app -- sudo mn --topo tree,3 --controller=remote

#gnome-terminal --title="remote" --working-directory=~/Backend-SDN/ryu-app --command "ryu-manager --observe-links ryu.app.simple_switch ryu.app.gui_topology.gui_topology"


