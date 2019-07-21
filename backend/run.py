import threading
import atexit
import qrcode
import subprocess
from datetime import datetime
from TimeService import TimeService
from flask import Flask, render_template
# from hardware.relay_controlls import enable_power, disable_power
from gpiozero import LED

power_enabled_pin = LED(23)

def enable_power():
    power_enabled_pin.on()


def disable_power():
    power_enabled_pin.off()

services = {
    'power-socket' : {
        'address' : '0x5e64b75867d7a3495d66480e404f4210ad93604d',
        'object'  : None,
        'endtime' : 0,
        'active' : False
    },
    'wifi' : {
        'address' : '0xef58a22c82cf0cc8fb0f038259ed651315a98717',
        'object'  : None,
        'endtime' : 0,
        'active' : False
    }
}


POOL_TIME = 5 #Seconds

# variables that are accessible from anywhere
commonDataStruct = {}
# lock to control access to variable
dataLock = threading.Lock()
# thread handler
ioThread = threading.Thread()


def check_power_socket(service):
    power_socket = service['object']
    new_is_active = power_socket.is_active()
    if service['active'] == False and new_is_active == True:
        service['endtime'] = power_socket.get_end_time()
        print('endtime: {}'.format(service['endtime']))
        enable_power()
    elif new_is_active == False:
        disable_power()
    service['active'] = new_is_active


def check_wifi(service):
    wifi = service['object']
    new_is_active = wifi.is_active()
    if service['active'] == False and new_is_active == True:
        service['endtime'] = wifi.get_end_time()
        subprocess.call(['systemctl', 'start', 'create_ap'])
    elif new_is_active == False:
        subprocess.call(['systemctl', 'stop', 'create_ap'])
    service['active'] = new_is_active


def create_app():
    app = Flask(__name__)

    @app.route("/power-socket")
    def power_socket_endpoint():
        return render_template(
            'time-service.html', 
            name='power-socket', 
            is_active=services['power-socket']['active'], 
            endtime=datetime.fromtimestamp(services['power-socket']['endtime']).strftime('%d-%m-%Y %H:%M:%S'),
            next='wifi'
        )
    
    @app.route("/power-socket/active")
    def power_socket_active_endpoint():
        return "%s" % services['power-socket']['active']

    @app.route("/wifi")
    def wifi_endpoint():
        return render_template(
            'time-service.html', 
            name='wifi', 
            is_active=services['wifi']['active'], 
            endtime=datetime.fromtimestamp(services['wifi']['endtime']).strftime('%d-%m-%Y %H:%M:%S'),
            next='power-socket'
        )
    
    @app.route("/wifi/active")
    def wifi_active_endpoint():
        return "%s" % services['wifi']['active']

    def interrupt():
        global ioThread
        ioThread.cancel()

    def doStuff():
        # global commonDataStruct
        global services
        global ioThread
        with dataLock:
            print("hello")
            check_power_socket(services['power-socket'])
            check_wifi(services['wifi'])

        ioThread = threading.Timer(POOL_TIME, doStuff, ())
        ioThread.start()   

    def doStuffStart():
        # Do initialisation stuff here
        global ioThread
        ioThread = threading.Timer(POOL_TIME, doStuff, ())
        ioThread.start()

    doStuffStart()
    atexit.register(interrupt)
    return app

if __name__ == '__main__':

    for service, service_info in services.items():
        address = service_info['address']
        service_info['object'] = TimeService(address)
        img = qrcode.make(address)
        img.save('static/qrcodes/' + service + '.png')


    app = create_app()
    app.run(debug = True)