"""Custom topology example

Two directly connected switches plus a host for each switch:

   host --- switch --- switch --- host
   h1   --- s1     --- s2     --- h2

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=twoswitch' from the command line.
"""

from mininet.topo import Topo

class twoswitch( Topo ):
    "Simple topology example."

    def build( self ):
        "Create custom topo."

        # Add hosts and switches
        leftHost = self.addHost( 'h1' )
        rightHost = self.addHost( 'h2' )
        leftSwitch = self.addSwitch( 's1' )
        rightSwitch = self.addSwitch( 's2' )

        # Add links
        self.addLink( leftHost, leftSwitch )
        self.addLink( leftSwitch, rightSwitch )
        self.addLink( rightSwitch, rightHost )


topos = { 
    'twostar': twoswitch
    }
