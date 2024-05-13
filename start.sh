#!/bin/bash

#!/bin/bash

# Open terminal window for Backend-SDN
gnome-terminal --working-directory=/Backend-SDN -- npm start

# Open terminal window for Ryu controller
gnome-terminal --working-directory=/Backend-SDN/ryu-app -- mn --topo tree,3 --controller=remote

# Open terminal window for Ryu manager
gnome-terminal --working-directory=/Backend-SDN/ryu-app -- ryu-manager --observe-links ryu.app.simple_switch ryu.app.gui_topology.gui_topology


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


