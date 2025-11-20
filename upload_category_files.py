from ftplib import FTP
import os

# FTP 접속 정보
host = "health9988234.mycafe24.com"
username = "health9988234"
password = "ssurlf7904!"
remote_dir = "/www"

# 업로드할 파일 목록
files_to_upload = [
    'category-cardiovascular.html',
    'category-diabetes.html',
    'category-musculoskeletal.html',
    'category-digestive.html',
    'category-endocrine.html',
    'category-neuroscience.html',
    'category-others.html'
]

# FTP 연결
ftp = FTP(host)
ftp.login(username, password)
ftp.cwd(remote_dir)

print("FTP 연결 성공. 파일 업로드 시작...\n")

uploaded_count = 0
failed_count = 0

for filename in files_to_upload:
    local_path = filename
    
    if not os.path.exists(local_path):
        print(f"[건너뜀] {filename} - 로컬 파일이 없습니다.")
        failed_count += 1
        continue
    
    try:
        # 파일 업로드 (바이너리 모드)
        with open(local_path, 'rb') as file:
            ftp.storbinary(f'STOR {filename}', file)
        
        print(f"[OK] {filename}")
        uploaded_count += 1
        
    except Exception as e:
        print(f"[ERROR] {filename}: {str(e)}")
        failed_count += 1

ftp.quit()

print(f"\n업로드 완료: {uploaded_count}개 성공, {failed_count}개 실패")

