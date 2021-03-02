# flask
from flask import Flask, request, render_template
from flask_restful import Resource, Api

# modules
import os
import sys
from modules.utils import Utils
from modules.chapter import Chapter             # Chapter operations
from typing import List, Dict
import importlib

# constants
CHAPTER: str = None                 # Chapter folder
CHAPTER_METHODS: List[str] = []     # Method folder of the chapter
METHOD: str = None                  # Method folder
METHOD_PATH: str = None             # Method path to the executable python file
METHOD_PARAMS: Dict = None          # Method parameters
SERVER_PATH: str = os.getcwd()      # Server Path

# objects
method_obj: object = None
utils = Utils()

"""Create flask application"""

# Flask application
app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app)

"""
HTTP Status                                                   
200 - Ok
201 - Created
404 - Error
"""

# path to global modules
# leave IMethod class acessible by Method class wherever it is
sys.path.append(os.path.join(SERVER_PATH, "modules/interfaces/"))

# Routes
@app.route('/', methods=['GET', 'POST'])
def homepage():
    """Route to render the homepage
    """
    return render_template('homepage.html')

@app.route('/chapter', methods=['GET', 'POST'])
def chapter():
    global Chapter
    global CHAPTER
    global CHAPTER_METHODS
    """Route to render the choosen chapter
    01 --- introduction
    02 --- roots
    03 --- linear_systems
    04 --- interpolation
    05 --- integration"""
    
    CHAPTER = request.form["chapter"]
    CHAPTER_METHODS = Chapter.get_chapter_methods(CHAPTER)
    print('chapter methods:\n',CHAPTER_METHODS)

    return render_template('chapter.html')

@app.route('/parametrization', methods=['GET', 'POST'])
def parametrization():
    global CHAPTER    
    global METHOD
    global METHOD_PATH
    global METHOD_PARAMS
    global SERVER_PATH
    global method_obj

    METHOD = request.form["method"]
    METHOD_PATH = os.path.join(SERVER_PATH, "methods", CHAPTER, METHOD)    

    sys.path.append(METHOD_PATH)

    from method import Method # The Class to instantiate the method_obj

    method_obj = Method()
    METHOD_PARAMS = method_obj.parameters
    
    return render_template('parametrization.html')

@app.route('/method', methods=["GET", "POST"])
def method():
    global METHOD_PATH
    global SERVER_PATH
    global method_obj

    # change to MMETHOD_PATH to export log in method folder
    os.chdir(METHOD_PATH)
    method_obj.execute(request.form)
    os.chdir(SERVER_PATH)

    # remove the method path to the PATH SYSTEMS ENV
    sys.path.pop()

    return render_template('method.html')

# Apis
class MethodList(Resource):    
    """
    RESTful API for consulting/list the methods for the chapter that can be executed
    """

    def get(self):
        global CHAPTER_METHODS
        return CHAPTER_METHODS, 200

class LogItem(Resource):
    """
    RESTful API for get the log of the executed model
    """

    def get(self):
        global METHOD_PATH
        global SERVER_PATH

        os.chdir(METHOD_PATH)

        log_path: str = os.path.join(METHOD_PATH, 'log.txt')

        log = None
        with open(log_path, 'r') as f:
            log = f.readlines()

        os.chdir(SERVER_PATH)
        return {'log': log}, 200

class ParamsMethodItem(Resource):
    """
    RESTful API for get the parameters of the method which will be executed
    """

    def get(self):
        return METHOD_PARAMS, 200

class GraphList(Resource):
    """
    RESTful API for get the graphs of the method
    generated after its execution
    """
    global METHOD_PATH    
    def get(self):        
        li_graphs: List = utils.get_images_from_directory(METHOD_PATH)        
        di_graphs: Dict = {'graphs': []}
        for graph in li_graphs:
            di_graphs['graphs'].append(utils.serialize_image(os.path.join(METHOD_PATH, graph)))

        return di_graphs

api.add_resource(MethodList, '/methods')
api.add_resource(LogItem, '/log')
api.add_resource(ParamsMethodItem, '/parameters')
api.add_resource(GraphList, '/graphs')
        

# Start server

if __name__ == '__main__':    
    app.run('127.0.0.1', '5000', debug=True)  # important to mention debug=True