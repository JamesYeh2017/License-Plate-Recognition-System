import detect_car_license
import sys
import car_lic_split
import cv2

mapping = {
    "0": "A",
    "1": "B",
    "2": "C",
    "3": "D",
    "4": "E",
    "5": "F",
    "6": "G",
    "7": "H",
    "8": "I",
    "9": "J",
    "10": "K",
    "11": "L",
    "12": "M",
    "13": "N",
    "14": "O",
    "15": "P",
    "16": "Q",
    "17": "R",
    "18": "S",
    "19": "T",
    "20": "U",
    "21": "V",
    "22": "W",
    "23": "X",
    "24": "Y",
    "25": "Z",
    "30": "1",
    "31": "2",
    "32": "3",
    "33": "4",
    "34": "5",
    "35": "6",
    "36": "7",
    "37": "8",
    "38": "9",
    "39": "0",
}


# 均值哈希算法
def aHash(img):
    img = cv2.resize(img, (9, 8), interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
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


def cmpHash(hash1, hash2):  # Hash值對比
    n = 0
    if len(hash1) != len(hash2):  # hash長度不同則返回-1代表傳參出錯
        return -1
    for i in range(len(hash1)):  # 遍歷判斷
        if hash1[i] != hash2[i]:  # 不相等則n計數+1，n最終爲相似度
            n = n + 1
    return n


def OCR(char_imgs):
    try:
        car_license = ""
        for i, char_img in enumerate(char_imgs):
            char_img = cv2.cvtColor(char_img, cv2.COLOR_BGR2RGB)
            result = {}
            for idx in range(40):
                img2 = cv2.imread('./template_fonts/{}.bmp'.format(idx))

                hash1 = aHash(char_img)
                hash2 = aHash(img2)
                n = cmpHash(hash1, hash2)
                result[idx] = n
            idx = str(min(result, key=result.get))
            if idx in ["26", "27", "28", "29"]:
                continue
            car_license_char = str(mapping[idx])
            if i == 0 and car_license_char == "1":
                continue
            car_license += car_license_char
        car_license_list = list(car_license)
        car_license_list.insert(3, '-')
        car_license = ''.join(car_license_list)
        print("License Plate: ", car_license)
        return car_license
    except Exception as e:
        print(e)


def main(filename):
    car_license = detect_car_license.main(filename)
    char_imgs = car_lic_split.car_lic_split(car_license)
    OCR(char_imgs)


if __name__ == '__main__':
    # python ./img/Train01.jpg
    filename = "./img/Train01.jpg"
    if len(sys.argv) > 1:
        main(sys.argv[1])
