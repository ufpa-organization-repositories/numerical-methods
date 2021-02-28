# flask
from flask import Flask, request, render_template
from flask_restful import Resource, Api

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app)


"""
HTTP Status                                                   
200 - Ok
201 - Created
404 - Error
"""

# modules
import os
from modules.utils import Utils
from modules.chapter import Chapter             # Chapter operations
from typing import List, Dict

# constants
CHAPTER: str = None                 # Chapter folder
CHAPTER_METHODS: List[str] = []     # Method folder of the chapter
METHOD: str = None                  # Method folder
METHOD_PATH: str = None             # Method path to the executable python file
METHOD_PARAMS: Dict = None          # Method parameters
SERVER_PATH: str = os.getcwd()      # Server Path

# objects
method: object = None
utils = Utils()

# global modules

# https://stackoverflow.com/questions/301134/how-to-import-a-module-given-its-name-as-string
import importlib
spec = importlib.util.spec_from_file_location("method", os.path.join(SERVER_PATH, "modules", "interfaces", "method.py"))
method_interface_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(method_interface_module)

# method_interface_module = utils.load_module("method", os.path.join(SERVER_PATH, "modules", "interfaces", "method.py"))
IMethod = method_interface_module.IMethod
setattr(__builtins__, 'IMethod', IMethod)

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
    global method

    METHOD = request.form["method"]
    METHOD_PATH = os.path.join(os.sep.join(SERVER_PATH.split(os.sep)[:-1]), "methods", CHAPTER, METHOD)    

    # load functions
    # set them builtin
    method_functions_module = utils.load_module(module_name="modules.py", path=METHOD_PATH)    
    for key in method_functions_module.__dict__:
        if not "__" in key:
            print(key, method_functions_module.__dict__[key])
            setattr(__builtins__, key, method_functions_module.__dict__[key])

    # load method module
    method_module = utils.load_module(module_name="main.py", path=METHOD_PATH)
    # load Method class from method module
    Method = method_module.Method
    # instantiate GLOBAL Method object
    method = Method()
    # get default method parameters
    METHOD_PARAMS = method.parameters    
    
    return render_template('parametrization.html')

@app.route('/method', methods=["GET", "POST"])
def method():
    global METHOD_PARAMS
    global method    

    # change to MMETHOD_PATH to export log in method folder
    os.chdir(METHOD_PATH)
    method.execute(request.form)    
    os.chdir(SERVER_PATH)

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
        print(METHOD_PATH)
        li_graphs: List = utils.get_images_from_directory(METHOD_PATH)

        print('di: ', li_graphs)
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