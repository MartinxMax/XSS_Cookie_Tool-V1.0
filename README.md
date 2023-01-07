# XSS steals cookies
* The current version v3.0 is simpler and faster
* Obtain the victim's Internet IP address
* Python version 3.6 or above
* Automatically steal cookies
* Compatible with Windows or Linux
## usage method
  * View help information

      ```#python3 XSS_Tool_V3.0.py -h```

  ![图片名称](./Demo_image/Help.png "Help")  

  * LAN attack

      ```#python3 XSS_Tool_V3.0.py -lp (Local port)```

  * Internet attack

      ```#python3 XSS_Tool_V3.0.py -t -lp (Local port) -rh (Remote host IP) -rp (Remote host port)```

## Effect demonstration 
 * We will use WordPress-6.1.1 for XSS attack simulation test
 * _If your machine has a public IP address, just listen to the local port_

# Use Extranet attack
* Enable port forwarding (Ngrok is used for demonstration)

    ![图片名称](./Demo_image/forwarding.png "Port forwarding")  


* Use Extranet attack

    ```#python3 XSS_Tool_V3.0.py -t -lp 8080 -rh ***.***.***.*** -rp 10029```

    ![图片名称](./Demo_image/Internet.png "Extranetattack")  


# Use Intranet attack [Now Test]
-----------------Hacker--------------------------
* You can use the - lp parameter to specify the port. If you do not write, the default port is 8888

```#python3 XSS_Tool_V3.0.py```

![图片名称](./Demo_image/Runing.png "Run")  

* Copy payload and inject XXS injection point

![图片名称](./Demo_image/Hacking.png "Run")  

----------------Server Admin------------------------

* Normal status of administrator

![图片名称](./Demo_image/Admin_no_hack.png "Admin_no_hack")  

* The administrator was hacked to execute malicious code when viewing comments

![图片名称](./Demo_image/Admin_hacked2.png "Admin_hacked2")  

-----------------Hacker--------------------------
* Hacker gets the administrator's cookie

![图片名称](./Demo_image/Hack_Get_Cookie.png "Hack_Get_Cookie")