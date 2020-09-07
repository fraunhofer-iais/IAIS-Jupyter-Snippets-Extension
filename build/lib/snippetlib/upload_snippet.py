from IPython.display import display
from ipywidgets import widgets
import os 


class Upload_Snippet():
    def __init__(self):
        self.menu_KD = '/menu/KD-Snippets/'
        self.uploader = widgets.FileUpload(accept='.py',multiple=True)
        self.upload_button = widgets.Button(
            description='upload snippet',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Click me',
            icon='check')

        dir = os.path.dirname(os.path.abspath(__file__))

        menu_KD = self.menu_KD
        uploader = self.uploader
        upload_button = self.upload_button



        upload_directory = widgets.Text(placeholder="Optional",disabled=False)
        c = widgets.HTML(
            value="Snippet Added <b>Successfully</b>",
        )
        def add(sender):

            [uploaded_file] = uploader.value

            name = list()
            for i in uploaded_file: 
                name.append(i)
            code_name = ''.join(name)



            if upload_directory.value != "": 
                try:
                    os.chdir(dir+'/menu/KD-Snippets/')
                    os.mkdir(str.capitalize(upload_directory.value))
                    with open(str.capitalize(upload_directory.value) +"/"+str.capitalize(code_name),"wb") as fp: 
                        fp.write(uploader.value[code_name]['content'])
                    os.chdir('..')
                    os.chdir('..')
                except FileExistsError:
                    os.chdir(dir+'/menu/KD-Snippets/'+str.capitalize(upload_directory.value)+"/")
                    with open(str.capitalize(code_name),"wb") as fp: 
                        fp.write(uploader.value[code_name]['content'])
                    os.chdir('..')
                    os.chdir('..')

            else:
                os.chdir(dir+'/menu/KD-Snippets/')
                with open(str.capitalize(code_name),"wb") as fp: 
                    fp.write(uploader.value[code_name]['content'])
                os.chdir('..')
                os.chdir('..')

            upload_button.button_style = 'success'
            upload_button.description='Uploaded'
            display(c)


        upload_button.on_click(add)

        display("Enter a Folder Name:",upload_directory)
        display(uploader,upload_button)


 

   

  
   



