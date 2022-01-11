import cv2
import numpy as np


def preprocess(img):
    # 前處理：包括灰度處理，高斯濾波平滑處理，Sobel提取邊界，影象二值化
    # 對於Sobel提取邊界的引數設定，第四個引數設為零，表示不計算y方向的梯度，原因是車牌上的數字在豎方向較長，重點在於得到豎方向的邊界
    # 對於二值化函式的引數設定，第二個引數設為220，是二值化的閾值，是一個經驗值
    gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    kernel_size = 5
    GaussianBlur_img = cv2.GaussianBlur(gray_img, (kernel_size, kernel_size), 0)
    # cv2.imshow("GaussianBlur_img", GaussianBlur_img)
    # cv2.waitKey(0)
    Sobel_img = cv2.Sobel(GaussianBlur_img, -1, 1, 0, ksize=3)
    # cv2.imshow("Sobel_img", Sobel_img)
    # cv2.waitKey(0)
    ret, binary_img = cv2.threshold(Sobel_img, 200, 255, cv2.THRESH_BINARY)
    # cv2.imshow("binary_img", binary_img)
    # cv2.waitKey(0)

    # 形態學運算
    kernel = np.ones((40, 80), np.uint8)
    # 先閉運算將車牌數字部分連線，再開運算將不是塊狀的或是較小的部分去掉
    close_img = cv2.morphologyEx(binary_img, cv2.MORPH_CLOSE, kernel)
    open_img = cv2.morphologyEx(close_img, cv2.MORPH_OPEN, kernel)
    # cv2.imshow("open_img", close_img)
    # cv2.waitKey(0)

    # kernel2 = np.ones((10, 10), np.uint8)
    # open_img2 = cv2.morphologyEx(open_img, cv2.MORPH_OPEN, kernel2)
    # 由於部分影象得到的輪廓邊緣不整齊，因此再進行一次膨脹操作
    element = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    dilation_img = cv2.dilate(open_img, element, iterations=3)
    for x in range(280):
        for y in range(1400):
            dilation_img[x, y] = 0
    # cv2.imshow("dilation_img", dilation_img)
    # cv2.waitKey(0)
    return dilation_img


def dtc_cat_lic(gray_img):
    # 獲取輪廓
    contours, hierarchy = cv2.findContours(gray_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # 測試邊框識別結果
    # cv2.drawContours(gray_img, contours, -1, (0, 0, 255), 3)

    temp_contours = []
    for contour in contours:
        if cv2.contourArea(contour) > 11000 and cv2.contourArea(contour) < 30000:
            temp_contours.append(contour)

    car_plates = []
    for temp_contour in temp_contours:
        rect_tupple = cv2.minAreaRect(temp_contour)
        rect_width, rect_height = rect_tupple[1]
        if rect_width < rect_height:
            rect_width, rect_height = rect_height, rect_width
        aspect_ratio = rect_width / rect_height
        # 車牌正常情況下寬高比在2 - 4之間
        if aspect_ratio > 2 and aspect_ratio < 4:
            car_plates.append(temp_contour)
            rect_vertices = cv2.boxPoints(rect_tupple)
            rect_vertices = np.int0(rect_vertices)
    return car_plates


def capture_car_lic(img, car_plates):
    for car_plate in car_plates:
        row_min, col_min = np.min(car_plate[:, 0, :], axis=0)
        row_max, col_max = np.max(car_plate[:, 0, :], axis=0)
        row_min -= 15
        col_min -= 10
        row_max += 8
        col_max += 3

        cv2.rectangle(img, (row_min, col_min), (row_max, col_max), (0, 255, 0), 2)
        # cv2.imwrite("./dtc_img/" + d, img)
        # cv2.imshow("img", img)
        # cv2.waitKey(0)
        car_license = img[col_min:col_max, row_min:row_max, :]
        return car_license


def main(filename):
    img = cv2.imread(filename)
    # 修改圖片大小
    resize_h = 800
    height = img.shape[0]
    scale = img.shape[1] / float(height)
    img = cv2.resize(img, (int(scale * resize_h), resize_h))
    gray_img = preprocess(img)
    car_plates = dtc_cat_lic(gray_img)

    # print(filename, len(car_plates))
    if len(car_plates) == 1:
        car_license = capture_car_lic(img, car_plates)
        # cv2.imwrite("./car_license_img/" + d, car_license)
        # cv2.imshow("car_license_img.jpg", car_license)
        # cv2.waitKey(0)
        return car_license


if __name__ == '__main__':
    data = ["Train01.jpg", "Train05.jpg", "Train09.jpg", "Train13.jpg", "Train17.jpg",
            "Train02.jpg", "Train06.jpg", "Train10.jpg", "Train14.jpg",
            "Train03.jpg", "Train07.jpg", "Train11.jpg", "Train15.jpg",
            "Train04.jpg", "Train08.jpg", "Train12.jpg", "Train16.jpg"]

    # data = ["Train17.jpg", "Train12.jpg", "Train15.jpg"]
    for d in data:
        main("./img/" + d)

    # main("./img/Train01.jpg")
