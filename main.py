# MMA8452模块 数字三轴模块 模块 倾斜度模块 GY-45
# https://item.taobao.com/item.htm?spm=a1z09.2.0.0.22432e8dE2q9wd&id=15459276886&_u=gmlmtak847b
# https://pan.baidu.com/s/1gdFuV7P?_at_=1700118969629
import machine
import time
import math
import struct
import sys
who_am_i = 0x75
sdaPIN=machine.Pin(16)
sclPIN=machine.Pin(17)

import time

def getValue(data):
    Accl = (data[0] * 256 + data[1]) / 16
    if Accl > 2047 :
        Accl -= 4096
    Accl = Accl / 2048 * 2 # 2g
    return Accl

def MMA8452():
    i2c=machine.I2C(0,sda=sdaPIN, scl=sclPIN, freq=400000)        
    devices = i2c.scan()
    if len(devices) == 0:
        raise "No i2c device !"
    #for device in devices:
    # print("Decimal address: ",device," | Hexa address: ",hex(device)," | WHO_AM_I",i2c.readfrom_mem(device,0x00,1))
    device = devices[0]
    
    # 设置工作模式
    i2c.writeto_mem(device, 0x2A, bytearray([0x00])) #  Control register(0x2A) : StandBy mode(0x00)
    i2c.writeto_mem(device, 0x2A, bytearray([0x01])) #  Control register(0x2A) : Active mode(0x01)
    i2c.writeto_mem(device, 0x0E, bytearray([0x00])) #  Configuration register(0x0E) : Set range to +/- 2g (0x00)

    while True:
        data = i2c.readfrom_mem(device, 0x00, 7)
        x = getValue(data[1:])
        y = getValue(data[3:])
        z = getValue(data[5:])        
        p = math.atan2(x,-z)/math.pi*180
        p = (p + 360) % 360        
        sys.stdout.buffer.write(struct.pack('f', p))
        time.sleep(0.1)
while True:
    try:
        MMA8452()
    except Exception as e:
        if isinstance(e, KeyboardInterrupt):
            raise e
        
