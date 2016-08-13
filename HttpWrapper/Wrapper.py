# -*- coding: utf-8 -*-
import requests
from SettingParser.SettingsReader import read_authentication, read_config, read_map
from Logging.Logger import logger
import time
try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

class http_wrapper():
    """Http Class"""

    def __init__(self):
        self.s = requests.session()
        self.a = read_authentication()
        self.c = read_config()
        self.m = read_map()
        self.l = logger()

    @property
    def do_login(self):
        try:
            self.l.writelog("Logining. !", "info")
            url = "http://" + self.a["Server"] + ".pokemon-vortex.com/checklogin.php"
            data = {"myusername": self.a["Username"], "mypassword": self.a["Password"]}
            r = self.s.post(url, data)

            if "dashboard" in str(r.url) :
                self.l.writelog("Login success!", "info")
            else :
                self.l.writelog("Login unsuccess!", "error")
            return True
        except Exception as e:
            self.l.writelog(str(e), "critical")

    def start_bot(self):
        try:
            self.find_pokemon()
        except Exception as e:
         self.l.writelog(str(e), "critical")

    def find_pokemon(self):
        try:
            while(True):
                self.l.writelog("Pokemon searching...", "info")
                tmp_current_map = self.m["MapList"]['' + str(self.c["CurrentMap"]) + '']
                url = "http://" + self.a["Server"] + ".pokemon-vortex.com/xml/toolbox.php?map=" + str(
                    tmp_current_map["map"]) +"&move=" + str(tmp_current_map["move"]) +"&main="+str(tmp_current_map["move"])
                r = self.s.get(url)

                if("No wild Pok" in r.text) :
                    self.l.writelog("Pokémon not found, searching...", "info")
                else:
                    #Battle form id finding
                    form_id_start = r.text.index('name="')
                    form_id_end = r.text.index(' action')
                    form_id_start = form_id_start + 6
                    form_id_end = form_id_end - 1
                    form_id = r.text[form_id_start:form_id_end]

                    #Pokemon information finding
                    pokemon_start = r.text.index("Wild")
                    pokemon_end = r.text.index("appeared.") + 9
                    self.l.writelog(r.text[pokemon_start:pokemon_end], "info")
                    self.catch_pokemon(form_id)
                    break
        except Exception as e:
         self.do_login()
         self.l.writelog(str(e), "critical")

    def catch_pokemon(self, FormId):
        try:
            self.l.writelog("Entering the battle!", "info")
            url = "http://" + self.a["Server"] + ".pokemon-vortex.com/wildbattle.php"
            data = {"wildpoke" : "Battle", str(FormId) : "Battle!"}
            r = self.s.post(url, data)

            self.l.writelog("Entered battle!", "info")
            ph = BeautifulSoup(r.text, "html.parser")
            active_pokemon = ph.find('input', attrs={'name': 'active_pokemon', 'type': 'radio', 'checked': 'checked'})

            if active_pokemon is None:
                self.l.writelog("None pokemon selected", "error")
                self.find_pokemon()
            else:
                active_pokemon = active_pokemon["value"]


            self.l.writelog("Entering catch", "info")
            url = "http://" + self.a["Server"] + ".pokemon-vortex.com/wildbattle.php?&ajax=1"
            data = {"bat": "1", "action" : "1", "active_pokemon": str(active_pokemon), "action": "select_attack"}
            r = self.s.post(url, data)
            ph = BeautifulSoup(r.text, "html.parser")
            o1 = ph.find("input", attrs={"name":"o1"})
            o2 = ph.find("input", attrs={"name":"o2"})
            o3 = ph.find("input", attrs={"name":"o3"})
            o4 = ph.find("input", attrs={"name":"o4"})

            if(o1 is None or o2 is None or o3 is None or o4 is None):
                self.l.writelog("Pokémon attack list not found", "critical")
                self.find_pokemon()
            else:
                o1 = o1["value"]
                o2 = o2["value"]
                o3 = o3["value"]
                o4 = o4["value"]

            while(True) :
                self.l.writelog("Catch started", "info")
                url = "http://" + self.a["Server"] + ".pokemon-vortex.com/wildbattle.php?&ajax=1"
                data = {"o1" : o1, "o2" : o2, "o3" : o3, "o4" : o4, "actionattack" : "1", "actionattack" : "1", "bat" : "1", "item" : self.c["PokeBall"],
                        "action" : "use_item", "active_pokemon" : "1" }
                r = self.s.post(url, data)

                if("has been caught" in r.text) :
                    url = "http://" + self.a["Server"] + ".pokemon-vortex.com/wildbattle.php?&ajax=1"
                    data = {"action": "1", "bat": "1"}
                    r = self.s.post(url, data)
                    time.sleep(self.c["SleepSecondsAfterBattle"])
                    self.find_pokemon()
                    break
                else:
                    self.l.writelog("Catch not succcess, may be you not enough pokeball", "error")
                    url = "http://" + self.a["Server"] + ".pokemon-vortex.com/wildbattle.php?&ajax=1"
                    data = {"action": "1", "bat": "1"}
                    r = self.s.post(url, data)
        except Exception as e:
         self.l.writelog(str(e), "critical")
         self.find_pokemon()


