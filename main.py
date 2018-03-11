import functions;
from functions import *;

folder_setup();
print("Folder Setup");

while 1:
    stdout_message = ser.readline().strip().decode('utf-8', 'ignore');
    print(stdout_message);

    if stdout_message == "START: Transfer Sequence":
        break;


#ダウンリンク確認
while connection_confirm() == False:
    continue;


sub_img_num = ser.read(1).strip().decode('utf-8', 'ignore');
main_img_num = ser.read(1).strip().decode('utf-8', 'ignore');

#サブミッション画像受け取り・保存
save_img('sub', sub_img_num);

#メインミッション画像受け取り・保存
save_img('main', main_img_num);
