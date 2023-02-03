#!/usr/bin/python

"""
This example shows how to create a fat Tree DC network with k=4, where k is the number of the pods, starting from 0-3.
This schema uses 4 core switches from 1-4


CORE LAYER:                  sw1                     sw2                     sw3                     sw4
                            /   \                   /   \                   /   \                   /   \  
AGGREGATION LAYER:      sw0-2   sw0-3           sw1-2   sw1-3           sw2-2   sw2-3           sw3-2   sw3-3
                          |   X   |               |   X   |               |   X   |               |   X   |
EDGE LAYER:             sw0-0   sw0-1           sw1-0   sw1-1           sw2-0   sw2-1           sw3-0   sw3-1
                       /  |       |  \          / |       |  \ 
HOSTS:                h1  h2      h3  h4      h5  h6      h7  h8 
                     |__________________|    |__________________|
                            POD 0                    POD 1
"""

from ipaddress import ip_address
from mininet.topo import Topo
from mininet.net import Mininet
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
    net = Mininet( controller = RemoteController, waitConnected=True  )

    info( '*** Adding controller\n' )
    c0 = net.addController( 'c0' )

    ################# Core Switches ############################
    info( '*** Adding Core Switches\n' )
    sw1 = net.addSwitch( 'sw1' )      #SW Core 0    IP: 10.4.1.1
    sw2 = net.addSwitch( 'sw2' )      #SW Core 1    IP: 10.4.1.2
    sw3 = net.addSwitch( 'sw3' )      #SW Core 2    IP: 10.4.1.3
    sw4 = net.addSwitch( 'sw4' )      #SW Core 3    IP: 10.4.1.4

    ################# AGGREGATION SWITCHES #####################
    info( '*** Adding Aggregation Switches\n' )
    sw0_2 = net.addSwitch( 'sw0_2' )      #SW Agg POD 0      ip="10.0.2.1"
    sw0_3 = net.addSwitch( 'sw0_3' )      #SW Agg POD 0      ip="10.0.3.2"

    sw1_2 = net.addSwitch( 'sw1_2' )      #SW Agg POD 1      ip="10.1.2.1"
    sw1_3 = net.addSwitch( 'sw1_3' )      #SW Agg POD 1      ip="10.1.3.2"

    sw2_2 = net.addSwitch( 'sw2_2' )      #SW Agg POD 2      ip="10.2.2.1"
    sw2_3 = net.addSwitch( 'sw2_3' )      #SW Agg POD 2      ip="10.2.3.2"

    sw3_2 = net.addSwitch( 'sw3_2' )      #SW Agg POD 3      ip="10.3.2.1"
    sw3_3 = net.addSwitch( 'sw3_3' )      #SW Agg POD 3      ip="10.3.3.2"

    ####################### EDGE SWITCHES ######################
    info( '*** Adding Edge Switches\n' )
    sw0_0 = net.addSwitch( 'sw0_0' )      #SW Edge POD 0     ip="10.0.0.1"
    sw0_1 = net.addSwitch( 'sw0_1' )      #SW Edge POD 0     ip="10.0.1.1"

    sw1_0 = net.addSwitch( 'sw1_0' )      #SW Edge POD 1     ip="10.1.0.1"
    sw1_1 = net.addSwitch( 'sw1_1' )      #SW Edge POD 1     IP="10.1.1.1"

    sw2_0 = net.addSwitch( 'sw2_0' )      #SW Edge POD 2     ip="10.2.0.1"
    sw2_1 = net.addSwitch( 'sw2_1' )      #SW Edge POD 2     ip="10.2.1.1"

    sw3_0 = net.addSwitch( 'sw3_0' )      #SW Edge POD 3     ip="10.3.0.1"
    sw3_1 = net.addSwitch( 'sw3_1' )      #SW Edge POD 3     ip="10.3.1.1"


    ################# POD Hosts ############################
    info( '*** Adding Hosts POD 0\n' )
    h1 = net.addHost( 'h1', ip="10.0.0.2/24")  #Host 1 POD 0
    h2 = net.addHost( 'h2', ip="10.0.0.3/24")  #Host 2 POD 0
    h3 = net.addHost( 'h3', ip="10.0.1.2/24")  #Host 3 POD 0
    h4 = net.addHost( 'h4', ip="10.0.1.3/24")  #Host 4 POD 0

    info( '*** Adding Hosts POD 1\n' )
    h5 = net.addHost( 'h7', ip="10.1.0.2/24")  #Host 5 POD 1
    h6 = net.addHost( 'h6', ip="10.1.0.3/24")  #Host 6 POD 1
    h7 = net.addHost( 'h7', ip="10.1.1.2/24")  #Host 7 POD 1
    h8 = net.addHost( 'h8', ip="10.1.1.3/24")  #Host 8 POD 1

    info( '*** Adding Hosts POD 2\n' )
    h9 = net.addHost( 'h9' , ip="10.2.0.2/24")   #Host 9  POD 2
    h10 = net.addHost( 'h10', ip="10.2.0.3/24")  #Host 10 POD 2
    h11 = net.addHost( 'h11', ip="10.2.1.2/24")  #Host 11 POD 2
    h12 = net.addHost( 'h12', ip="10.2.1.3/24")  #Host 12 POD 2

    info( '*** Adding Hosts POD 3\n' )
    h13 = net.addHost( 'h13', ip="10.3.0.2/24")  #Host 13 POD 3
    h14 = net.addHost( 'h14', ip="10.3.0.3/24")  #Host 14 POD 3
    h15 = net.addHost( 'h15', ip="10.3.1.2/24")  #Host 15 POD 3
    h16 = net.addHost( 'h16', ip="10.3.1.3/24")  #Host 16 POD 3

    ################# Linking POD 0 ############################
    info( '*** Linking POD 0 Hosts h1,h2 to Edge Switch sw0-0\n' )
    net.addLink( h1, sw0_0) 
    net.addLink( h2, sw0_0)
    info( '*** Linking POD 0 Hosts h3,h4 to Edge Switch sw0-1\n' )
    net.addLink( h3, sw0_1)
    net.addLink( h4, sw0_1)

    ################# Linking POD 1 ############################
    info( '*** Linking POD 1 Hosts h5,h6 to Edge Switch sw1-0\n' )
    net.addLink( h5, sw0_0) 
    net.addLink( h6, sw0_0)
    info( '*** Linking POD 1 Hosts h7,h8 to Edge Switch sw1-1\n' )
    net.addLink( h7, sw0_1)
    net.addLink( h8, sw0_1)
    
    ################# Linking POD 2 ############################
    info( '*** Linking POD 2 Hosts h9,h10 to Edge Switch sw2-0\n' )
    net.addLink( h9, sw2_0) 
    net.addLink( h10, sw2_0)
    info( '*** Linking POD 2 Hosts h11,h12 to Edge Switch sw2-1\n' )
    net.addLink( h11, sw2_1)
    net.addLink( h12, sw2_1)

    ################# Linking POD 3 ############################
    info( '*** Linking POD 3 Hosts h3,h14 to Edge Switch sw3-0\n' )
    net.addLink( h13, sw3_0) 
    net.addLink( h14, sw3_0)
    info( '*** Linking POD 3 Hosts h15,h16 to Edge Switch sw3-1\n' )
    net.addLink( h15, sw3_1)
    net.addLink( h16, sw3_1)

    ############# Linking Edge Sw to Agg Sw POD 0 ##############
    info( '*** Linking POD 0 Edge Sw to Agg Sw\n' )
    net.addLink( sw0_0, sw0_2 ) # |
    net.addLink( sw0_0, sw0_3 ) # /

    net.addLink( sw0_1, sw0_2 ) # \
    net.addLink( sw0_1, sw0_3 ) # |

    ############# Linking Edge Sw to Agg Sw POD 1 ##############
    info( '*** Linking POD 1 Edge Sw to Agg Sw\n' )
    net.addLink( sw1_0, sw1_2 ) # |
    net.addLink( sw1_0, sw1_3 ) # /

    net.addLink( sw1_1, sw1_2 ) # \
    net.addLink( sw1_1, sw1_3 ) # |

    ############# Linking Edge Sw to Agg Sw POD 2 ##############
    info( '*** Linking POD 2 Edge Sw to Agg Sw\n' )
    net.addLink( sw2_0, sw2_2 ) # |
    net.addLink( sw2_0, sw2_3 ) # /

    net.addLink( sw2_1, sw2_2 ) # \
    net.addLink( sw2_1, sw2_3 ) # |

    ############# Linking Edge Sw to Agg Sw POD 3 ##############
    info( '*** Linking POD 3 Edge Sw to Agg Sw\n' )
    net.addLink( sw3_0, sw3_2 ) # |
    net.addLink( sw3_0, sw3_3 ) # /

    net.addLink( sw3_1, sw3_2 ) # \
    net.addLink( sw3_1, sw3_3 ) # |

    ############# Linking Agg Sw to Core Sw POD 0 ##############
    info( '*** Linking POD 0 Agg Sw to Core Sw\n' )
    net.addLink( sw0_2, sw1 ) # Core 1
    net.addLink( sw0_2, sw2 ) # Core 2

    net.addLink( sw0_3, sw3 ) # Core 3
    net.addLink( sw0_3, sw4 ) # Core 4

    ############# Linking Agg Sw to Core Sw POD 1 ##############
    info( '*** Linking POD 1 Agg Sw to Core Sw\n' )
    net.addLink( sw1_2, sw1 ) # Core 1
    net.addLink( sw1_2, sw2 ) # Core 2

    net.addLink( sw1_3, sw3 ) # Core 3
    net.addLink( sw1_3, sw4 ) # Core 4

    ############# Linking Agg Sw to Core Sw POD 2 ##############
    info( '*** Linking POD 1 Agg Sw to Core Sw\n' )
    net.addLink( sw2_2, sw1 ) # Core 1
    net.addLink( sw2_2, sw2 ) # Core 2

    net.addLink( sw2_3, sw3 ) # Core 3
    net.addLink( sw2_3, sw4 ) # Core 4

    ############# Linking Agg Sw to Core Sw POD 3 ##############
    info( '*** Linking POD 3 Agg Sw to Core Sw\n' )
    net.addLink( sw3_2, sw1 ) # Core 1
    net.addLink( sw3_2, sw2 ) # Core 2

    net.addLink( sw3_3, sw3 ) # Core 3
    net.addLink( sw3_3, sw4 ) # Core 4

    #############################################################################################################
    
    info( '*** Starting network\n')
    net.start()


    info('\n*** Testing Network\n')
    net.pingAll()

    info('\n*** Topology Morphing\n')    

    net.configLinkStatus("sw1", "router", "up")
    net.configLinkStatus("sw2", "router", "up")
    #net.configLinkStatus("sw3", "router", "up")


    router.cmd("wireshark -i router-eth1 --display-filter icmp -k &")
    router.cmd("wireshark -i router-eth2 --display-filter icmp -k &")
    router.cmd("wireshark -i router-eth3 --display-filter icmp -k &")

    time.sleep(8)
    
    info( '*** Changing hosts default routes...\n')

    pc1.cmd("ip route add default via 192.168.1.254")
    pc2.cmd("ip route add default via 192.168.1.254")
    pc3.cmd("ip route add default via 192.168.1.254")
    pc4.cmd("ip route add default via 192.168.1.254")

    cam1.cmd("ip route add default via 192.168.2.254")
    cam2.cmd("ip route add default via 192.168.2.254")
    cam3.cmd("ip route add default via 192.168.2.254")
    cam4.cmd("ip route add default via 192.168.2.254")

    #pr1.cmd("ip route add default via 192.168.3.254")
    #pr2.cmd("ip route add default via 192.168.3.254")
    #pr3.cmd("ip route add default via 192.168.3.254")
    #pr4.cmd("ip route add default via 192.168.3.254")

    router.cmd("ip route add 192.168.1.0 via 192.168.1.254")
    router.cmd("ip route add 192.168.2.0 via 192.168.2.254")
    #router.cmd("ip route add 192.168.2.0 via 192.168.3.254")

    info('\n*** Testing Network #2\n')
    net.pingAll()

    CLI(net)
    net.stop() 


if __name__ == '__main__':
    setLogLevel( 'info' )
    defineNet()
