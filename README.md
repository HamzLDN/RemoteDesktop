# RemoteDesktop
Reverse remote desktop application which is currently in development.

I would appreciate a small donation for this project to keep me motivated keep it going. This is just the start :)

JOIN MY DISCORD FOR THE LATEST UPDATES: https://discord.gg/Fm6ZhrzJsp
## Setup
First:
- Make sure to install git ([Windows](https://git-scm.com/download/win), [Linux](https://git-scm.com/download/linux)
- If you dont have python installed make sure to install it from [here](https://www.python.org/ftp/python/3.10.8/python-3.10.8-amd64.exe)
- On Windows, make sure to add python.exe to your PATH during the installation.
![diagram](https://linuxhint.com/wp-content/uploads/2022/09/How-to-Add-Python-to-Windows-Path-1.png)
- Then, clone the repository:
```
git clone https://github.com/HamzLDN/RemoteDesktop.git
cd RemoteDesktop
pip install -r requirements.txt
```

If you are on Windows, install this too:
```pip install pywin32```

Once that is done you can also use pyinstaller to compile the code to a single executable.
```
pip install pyinstaller
pyinstaller client.py --onefile --noconsole --icon=NONE
```


The output should be inside of the dist folder.
- The argument --onefile makes pyinstaller compile everything into a single executable.
- The argument --noconsole prevents the terminal from displaying itself to the clients computer.

Once all of that is done, make sure to run the server first and then run the client.

## How it works
![diagram](https://github.com/HamzLDN/RemoteDesktop/blob/main/Diagram.png)

## IMPORTANT!
- I do not support any type of malicious activity with my code, nor take any responsability for any damage caused by it. Use at your own risk. 
- If the program is running slowly despite you having a fast internet connection, try using it in windowed mode since at the moment it is slightly buggy for some users.

## Updates
This update I made a new folder for the encrypted socket version under the folder EncryptedVersion.
However it's slightly slow.

## How to connect to a device outside my network?
- Using port forwarding, you can direct network traffic from a certain port on your firewall or router to a particular IP address or network device on your home network. This enables you to connect a local network device, such as a computer or server, to the internet.

- Depending on the router or firewall you're using, there may be different steps to enable port forwarding. To enable port forwarding on your router, follow these general instructions:

* 1. Connect to your router's web interface (by typing it's IP adress, found inside of the user manual, into a web browser). Running the command `ipconfig` (on Windows) `ifconfig` (on Linux and macOS) inside of a terminal will reveal the router's IP address.
Log into your router: You will need to enter a username and password. If you haven't changed the default login credentials, you can find them in the user manual (or by looking up it's manufacturer defaults online).
* 2. Find the port forwarding section: Once you're logged in, look for the "Port Forwarding" or "Virtual Server" section. This section is usually located between the advanced settings or security section of the  web interface of the browser.
* 3. Add a new port forwarding rule: In the port forwarding section, add a new rule by specifying the protocol (TCP or UDP), the port you want to forward, and the local IP address of the device you want to forward traffic to.
* 4. Save your changes: Make sure to save your changes before you exit this interface.
* 5. Test your port forwarding: You can use online tools such as canyouseeme.org to check if your port is open or not.

## Next update
- I will add a feature to add client.py to startup and replicate to a hidden directory.

## Contact me on discord if you need any help
Hamz#0366

Inspired by this great project: https://github.com/NeuralNine/vidstream
