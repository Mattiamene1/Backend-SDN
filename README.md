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
- we used Virtualbox, so we set NAT with some port forwarding rules as follow:
    
    **Name** | **Protocol** | **Host IP** | **Host Port** | **Guest IP** | **Guest Port** 
    --- | --- | --- | --- |--- |--- 
    Back End | TCP | empty | 3000 | 10.0.2.15 | 3000
    Front End | TCP | empty | 8000 | 10.0.2.15 | 80
    API1 | TCP | empty | 8080 | 10.0.2.15 | 8080
    API2 | TCP | empty | 8082 | 10.0.2.15 | 8082
    SSH | TCP | empty | 2200 | 10.0.2.15 | 22

- Launch the Virtualbox Comnetsemu VM and then connect to the machine via ssh
    - ```ssh -p 2200 comnetsemu@localhost```
    - use the password: *comnetsemu*
- clone this repository inside
- ```npm install``` to install all the dependencies

> The files into **ryu_app** folder are the Ryu's APIs, they are available into the [Ryu repository](https://github.com/faucetsdn/ryu/tree/master/ryu/app).

### Add the Front End
Our front end is available [here](https://github.com/Mattiamene1/Frontend-SDN), check the README file.

## Run the project
Once the environment is ready, open the terminal
- Run the nodeJs code
    - ```cd Backend-SDN```
    - ```screen``` Then press *Enter*, a new shell will appear:
    - ```npm start```
    - <ctrl + a>, then <d> to close the shell

- Run the rest_topology.py Ryu app
    - ```cd Backend-SDN/ryu_app```
    - ```screen``` Then press *Enter*, a new shell will appear:
    - ```ryu-manager rest_topology.py```
    - <ctrl + a>, then <d> to close the shell

- Run the ofctl_rest.py Ryu app
    - ```cd Backend-SDN/ryu_app```
    - ```screen``` Then press *Enter*, a new shell will appear:
    - ```ryu-manager ofctl_rest.py```
    - <ctrl + a>, then <d> to close the shell

> ```screen -ls``` to show the screens list

## Use the GUI
Navigate the *http://localhost:8000/*