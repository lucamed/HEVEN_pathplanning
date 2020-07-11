import inspect
import logging

class Authority:
    def __init__(self, name, get_permission, set_permission):
        self.name = name
        self.get_permission = get_permission
        self.set_permission = set_permission
    
    def GetterDecorator(self, func):
        def decorated(_self):
            frame, filename, line_number, function_name, lines, index = inspect.stack()[1]
            filename = filename.split('\\')[-1][:-3]
            logging.info(filename + " called " + self.name + " data.")
            if filename not in self.get_permission:
                logging.warning(filename + " has no permission to get " + self.name + " data.")
            return func(_self)
        return decorated

    def SetterDecorator(self, func):
        def decorated(_self, new_data):
            frame, filename, line_number, function_name, lines, index = inspect.stack()[1]
            filename = filename.split('\\')[-1][:-3]
            logging.info(filename + " changed " + self.name + " data.")
            if filename not in self.set_permission:
                logging.warning(filename + " has no permission to change " + self.name + " data.")
            func(_self, new_data)
        return decorated
