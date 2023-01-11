# Martin_XSS_V3.5.2
* Update redirection module,You can make XSS worms
* Update Form Hijacking
* Python version 3.6 or above
* Obtain the victim's public IP address and cookie
* Social engineering, obtaining account password
* Compatible with Windows or Linux
## usage method
  * View help information

      ```#python3 XSS_Tool_V3.5.2.py -h```

  ![图片名称](./Demo_image/help3.5.2.png)  

  * Intranet attack

      ```#python3 XSS_Tool_V3.5.2.py (-lp xxxx)```

![图片名称](./Demo_image/NoPar3.5.2.png )  

![图片名称](./Demo_image/lp3.5.2.png )  


  * Internet attack

    ```#python3 XSS_Tool_V3.5.2.py -t -rh [Remote host IP] (-rp Remote host port)```

![图片名称](./Demo_image/rh23.5.2.png )  

* Redirect attack

```#python3 XSS_Tool_V3.5.2.py -rd xxxxx```

 ![图片名称](./Demo_image/rd3.5.2.png )  
* Push Message
1. 
    
```#vim DingTalk.conf```

![图片名称](./Demo_image/dcf13.5.2.png )  

```#python3 XSS_Tool_V3.5.2.py -dcf```
 ![图片名称](./Demo_image/dcf23.5.2.png )  

2. 
    ```#python3 XSS_Tool_V3.5.2.py -dt xxx -dk xxx```

 ![图片名称](./Demo_image/dtdk3.5.2.png ) 

# Use Intranet attack [Example: push message module combination]
 * _If your machine has a public IP address, just listen to the local port_
 * _You can not specify the port. The default port is 8888_
 
-----------------Hacker--------------------------

```#vim DingTalk.conf```

![图片名称](./Demo_image/dcf13.5.2.png)

```#python3 XSS_Tool_V3.5.2.py -dcf```

![图片名称](./Demo_image/WP1.png)  

* Copy payload and inject XXS injection point



----------------Server Admin------------------------
* Admin Cookie

![图片名称](./Demo_image/Admin_no_hack.png )  

* The administrator was hacked to execute malicious code when viewing comments

![图片名称](./Demo_image/WP2.png )  

-----------------Hacker--------------------------
* Hacker gets the administrator's cookie

![图片名称](./Demo_image/WP3.png)
* Auto Push Message

![图片名称](./Demo_image/WP4.jpg)

# Use Internet attack [Example:Social engineering]
* Modify code

```vim Index.html```

![图片名称](./Demo_image/rhhijack3.5.2.png )  

* The victim visits the phishing link

![图片名称](./Demo_image/loginrhhijack3.5.2.png)

* Wait for submission. The hacker obtains the plaintext account password

![图片名称](./Demo_image/rhhijackOK3.5.2.png)


# Use Intranet attack [Example:Redirection+CSRF]

* Normal user
![图片名称](./Demo_image/CSRF1.png)
* Hacker inject code into web pages
![图片名称](./Demo_image/CSRF2.png)
* User data is maliciously modified
![图片名称](./Demo_image/CSRF3.png)