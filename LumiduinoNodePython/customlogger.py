import time

class CustomLogger(object):

    def __init__(self, file_path: str="", verbose: bool=True):
        self.logging_file = open(file_path+"/LumiduinoLog.log", 'w')
        self.verbose = verbose

    def write_log(self, log_msg):
        if self.verbose:
            print(log_msg)
        self.logging_file.write(log_msg+'\n')

    def log_task_start(self, task_name):
        message = "[TASK START] {} at time {}".format(task_name, time.time())
        self.write_log(message)

    def log_task_stop(self, task_name):
        message = "[TASK STOP] {} at time {}".format(task_name, time.time())
        self.write_log(message)

    def log_error(self, message, traceback):
        message = "[ERROR] message: {},\n Traceback: {} --- ".format(message, traceback, time.time())
        self.write_log(message)

    def log_warning(self, warning):
        message = "[WARNING] {} --- {}".format(warning, time.time())
        self.write_log(message)

    def log_activity(self, message):
        message = "[NOTIFICATION] {} --- {}".format(message, time.time())
        self.write_log(message)

    def close(self):
        print("closing")
        self.logging_file.close()