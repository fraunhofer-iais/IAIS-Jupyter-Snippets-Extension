from notebook.base.handlers import IPythonHandler
import json;
import os;
from os.path import expanduser;
import sys;

class MenuHandler(IPythonHandler):
    def get(self):
        self.finish(self.menu())

    @staticmethod
    def create(path):
        submenu=[]
        has_dirs = False
        for entry in sorted(os.scandir(path), key=lambda e: e.name):
            if entry.is_dir():
                if str(entry.name).startswith("__pycache__"):
                    pass
                else:
                    has_dirs = True

                    submenu.append({"name": str(entry.name), "sub-menu": MenuHandler.create(entry.path)})
        if has_dirs:
            submenu.append({"name":""})

        for entry in sorted(os.scandir(path), key=lambda e: e.name):
            if entry.is_file() and entry.name != "Base imports.py" and entry.name != "How to add your snippets.py":
            

                with open(entry.path,'rb') as f:
                    snippet = [line for line in f.read().splitlines()]
                    snippet = [line.decode('utf-8') for line in snippet]

                
                    
                    
                if str(entry.name).startswith("Documentation"):
                    submenu.insert(0, {"name":str(entry.name).replace('Documentation ', 'Doc '), "external-link":snippet})
                else:
                    if str(entry.name).endswith(".py"): 

                        submenu.append({"name":str(entry.name[:-3]), "snippet":snippet})
                    else: 
                        submenu.append({"name":str(entry.name), "snippet":snippet})

                if str(entry.name).startswith("__pycache__") or str(entry.name).startswith(" .ipynb_checkpoints") or str(entry.name).startswith("  "):
                    pass

        for entry in sorted(os.scandir(path), key=lambda e: e.name):
            if entry.is_file() and entry.name == "How to add your snippets.py":
            

                with open(entry.path,'rb') as f:
                    snippet = [line for line in f.read().splitlines()]
                    snippet = [line.decode('utf-8') for line in snippet]

                
                    
                    
                if str(entry.name).startswith("Documentation"):
                    submenu.insert(0, {"name":str(entry.name).replace('Documentation ', 'Doc '), "external-link":snippet})
                else:
                    if str(entry.name).endswith(".py"): 

                        submenu.append({"name":str(entry.name[:-3]), "snippet":snippet})
                    else: 
                        submenu.append({"name":str(entry.name), "snippet":snippet})

                if str(entry.name).startswith("__pycache__") or str(entry.name).startswith(" .ipynb_checkpoints") or str(entry.name).startswith("  "):
                    pass

                
        for entry in sorted(os.scandir(path), key=lambda e: e.name):
            if entry.is_file() and entry.name == "Base imports.py":
            

                with open(entry.path,'rb') as f:
                    snippet = [line for line in f.read().splitlines()]
                    snippet = [line.decode('utf-8') for line in snippet]

                
                    
                    
                if str(entry.name).startswith("Documentation"):
                    submenu.insert(0, {"name":str(entry.name).replace('Documentation ', 'Doc '), "external-link":snippet})
                else:
                    if str(entry.name).endswith(".py"): 

                        submenu.append({"name":str(entry.name[:-3]), "snippet":snippet})
                    else: 
                        submenu.append({"name":str(entry.name), "snippet":snippet})

                if str(entry.name).startswith("__pycache__") or str(entry.name).startswith(" .ipynb_checkpoints") or str(entry.name).startswith("  "):
                    pass

        

            
     

        return submenu

    @staticmethod
    def menu():
        
        #Return the directory name of pathname path 
        # Return a normalized absolutized version of the pathname path
        dir = os.path.dirname(os.path.abspath(__file__))
        return json.dumps(MenuHandler.create(dir + "/menu"))


