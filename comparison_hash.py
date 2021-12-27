import cv2


# 均值哈希算法
def aHash(img):
    img = cv2.resize(img, (8, 8), interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # s爲像素和初值爲0，hash_str爲hash值初值爲''
    s = 0
    ahash_str = ''
    for i in range(8):  # 遍歷累加求像素和
        for j in range(8):
            s = s + gray[i, j]
    avg = s / 64  # 求平均灰度
    for i in range(8):  # 灰度大於平均值爲1相反爲0生成圖片的hash值
        for j in range(8):
            if gray[i, j] > avg:
                ahash_str = ahash_str + '1'
            else:
                ahash_str = ahash_str + '0'
    return ahash_str


# 差值感知算法
def dHash(img):
    img = cv2.resize(img, (9, 8), interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    dhash_str = ''
    for i in range(8):  # 每行前一個像素大於後一個像素爲1，相反爲0，生成哈希
        for j in range(8):
            if gray[i, j] > gray[i, j + 1]:
                dhash_str = dhash_str + '1'
            else:
                dhash_str = dhash_str + '0'
    return dhash_str


def cmpHash(hash1, hash2):  # Hash值對比
    n = 0
    if len(hash1) != len(hash2):  # hash長度不同則返回-1代表傳參出錯
        return -1
    for i in range(len(hash1)):  # 遍歷判斷
        if hash1[i] != hash2[i]:  # 不相等則n計數+1，n最終爲相似度
            n = n + 1
    return n


if __name__ == '__main__':
    img1 = cv2.imread('./car_lic_char_img/47.png')
    for idx in range(40):
        img2 = cv2.imread('./template_fonts/{}.bmp'.format(idx))
        gray_img_2 = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)
        img2 = cv2.cvtColor(gray_img_2, cv2.COLOR_BGR2RGB)

        hash1 = aHash(img1)
        hash2 = aHash(img2)
        # print(hash1)
        # print(hash2)
        n = cmpHash(hash1, hash2)
        # print('{}: 均值哈希算法相似度: {}'.format(idx, n))

        hash1 = dHash(img1)
        hash2 = dHash(img2)
        # print(hash1)
        # print(hash2)
        n = cmpHash(hash1, hash2)
        print('{}: 差值哈希算法相似度： {}'.format(idx, n))
