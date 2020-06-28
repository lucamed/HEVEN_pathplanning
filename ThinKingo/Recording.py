import threading
import time

class Recording:
    def __init__(self, db):
        self.db = db
        self.flag = db.flag
        self.__recording_thread = threading.Thread(target=self.__main)

    def __main(self):

        f = open("C:\\Users\\HEVEN\\Documents\\GitHub\\HEVEN-AutonomousCar-2019\\DB-Team\\Real-World\\Database\\gps_park_test.txt", 'w')
        time.sleep(2)

        while not self.flag.system_stop:
            p_curr = self.db.gps.data
            print(p_curr)
            data = str(p_curr) + '\n'
            f.write(data)
            time.sleep(1)

        f.close()
        
    def start(self):
        print("Starting Recording thread...")
        self.__recording_thread.start()
        time.sleep(1)
        print("Recording thread start!")

    def join(self):
        print("Terminating Recording thread...")
        self.__recording_thread.join()
        time.sleep(0.1)
        print("Recording termination complete!")
