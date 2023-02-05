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

from mininet.net import Mininet
from mininet.node import Node
from mininet.node import RemoteController, OVSKernelSwitch, UserSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import Link, TCLink

from ipaddress import ip_address
import time
from mininet.topo import Topo
from mininet.node import CPULimitedHost
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
    
    info( '*** Adding Hosts ***\n' )
    h1 = net.addHost( 'h1', ip="10.0.0.2/24", mac="00:00:00:00:00:01")  #Host 1 POD 0
    h2 = net.addHost( 'h2', ip="10.0.0.3/24", mac="00:00:00:00:00:02")  #Host 2 POD 0
    h3 = net.addHost( 'h3', ip="10.0.1.2/24", mac="00:00:00:00:00:03")  #Host 3 POD 0
    h4 = net.addHost( 'h4', ip="10.0.1.3/24", mac="00:00:00:00:00:04")  #Host 4 POD 0

    ################# Core Routers ############################
    #info( '*** Adding Core Routers\n' )
    #r1 = net.addHost( 'r1') #, ip="10.4.1.1/24", cls=LinuxRouter)    #Router core 0
    #r2 = net.addHost( 'r2', ip="10.4.1.2/24", cls=LinuxRouter)    #Router core 1
    #r3 = net.addHost( 'r3', ip="10.4.1.3/24", cls=LinuxRouter)    #Router core 2
    #r4 = net.addHost( 'r4', ip="10.4.1.4/24", cls=LinuxRouter)    #Router core 3 

    ################# AGGREGATION SWITCHES #####################
    info( '*** Adding Aggregation Routers ***\n' )
    r00 = net.addHost( 'r00' )      
    r01 = net.addHost( 'r01' )      

    ##r10 = net.addHost( 'r10', ip="10.1.2.1/24", cls=LinuxRouter )      #Router Agg POD 1      
    #r11 = net.addHost( 'r11', ip="10.1.3.2/24", cls=LinuxRouter )      #Router Agg POD 1      

    #r20 = net.addHost( 'r20', ip="10.2.2.1/24", cls=LinuxRouter )      #Router Agg POD 2      
    #r21 = net.addHost( 'r21', ip="10.2.3.2/24", cls=LinuxRouter )      #Router Agg POD 2      

    #r30 = net.addHost( 'r30', ip="10.3.2.1/24", cls=LinuxRouter )      #Router Agg POD 3      
    #r31 = net.addHost( 'r31', ip="10.3.3.2/24", cls=LinuxRouter )      #Router Agg POD 3      

    ####################### EDGE SWITCHES ######################
    info( '*** Adding Edge Switches ***\n' )
    sw00 = net.addSwitch( 'sw00')#, ip="10.0.0.1/24" )      #SW Edge POD 0     
    sw01 = net.addSwitch( 'sw01')#, ip="10.0.1.1/24" )      #SW Edge POD 0     

    #sw10 = net.addSwitch( 'sw10', ip="10.1.0.1/24" )      #SW Edge POD 1     
    #sw11 = net.addSwitch( 'sw11', ip="10.1.1.1/24" )      #SW Edge POD 1     

    #sw20 = net.addSwitch( 'sw20', ip="10.2.0.1/24" )      #SW Edge POD 2     
    #sw21 = net.addSwitch( 'sw21', ip="10.2.1.1/24" )      #SW Edge POD 2     

    #sw30 = net.addSwitch( 'sw30', ip="10.3.0.1/24" )      #SW Edge POD 3     
    #sw31 = net.addSwitch( 'sw31', ip="10.3.1.1/24" )      #SW Edge POD 3     

    info( '*** Adding controller ***\n' )
    c0 = net.addController('c0',controller=RemoteController,ip='127.0.0.1',port = 6633)


    ############# Linking Edge Sw to Agg Sw POD 0 ##############
    info( '*** Linking Edge Switches to Aggregate Switches\n' )
    net.addLink( r00, sw00) # |
    net.addLink( r00, sw01) # \
    #net.addLink( r01, sw00) # /
    #net.addLink( r01, sw01) # |

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
    r00.cmd("ip addr add 10.0.0.1/24 brd + dev r00-eth0") #sw00 subnet 0
    r00.cmd("ip addr add 10.0.1.1/24 brd + dev r00-eth1") #sw01 subnet 1
    r00.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")

    #### r01 agg Router #####
    r01.cmd("ifconfig r01-eth0 0")
    r01.cmd("ifconfig r01-eth1 0")
    r01.cmd("ifconfig r01-eth0 hw ether 00:00:00:02:01")
    r01.cmd("ifconfig r01-eth1 hw ether 00:00:00:02:02")
    r01.cmd("ip addr add 10.0.0.1/24 brd + dev r01-eth0") #sw00 subnet 00
    r01.cmd("ip addr add 10.0.1.1/24 brd + dev r01-eth0") #sw01 subnet 01
    r01.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")

    #### Hosts pod 0 ####
    h1.cmd("ip route add default via 10.0.0.1")
    h2.cmd("ip route add default via 10.0.0.1")
    h3.cmd("ip route add default via 10.0.1.1")
    h4.cmd("ip route add default via 10.0.1.1")

    sw00.cmd("ovs-ofctl add-flow sw00 priority=1,arp,actions=flood")
    sw00.cmd("ovs-ofctl add-flow sw00 priority=65535,ip,dl_dst=00:00:00:00:01:01,actions=output:1") #r00-eth0
    sw00.cmd("ovs-ofctl add-flow sw00 priority=65535,ip,dl_dst=00:00:00:00:02:01,actions=output:1") #r01-eth0
    sw00.cmd("ovs-ofctl add-flow sw00 priority=10,ip,nw_dst=10.0.0.2,actions=output:2")   #h1
    sw00.cmd("ovs-ofctl add-flow sw00 priority=10,ip,nw_dst=10.0.0.3,actions=output:3")   #h2

    sw01.cmd("ovs-ofctl add-flow sw01 priority=1,arp,actions=flood")
    sw01.cmd("ovs-ofctl add-flow sw01 priority=65535,ip,dl_dst=00:00:00:00:01:02,actions=output:1") # r00-eth1
    sw01.cmd("ovs-ofctl add-flow sw01 priority=65535,ip,dl_dst=00:00:00:00:02:02,actions=output:1") # r01-eth1
    sw01.cmd("ovs-ofctl add-flow sw01 priority=10,ip,nw_dst=10.0.1.2,actions=output:2")  #h3
    sw01.cmd("ovs-ofctl add-flow sw01 priority=10,ip,nw_dst=10.0.1.3,actions=output:3")  #h4


    
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
