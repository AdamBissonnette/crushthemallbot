import louie
import threading
import time
import atexit

class Thread(threading.Thread):
    stopping = False
    kill_signal = "androidbot.killall"
    stop_signal = "androidbot.stop"
    timeout = 0.02

    def __init__(self):
        super().__init__()
        louie.connect(self.stop, signal=self.kill_signal)
        louie.connect(self.stop, signal=self.stop_signal)
        atexit.register(self.stop)

    def stop(self):
        self.stopping = True
        # print ("stopped {}".format(self))

    def run(self):
        while not self.stopping:
            self.do_action()
            time.sleep(self.timeout)
    
    def do_action(self):
        pass