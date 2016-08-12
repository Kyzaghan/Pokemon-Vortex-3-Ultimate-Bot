import requests
from SettingParser.SettingsReader import read_authentication, read_config
from Logging.Logger import logger
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
        self.l = logger()
        self.active_pokemon = ""
        self.nojscheck = ""

    @property
    def do_login(self):
        try:
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
            self.select_battle()
            self.start_battle()
        except Exception as e:
         self.l.writelog(str(e), "critical")

    def select_battle(self):
        try:
            url = "http://" + self.a["Server"] + ".pokemon-vortex.com/battle_select.php?type=member"
            data = {"battle" : "Username", "buser" : self.c["BattleUser"], "submitb" : "Battle!"}
            r = self.s.post(url, data)
            self.l.writelog("Battle selected", "info")
            ph = BeautifulSoup(r.text, "html.parser")
            active_pokemon = ph.find('input', attrs={'name':'active_pokemon', 'type' : 'radio', 'checked' : 'checked'})

            if active_pokemon is None:
               self.l.writelog("None pokemon selected", "error")
            else:
               active_pokemon = active_pokemon["value"]

            self.l.writelog("Active pokemon : " + active_pokemon, "info")
            nojssolvea = ph.find('input', attrs={'id':'nojs-solve-a'})
            nojssolveb = ph.find('input', attrs={'id':'nojs-solve-b'})
            if(nojssolvea is not None and nojssolveb is not None) :
                self.l.writelog("no-js-solve-a : " + nojssolvea["value"], "info")
                self.l.writelog("no-js-solve-b : " + nojssolveb["value"], "info")
                nojscheck = int(nojssolvea["value"]) + int(nojssolveb["value"])
                self.l.writelog("no-js-check : " + str(nojscheck), "error")
            else:
                self.l.writelog("Js questions not found", "error")

            self.nojscheck = str(nojscheck)
            self.active_pokemon = str(active_pokemon)
        except Exception as e:
         self.l.writelog(str(e), "critical")

    def start_battle(self):
        try:
            url = "http://" + self.a["Server"] + ".pokemon-vortex.com/battle.php?&ajax=1"
            data = {"active_pokemon": self.active_pokemon, "action": "select_attack", "" : "", "" : "", "nojs-check": self.nojscheck}
            r = self.s.post(url, data)
            self.l.writelog("Battle started", "info")
            print(r.text)
            
        except Exception as e:
         self.l.writelog(str(e), "critical")

