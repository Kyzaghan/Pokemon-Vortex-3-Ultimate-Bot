from Bot.PVBot import http_wrapper

hw = http_wrapper()
if(hw.do_login) :
    hw.start_bot()

