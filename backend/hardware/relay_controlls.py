from gpiozero import LED

power_enabled_pin = LED(23)

def enable_power():
    power_enabled_pin.on()


def disable_power():
    power_enabled_pin.off()


if __name__ == '__main__':
    import time
    while True:
        enable_power()
        time.sleep(1)
        disable_power()
        time.sleep(1)
    