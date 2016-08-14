# -*- coding: utf-8 -*-
import logging
import time
from Util.termcolor import cprint

class logger:
    def __init__(self):
        self.l = logging
        self.l.basicConfig(filename=time.strftime("%Y-%m-%d") + '.log', format='%(asctime)s %(message)s',level=logging.DEBUG)

    def writelog(self, message, type):
        message = "[" + time.strftime("%d-%m-%Y %H:%M %S") + "]" + message
        if type == "critical":
            cprint(message, 'red', attrs=['bold'])
            self.l.critical(message)
        elif type == "warning":
            cprint(message, 'cyan')
            self.l.warning(message)
        elif type == "error":
            cprint(message, 'red')
            self.l.error(message)
        else:
            self.l.info(message)
            if type == "catched" :
                cprint(message, "green", attrs=['bold', 'dark'])
            elif(type == "green") :
                cprint(message, "green")
            else :
                cprint(message)

