import cv2


def car_lic_split(img_path):
    binary_threshold = 100
    segmentation_spacing = 0.9

    # 前處理：灰階、二值化
    img = cv2.imread(img_path)
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # cv2.imshow('gray', img_gray)
    # cv2.waitKey(0)
    img_thre = img_gray
    cv2.threshold(img_gray, binary_threshold, 255, cv2.THRESH_BINARY_INV, img_thre)
    # cv2.imshow('threshold', img_thre)
    # cv2.waitKey(0)

    # 分割字符
    white = []      # 記錄每一列的白色像素總和
    black = []      # 記錄每一列的黑色像素總和
    height, width = img_thre.shape[:2]
    white_max = 0   # 僅保存每列，取列中白色最多的像素總數
    black_max = 0   # 僅保存每列，取列中黑色最多的像素總數

    # 循環計算每一列的黑白色像素總和
    for i in range(width):
        w_count = 0     # 這一列白色總數
        b_count = 0     # 這一列黑色總數
        for j in range(height):
            if img_thre[j][i] == 255:
                w_count += 1
            else:
                b_count += 1
        white_max = max(white_max, w_count)
        black_max = max(black_max, b_count)
        white.append(w_count)
        black.append(b_count)

    # False表示白底黑字；True表示黑底白字
    arg = black_max > white_max

    # 分割圖像，給定參數爲要分割字符的開始位
    def find_end(start_):
        end_ = start_ + 1
        for m in range(start_+1, width - 1):
            if(black[m] if arg else white[m]) > (segmentation_spacing * black_max if arg else segmentation_spacing * white_max):
                end_ = m
                break
        return end_

    n = 1
    count = 0
    start = 0
    end = 0
    while n < width - 1:
        n += 1
        if(white[n] if arg else black[n]) > ((1 - segmentation_spacing) * white_max if arg else (1 - segmentation_spacing) * black_max):
            # 上面這些判斷用來辨別是白底黑字還是黑底白字
            start = n
            end = find_end(start)
            n = end
            if end - start > 5:
                cj = img_thre[1:height, start:end]

                cv2.imwrite('./car_lic_char_img/{0}_{1}.png'.format(d, count), cj)
                # cv2.imshow('cutChar', cj)
                # cv2.waitKey(0)
                count += 1


if __name__ == '__main__':
    data = ["Train01.jpg", "Train05.jpg", "Train09.jpg", "Train13.jpg", "Train17.jpg",
            "Train02.jpg", "Train06.jpg", "Train10.jpg", "Train14.jpg",
            "Train03.jpg", "Train07.jpg", "Train11.jpg", "Train15.jpg",
            "Train04.jpg", "Train08.jpg", "Train12.jpg", "Train16.jpg"]
    for d in data:
        img_path = './car_license_img/'+d
        car_lic_split(img_path)

    # img_path = './car_license_img/Train02.jpg'
    # car_lic_split(img_path)
