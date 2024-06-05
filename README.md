# TopologyDisplay - SDN - Backend
Softwarized And Virtualized mobile networks project 2024

## Authors
- Mattia Meneghin
- Francesco La Rosa
- Diamand Muka

## Main Dependencies
- Bootstrap
- Cors
- Axios
- Express

## Environment
- Download the comnetsemu environment [here](https://www.granelli-lab.org/researches/relevant-projects/comnetsemu-labs)
- Check the IP of the VM typing ```ifconfig``` that will be used in the VM port forwarding config (in my case 10.0.2.15)
- we used Virtualbox, so we set NAT with some port forwarding rules as follow:
    
    **Name** | **Protocol** | **Host IP** | **Host Port** | **Guest IP** | **Guest Port** 
    --- | --- | --- | --- |--- |--- 
    SSH | TCP | empty | 2200 | 10.0.2.15 | 22
    Front End | TCP | empty | 8000 | 10.0.2.15 | 80
    
- Launch the Virtualbox Comnetsemu VM and then connect to the machine via ssh
    - ```ssh -p 2200 comnetsemu@localhost``` and type *yes*    
    - use the password: *comnetsemu*  

## Set Up the environment
- Install git
- Clone this repository inside
- Move inside ```cd Backend-SDN``` and then download all the dependencies ```npm i```
- Make all the actions as sudo
> Edit sudoers file ```sudo visudo``` and configure it as follow:
- root    ALL=(ALL:ALL) ALL
- %admin ALL=(ALL) ALL
- %sudo   ALL=(ALL:ALL) ALL
Now you can operate as sudo

## Setup Apache2
Our front end is available [here](https://github.com/Mattiamene1/Frontend-SDN), clone it in this way inside the folder that will be expose by Apache2 <br>
Follow this guidelines for more details [Install and Configure Apache](https://ubuntu.com/tutorials/install-and-configure-apache#1-overview)
- Install apache with ```sudo apt update``` and then ```sudo apt install apache2```
- Now in the /var/www/html/ folder you should see an index.html (default welcome page of Apache)
- Move into the Apache root with ```cd /var/www/html/```
- Import our frontend with ```sudo git clone https://github.com/Mattiamene1/Frontend-SDN .``` (Don't forget the point!)
- Make the www-data user owner of the folder /var/www/html/ and subfolders ```chown www-data:www-data -R *``` 
> Remember to configure it in order to expose the web interface

# Automatic Start
- ```sudo su``` 
- Make start.sh file executable ```chmod u+x start.sh```
- Launch the start script inside the repo folder ```./start.sh``` to run the project

> The files into **ryu_app** folder are the Ryu's APIs, they are available into the [Ryu repository](https://github.com/faucetsdn/ryu/tree/master/ryu/app).

<img src="hhtps://github.com/Mattiamene1/Backend-SDN/blob/main/docs/start_image.png">

> This script will ask the user the parameters based on the topology choosen.

If something goes wrong
# Manual Start
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
Navigate the *http://localhost:8000/* or follow the start.sh prompt

## Folder Structure
.<br>
├── Gui.py<br>
├── README.md<br>
├── index.js<br>
├── package-lock.json<br>
├── package.json<br>
├── ryu_app<br>
│   ├── ofctl_rest.py<br>
│   └── rest_topology.py<br>
└── start.sh<br>
