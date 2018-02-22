import serial, shutil, os;

COM_NUM = 3

#シリアルポート設定
ser = serial.Serial('COM' + str(COM_NUM), baudrate = 9600, bytesize = 8, parity = 'N', stopbits = 1, rtscts = 1);


#ディレクトリが存在する場合は削除
if os.path.isdir("CanSat_camera_data"):
    shutil.rmtree("CanSat_camera_data");


#ディレクトリ作成
os.mkdir("CanSat_camera_data");


#ダウンリンク確認関数
def connection_confirm():
    print("Start: connection_confirm");
    downlink_confirm_text = ser.read(5).decode('utf-8');

    if downlink_confirm_text == 'Hello':
        ser.write(b'1');

        print("Success: connection_confirm");

        return True;
    else:
        ser.write(b'0');

        print("Failure: connection_confirm");

        return False;


line_count = 0;

#画像受け取り・保存関数
def save_img(fo_test):
    global line_count;

    receive_img_data = truncate(ser.readline().decode(), 10); #一行データ受け取り

    print("Receive line_data( %d )" % line_count);

    receive_checksum = ser.read(2); #チェックサム受取
    print("Receive checksum");

    checksum = 0;
    #一行分のデータを足し合わせる
    for i in range(len(receive_img_data)):
        checksum += receive_img_data[i];

    print(receive_img_data);
    print(receive_checksum);

    if checksum == receive_checksum: #チェックサムが一致した時
        fo_test.write(receive_img_data.strip().encode('utf-8')); #受信データを保存ファイルに追記

        ser.write(b'1');

        line_count = line_count + 1;

        print("Checksums are same");

        return True;
    else:
        ser.write(b'0');

        print("Checksums are different");

        return False;
