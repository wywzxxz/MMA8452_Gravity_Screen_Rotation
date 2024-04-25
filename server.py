import serial
import struct
import time

import win32api as win32
import win32con
import sys

rotation_args = [win32con.DMDO_DEFAULT,win32con.DMDO_270,win32con.DMDO_180,win32con.DMDO_90]

def rotate_screen(id,direction):
	device = win32.EnumDisplayDevices(None,id)
	dm = win32.EnumDisplaySettings(device.DeviceName,win32con.ENUM_CURRENT_SETTINGS)
	rotation_val = rotation_args[direction]
	if((dm.DisplayOrientation + rotation_val)%2==1):
		dm.PelsWidth, dm.PelsHeight = dm.PelsHeight, dm.PelsWidth   
	if dm.DisplayOrientation == rotation_val:
		return
	dm.DisplayOrientation = rotation_val

	win32.ChangeDisplaySettingsEx(device.DeviceName,dm)
last = -1
def auto_rotate_screen():
	global last
	# 设置串口
	ser = serial.Serial('COM3', baudrate=9600,timeout=1)  # 根据实际情况修改串口名称
	ser.bytesize = serial.EIGHTBITS
	ser.parity = serial.PARITY_NONE
	ser.stopbits = serial.STOPBITS_ONE

	def argmin(arr):
		res =0 
		for i in range(len(arr)):
			if arr[res]>arr[i]:
					res = i
		return res

	# 接收数据	
	deg = [0,90,180,270]
	while True:
		#time.sleep(0.1)
		if True:#if ser.in_waiting > 0:		
			data = ser.read(4)
			data = struct.unpack('f', data)[0]
			zone = argmin([ min(abs(data-p),abs(-360+data-p)) for p in deg])
			#print("{:4.2f}".format(data),zone)				
			#if last == zone:
			#	continue
			last = zone
			rotate_screen(2,zone)		
auto_rotate_screen()
"""
while True:
    auto_rotate_screen()
    try:
        auto_rotate_screen()
    except Exception as e:
        if isinstance(e, KeyboardInterrupt):
            raise e
        time.sleep(5)
"""
        