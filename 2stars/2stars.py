from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch, UserSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import Link, TCLink

def topology():

    net = Mininet( controller=RemoteController, link=TCLink, switch=OVSKernelSwitch )

    # Add hosts and switches
    h1 = net.addHost( 'h1', ip="10.0.1.2/24", mac="00:00:00:00:00:01" )
    h2 = net.addHost( 'h2', ip="10.0.1.3/24", mac="00:00:00:00:00:02" )
    h3 = net.addHost( 'h3', ip="10.0.2.2/24", mac="00:00:00:00:00:03" )
    h4 = net.addHost( 'h4', ip="10.0.2.3/24", mac="00:00:00:00:00:04" )

    r1 = net.addHost( 'r1') 

    s1 = net.addSwitch( 's1')
    s2 = net.addSwitch( 's2')

    c0 = net.addController( 'c0', controller=RemoteController, ip='127.0.0.1', port=6633 )

    net.addLink( r1, s1 )
    net.addLink( r1, s2 )
    
    net.addLink( h1, s1 )
    net.addLink( h2, s1 )
    net.addLink( h3, s2 )
    net.addLink( h4, s2 )

    net.build()
    c0.start()
    #s1.start( [c0] )
    #s2.start( [c0] )

    r1.cmd("ifconfig r1-eth0 0")
    r1.cmd("ifconfig r1-eth1 0")
    r1.cmd("ifconfig r1-eth0 hw ether 00:00:00:00:01:01")   #eth0
    r1.cmd("ifconfig r1-eth1 hw ether 00:00:00:00:01:02")   #eth1
    r1.cmd("ip addr add 10.0.1.1/24 brd + dev r1-eth0")
    r1.cmd("ip addr add 10.0.2.1/24 brd + dev r1-eth1")
    r1.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")

    h1.cmd("ip route add default via 10.0.1.1") #s1
    h2.cmd("ip route add default via 10.0.1.1") #s1
    h3.cmd("ip route add default via 10.0.2.1") #s2
    h4.cmd("ip route add default via 10.0.2.1") #s2

    s1.cmd("ovs-ofctl add-flow s1 priority=1,arp,actions=flood")
    s1.cmd("ovs-ofctl add-flow s1 priority=65535,ip,dl_dst=00:00:00:00:01:01,actions=output:1") #r1-eth0 s1 -> r1
    s1.cmd("ovs-ofctl add-flow s1 priority=10,ip,nw_dst=10.0.1.2,actions=output:2") #h1 -> s1
    s1.cmd("ovs-ofctl add-flow s1 priority=10,ip,nw_dst=10.0.1.3,actions=output:3") #h2 -> s1

    s2.cmd("ovs-ofctl add-flow s2 priority=1,arp,actions=flood")
    s2.cmd("ovs-ofctl add-flow s2 priority=65535,ip,dl_dst=00:00:00:00:01:02,actions=output:1") #r1-eth1 s2 -> r1
    s2.cmd("ovs-ofctl add-flow s2 priority=10,ip,nw_dst=10.0.2.2,actions=output:2") #h3 -> s2
    s2.cmd("ovs-ofctl add-flow s2 priority=10,ip,nw_dst=10.0.2.3,actions=output:3") #h4 -> s2

    info( '\n*** Starting network\n')
    net.start()

    info('\n*** Testing Network\n')
    net.pingAll()

    CLI(net)
    net.stop() 

if __name__ == '__main__':
    setLogLevel( 'info' )
    topology()  