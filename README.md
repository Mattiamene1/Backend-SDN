# TopologyDisplay - SDN - Backend
Softwarized And Virtualized mobile networks project 2022

## Authors
- Mattia Meneghin
- Francesco La Rosa
- Diamand Muka

## Dependencies
- Node (npm v10.1.0, nvm v0.39.5)
- Cors

## Environment
- Download the comnetsemu environment [here](https://www.granelli-lab.org/researches/relevant-projects/comnetsemu-labs)
- Check the IP of the VM typing ```ifconfig``` that will be used in the VM port forwarding config (in my case 10.0.2.15)
- we used Virtualbox, so we set NAT with some port forwarding rules as follow:
    
    **Name** | **Protocol** | **Host IP** | **Host Port** | **Guest IP** | **Guest Port** 
    --- | --- | --- | --- |--- |--- 
    SSH | TCP | empty | 2200 | 10.0.2.15 | 22
    Back End | TCP | empty | 3000 | 10.0.2.15 | 3000
    Front End | TCP | empty | 8000 | 10.0.2.15 | 80
    API1 | TCP | empty | 8080 | 10.0.2.15 | 8080
    
- Launch the Virtualbox Comnetsemu VM and then connect to the machine via ssh
    - ```ssh -p 2200 comnetsemu@localhost``` and type *yes*    
    - use the password: *comnetsemu*

## Set Up
- Install git
- clone this repository inside
- - Launch the set up script ```sudo bash script.sh```

> The files into **ryu_app** folder are the Ryu's APIs, they are available into the [Ryu repository](https://github.com/faucetsdn/ryu/tree/master/ryu/app).

### Add the Front End -------- Da implementare nello script
Our front end is available [here](https://github.com/Mattiamene1/Frontend-SDN), check the README file.

## Run the project
Once the environment is ready, open the terminal (If you used the script, you can go to the next step)
- Run the backend
    - ```cd Backend-SDN```
    - ```screen``` Then press *Enter*, a new shell will appear:
    - ```npm start```
    - <ctrl + a>, then <d> to close the shell

- Run the Mininet network
    - ```ssh -p 2200 comnetsemu@localhost``` and use the password: *comnetsemu*
    - ```cd Backend-SDN/ryu_app```
    - ```screen``` Then press *Enter*, a new shell will appear:
    - ```sudo mn --topo tree,3 --controller remote```
    - <ctrl + a>, then <d> to close the shell

- Run the ofctl_rest.py Ryu app
    - ```ssh -p 2200 comnetsemu@localhost``` and use the password: *comnetsemu*
    - ```cd Backend-SDN/ryu_app```
    - ```screen``` Then press *Enter*, a new shell will appear:
    - ```ryu-manager --observe-links ryu.app.simple_switch ryu.app.gui_topology.gui_topology```
    - <ctrl + a>, then <d> to close the shell

> ```screen -ls``` to show the screens list

## Use the GUI
Navigate the *http://localhost:8000/*
> Watch Out! It may needs a few refreshes