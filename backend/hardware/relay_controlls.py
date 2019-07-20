from gpiozero import LED

if __name__ == '__main__':
    pass
    
power_enabled_pin = LED(22)

def enable_power():
    power_enabled_pin.on()
    
def disable_power():
    power_enabled_pin.off()
    