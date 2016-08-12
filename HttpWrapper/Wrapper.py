import requests
from SettingParser.SettingsReader import read_authentication
from Logging.Logger import logger

class http_wrapper():
    """Http Class"""

    def __init__(self):
        self.s = requests.session()
        self.c = read_authentication()
        self.l = logger()

    def do_login(self):
        try:
            url = "http://" + self.c["Server"] + ".pokemon-vortex.com/checklogin.php"
            data = {"myusername": self.c["Username"], "mypassword": self.c["Password"]}
            r = self.s.post(url, data)

            if "dashboard" in str(r.url) :
                self.l.writelog("Login success!", "info")
            else :
                self.l.writelog("Login unsuccess!", "error")

        except Exception as e:
            self.l.writelog(str(e), "critical")

