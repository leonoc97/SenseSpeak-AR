import serial
ser = serial.Serial("COM16", 115200)

command = input("Type Letter")
ser.write((command + '\n').encode('utf-8'))
while True:
     cc=str(ser.readline())
     print(cc[2:][:-5])