# -*- coding: utf-8 -*-
from Util.Logger import logger
from Util.SettingsReader import read_config, read_authentication
from Util.Translation import translation

try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup


class Inventory:
    def __init__(self, session):
        self.c = read_config()

        #Poké Balls
        self.Pokeball = 0
        self.GreatBall = 0
        self.UltraBall = 0
        self.MasterBall = 0

        #Potions
        self.Potion = 0
        self.SuperPotion = 0
        self.HyperPotion = 0
        self.FullHeal = 0

        #Required class
        self.l = logger()
        self.s = session
        self.tl = translation()
        self.a = read_authentication()

    def get_inventory(self):
        """
        Print inventory
        :rtype: object
        """
        try:
            self.l.writelog(self.tl.get_language("Catcher", "gettingInventory"), "info")
            url = "http://" + self.a["Server"] + ".pokemon-vortex.com/inventory.php"
            r = self.s.do_request(url)
            self.get_balls(r.text)
            self.l.writelog(self.tl.get_language("Catcher", "gettingInventorySuccess"), "success")
            self.print_current_inventory()
        except Exception as e:
            self.l.writelog(str(e), "critical")
            return None

    def get_balls(self, response):
        """
        Gettings pokéballs
        :param response: Inventory response text (html)
        :return: None
        """
        try:
            ph = BeautifulSoup(response, "html.parser")
            pokeball_div = ph.find_all('div', attrs={"class": "list autowidth"})
            ph = BeautifulSoup(str(pokeball_div[1]), "html.parser")
            ph = BeautifulSoup(str(ph.find_all("tr")), "html.parser")
            i = 0
            for tdList in ph.find_all("td"):
                if i == 3:  # Pokeball
                    self.Pokeball = int(tdList.text)
                elif i == 10:  # Great Ball
                    self.GreatBall = int(tdList.text)
                elif i == 17:  # Ultra Ball
                    self.UltraBall = int(tdList.text)
                elif i == 24:  # Master Ball
                    self.MasterBall = int(tdList.text)
                i += 1
        except Exception as e:
            self.l.writelog(str(e), "critical")
            return None

    def print_current_inventory(self):
        """
        Print inventory
        """
        print("Poké ball={0}\nGreat Ball={1}\nUltra Ball={2}\nMaster Ball={3}".format(self.Pokeball, self.GreatBall,
                                                                                      self.UltraBall, self.MasterBall))

    @property
    def get_current_ball_count(self):
        """
        Get current pokéball count from class
        :return: Current Pokéball Count
        """
        if self.c["Catcher"]["PokeBall"] == "Poke Ball":
            return self.Pokeball
        elif self.c["Catcher"]["PokeBall"] == "Great Ball":
            return self.GreatBall
        elif self.c["Catcher"]["PokeBall"] == "Ultra Ball":
            return self.UltraBall
        else:
            return self.MasterBall

    def remove_current_ball(self, islegend):
        """
        Remove current pokéball count -1
        :param islegend: If pokéball legend set this, remove Master Ball
        :rtype: object
        """
        if islegend:
            self.MasterBall -= 1
        else:
            if self.c["Catcher"]["PokeBall"] == "Poke Ball":
                self.Pokeball -= 1
            elif self.c["Catcher"]["PokeBall"] == "Great Ball":
                self.GreatBall -= 1
            elif self.c["Catcher"]["PokeBall"] == "Ultra Ball":
                self.UltraBall -= 1
            else:
                self.MasterBall -= 1

    def get_ball_buy_count(self, poke_type):
        """
        Get pokéball buy count
        :param type: Pokéball type
        :return: Count
        :rtype: object
        """
        try:
            if poke_type == "Poke Ball" and int(self.c["Catcher"]["PokeBallBuyList"]["" + poke_type + ""]) > 0:
                poke_ball_diff = int(self.c["Catcher"]["PokeBallBuyList"]["" + poke_type + ""]) - self.Pokeball
            elif poke_type == "Great Ball" and int(self.c["Catcher"]["PokeBallBuyList"]["" + poke_type + ""]) > 0:
                poke_ball_diff = int(self.c["Catcher"]["PokeBallBuyList"]["" + poke_type + ""]) - self.GreatBall
            elif poke_type == "Ultra Ball" and int(self.c["Catcher"]["PokeBallBuyList"]["" + poke_type + ""]) > 0:
                poke_ball_diff = int(self.c["Catcher"]["PokeBallBuyList"]["" + poke_type + ""]) - self.UltraBall
            elif poke_type == "Master Ball" and int(self.c["Catcher"]["PokeBallBuyList"]["" + poke_type + ""]) > 0:
                poke_ball_diff = int(self.c["Catcher"]["PokeBallBuyList"]["" + poke_type + ""]) - self.MasterBall
            else:
                poke_ball_diff = 0
            if poke_ball_diff <= 0:
                return 0
            else:
                if poke_ball_diff >= 100 or poke_ball_diff > 50:
                    return 100
                elif 25 < poke_ball_diff <= 50:
                    return 50 * 2
                elif 10 < poke_ball_diff <= 25:
                    return 25 * 2
                elif 5 < poke_ball_diff <= 10:
                    return 10 * 2
                else:
                    return 5 * 2
        except Exception as e:
            self.l.writelog(str(e), "critical")

    def purchase_pokeball(self):
        try:
            self.l.writelog(self.tl.get_language("Catcher", "buyingPokeBalls"), "info")
            url = "http://" + self.a["Server"] + ".pokemon-vortex.com/items.php"
            data = {"potion": 0,
                    "superpotion": 0,
                    "hyperpotion": 0,
                    "pokeball": self.get_ball_buy_count("Poke Ball"),
                    "greatball": self.get_ball_buy_count("Great Ball"),
                    "ultraball": self.get_ball_buy_count("Ultra Ball"),
                    "masterball": self.get_ball_buy_count("Master Ball"),
                    "fullheal": 0,
                    "antidote": 0,
                    "parlyzheal": 0,
                    "burnheal": 0,
                    "iceheal": 0,
                    "awakening": 0,
                    "dawnstone": 0,
                    "duskstone": 0,
                    "firestone": 0,
                    "leafstone": 0,
                    "moonstone": 0,
                    "ovalstone": 0,
                    "shinystone": 0,
                    "sunstone": 0,
                    "thunderstone": 0,
                    "waterstone": 0,
                    "deepseascale": 0,
                    "deepseatooth": 0,
                    "dragonscale": 0,
                    "dubiousdisc": 0,
                    "electirizer": 0,
                    "magmarizer": 0,
                    "kingsrock": 0,
                    "metalcoat": 0,
                    "prismscale": 0,
                    "protector": 0,
                    "razorclaw": 0,
                    "razorfang": 0,
                    "reapercloth": 0,
                    "upgrade": 0,
                    "sachet": 0,
                    "whippeddream": 0,
                    "icerock": 0,
                    "mossrock": 0,
                    "abomasite": 0,
                    "absolite": 0,
                    "aerodactylite": 0,
                    "aggronite": 0,
                    "alakazite": 0,
                    "altarianite": 0,
                    "ampharosite": 0,
                    "audinite": 0,
                    "banettite": 0,
                    "beedrillite": 0,
                    "blastoisinite": 0,
                    "blazikenite": 0,
                    "cameruptite": 0,
                    "charizarditex": 0,
                    "charizarditey": 0,
                    "diancite": 0,
                    "galladite": 0,
                    "garchompite": 0,
                    "gardevoirite": 0,
                    "gengarite": 0,
                    "glalitite": 0,
                    "gyaradosite": 0,
                    "heracronite": 0,
                    "houndoominite": 0,
                    "kangaskhanite": 0,
                    "lopunnite": 0,
                    "lucarionite": 0,
                    "manectite": 0,
                    "mawilite": 0,
                    "medichamite": 0,
                    "metagrossite": 0,
                    "mewtwonitex": 0,
                    "mewtwonitey": 0,
                    "pidgeotite": 0,
                    "pinsirite": 0,
                    "sablenite": 0,
                    "salamencite": 0,
                    "sceptilite": 0,
                    "scizorite": 0,
                    "sharpedonite": 0,
                    "slowbronite": 0,
                    "steelixite": 0,
                    "swampertite": 0,
                    "tyranitarite": 0,
                    "venusaurite": 0,
                    "buy": "Buy Items"
                    }
            self.s.do_request(url, "post", data)
            self.l.writelog(self.tl.get_language("Catcher", "pokeballsbuyed"), "info")
            self.get_inventory()
        except Exception as e:
            self.l.writelog(str(e), "critical")
            return None


class Trainer:
    def __init__(self, session):
        self.s = session
        self.inventory = Inventory(session)
