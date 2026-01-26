import wget
from ftplib import FTP

# url链接 // url link
url = r'http://clouddata.nsmc.org.cn:8089/DATA/FY3/FY3F/MERSI/L1/GEO1K/2025/20250301/FY3F_MERSI_GRAN_L1_20250301_0735_GEO1K_V0.HDF?AccessKeyId=LKI0VZTG4IR1UYTUSXQZ&Expires=1765699022&Signature=SeGf7v4qL6Dx4H84Aq3Haqpv5So%3D'

# 存储文件的文件夹路径 // The folder path where the file is saved
folder_path = r'./'

# 将返回文件的存储路径 // The savepath of the file will be returned
# 如果增加参数bar=None，能够使得进度条不显示 // If the parameter bar=None is added, the progress bar will not be displayed
file_path = wget.download(url, out=folder_path)      



