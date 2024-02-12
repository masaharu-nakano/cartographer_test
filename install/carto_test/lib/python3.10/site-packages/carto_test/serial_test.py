import serial
import time

# Arduino Unoのデバイスファイルを指定
arduino_port = '/dev/ttyACM0'

# シリアル通信の設定
ser = serial.Serial(arduino_port, 9600, timeout=1)

try:
    while True:
        # Raspberry PiからArduino Unoにデータを送信
        data_to_send = "Hello Arduino!\n"
        ser.write(data_to_send.encode('utf-8'))
        
        # Arduino Unoからのレスポンスを読み取り
        response = ser.readline().decode('utf-8')
        print("Arduino says:", response)
        
        time.sleep(1)

except KeyboardInterrupt:
    ser.close()
    print("Serial communication closed.")
