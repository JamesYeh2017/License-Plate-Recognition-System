# 使用SVC model（4 cross fold validation）做訓練
# training dataset：train20X20，訓練資料名稱：0資料夾-0_0.jpg、0_1.jpg... 1資料夾-1_0.jpg、1_1.jpg...
# modelj存為：finalized_model.sa

import os
import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score
from skimage.io import imread
from skimage.filters import threshold_otsu
import pickle

letters = [
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D',
            'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T',
            'U', 'V', 'W', 'X', 'Y', 'Z'
        ]

def read_training_data(training_directory):
    image_data = []
    target_data = []
    for each_letter in letters:
        # 每個字有10個用來訓練的圖
        for each in range(10):
            # 讀training data
            image_path = os.path.join(training_directory, each_letter, each_letter + '_' + str(each) + '.jpg')
            img_details = imread(image_path, as_gray=True)
            
            # 轉成binary image
            binary_image = img_details < threshold_otsu(img_details)
            
            # classifier requires that each sample is a 1D array(圖原為2D array)
            #  20*20 image 變 1*400 image
            flat_bin_image = binary_image.reshape(-1)
            image_data.append(flat_bin_image)
            target_data.append(each_letter)

    return (np.array(image_data), np.array(target_data))

# 使用交叉驗證
# num_of_fold設N (N-fold cross validation)
# 資料 1/N用來testing，N-1/N 用來training
def cross_validation(model, num_of_fold, train_data, train_label):
    accuracy_result = cross_val_score(model, train_data, train_label, cv=num_of_fold)
    print("Cross Validation Result for ", str(num_of_fold), " -fold")
    print(accuracy_result * 100)


training_dataset_dir = './train20X20'
image_data, target_data = read_training_data(training_dataset_dir)

# the kernel can be 'linear', 'poly' or 'rbf'
# the probability was set to True so as to show
# how sure the model is of it's prediction
svc_model = SVC(kernel='linear', probability=True)

# 4-fold cross validation
cross_validation(svc_model, 4, image_data, target_data)

print('training model')

# train the model with all the input data
svc_model.fit(image_data, target_data)

filename = './finalized_model.sav'
pickle.dump(svc_model, open(filename, 'wb'))
print("model saved")
