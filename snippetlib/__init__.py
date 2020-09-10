from notebook.utils import url_path_join
from snippetlib.menu import MenuHandler
import os 

def _jupyter_server_extension_paths():
    return [{
        "module": "snippetlib",
    }]

def _jupyter_nbextension_paths():
    return [dict(
        section="notebook",
        src="nbextension",
        dest="snippetlib",
        require="snippetlib/index"
    )]

def load_jupyter_server_extension(nb_app):
    web_app = nb_app.web_app
    host_pattern = '.*$'
    route_pattern = url_path_join(web_app.settings['base_url'], '/menu')
    web_app.add_handlers(host_pattern, [(route_pattern, MenuHandler)])
    
