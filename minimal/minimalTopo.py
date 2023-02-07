from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info

class minimalTopo( Topo ):
    "Minimal topology with a single switch and two hosts"

    def build( self ):
        h1 = self.addHost( 'h1' )
        h2 = self.addHost( 'h2' )

        s1 = self.addSwitch( 's1' )

        self.addLink( s1,h1 )
        self.addLink( s1,h2 )

def runMinimalTopo():
    topo = minimalTopo()

    net = Mininet(
        topo=topo,
        controller=lambda name: RemoteController( name, ip='127.0.0.1' ),
        switch=OVSSwitch,
        autoSetMacs=True )

    net.start()
    net.pingAll()
    CLI( net )
    net.stop()

if __name__ == 'main':
    setLogLevel( 'info' )
    runMinimalTopo()

topos = {
    'minimal': minimalTopo
}