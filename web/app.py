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
from modules.chapter import Chapter
from modules.method import Method
from typing import List

# constants
CHAPTER: str = None                 # Chapter folder
CHAPTER_METHODS: List[str] = []     # Method folder of the chapter
METHOD: str = None                  # Method folder

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
    global Method
    global METHOD

    METHOD = request.form["method"]
    print('method: ', METHOD)
    Method.execute(chapter_folder=CHAPTER, method_folder=METHOD)
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
        global CHAPTER
        global METHOD
        home_path: str = os.getcwd()        
        method_path: str = os.path.join(os.sep.join(os.getcwd().split(os.sep)[:-1]), "methods", CHAPTER, METHOD)        
        os.chdir(method_path)

        log_path: str = os.path.join(method_path, 'log.txt')
        log = None
        with open(log_path, 'r') as f:
            log = f.readlines()
        os.chdir(home_path)
        return {'log': log}, 200
        
api.add_resource(MethodList, '/methods')
api.add_resource(LogItem, '/log')

# Start server
if __name__ == '__main__':
    app.run('127.0.0.1', '5000', debug=True)  # important to mention debug=True