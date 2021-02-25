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
from modules.chapter import Chapter             # Chapter operations
from typing import List

# constants
CHAPTER: str = None                 # Chapter folder
CHAPTER_METHODS: List[str] = []     # Method folder of the chapter
METHOD: str = None                  # Method folder
METHOD_PATH: str = None             # Method path to the executable python file
SERVER_PATH: str = os.getcwd()      # Server Path

# global modules

# https://stackoverflow.com/questions/301134/how-to-import-a-module-given-its-name-as-string
import importlib
spec = importlib.util.spec_from_file_location("method", os.path.join(SERVER_PATH, "modules", "interfaces", "method.py"))
method_interface_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(method_interface_module)

IMethod = method_interface_module.IMethod
setattr(__builtins__, 'IMethod', IMethod)

# Routes
@app.route('/', methods=['GET', 'POST'])
def homepage():
    """Route to render the homepage
    """
    return render_template('homepage/index.html')

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

    return render_template('chapter/index.html')

@app.route('/method', methods=['GET', 'POST'])
def method():    
    global METHOD
    global METHOD_PATH    
    global SERVER_PATH

    def load_module(module_name: str, path: str):
        # https://www.dev2qa.com/how-to-import-a-python-module-from-a-python-file-full-path/

        spec = importlib.util.spec_from_file_location(\
            module_name.replace(".py", ""), os.path.join(path, module_name))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        return module

    METHOD = request.form["method"]
    METHOD_PATH = os.path.join(os.sep.join(SERVER_PATH.split(os.sep)[:-1]), "methods", CHAPTER, METHOD)
    print(f'method path: {METHOD_PATH}')

    os.chdir(METHOD_PATH)                                                                # change to method path

    # load functions
    # set them builtin
    method_funcions_modules = load_module(module_name="modules.py", path=METHOD_PATH)
    for key in method_funcions_modules.__dict__:
        if not "__" in key:
            setattr(__builtins__, key, method_funcions_modules.__dict__[key])

    # load method
    method_module = load_module(module_name="main.py", path=METHOD_PATH)
    Method = method_module.Method                                                             # instantiate Method
    method = Method()                                                                  # create Method instance
    method.execute()                                                                   # execute Method
    
    os.chdir(SERVER_PATH)                                                                # change to server path

    return render_template('method/index.html')


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
    RESTful API for get the log og the executed model
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
        
api.add_resource(MethodList, '/methods')
api.add_resource(LogItem, '/log')

# Start server
if __name__ == '__main__':
    app.run('127.0.0.1', '5000', debug=True)  # important to mention debug=True