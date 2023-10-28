# TopologyDisplay - SDN - Backend
Softwarized And Virtualized mobile networks project 2022

## Authors
- Mattia Meneghin
- Francesco La Rosa
- Diamand Muka

## Dependencies
- Node (npm v10.1.0, nvm v0.39.5)
- Cors

## To run
- Download the comnetsemu environment [here](https://www.granelli-lab.org/researches/relevant-projects/comnetsemu-labs)
- we used Virtualbox, so we set NAT as network adapter and into advanced settings add the port forwarding as follow:
    - Name: ssh
    - Protocol: TPC
    - Host IP: empty
    - Host Port: 3000
    - Guest IP: empty
    - Guest Port: 22
- connect to the machine via ssh
    - ```ssh -p 3000 comnetsemu@127.0.0.1```
    - use the password: comnetsemu
- clone this repository inside
- ```npm install``` to install all the dependencies
- ```npm start``` to run the backend

## Api Request
- /host
- /switches
- /links
- /stats/flow/:id