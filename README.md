# RemoteDesktop
Remote desktop application still in development

I would appreciate some support on this project to keep me going. This is just the start :)

## Setup
- Make sure to install git here:
https://git-scm.com/download/win
- If you dont have python installed make sure to install it here: https://www.python.org/downloads/
- Make sure when you are installing python u add python.exe to path on the installation process.

```
git clone https://github.com/HamzLDN/RemoteDesktop.git
cd RemoteDesktop
pip install -r requirements.txt
```

Once that is done you can also use pyinstaller to compile the code to an executable.
```
pip install pyinstaller
pyinstaller client.py --onefile --noconsole --icon=NONE
```

The output should be under the dist folder.
- The command --onefile means it will pack all of the files and put it in the exe
- The command --noconsole means it would not display the console and it would be running in the background

Once all of that is done. Make sure to run the server first before you run the client :)

## How it works
![alt text](https://github.com/HamzLDN/RemoteDesktop/blob/main/Diagram.png)

## IMPORTANT!
Please i do not support any type of malicious activities with my code please use it at your own risk.  
## Updates
This update i made a new folder for the encrypted socket version under the folder EncryptedVersion.
However its slightly slow.

## How to connect to a device outside my network?
-Using port forwarding, you can direct network traffic from a certain port on your firewall or router to a particular IP address or network device on your home network. This enables you to connect a local network device, such as a computer or server, to the internet.

-Depending on the router or firewall you're using, there may be different steps to enable port forwarding. To enable port forwarding on your router, follow these general instructions:

-1. Connect to your router's web interface: The IP address of your router can be found on its user manual or by typing it into a web browser. Running the command ipconfig on the Windows command prompt or ifconfig on a Linux or Mac computer will reveal the router's IP address.
Log in to your router: You will need to enter a username and password to log in to your router. If you haven't changed the default login credentials, you can find them in the router's manual or by searching online for the make and model of your router.

-2. Find the port forwarding section: Once you're logged in, look for the port forwarding or virtual server section. This section is usually located in the advanced settings or security section of the router's web interface.

-3. Add a new port forwarding rule: In the port forwarding section, add a new rule by specifying the protocol (TCP or UDP), the port you want to forward, and the local IP address of the device you want to forward traffic to.

-4. Save your changes: Make sure to save your changes before you exit the router's web interface.

-5. Test your port forwarding: You can use online tools such as canyouseeme.org to check if your port is open or not.

## Next update
- Increase the performance of the EncryptedVersion of the code.
- Make the client keep listening for a connection and just not make it disconnect.

## Contact me on discord for any help
Hamz#0366

Fully inspired by the project: https://github.com/NeuralNine/vidstream
