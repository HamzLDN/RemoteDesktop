# RemoteDesktop
Remote desktop application still in development

Fully inspired by the project: https://github.com/NeuralNine/vidstream
I just wanted to improve on it and add more features. I am still not done.

## Setup
```
git clone https://github.com/HamzLDN/RemoteDesktop.git
cd RemoteDesktop
pip install -r requirements.txt
```

Once that is done you can also use pyinstaller to compile the code to an executable.
```
pip install pyinstaller
pyinstaller client.py --onefile --noconsole
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

## Next update
- Increase the performance of the EncryptedVersion of the code.

## Contact me on discord for any help
Hamz#0366

I would appreciate a donation
BTC: 3JdzGoaq8n4j6eFLJa6KcMXCcedqpXQmbC
