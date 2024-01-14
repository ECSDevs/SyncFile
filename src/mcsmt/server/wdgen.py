# code from https://www.geeksforgeeks.org/create-a-watchdog-in-python-to-look-for-filesystem-changes/

# import time module, Observer, FileSystemEventHandler
from time import sleep
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from .gen import do_job as generate

class OnMyWatch:
    # Set the directory on watch
    def __init__(self,watchdir,configFile):
        self.observer = Observer()
        self.watchingDirectory = watchdir
        self.configFile = configFile
    def run(self):
        event_handler = Handler(self.configFile)
        self.observer.schedule(event_handler, self.watchingDirectory, recursive = True)
        self.observer.start()
        try:
            while True:
                sleep(5)
        except:
            self.observer.stop()
            print("Observer Stopped")
        self.observer.join()

class Handler(FileSystemEventHandler):
    def __init__(self,configFile,**args):
        super().__init__(**args)
        self.configFile = configFile
    def on_any_event(self,event):
        if event.is_directory:
            return None
        print("WatchDog FileSystemEventHandler found a event. regenerating client.json.")
        generate(self.configFile)

def do_job(watchdir="res",config_file="config.json"):
    global gConfigFile
    watch = OnMyWatch(watchdir,config_file)
    watch.run()

if __name__ == "__main__":
    from sys import argv
    argv = argv[1::]
    kwargv  = {}
    for a in argv:
        if ":" in a:
            x = a.split(":")
            kwargv[x[0]]=':'.join(x[1::])
            argv.remove(a)
    do_job(*argv, **kwargv)