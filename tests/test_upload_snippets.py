from unittest import TestCase
import unittest
from IPython.utils.capture import capture_output
import ipywidgets
from ipywidgets.widgets.widget import Widget
from ipywidgets.widgets import FileUpload
from ipywidgets.widgets.widget_button import Button
from IPython.display import display
from IPython.core.interactiveshell import InteractiveShell
#CHECK THE IMPORTATION SOURCE
from snippetlib.upload_snippet import Upload_Snippet as us
from snippetlib.menu import MenuHandler as mh
import os


FILE_UPLOAD_FRONTEND_CONTENT = {
    'name': 'file-name.py',
    'type': 'text/plain',
    'size': 20760,
    'last_modified': 12345,
    'content': b'hi',
}


class TestUploadSnippet(TestCase):


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

            w = us()
            self.assertIsNotNone(w)
            #check if length of cap.outputs == 4 or number of components you're using ..
            # 4 because : 'Enter a Folder Name:', text box, choose file button, and upload button
            self.assertEqual(len(cap.outputs),4,"not equal")
               

    def test_uploading(self):

        '''
        Test if file is uploaded by Upload_Snippet and moved to a snippets testing directory
        '''

        w = us()
        uploader = w.uploader

        #simulate uploading a file is successful and without any change 
        msg = {FILE_UPLOAD_FRONTEND_CONTENT['name']:{'metadata':{'name':FILE_UPLOAD_FRONTEND_CONTENT['name'],'type':FILE_UPLOAD_FRONTEND_CONTENT['type'],'size':FILE_UPLOAD_FRONTEND_CONTENT['size'],'last_modified':FILE_UPLOAD_FRONTEND_CONTENT['last_modified']},'content':FILE_UPLOAD_FRONTEND_CONTENT['content']}}
        uploader.set_trait('value',msg)

        traits = uploader.value 
        upload_button = w.upload_button
        upload_button.click()

        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        os.chdir('..')
        print(os.getcwd())
        #os.chdir('snippetlib/menu/My-Snippets')
        
        menu = mh.menu()
        print(menu)
        
          
        check_file_exists = 'File-name' in menu

        self.assertEqual(check_file_exists,True)

        #dir = os.path.dirname(os.path.abspath(__file__))
        #os.chdir('..')
        #os.chdir('snippetlib/menu/KD-Snippets/') 
        #check_file_exists = os.path.exists(str.capitalize(FILE_UPLOAD_FRONTEND_CONTENT['name']))


        # test if the file is successfully uploaded
        #self.assertEqual(len(uploader.value),1)
        #self.assertEqual(check_file_exists,True)
        #os.remove(str.capitalize(FILE_UPLOAD_FRONTEND_CONTENT['name']))




if __name__ == '__main__':
    unittest.main()