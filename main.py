import functions;
from functions import *;

while 1:
    stdout_message = ser.readline().strip().decode('utf-8', 'ignore');
    print(stdout_message);

    if stdout_message == "Transfer Sequence Start":
        break;

#ダウンリンク確認
# while connection_confirm() == False:
#     continue;

#サブミッション画像受け取り・保存
print("Start: save_img( sub )");
save_img_pass = 'CanSat_camera_data/sub_img.bmp';
fo = open("test.txt", 'ab');
print("File opened");
save_img(fo);

#メインミッション画像受け取り・保存
# for i in range(360):
#     while save_img("main") == False:
#         continue;
