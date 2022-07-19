"""
Created on Tue May 24 00:31:42 2022
Last edited on Jul 13 12:00:33 2022

@author: Mohamed Elhayany
@author: Ranji Raj
"""

import sys
from testbook import testbook
import ipywidgets as widgets
from IPython.display import display, Javascript, clear_output, display_javascript
from ipylab import JupyterFrontEnd
import glob


names = glob.glob('./*.ipynb')

def getIPYNBCount():
    if len(names) > 1:
        print('Two or more (.ipynb) files detected! Please keep only one file for grading')
        sys.exit()

getIPYNBCount()

nbfile = names[0]

def get_point(loc, task_number=1, cells = []):
    '''
    Checks and returns whether a task is passed(1) or failed(0)
    '''
    
    point=0.0
    try:
        with testbook(loc, execute=cells) as tb1:
            if tb1.cell_output_text(cells[-1]) == 'Test passed.':
                point+=1
                print(f"Task {task_number} Passed. \u2705")
    except Exception:
        print(f"Task {task_number} failed. \u274c")
        return point
    return point


def get_score(loc = nbfile):
                                          
    for i in range(1):                                  
        print("\n")
    
    print("Testing your solution for Task 1: SGD")
    points_a = get_point(loc, task_number=1, cells = [1,3,5,7])

    print("*"*60)
    print("Testing your solution for Task 2: Fully Connected Layer")
    points_b = get_point(loc, task_number=2, cells = [1,3,9,11,13])

    print("*"*60)
    print("Testing your solution for Task 3: Mean Squared Error")
    points_c = get_point(loc, task_number=3, cells = [1,3,11,15,17])

    print("*"*60)
    print("Testing your solution for Task 4: ReLU (Rectified Linear Unit)")
    points_d = get_point(loc, task_number=4, cells = [1,3,19,21])
    
    pts = {"score": (points_a + points_b + points_c + points_d)/4}
    print(pts['score'])
    return {"score": points_a + points_b + points_c + points_d}


print("*"*85)
print("Note: Please make sure you entered the correct notebook name for a successful grading")
print("*"*85)
print(f"Notebook name recieved: {nbfile}")
loc = nbfile

if __name__ == "__main__":
    print(f"Your score is: {get_score(loc)['score']} / 4.0")


    link_view = widgets.Output()
    params = widgets.Output()

    @params.capture(clear_output=True)
    def params(_):
        app = JupyterFrontEnd()
        app.commands.execute('docmanager:save')
        clear_output()
        print(names[0])
        #print('score')

    @link_view.capture(clear_output=True)
    def callback(url):
        display(Javascript(f'window.open("{url.tooltip}");'))

    button = widgets.Button(
        description = "Submit to openHPI", 
        tooltip = 'https://jupyterhub.xopic.de/services/grading-service/', 
        button_style = 'success'
    )
    button.on_click(callback)
    display(button, link_view)
