import warnings 
import importlib

with open("requirements.txt","r") as f:
    dependencies = [line for line in f.read().splitlines()]

dependencies = ['ipywidgets',
'notebook']

print(dependencies)

for i in dependencies:
    
    
    try:
        importlib.import_module(i)
    except ImportError:
        print("for"+x)
        warnings.warn("The module {} needs to be installed".format(i))