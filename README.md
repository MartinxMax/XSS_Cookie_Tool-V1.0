# XSS steals cookies
* The current version is 1.0 and will be updated continuously
* Python version 3.6 or above
* Automatically steal cookies
* Compatible with Windows or Linux
## usage method
  * View help information

      ```#python3 XSS.py -h```

  ![图片名称](https://github.com/MartinxMax/XSS_Cookie_Tool-V1.0/blob/master/%C2%96%C2%96Demo_image/Command.png "Help")  

  * LAN attack

      ```#python3 XSS.py -lp (Local port)```

  * Internet attack

      ```#python3 XSS.py -t -lp (Local port) -rh (Remote host IP) -rp (Remote host port)```

## Effect demonstration 
 * Here, XSS will be demonstrated in the local DVWA shooting range, and cookies will be stolen through the internet

_If your machine has a public IP address, just listen to the local port_

* Enable port forwarding (Ngrok is used for demonstration)

    ![图片名称](https://github.com/MartinxMax/XSS_Cookie_Tool-V1.0/blob/master/%C2%96%C2%96Demo_image/TCP.png "Port forwarding")  

* Use Internet attack

    ```#python3 XSS.py -t -lp 8080 -rh ***.***.***.*** -rp 10029```

    ![图片名称](https://github.com/MartinxMax/XSS_Cookie_Tool-V1.0/blob/master/%C2%96%C2%96Demo_image/PAYLOAD.png "PAYLOAD")  
Copy PAYLOAD

* Attempt to inject statement
   ![图片名称](https://github.com/MartinxMax/XSS_Cookie_Tool-V1.0/blob/master/%C2%96%C2%96Demo_image/ADMIN.png "Cookie")  
* Administrator visits malicious page
  The administrator is redirected to the specified page

  ![图片名称](https://github.com/MartinxMax/XSS_Cookie_Tool-V1.0/blob/master/%C2%96%C2%96Demo_image/redirect.png "page")  
    
* Got cookies
      ![图片名称](https://github.com/MartinxMax/XSS_Cookie_Tool-V1.0/blob/master/%C2%96%C2%96Demo_image/Cookie.png "Cookie")  