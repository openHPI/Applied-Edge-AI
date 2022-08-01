"""
Created on Tue May 24 00:31:42 2022
Last edited on Jul 28 21:55:19 2022

@author: Mohamed Elhayany
@author: Ranji Raj
"""

import sys
from testbook import testbook
import ipywidgets as widgets
from IPython.display import display, Javascript, clear_output, display_javascript
from ipylab import JupyterFrontEnd
import glob
import os
from stat import S_IREAD, S_IRGRP, S_IROTH, S_IWUSR
import time



def getIPYNBName():
    
    names = glob.glob('./*.ipynb')
    if len(names) > 1:
        print('More than one (.ipynb) files detected! Please keep only one file for grading')
        sys.exit()
    else:
        return names[0]


def get_point(loc, task_number=1, cells = []):
    '''
    Checks and returns whether a task is passed(1) or failed(0)
    '''
    
    point=0.0
    try:
        with testbook(loc, execute=cells) as tb:
            if tb.cell_output_text(cells[-1]) == 'Test passed.':
                point+=1
                print(f"Task {task_number} Passed. \u2705")
    except Exception:
        print(f"Task {task_number} failed. \u274c")
        return point
    return point


def get_score(loc):
                                          
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
    
    
    return {"score": points_a + points_b + points_c + points_d}


def restartkernel():
    time.sleep(1.5)
    os._exit(00)
    
def save_data(textlist):
    user = os.getenv('JUPYTERHUB_USER')
    filename = f"/home/jovyan/.user_score/{user}.txt"
    if os.path.exists(filename):
        os.chmod(filename, S_IWUSR|S_IREAD)
    outF = open(filename, "w")
    for line in textlist:
      # write line to output file
      outF.write(line)
      outF.write("\n")
    os.chmod(filename, S_IREAD|S_IRGRP|S_IROTH)

    outF.close()
    



if __name__ == "__main__":
        
    # Checking if more than one notebook exist. If only one notebook exists, return the name of that notebook
    nbfile = getIPYNBName()
    
    print("*"*85)
    print("Note: Please make sure you entered the correct notebook name for a successful grading")
    print("*"*85)
    print(f"Notebook name recieved: {nbfile}")

    # Intends to save the notebook before auto-grading
    JupyterFrontEnd().commands.execute('docmanager:save') 
    
    ###########################
    ##### Scoring #############
    ###########################
    import time
    # get the start time
    st = time.time()
    
    user_score = get_score(nbfile)['score']
    
    # get the end time
    et = time.time()
    # get the execution time
    elapsed_time = et - st
 #   print('Execution time:', elapsed_time, 'seconds')

    print(f"Your score is: {user_score} / 4.0")
    print("*"*85)
    
#    print("Debug Info")
#    os.environ['NBPATH'] = nbfile
#    os.environ['NBSCORE'] = str(user_score/4)
    
    save_data(textlist=[nbfile, str(user_score/4)])
    
    # Submit button code
    link_view = widgets.Output()
    
    @link_view.capture(clear_output=True)
    def callback(url):
        display(Javascript(data=f'window.open("{url.tooltip}");'))
        restartkernel()

    button = widgets.Button(
        description = "Submit Assignment", 
        tooltip = 'https://jupyterhub.xopic.de/services/grading-service/', 
        button_style = 'success'
        )
    button.on_click(callback)
    display(button, link_view)
