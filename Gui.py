import json
from ryu.base import app_manager
from ryu.app.wsgi import ControllerBase, WSGIApplication, route
from ryu.topology.api import get_switch, get_link, get_host
from webob import Response

class GUIServerApp(app_manager.RyuApp):
    _CONTEXTS = {'wsgi': WSGIApplication}

    def __init__(self, *args, **kwargs):
        super(GUIServerApp, self).__init__(*args, **kwargs)
        wsgi = kwargs['wsgi']
        wsgi.register(GUIServerController, {'data': self})

class GUIServerController(ControllerBase):
    def __init__(self, req, link, data, **config):
        super(GUIServerController, self).__init__(req, link, data, **config)

    @route('gui', '/gui', methods=['GET'])
    def get_gui(self, req, **kwargs):
        # Qui puoi generare il contenuto HTML per la GUI
        content = '<html><body><h1>Benvenuto nella GUI SDN</h1></body></html>'
        return Response(content_type='text/html', body=content)

    @route('topology', '/topology/switches', methods=['GET'])
    def get_topology_switches(self, req, **kwargs):
        switches = get_switch(self, None)
        switches_data = [{'dpid': str(switch.dp.id)} for switch in switches]
        return Response(content_type='application/json', body=json.dumps(switches_data))

    @route('topology', '/topology/links', methods=['GET'])
    def get_topology_links(self, req, **kwargs):
        links = get_link(self, None)
        links_data = [{'src': str(link.src.dpid), 'dst': str(link.dst.dpid)} for link in links]
        return Response(content_type='application/json', body=json.dumps(links_data))

    # Aggiungi altre route come necessario per ottenere informazioni su host, flow, ecc.
