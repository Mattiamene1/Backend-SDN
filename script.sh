#!/bin/bash

banner() {
    clear
    printf "   \n"
    printf "   \e[100m\e[1;77m:: Networkin 2 Project: Topology Display      ::\e[0m\n"
    printf "   \e[100m\e[1;77m:: Authors:                                   ::\e[0m\n"
    printf "   \e[100m\e[1;77m::    - Meneghin Mattia                       ::\e[0m\n"
    printf "   \e[100m\e[1;77m::    - Muka Diamand                          ::\e[0m\n"
    printf "   \e[100m\e[1;77m::    - La Rosa Francesco                     ::\e[0m\n"
    printf "   \n"
}

installation(){
    apt-get update
    sleep 1
    apt install nodejs -y
    apt-get update
    sleep 1
    apt install npm -y
    apt-get update
    sleep 1
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.3/install.sh | bash
    sleep 1    
    source ~/.nvm/nvm
    sleep 1
    nvm install 20.9.0
    apt-get update
    sleep 1
    apt install apache2 -y
    printf "Set up \e[1;93mCompleted\e[0m\n"
    #Manca la parte di config apache
}

backend() {
    printf "Starting the \e[1;93mBack-End\e[0m service\n"
    cd Backend-SDN/ && npm start
    sleep 3
}

banner
installation
backend