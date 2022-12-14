# RemoteDesktop
Remote desktop application still in development

I used the tcp protocal to send data back and forth on port 443.
At first when i was sending data i was using PNG which slowed down the the software. Therefore i moved to jpeg and i found a huge increase more than 50%. But i didnt stop there. I wanted to make it better. So i used compression from the zlib liberay to compress the data and i was able to compress more than 40k bytes per image which was outstanding.

NOTE:
In the next update i will add symmetrical encryption to increase the security of the software.
I will also add user input so the server can control the clients computer. Something like a vnc

Dont forget to star this project!
