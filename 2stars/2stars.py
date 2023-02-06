#!/usr/bin/python

"""
This example shows how to create an empty Mininet object
(without a topology object) and add nodes to it manually.
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

    info( '*** Adding Linux Router\n' )
    router = net.addHost( 'router', ip="192.168.1.254/24", cls=LinuxRouter)

    info( '*** Adding Switches\n' )
    sw1 = net.addSwitch( 'sw1' )
    sw2 = net.addSwitch( 'sw2' )

    info( '*** Adding Pcs\n' )
    h1 = net.addHost( 'h1', ip="192.168.1.1/24")  #h1
    h2 = net.addHost( 'h2', ip="192.168.1.2/24")  #h2
    h3 = net.addHost( 'h3', ip="192.168.1.3/24")  #h3
    h4 = net.addHost( 'h4', ip="192.168.1.4/24")  #h4

    info( '*** Adding Cams\n' )
    h5 = net.addHost( 'h5', ip="192.168.2.1/24")  #h5
    h6 = net.addHost( 'h6', ip="192.168.2.2/24")  #h6
    h7 = net.addHost( 'h7', ip="192.168.2.3/24")  #h7
    h8 = net.addHost( 'h8', ip="192.168.2.4/24")  #h8

    net.addLink( h1, sw1) 
    net.addLink( h2, sw1)
    net.addLink( h3, sw1)
    net.addLink( h4, sw1)

    net.addLink( h5, sw2)
    net.addLink( h6, sw2)
    net.addLink( h7, sw2)  
    net.addLink( h8, sw2)

    net.addLink( sw1, router, intfName1='sw1-eth5', intfName2='router-eth1') 
    net.addLink( sw2, router, intfName1='sw2-eth5', intfName2='router-eth2', params2={'ip' : "192.168.2.254/24"} )
    
    net.configLinkStatus("sw1", "router", "down")
    net.configLinkStatus("sw2", "router", "down")
    
    
    info( '*** Starting network\n')
    net.start()


    info('\n*** Testing Network\n')
    net.pingAll()

    info('\n*** Topology Morphing\n')    

    net.configLinkStatus("sw1", "router", "up")
    net.configLinkStatus("sw2", "router", "up")


    router.cmd("wireshark -i router-eth1 --display-filter icmp -k &")
    router.cmd("wireshark -i router-eth2 --display-filter icmp -k &")

    time.sleep(8)
    
    info( '*** Changing hosts default routes...\n')

    h1.cmd("ip route add default via 192.168.1.254")
    h2.cmd("ip route add default via 192.168.1.254")
    h3.cmd("ip route add default via 192.168.1.254")
    h4.cmd("ip route add default via 192.168.1.254")

    h5.cmd("ip route add default via 192.168.2.254")
    h6.cmd("ip route add default via 192.168.2.254")
    h7.cmd("ip route add default via 192.168.2.254")
    h8.cmd("ip route add default via 192.168.2.254")

    router.cmd("ip route add 192.168.1.0 via 192.168.1.254")
    router.cmd("ip route add 192.168.2.0 via 192.168.2.254")

    net.build()
    c0.start()

    info('\n*** Testing Network #2\n')
    net.pingAll()

    CLI(net)
    net.stop() 


if __name__ == '__main__':
    setLogLevel( 'info' )
    defineNet()
