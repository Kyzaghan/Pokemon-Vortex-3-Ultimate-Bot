# -*- coding: utf-8 -*-
import logging
import time

from colorama import init, Fore, Style

from Util.Translation import translation

init()


class logger:
    def __init__(self):
        self.l = logging
        self.p = logging
        self.tl = translation()
        self.l.basicConfig(filename=time.strftime("%Y-%m-%d") + '.log', format='%(asctime)s %(message)s',
                           level=logging.DEBUG)
        self.p.basicConfig(filename=time.strftime("%Y-%m-%d") + 'catch.log', format='%(asctime)s %(message)s',
                           level=logging.INFO)

    def writelog(self, message, log_type="info", do_print=True):
        """
        Write log file
        :param message: Log Text
        :param log_type: Log type (info, critical, error, warning, success, catch)
        :param do_print: Print to screen
        """
        try:
            print(Style.RESET_ALL)
            message = "[" + time.strftime("%d-%m-%Y %H:%M %S") + "]" + message
            if log_type == "critical":
                self.l.critical(message)
                if do_print:
                    print(Fore.RED + Style.BRIGHT + message)
            elif log_type == "warning":
                self.l.warning(message)
                if do_print:
                    print(Fore.YELLOW + message)
            elif log_type == "error":
                self.l.error(message)
                if do_print:
                    print(Fore.RED + message)
            elif log_type == "info":
                self.l.info(message)
                if do_print:
                    print(Fore.WHITE + message)
            elif log_type == "success":
                self.l.info(message)
                if do_print:
                    print(Fore.GREEN + message)
            elif log_type == "catch":
                self.l.info(message)
                if do_print:
                    print(Fore.BLUE + message)
        except Exception as e:
            print(str(e))

    def write_pokemon(self, pokemon_name):
        """
        Write catched pokémon in the file
        :param pokemon_name: Just pokémon name :)
        """
        try:
            with open('catchList.log', 'a') as f:
                f.write("[" + time.strftime("%d-%m-%Y %H:%M %S") + "] " +
                        self.tl.get_language("Catcher", "pokemonCaught").format(pokemon_name) + "\n")
                f.close()
        except Exception as e:
            self.writelog(str(e), "critical")
