from ftplib import FTP

# url链接 // url link
url = r'ftp://A202601271457142987:8Aam0I__@ftp.nsmc.org.cn/FY3D_MERSI_GBAL_L1_20250320_2220_GEO1K_MS.HDF'

# 获取 FTP 相关信息 // Get FTP Information
parts = url.split('//')[1].split('@')  
auth = parts[0]     
host_path = parts[1]           
username = auth.split(':')[0]       
password = auth.split(':')[1]              
hostname = host_path.split('/')[0]    
remote_filename = '/' + host_path.split('/')[1]    

# 存储文件的文件夹路径 // The folder path where the file is saved
folder_path = r'.'

# 开始下载 // Start Downloading
file_path = folder_path + '\\' + remote_filename
print(file_path)
with FTP(hostname) as ftp:
    ftp.login(user=username, passwd=password)
    with open(file_path, 'wb') as f:
        ftp.retrbinary(f'RETR {remote_filename}', f.write)    





