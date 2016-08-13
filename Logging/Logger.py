# -*- coding: utf-8 -*-
import logging, time


class logger:
    def __init__(self):
        self.l = logging
        self.l.basicConfig(filename=time.strftime("%Y-%m-%d") + '.log', format='%(asctime)s %(message)s',level=logging.DEBUG)

    def writelog(self, message, type):
        if type == "critical":
            self.l.critical(message)
        elif type == "warning":
            self.l.warning(message)
        elif type == "error":
            self.l.error(message)
        else:
            self.l.info(message)
        print(message)
