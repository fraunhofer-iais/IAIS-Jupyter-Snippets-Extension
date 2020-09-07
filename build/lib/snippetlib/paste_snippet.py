from IPython.display import display
from ipywidgets import widgets
import os 


class Paste_Snippet():

    def __init__(self):
        #dir = os.path.dirname(os.path.abspath(__file__))
        self.menu_KD = '/menu/KD-Snippets/'
        self.inputtext = widgets.Textarea()
        self.outputtext = widgets.Textarea(value=self.inputtext.value)
        self.code_name = widgets.Text(placeholder="Enter name without the '.py' ")
        self.directory = widgets.Text(placeholder="Optional",disabled=False)

        self.button = widgets.Button(
            description='Add to snippets',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Click me',
            icon='check'
        )

        self.add_directory_checkbox = widgets.Checkbox(
            value=False,
            description='Add Folder?',
            disabled=False
        )

        self.output = widgets.Output()

        self.c = widgets.HTML(
            value="Snippet Added <b>Successfully</b>",
        )
        inputtext = widgets.Textarea(placeholder="Paste/Type your code here")


        
        menu_KD = self.menu_KD
        inputtext = self.inputtext
        outputtext = self.outputtext
        code_name = self.code_name 
        directory = self.directory
        output = self.output
        button = self.button
        c = self.c 
        dir = os.path.dirname(os.path.abspath(__file__))
        def update_snippets(sender):
            if directory.value != "": 
                
                try:
                    os.chdir(dir+'/menu/KD-Snippets/')
                    os.mkdir(str.capitalize(directory.value))
                    with open(str.capitalize(directory.value)+"/"+str.capitalize(code_name.value)+".py","w") as t: 
                        t.write(inputtext.value)
                    os.chdir('..')
                    os.chdir('..')
                except FileExistsError:
                    os.chdir(dir+'/menu/KD-Snippets/'+str.capitalize(directory.value)+"/")
                    with open(str.capitalize(code_name.value)+".py","w") as t: 
                        t.write(inputtext.value)

            else:
                
                os.chdir(dir+"/menu/KD-Snippets/")
                with open(str.capitalize(code_name.value)+".py","w") as t: 
                    t.write(inputtext.value)
                os.chdir('..')
                os.chdir('..')
            button.button_style = 'success'
            display(c)

            with output:
                print("Snippet Added Successfully")



        button.on_click(update_snippets)

        display("Enter a Folder Name:",directory)
        display("Enter a Snippet Name (without .py):",code_name)
        display("Enter your Snippet here:",inputtext)
        display(button)



if __name__ == '__main__':
    e = Paste_Snippet()
   



