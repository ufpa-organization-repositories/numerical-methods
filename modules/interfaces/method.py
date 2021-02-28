import os
from typing import List, Dict
from abc import ABC, abstractmethod

class IMethod(ABC):
    """Method Interface"""
    
    def __init__(self, params):        
        self.parameters: Dict = {}
        for param in params:
            self.parameters[param] = 0
        self.log: Dict = {'log': []}

    def execute(self, request_form: Dict):
        print('execute: ', request_form, type(request_form))
        self.hook_show_information_method()
        self.get_parameters(request_form)
        self.hook_validate_parameters()
        self.set_params_to_log()
        self.run()
        self.export_graph()
        self.export_log()
        self.hook_export_table()
	
    def hook_show_information_method(self): pass        
    
    def get_parameters(self, request_form):
        for key in self.parameters.keys():
            value = request_form[key]
            # print(key, value)
            self.parameters[key] = float(value)        

    def hook_validate_parameters(self): pass

    def set_params_to_log(self):
        self.log['log'].append("PARAMETERS\n")
        for key, value in self.parameters.items():
            print(f'key:{key} value:{value}')
            self.log['log'].append(f">>> {key}: {value}\n")

    @abstractmethod
    def run(self): pass

    @abstractmethod
    def export_graph(self): pass
        
    def export_log(self):
        with open('log.txt', 'w') as f:
            for line in self.log['log']:
                f.write(line + '\n')
    
    def hook_export_table(self): pass
