# License-Plate-Recognition-System

目前問題：  
1.切車牌  
  -切到一部分不必要的背景 
  
2.字元切割  
檔1：car_lic_split.py
  -部分車牌切分失敗
  -把多餘背景當作一個字  
  -把。當一個字  
  -U、L、H被切分開成2~3個字
  
檔2：cropNum.py(car_lic_split.py比起來字切得好一點)  
  -數字1切分不完整  
  -車牌孔、鏡頭附近的字有機率無法切分  
  -若字附近黑影偏多就會無法切分(如Train13)  
  -13、17把陰影當字  
  

  
