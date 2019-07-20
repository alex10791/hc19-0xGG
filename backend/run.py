import threading
import atexit
import qrcode
from TimeService import TimeService
from flask import Flask, render_template

services = {
    'power-socket' : {
        'address' : '0x5e64b75867d7a3495d66480e404f4210ad93604d',
        'object'  : None,
        'endtime' : 0,
        'active' : False
    },
    'wifi' : {
        'address' : '0x313f9b80B296388042b0d611F0b342bccf83B417',
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
        service['active'] = power_socket.get_end_time()
    service['active'] = new_is_active

# def check_wifi():
#     is_active = True
    
#     if is_active:
#         if services['active'] == False:
#             # start wifi
#             services['active'] = True
#         else:
#             pass
#     else:
#         services['']


def create_app():
    app = Flask(__name__)

    @app.route("/power-socket")
    def switch_endpoint():
        return render_template('time-service.html', name='power-socket', is_active=services['power-socket']['active'])

    @app.route("/wifi")
    def wifi_endpoint():
        return render_template('time-service.html', name='wifi', is_active=services['wifi']['active'])

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