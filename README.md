# PWMFanControl
Simple script to control a PWM fan on a Raspberry Pi based on CPU temperature.

You should edit your crontab file to have something like that:
```
@reboot /root/rpi-pwm-fan-control/fan_control.py >/var/log/fan_control
```
