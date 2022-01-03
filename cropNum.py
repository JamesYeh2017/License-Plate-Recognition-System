def emptydir(dirname):  #清空資料夾
    if os.path.isdir(dirname):  #資料夾存在就刪除
        shutil.rmtree(dirname)
        sleep(2)  #需延遲,否則會出錯
    os.mkdir(dirname)  #建立資料夾

import cv2
import glob
import shutil, os
from time import sleep

print('開始擷取車牌數字！')
emptydir('cropNum')
myfiles = glob.glob('license_process_img\*.jpg')
for f in myfiles:
    filename = (f.split('\\'))[-1].replace('.jpg', '')  #移除檔名中的「.jpg」
    emptydir('cropNum/' + filename)  #以車牌號碼做資料夾名稱
    image = cv2.imread(f)  #讀取車牌號碼圖片
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  #灰階
    _,thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)  #轉為黑白
    contours1 = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  #尋找輪廓
    contours = contours1[0]  #取得輪廓
    letter_image_regions = []  #文字圖形串列
    for contour in contours:  #依序處理輪廓
        (x, y, w, h) = cv2.boundingRect(contour)  #單一輪廓資料
        letter_image_regions.append((x, y, w, h))  #輪廓資料加入串列
    letter_image_regions = sorted(letter_image_regions, key=lambda x: x[0])  #按X坐標排序
    #存檔
    i=0
    for letter_bounding_box in letter_image_regions:  #依序處理輪廓資料
        x, y, w, h = letter_bounding_box
        if w>=6 and h>45 and h<90:  #長度>6且高度在30-48才是文字
            letter_image = gray[y:y+h, x:x+w]  #擷取圖形
            letter_image = cv2.resize(letter_image, (18, 38))
            cv2.imwrite('cropNum/' + filename + '/{}.jpg'.format(i+1), letter_image)  #存各車牌文字檔
            i += 1
print('擷取車牌數字結束！')
