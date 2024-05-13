#!/bin/bash

gnome-terminal --title="backend" --working-directory=~/Backend-SDN/ -- npm start
gnome-terminal --title="mininet" --working-directory=~/Backend-SDN/ryu-app -- sudo mn --topo tree,3 --controller remote
gnome-terminal --title="remote" --working-directory=~/Backend-SDN/ryu-app -- ryu-manager --observe-links ryu.app.simple_switch ryu.app.gui_topology.gui_topology

