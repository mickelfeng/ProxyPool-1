from .mimvp.mimvp_proxy import mimvp_proxy
import threading


class SpiderMimvp(threading.Thread):
    def __init__(self):
        super(SpiderMimvp, self).__init__()

    def run(self):
        self.result = mimvp_proxy()
