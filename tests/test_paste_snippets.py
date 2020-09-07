from unittest import TestCase
import unittest
from IPython.utils.capture import capture_output
import ipywidgets
from ipywidgets.widgets.widget import Widget
from ipywidgets.widgets.widget_button import Button
from IPython.display import display
from IPython.core.interactiveshell import InteractiveShell
#CHECK THE IMPORTATION SOURCE
from snippetlib.paste_snippet import Paste_Snippet as ps
from snippetlib.menu import MenuHandler as mh

import os


FILE_UPLOAD_FRONTEND_CONTENT = {
    'name': 'file-name.py',
    'type': 'text/plain',
    'size': 20760,
    'last_modified': 12345,
    'content': b'hi',
}


class TestPasteSnippet(TestCase):


    def test_instantiation_of_InteractiveShell(self):
        ''' 
        Test if the interactive shell is instantiated
        '''
        s = InteractiveShell.instance()
        self.assertIsNotNone(s)


    def test_feature_activation(self):
        ''' 
        Test if the uploading snippets feature is activated 
        
        '''
        #ensure the Ipython shell is instantiated first
        #when us is called, all display functions are captured by capture output
        shell = InteractiveShell.instance()
        with capture_output() as cap:

            w = ps()
            self.assertIsNotNone(w)
            #check if length of cap.outputs == 4 or number of components you're using ..
            # 4 because : 'Enter a Folder Name:', text box, choose file button, and upload button
            self.assertEqual(len(cap.outputs),7,"not equal")
               

    def test_pasting(self):

        p=ps()
        button = p.button
        code = p.inputtext
        code_name = p.code_name 

        name = 'File-name'
        content = 'print("Hello world")'

        code_name.value = name 
        code.value = content

        button.click()
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        os.chdir('..')
        os.chdir('snippetlib/menu/KD-Snippets')
        
        menu = mh.menu()
        
          
        check_file_exists = name in menu

        self.assertEqual(check_file_exists,True)
        
        #os.chdir(os.path.dirname(os.path.abspath(__file__)))
        #os.remove('File.py')


if __name__ == '__main__':
    unittest.main()
