import serial, shutil, os;
from distutils.dir_util import copy_tree;
from datetime import datetime;
from tqdm import tqdm;

#ポート番号
COM_NUM = 6

#シリアルポート設定
ser = serial.Serial('COM' + str(COM_NUM),
                    baudrate = 115200,
                    bytesize = 8,
                    parity = 'N',
                    stopbits = 1,
                    rtscts = 1);

#フォルダセットアップ関数
def folder_setup():
    #バックアップフォルダが存在しない場合は新規作成
    if not os.path.isdir("CanSat_camera_data_BACKUP"):
        os.mkdir("CanSat_camera_data_BACKUP");

    #ディレクトリが存在する場合はファイル名に時刻を書き加えてバックアップフォルダに移動
    if os.path.isdir("CanSat_camera_data"):
        new_name = "CanSat_camera_data_%s" % datetime.now().strftime("%Y_%m_%d_%H_%M_%S");
        os.rename("CanSat_camera_data", new_name);
        shutil.move(new_name, "CanSat_camera_data_BACKUP");

    #受信データ保存用フォルダ新規作成
    os.mkdir("CanSat_camera_data");

#ダウンリンク確認関数
def connection_confirm():
    print("↓ Start:   Connection Confirm");
    downlink_confirm_text = ser.read(5).decode('utf-8');
    print(downlink_confirm_text);

    if downlink_confirm_text == 'Hello':
        ser.write(b'1');

        print("○ Success: Connection Confirm");

        return True;
    else:
        ser.write(b'0');

        print("× Failure: Connection Confirm");

        return False;



#画像一部保存関数
def save_img_component(fo_test, receive_data, receive_checksum):
    checksum = 0;

    #受信データを足し合わせる
    for i in range(len(receive_data)):
        checksum += ord(receive_data[i]);


    if checksum == int(receive_checksum): #チェックサムが一致した時
        fo_test.write(receive_data.strip().encode('utf-8')); #受信データを保存ファイルに追記

        ser.write(b'1');

        return True;
    else:
        ser.write(b'0');

        return False;


#画像保存関数
def save_img(mission_type, img_num):
    #画像枚数分繰り返し
    for i in range(img_num):
        print("↓ Start:   Save Image( %s ) %d / %d" % (mission_type, i + 1 , img_num));

        pbar = tqdm(total = 587574);

        save_img_pass = 'CanSat_camera_data/%s_img%d.bmp' % (mission_type, i);
        fo = open(save_img_pass, 'ab');

        receive_header_data = ser.readline().strip().decode('utf-8', 'ignore');
        receive_checksum = ser.read(1).strip().decode('utf-8', 'ignore');

        while save_img_component(fo, receive_header_data, receive_checksum) == False:
            continue;
        pbar.update(54);

        #一行データ × 360回繰り返し
        for i in range(360):
            receive_img_line_data = ser.readline().strip().decode('utf-8', 'ignore'); #一行データ受け取り
            receive_checksum = ser.read(1).strip().decode('utf-8', 'ignore');

            while save_img_component(fo, receive_img_line_data, receive_checksum) == False:
                continue;
            pbar.update(544 * 3);

        pbar.close();
