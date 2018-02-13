import serial;
ser = serial.Serial('COM7', baudrate = 9600, bytesize = 8, parity = 'N', stopbits = 1, rtscts = 1 );

#ダウンリンク確認関数
def connection_confirm():
    while ser.read().decode('utf-8') != '#':
        continue;

    downlink_confirm_text = ser.read(5).decode('utf-8');

    ser.write(b'#');
    if downlink_confirm_text == 'Hello':
        ser.write(b'1');
        print(ser.readline().decode('utf-8'));

        return True;
    else:
        ser.write(b'0');
        print(ser.readline().decode('utf-8'));

        return False;

#ダウンリンク確認
while connection_confirm() == False:
    continue;
