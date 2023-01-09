# RemoteDesktop
Remote desktop application still in development

Fully inspired by the project: https://github.com/NeuralNine/vidstream

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
![](https://github.com/HamzLDN/RemoteDesktop/blob/main/Diagram.png  =250x250)

## IMPORTANT!
Please i do not support any type of malicious activities with my code please use it at your own risk.  
## Updates
This update i made a new folder for the encrypted socket version under the folder EncryptedVersion.
However its slightly slow.

## Next update
- Increase the performance of the EncryptedVersion of the code.
- Make the client keep listening for a connection and just not make it disconnect.

## Contact me on discord for any help
Hamz#0366

I would appreciate some support on this project. This is just the start!
BTC: 3JdzGoaq8n4j6eFLJa6KcMXCcedqpXQmbC
