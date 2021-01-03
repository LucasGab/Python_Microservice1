from configobj import ConfigObj
import subprocess
import socket

SERVICE_DIR = 'services/'

servicesProcess = []

def checkPort(host,port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return sock.connect_ex((host, port))
    
def launchServer(service,host,port):
    resp = checkPort(host, int(port))
    if resp != 0:
        print("Service {} not running, starting service at port {} on host {}".format(service, port, host))
        new_process = subprocess.Popen(['python',SERVICE_DIR + service + '.py'])
        servicesProcess.append(new_process)
    else:
        print("Service {} running at port {} on host {}".format(service, port, host))


def startService(section,obj):
    if 'preload' in section:
        services = section['preload'].split(' ')
        for service in services:
            launchServer(service, obj[service]['host'], obj[service]['port'])
    launchServer(section.name, section['host'], section['port'])


def initMicroservice():
    config = ConfigObj('services.ini')
    for section in config:
        startService(config[section],config)
    
if __name__ == '__main__':
    initMicroservice()
    for p in servicesProcess:
        p.wait()
    for p in servicesProcess:
        p.terminate()
    
    

