import pandas as pd
import matplotlib.pyplot as pl
from io import BytesIO
from IPython.display import display, HTML
import urllib, base64
import numpy as np
from unidecode import unidecode
import webbrowser
 
class Report():
    def __init__(self, filename):
        self.filename = filename
        self.items = []
        self.html = ""
        self.color_dict = {'h1_bg':'#a4c2db', 'h1':'#000000', 'tb_header_bg':'#b7cfe1', 'tb_header':'#000000', 'tb_rows':'#dbe7f0'}
        self.head = """
<head>
    <title>Report</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
    <style>
        table {
            border-collapse: collapse;
        }
 
        th, td {
            text-align: center;
            padding: 10px 15px 10px 15px;
            border: 0px;
        }
 
        tr:nth-child(even){background-color: %s}
 
        th {
            background-color: %s;
            color: %s;
        }
        pre {font: 15px arial, sans-serif;}
        p {padding-left: 20px; padding-right: 20px; font: 15px arial, sans-serif; align: center}
        .navbar {background-color: #2b506e; font: 15px arial, sans-serif}
        .navbar-default .navbar-nav > li > a:hover {background-color: #a4c2db}
        .navbar-default .navbar-nav > li > a {color: #ffffff}
 
        body {position: relative}
        h1 {padding:20px;background-color:%s;color:%s}
        h2 {padding:10px}
        h3 {padding:10px}
    </style>
</head>
"""%(self.color_dict['tb_rows'], self.color_dict['tb_header_bg'], self.color_dict['tb_header'], self.color_dict['h1_bg'], self.color_dict['h1'])
 
    def _generate_nav_bar(self):
        s = '''
<nav class="navbar navbar-default navbar-fixed-top">
  <div class="container-fluid">
    <div class="navbar-header">
        <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#myNavbar">
          <span class="icon-bar"></span>
          <span class="icon-bar"></span>
          <span class="icon-bar"></span>                       
      </button>
    </div>
    <div>
      <div class="collapse navbar-collapse" id="myNavbar">
        <ul class="nav navbar-nav">
'''
        for i in self.items:
            if i.startswith('<div id='):
                section_name = i[9:].split('" class')[0]
                s += '          <li><a href="#%s">%s</a></li>\n' %(section_name, section_name)
        s +='''
       </ul>
      </div>
    </div>
  </div>
</nav>   
'''
        return s
       
        
    def export(self):
        self.html = self.__flattenListOfStrings(self.items)
        report = open(self.filename, 'w')
        report.write("<html>" + self.head + '<body data-spy="scroll" data-target=".navbar" data-offset="50">' + self._generate_nav_bar() + self.html + "</body>\n</html>")
        report.close()
   
    def __flattenListOfStrings(self, l, itemNumbers=False):
        s = ""
        for nr, i in enumerate(l):
            if itemNumbers:
                s += '</br>ITEM NR ' + str(nr) + '</br>'
            s+=i
        return s
   
    def add_html(self, h, destinationId=None):
        self.items.append(h)
       
        if destinationId is not None:
            lastId = len(self.items)-1
            self.moveItem(oldId=lastId, newId=destinationId, show=False)
   
    def add_header(self, h, level=1, destinationId=None):
        if level == 1:
            s= '<div id="%s" class="container-fluid" style="width:10px;height:25px;"></div><h%i>%s</h%i>\n' %(str(h), level, str(h), level)
        else:
            s= '<h%i>%s</h%i>\n' %(level, str(h), level)
        self.items.append(s)
       
        if destinationId is not None:
            lastId = len(self.items)-1
            self.moveItem(oldId=lastId, newId=destinationId, show=False)
           
    def add_text(self, t, destinationId=None):
        #s= '<pre></br>' + unidecode(unicode(t, 'utf8')) + '</pre>'
        s= '<p></br>' + str(t) + '</p>'
        self.items.append(s)
        if destinationId is not None:
            lastId = len(self.items)-1
            self.moveItem(oldId=lastId, newId=destinationId, show=False)
               
    def add_image(self, fig, destinationId=None):
        imgdata = BytesIO()
        fig.savefig(imgdata, format='png')
        imgdata.seek(0)  # rewind the data
        im = '<p>\n</ br>\n<img src="data:image/png;base64,%s">\n</ br>\n</p>\n' %base64.b64encode(imgdata.getvalue()).decode('utf8')
        self.items.append(im)
        if destinationId is not None:
            lastId = len(self.items)-1
            self.moveItem(oldId=lastId, newId=destinationId, show=False)
   
    def add_table(self, t, collapse=False, float_digits=2, destinationId=None):
        if collapse:
            s= "</ br>\n<p>" + t.to_html(max_cols=10, max_rows=6, float_format=('{:,.%df}'%float_digits).format) + "</p></ br>\n"
            s= "</br>\nNum columns: %i </br>\nNum rows:    %i </ br>\n</ br>\n" %t.shape
        else:
            s= "</ br>\n<p>" + t.to_html(float_format=('{:,.%df}'%float_digits).format) + "</p></ br>\n"
       
        self.items.append(s)
        if destinationId is not None:
            lastId = len(self.items)-1
            self.moveItem(oldId=lastId, newId=destinationId, show=False)
   
    def show(self):
        self.export()
        webbrowser.open(self.filename, new=2)
