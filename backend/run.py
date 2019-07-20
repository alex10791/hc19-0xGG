import threading
import atexit
import qrcode
from flask import Flask, render_template

services = {
    'power-socket' : {
        'address' : 'switch_address',
    },
    'wifi' : {
        'address' : 'wifi_address',
    }
}


POOL_TIME = 5 #Seconds

# variables that are accessible from anywhere
commonDataStruct = {}
# lock to control access to variable
dataLock = threading.Lock()
# thread handler
ioThread = threading.Thread()

def create_app():
    app = Flask(__name__)

    @app.route("/power-socket")
    def switch_endpoint():
        return render_template('time-service.html', name='power-socket')

    @app.route("/wifi")
    def wifi_endpoint():
        return render_template('time-service.html', name='wifi')

    def interrupt():
        global ioThread
        ioThread.cancel()

    def doStuff():
        global commonDataStruct
        global ioThread
        with dataLock:
            print("hello")
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
        img = qrcode.make(service_info['address'])
        img.save('static/qrcodes/' + service + '.png')

    app = create_app()
    app.run(debug = True)