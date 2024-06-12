import signal
import sys
import time
from threading import Thread

def test_thread(txt):
    # try:
    #     # Main program code here
    #     while True:
    #         for _ in range(100):
    #             print(txt)
    #         time.sleep(1)

    # except (KeyboardInterrupt, SystemExit):
    #     print("Ctrl-C pressed!")
    #     sys.exit(0)

    # except Exception as e:
    #     print(e)
    while True:
        try:
            for _ in range(100):
                print(txt)
        except (KeyboardInterrupt, SystemExit):
            print('# Interrupted')
        except Exception as e:
            print(e)
        time.sleep(1)



def test_thread2(txt):
    # try:
    #     # Main program code here
    #     while True:
    #         for _ in range(100):
    #             print(txt)
    #         time.sleep(1)

    # except (KeyboardInterrupt, SystemExit):
    #     print("Ctrl-C pressed!")
    #     sys.exit(0)

    # except Exception as e:
    #     print(e)
    while True:
        try:
            for _ in range(100):
                print(txt)
        except (KeyboardInterrupt, SystemExit):
            print('# Interrupted')
        except Exception as e:
            print(e)
        time.sleep(1)




if __name__ == "__main__":

    try:
        T = []
        th1 = Thread(target=test_thread, args=('test',))
        th1.daemon = True
        th1.start()
        T.append(th1)

        th2 = Thread(target=test_thread2, args=('test2',))
        th2.daemon = True
        th2.start()
        T.append(th2)

        [t.join() for t in T] # wait for all threads to terminate

    except (KeyboardInterrupt, SystemExit):
        print('# Interrupted')
        sys.exit(0) 

        