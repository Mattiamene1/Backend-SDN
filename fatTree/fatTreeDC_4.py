#!/usr/bin/python

"""
This example shows how to create a fat Tree DC network with k=4, where k is the number of the pods, starting from 0-3.
This schema uses 4 core switches from 1-4


CORE LAYER:                  r1                      r2                      r3                      r4
                            /   \                   /   \                   /   \                   /   \  
AGGREGATION LAYER:       r00     r01             r10     r11            r20      r21             r30     r31
                          |   X   |               |   X   |               |   X   |               |   X   |
EDGE LAYER:             sw00     sw01           sw10    sw11            sw20     sw21           sw30    sw31
                       /  |       |  \          / |       |  \ 
HOSTS:                h1  h2      h3  h4      h5  h6      h7  h8 
                     |__________________|    |__________________|
                            POD 0                    POD 1
"""

from ipaddress import ip_address
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.node import Node
from mininet.node import RemoteController
from mininet.log import setLogLevel, info
from mininet.cli import CLI
import time
from mininet.util import dumpNodeConnections

# Node implementing a linux router, source: https://github.com/mininet/mininet/blob/master/examples/linuxrouter.py
class LinuxRouter( Node ):
    "A Node with IP forwarding enabled."

    # pylint: disable=arguments-differ
    def config( self, **params ):
        super( LinuxRouter, self).config( **params )
        # Enable forwarding on the router
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( LinuxRouter, self ).terminate()

    def startRouting(self):
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )      #PC linux di fare da router
    
    def stopRouting(self):
        self.cmd( 'sysctl net.ipv4.ip_forward=0')


def defineNet():
    net = Mininet( controller=RemoteController, link=TCLink, switch=OVSKernelSwitch )
    
    info( '*** Adding controller\n' )
    c0 = net.addController('c0',controller=RemoteController,ip='127.0.0.1',port = 6633)

    ################# Core Routers ############################
    info( '*** Adding Core Routers\n' )
    r1 = net.addHost( 'r1') #, ip="10.4.1.1/24", cls=LinuxRouter)    #Router core 0
    #r2 = net.addHost( 'r2', ip="10.4.1.2/24", cls=LinuxRouter)    #Router core 1
    #r3 = net.addHost( 'r3', ip="10.4.1.3/24", cls=LinuxRouter)    #Router core 2
    #r4 = net.addHost( 'r4', ip="10.4.1.4/24", cls=LinuxRouter)    #Router core 3 

    ################# AGGREGATION SWITCHES #####################
    info( '*** Adding Aggregation Routers\n' )
    r00 = net.addHost( 'r00' ) #, ip="10.0.2.1/24", cls=LinuxRouter )      #Router Agg POD 0      
    r01 = net.addHost( 'r01' ) #, #ip="10.0.3.2/24", cls=LinuxRouter )      #Router Agg POD 0      

    ##r10 = net.addHost( 'r10', ip="10.1.2.1/24", cls=LinuxRouter )      #Router Agg POD 1      
    #r11 = net.addHost( 'r11', ip="10.1.3.2/24", cls=LinuxRouter )      #Router Agg POD 1      

    #r20 = net.addHost( 'r20', ip="10.2.2.1/24", cls=LinuxRouter )      #Router Agg POD 2      
    #r21 = net.addHost( 'r21', ip="10.2.3.2/24", cls=LinuxRouter )      #Router Agg POD 2      

    #r30 = net.addHost( 'r30', ip="10.3.2.1/24", cls=LinuxRouter )      #Router Agg POD 3      
    #r31 = net.addHost( 'r31', ip="10.3.3.2/24", cls=LinuxRouter )      #Router Agg POD 3      

    ####################### EDGE SWITCHES ######################
    info( '*** Adding Edge Switches\n' )
    sw00 = net.addSwitch( 'sw00')#, ip="10.0.0.1/24" )      #SW Edge POD 0     
    sw01 = net.addSwitch( 'sw01')#, ip="10.0.1.1/24" )      #SW Edge POD 0     

    #sw10 = net.addSwitch( 'sw10', ip="10.1.0.1/24" )      #SW Edge POD 1     
    #sw11 = net.addSwitch( 'sw11', ip="10.1.1.1/24" )      #SW Edge POD 1     

    #sw20 = net.addSwitch( 'sw20', ip="10.2.0.1/24" )      #SW Edge POD 2     
    #sw21 = net.addSwitch( 'sw21', ip="10.2.1.1/24" )      #SW Edge POD 2     

    #sw30 = net.addSwitch( 'sw30', ip="10.3.0.1/24" )      #SW Edge POD 3     
    #sw31 = net.addSwitch( 'sw31', ip="10.3.1.1/24" )      #SW Edge POD 3     


    ################# POD Hosts ############################
    info( '*** Adding Hosts in different PODs\n' )
    #( '*** Adding Hosts POD 0\n' )
    h1 = net.addHost( 'h1', ip="10.0.0.2/24", mac="00:00:00:00:00:01")  #Host 1 POD 0
    h2 = net.addHost( 'h2', ip="10.0.0.3/24", mac="00:00:00:00:00:02")  #Host 2 POD 0
    h3 = net.addHost( 'h3', ip="10.0.1.2/24", mac="00:00:00:00:00:03")  #Host 3 POD 0
    h4 = net.addHost( 'h4', ip="10.0.1.3/24", mac="00:00:00:00:00:04")  #Host 4 POD 0

    #( '*** Adding Hosts POD 1\n' )
    h5 = net.addHost( 'h7', ip="10.1.0.2/24", mac="00:00:00:00:00:05")  #Host 5 POD 1
    h6 = net.addHost( 'h6', ip="10.1.0.3/24", mac="00:00:00:00:00:06")  #Host 6 POD 1
    h7 = net.addHost( 'h7', ip="10.1.1.2/24", mac="00:00:00:00:00:07")  #Host 7 POD 1
    h8 = net.addHost( 'h8', ip="10.1.1.3/24", mac="00:00:00:00:00:08")  #Host 8 POD 1

    #( '*** Adding Hosts POD 2\n' )
    h9 = net.addHost( 'h9' , ip="10.2.0.2/24", mac="00:00:00:00:00:09")   #Host 9  POD 2
    h10 = net.addHost( 'h10', ip="10.2.0.3/24", mac="00:00:00:00:00:10")  #Host 10 POD 2
    h11 = net.addHost( 'h11', ip="10.2.1.2/24", mac="00:00:00:00:00:11")  #Host 11 POD 2
    h12 = net.addHost( 'h12', ip="10.2.1.3/24", mac="00:00:00:00:00:12")  #Host 12 POD 2

    #( '*** Adding Hosts POD 3\n' )
    h13 = net.addHost( 'h13', ip="10.3.0.2/24", mac="00:00:00:00:00:13")  #Host 13 POD 3
    h14 = net.addHost( 'h14', ip="10.3.0.3/24", mac="00:00:00:00:00:14")  #Host 14 POD 3
    h15 = net.addHost( 'h15', ip="10.3.1.2/24", mac="00:00:00:00:00:15")  #Host 15 POD 3
    h16 = net.addHost( 'h16', ip="10.3.1.3/24", mac="00:00:00:00:00:16")  #Host 16 POD 3

    ############################################################
    ############################################################
    net.addLink( r1, r00)
    net.addLink( r1, r01)
    ############################################################
    ############################################################
    ############# Linking Edge Sw to Agg Sw POD 0 ##############
    info( '*** Linking Edge Switches to Aggregate Switches\n' )
    net.addLink( r00, sw00) # |
    net.addLink( r00, sw01) # \
    net.addLink( r01, sw00) # /
    net.addLink( r01, sw01) # |

    net.addLink( sw00, h1)
    net.addLink( sw00, h2)
    net.addLink( sw01, h3)
    net.addLink( sw01, h4)

    net.build()
    c0.start()
    sw00.start( [c0] )
    sw01.start( [c0] )

    #### r00 agg Router #####
    r00.cmd("ifconfig r00-eth0 0")
    r00.cmd("ifconfig r00-eth1 0")
    r00.cmd("ifconfig r00-eth0 hw ether 00:00:00:00:01:01")
    r00.cmd("ifconfig r00-eth1 hw ether 00:00:00:00:01:02")
    r00.cmd("ip addr add 10.0.0.2/24 brd + dev r00-eth0") #h1
    r00.cmd("ip addr add 10.0.0.3/24 brd + dev r00-eth1") #h2
    r00.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")

    #### r01 agg Router #####
    r01.cmd("ifconfig r01-eth0 0")
    r01.cmd("ifconfig r01-eth1 0")
    r01.cmd("ifconfig r01-eth0 hw ether 00:00:00:02:01")
    r01.cmd("ifconfig r01-eth1 hw ether 00:00:00:02:02")
    r01.cmd("ip addr add 10.0.2.3/24 brd + dev r01-eth0") #h3
    r01.cmd("ip addr add 10.0.1.3/24 brd + dev r01-eth0") #h4
    r01.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")

    #### Hosts pod 0 ####
    h1.cmd("ip route add default via 10.0.0.1")
    h2.cmd("ip route add default via 10.0.0.1")
    h3.cmd("ip route add default via 10.0.1.1")
    h4.cmd("ip route add default via 10.0.1.1")

    sw00.cmd("ovs-ofctl add-flow sw00 priority=1,arp,actions=flood")
    sw00.cmd("ovs-ofctl add-flow sw00 priority=65535,ip,dl_dst=00:00:00:00:01:01,actions=output:1")
    sw00.cmd("ovs-ofctl add-flow sw00 priority=10,ip,nw_dst=10.0.0.2,actions=output:2")   #h1
    sw00.cmd("ovs-ofctl add-flow sw00 priority=10,ip,nw_dst=10.0.0.3,actions=output:3")   #h2

    sw01.cmd("ovs-ofctl add-flow sw01 priority=1,arp,actions=flood")
    sw01.cmd("ovs-ofctl add-flow sw01 priority=65535,ip,dl_dst=00:00:00:00:01:02,actions=output:1")
    sw01.cmd("ovs-ofctl add-flow sw01 priority=10,ip,nw_dst=10.0.1.2,actions=output:2")  #3
    sw01.cmd("ovs-ofctl add-flow sw01 priority=10,ip,nw_dst=10.0.1.3,actions=output:3")  #4




    ############# Linking Edge Sw to Agg Sw POD 1 ##############
    #net.addLink( sw1_0, sw1_2 ) # |
    #net.addLink( sw1_0, sw1_3 ) # /

    #net.addLink( sw1_1, sw1_2 ) # \
    #net.addLink( sw1_1, sw1_3 ) # |

    ############# Linking Edge Sw to Agg Sw POD 2 ##############
    #net.addLink( sw2_0, sw2_2 ) # |
    #net.addLink( sw2_0, sw2_3 ) # /

    #net.addLink( sw2_1, sw2_2 ) # \
    #net.addLink( sw2_1, sw2_3 ) # |

    ############# Linking Edge Sw to Agg Sw POD 3 ##############
    #net.addLink( sw3_0, sw3_2 ) # |
    #net.addLink( sw3_0, sw3_3 ) # /

    #net.addLink( sw3_1, sw3_2 ) # \
    #net.addLink( sw3_1, sw3_3 ) # |

    ############################################################
    ############################################################
    ################# Linking POD 0 ############################
    #info( '*** Linking hosts to Edge Switches\n' )
    #info( '*** Linking POD 0 Hosts h1,h2 to Edge Switch sw01\n' )
    #net.addLink( h1, sw0_0) 
    #net.addLink( h2, sw0_0)
    #info( '*** Linking POD 0 Hosts h3,h4 to Edge Switch sw0-1\n' )
    #net.addLink( h3, sw0_1)
    #net.addLink( h4, sw0_1)

    ################# Linking POD 1 ############################        ##Dopo aver corretto non pinga da h1 a h2
    #info( '*** Linking POD 1 Hosts h5,h6 to Edge Switch sw1-0\n' )
    #net.addLink( h5, sw1_0) 
    #net.addLink( h6, sw1_0)
    #info( '*** Linking POD 1 Hosts h7,h8 to Edge Switch sw1-1\n' )
    #net.addLink( h7, sw1_1)
    #net.addLink( h8, sw1_1)
    
    ################# Linking POD 2 ############################
    #info( '*** Linking POD 2 Hosts h9,h10 to Edge Switch sw2-0\n' )
    #net.addLink( h9, sw2_0) 
    #net.addLink( h10, sw2_0)
    #info( '*** Linking POD 2 Hosts h11,h12 to Edge Switch sw2-1\n' )
    #net.addLink( h11, sw2_1)
    #net.addLink( h12, sw2_1)

    ################# Linking POD 3 ############################
    #info( '*** Linking POD 3 Hosts h3,h14 to Edge Switch sw3-0\n' )
    #net.addLink( h13, sw3_0) 
    #net.addLink( h14, sw3_0)
    #info( '*** Linking POD 3 Hosts h15,h16 to Edge Switch sw3-1\n' )
    #net.addLink( h15, sw3_1)
    #net.addLink( h16, sw3_1)

    #c0.start()
    #h1.setDefaultRoute(intf='h1-eth0')
    #############################################################################################################
    
    info( '\n*** Starting network\n')
    net.start()

    info('\n*** Testing Network\n')
    net.pingAll()

    time.sleep(5)    

    CLI(net)
    net.stop() 


if __name__ == '__main__':
    setLogLevel( 'info' )
    defineNet()
