import os
import re
import sys
import io
from ftplib import FTP

# UTF-8 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 카테고리 파일 목록
CATEGORY_FILES = [
    "category-심혈관질환.html",
    "category-당뇨병.html",
    "category-관절근골격계.html",
    "category-호르몬내분비.html",
    "category-정신건강신경계.html",
    "category-소화기질환.html",
    "category-안과치과기타.html",
]


def fix_mapping_bug(filepath):
    """mapping.category_slugs 버그 수정"""
    if not os.path.exists(filepath):
        print(f"  ⚠️ 파일 없음: {filepath}")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # mapping.category_slugs를 mapping으로 수정
        content = re.sub(
            r'mapping\.category_slugs',
            'mapping',
            content
        )
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ {filepath} - 버그 수정 완료")
            return True
        else:
            print(f"  ℹ️ {filepath} - 변경사항 없음")
            return False
            
    except Exception as e:
        print(f"  ❌ {filepath} - 오류: {e}")
        return False


def upload_files_via_ftp(files):
    """FTP를 통해 수정된 파일들 업로드"""
    print("\n" + "=" * 60)
    print("📤 FTP 파일 업로드")
    print("=" * 60)
    
    FTP_HOST = "health9988234.mycafe24.com"
    FTP_USER = "health9988234"
    FTP_PASS = "ssurlf7904!"
    FTP_PORT = 21
    
    try:
        print(f"\n🔗 FTP 서버 연결 중...")
        ftp = FTP()
        ftp.encoding = 'utf-8'
        ftp.connect(FTP_HOST, FTP_PORT, timeout=10)
        print("✅ 연결 성공!")
        
        print(f"🔐 로그인 중...")
        ftp.login(FTP_USER, FTP_PASS)
        print("✅ 로그인 성공!")
        
        uploaded_count = 0
        print(f"\n📤 파일 업로드 시작...\n")
        
        for file in files:
            if os.path.exists(file):
                try:
                    print(f"  업로드 중: {file}...", end=" ")
                    with open(file, "rb") as f:
                        ftp.storbinary(f"STOR {file}", f)
                    print("✅ 완료")
                    uploaded_count += 1
                except Exception as e:
                    print(f"❌ 실패: {str(e)[:50]}")
        
        ftp.quit()
        print(f"\n✅ 총 {uploaded_count}개 파일 업로드 완료!")
        return True
            
    except Exception as e:
        print(f"\n❌ FTP 업로드 오류: {e}")
        return False


def main():
    """메인 실행"""
    print("=" * 60)
    print("🐛 카테고리 매핑 버그 수정")
    print("=" * 60)
    
    print("\n📝 파일 수정 중...\n")
    fixed_files = []
    
    for file in CATEGORY_FILES:
        if fix_mapping_bug(file):
            fixed_files.append(file)
    
    print(f"\n✅ 총 {len(fixed_files)}개 파일 수정 완료!")
    
    if fixed_files:
        print("\n📤 수정된 파일을 FTP로 업로드합니다...")
        upload_files_via_ftp(fixed_files)
    
    print("\n" + "=" * 60)
    print("✅ 작업 완료!")
    print("=" * 60)


if __name__ == "__main__":
    main()

