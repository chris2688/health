import os
import re
import sys
import io
from ftplib import FTP

# UTF-8 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# WordPress 기본 URL
WP_BASE_URL = "https://health9988234.mycafe24.com"

# 링크 매핑 (HTML 파일 → WordPress 카테고리 URL)
LINK_MAPPING = {
    # 카테고리 페이지
    "category-심혈관질환.html": f"{WP_BASE_URL}/category/질환별-정보/심혈관-질환/",
    "category-당뇨병.html": f"{WP_BASE_URL}/category/질환별-정보/당뇨병/",
    "category-관절근골격계.html": f"{WP_BASE_URL}/category/질환별-정보/관절-근골격계-질환/",
    "category-호르몬내분비.html": f"{WP_BASE_URL}/category/질환별-정보/호르몬-내분비-질환/",
    "category-정신건강신경계.html": f"{WP_BASE_URL}/category/질환별-정보/정신-건강-신경계/",
    "category-소화기질환.html": f"{WP_BASE_URL}/category/질환별-정보/소화기-질환/",
    "category-안과치과기타.html": f"{WP_BASE_URL}/category/질환별-정보/안과-치과-기타/",
    
    # 메인 페이지
    "food-main.html": f"{WP_BASE_URL}/category/식단-음식/",
    "exercise-main.html": f"{WP_BASE_URL}/category/운동-활동/",
    "lifestyle-main.html": f"{WP_BASE_URL}/category/생활습관/",
    "news-main.html": f"{WP_BASE_URL}/category/건강News/",
    "index-v2.html": f"{WP_BASE_URL}/index-v2.html",
}

# 업로드할 파일 목록
FILES_TO_FIX = [
    "index-v2.html",
    "category-심혈관질환.html",
    "category-당뇨병.html",
    "category-관절근골격계.html",
    "category-호르몬내분비.html",
    "category-정신건강신경계.html",
    "category-소화기질환.html",
    "category-안과치과기타.html",
    "food-main.html",
    "exercise-main.html",
    "lifestyle-main.html",
    "news-main.html"
]


def fix_links_in_file(filepath):
    """파일 내의 링크를 WordPress URL로 수정"""
    if not os.path.exists(filepath):
        print(f"  ⚠️ 파일 없음: {filepath}")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes_made = 0
        
        # 모든 링크 매핑 적용
        for old_link, new_link in LINK_MAPPING.items():
            # href="old_link" 패턴
            pattern1 = f'href="{re.escape(old_link)}"'
            replacement1 = f'href="{new_link}"'
            new_content = re.sub(pattern1, replacement1, content)
            if new_content != content:
                changes_made += len(re.findall(pattern1, content))
                content = new_content
            
            # href='old_link' 패턴
            pattern2 = f"href='{re.escape(old_link)}'"
            replacement2 = f"href='{new_link}'"
            new_content = re.sub(pattern2, replacement2, content)
            if new_content != content:
                changes_made += len(re.findall(pattern2, content))
                content = new_content
        
        # index-v2.html의 로고 링크도 수정
        if filepath == "index-v2.html":
            content = re.sub(
                r'href="index-v2\.html"',
                f'href="{WP_BASE_URL}/index-v2.html"',
                content
            )
            if content != original_content:
                changes_made += 1
        
        # 변경사항이 있으면 파일 저장
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ {filepath} - 링크 수정 완료")
            return True
        else:
            print(f"  ℹ️ {filepath} - 변경사항 없음")
            return False
            
    except Exception as e:
        print(f"  ❌ {filepath} - 오류: {e}")
        return False


def upload_files_via_ftp():
    """FTP를 통해 수정된 파일들 업로드"""
    print("\n" + "=" * 60)
    print("📤 FTP 파일 업로드")
    print("=" * 60)
    
    # FTP 정보
    FTP_HOST = "health9988234.mycafe24.com"
    FTP_USER = "health9988234"
    FTP_PASS = "ssurlf7904!"
    FTP_PORT = 21
    
    try:
        # FTP 연결
        print(f"\n🔗 FTP 서버 연결 중...")
        ftp = FTP()
        ftp.encoding = 'utf-8'
        ftp.connect(FTP_HOST, FTP_PORT, timeout=10)
        print("✅ 연결 성공!")
        
        # 로그인
        print(f"🔐 로그인 중...")
        ftp.login(FTP_USER, FTP_PASS)
        print("✅ 로그인 성공!")
        
        # 파일 업로드
        uploaded_count = 0
        print(f"\n📤 파일 업로드 시작...\n")
        
        for file in FILES_TO_FIX:
            if os.path.exists(file):
                try:
                    print(f"  업로드 중: {file}...", end=" ")
                    with open(file, "rb") as f:
                        ftp.storbinary(f"STOR {file}", f)
                    print("✅ 완료")
                    uploaded_count += 1
                except Exception as e:
                    print(f"❌ 실패: {str(e)[:50]}")
        
        # 연결 종료
        ftp.quit()
        
        print(f"\n✅ 총 {uploaded_count}개 파일 업로드 완료!")
        return True
            
    except Exception as e:
        print(f"\n❌ FTP 업로드 오류: {e}")
        return False


def main():
    """메인 실행"""
    print("=" * 60)
    print("🔗 HTML 파일 링크를 WordPress URL로 수정")
    print("=" * 60)
    
    # 파일 수정
    print("\n📝 파일 링크 수정 중...\n")
    fixed_count = 0
    
    for file in FILES_TO_FIX:
        if fix_links_in_file(file):
            fixed_count += 1
    
    print(f"\n✅ 총 {fixed_count}개 파일 수정 완료!")
    
    # FTP 업로드
    if fixed_count > 0:
        print("\n📤 수정된 파일을 FTP로 업로드합니다...")
        upload_files_via_ftp()
    else:
        print("\n💡 변경된 파일이 없습니다.")
    
    print("\n" + "=" * 60)
    print("✅ 작업 완료!")
    print("=" * 60)


if __name__ == "__main__":
    main()

