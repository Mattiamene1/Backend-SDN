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

    info( '*** Adding Switches\n' )
    sw1 = net.addSwitch( 'sw1' )
    sw2 = net.addSwitch( 'sw2' )
    #sw3 = net.addSwitch( 'sw3' )

    info( '*** Adding Pcs\n' )
    pc1 = net.addHost( 'PC1', ip="192.168.1.1/24")  #PC1 Network 1
    pc2 = net.addHost( 'PC2', ip="192.168.1.2/24")  #PC2 Network 1
    pc3 = net.addHost( 'PC3', ip="192.168.1.3/24")  #PC3 Network 1
    pc4 = net.addHost( 'PC4', ip="192.168.1.4/24")  #PC4 Network 1

    info( '*** Adding Cams\n' )
    cam1 = net.addHost( 'CAM1', ip="192.168.2.1/24")  #CAM1 Network 2
    cam2 = net.addHost( 'CAM2', ip="192.168.2.2/24")  #CAM2 Network 2
    cam3 = net.addHost( 'CAM3', ip="192.168.2.3/24")  #CAM3 Network 2
    cam4 = net.addHost( 'CAM4', ip="192.168.2.4/24")  #CAM4 Network 2

    #info( '*** Adding Printers\n' )
    #pr1 = net.addHost( 'PRINTER 1', ip="192.168.3.1/24")  #PRINTER 1 Network 3
    #pr2 = net.addHost( 'PRINTER 2', ip="192.168.3.2/24")  #PRINTER 2 Network 3
    #pr3 = net.addHost( 'PRINTER 3', ip="192.168.3.3/24")  #PRINTER 3 Network 3
    #pr4 = net.addHost( 'PRINTER 4', ip="192.168.3.4/24")  #PRINTER 4 Network 3

    info( '*** Adding Linux Router\n' )
    router = net.addHost( 'router', ip="192.168.1.254/24", cls=LinuxRouter)

    net.addLink( pc1, sw1) 
    net.addLink( pc2, sw1)
    net.addLink( pc3, sw1)
    net.addLink( pc4, sw1)

    net.addLink( cam1, sw2)
    net.addLink( cam2, sw2)
    net.addLink( cam3, sw2)  
    net.addLink( cam4, sw2)

    #net.addLink( pr1, sw3)
    #net.addLink( pr2, sw3)
    #net.addLink( pr3, sw3)  
    #net.addLink( pr4, sw3)

    #net.addLink( sw1, router, intfName1='sw1-eth5', intfName2='router-eth1',params2={'ip' : "192.168.1.254/24"} )
    net.addLink( sw1, router, intfName1='sw1-eth5', intfName2='router-eth1') 
    net.addLink( sw2, router, intfName1='sw2-eth5', intfName2='router-eth2', params2={'ip' : "192.168.2.254/24"} )
    #net.addLink( sw3, router, intfName1='sw3-eth5', intfName2='router-eth3', params2={'ip' : "192.168.3.254/24"} )
    
    net.configLinkStatus("sw1", "router", "down")
    net.configLinkStatus("sw2", "router", "down")
    #net.configLinkStatus("sw3", "router", "down")
    
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
