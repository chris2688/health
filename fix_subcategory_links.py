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

# 서브카테고리 매핑 (sub-*.html → WordPress 카테고리 URL)
# 카테고리별 서브카테고리 매핑
SUBCATEGORY_MAPPING = {
    # 심혈관 질환
    "sub-고혈압.html": f"{WP_BASE_URL}/category/질환별-정보/심혈관-질환/고혈압/",
    "sub-고지혈증.html": f"{WP_BASE_URL}/category/질환별-정보/심혈관-질환/고지혈증-콜레스테롤/",
    "sub-협심증심근경색.html": f"{WP_BASE_URL}/category/질환별-정보/심혈관-질환/협심증-심근경색/",
    "sub-동맥경화.html": f"{WP_BASE_URL}/category/질환별-정보/심혈관-질환/동맥경화/",
    "sub-뇌졸중.html": f"{WP_BASE_URL}/category/질환별-정보/심혈관-질환/뇌졸중/",
    "sub-협심증.html": f"{WP_BASE_URL}/category/질환별-정보/심혈관-질환/협심증-심근경색/",
    "sub-심근경색.html": f"{WP_BASE_URL}/category/질환별-정보/심혈관-질환/협심증-심근경색/",
    
    # 당뇨병
    "sub-당뇨.html": f"{WP_BASE_URL}/category/질환별-정보/당뇨병/당뇨/",
    "sub-공복혈당장애.html": f"{WP_BASE_URL}/category/질환별-정보/당뇨병/공복혈당장애/",
    "sub-혈당관리.html": f"{WP_BASE_URL}/category/질환별-정보/당뇨병/당뇨/",
    "sub-인슐린.html": f"{WP_BASE_URL}/category/질환별-정보/당뇨병/당뇨/",
    
    # 관절/근골격계
    "sub-관절염.html": f"{WP_BASE_URL}/category/질환별-정보/관절-근골격계-질환/퇴행성-관절염/",
    "sub-퇴행성관절염.html": f"{WP_BASE_URL}/category/질환별-정보/관절-근골격계-질환/퇴행성-관절염/",
    "sub-허리디스크.html": f"{WP_BASE_URL}/category/질환별-정보/관절-근골격계-질환/허리디스크-목디스크/",
    "sub-허리디스크목디스크.html": f"{WP_BASE_URL}/category/질환별-정보/관절-근골격계-질환/허리디스크-목디스크/",
    "sub-골다공증.html": f"{WP_BASE_URL}/category/질환별-정보/관절-근골격계-질환/골다공증/",
    "sub-오십견.html": f"{WP_BASE_URL}/category/질환별-정보/관절-근골격계-질환/오십견-유착성-관절낭염/",
    
    # 호르몬/내분비
    "sub-갑상선.html": f"{WP_BASE_URL}/category/질환별-정보/호르몬-내분비-질환/갑상선-기능-저하-항진/",
    "sub-갱년기.html": f"{WP_BASE_URL}/category/질환별-정보/호르몬-내분비-질환/갱년기-증후군/",
    "sub-대사증후군.html": f"{WP_BASE_URL}/category/질환별-정보/호르몬-내분비-질환/대사증후군/",
    
    # 정신 건강/신경계
    "sub-우울증.html": f"{WP_BASE_URL}/category/질환별-정보/정신-건강-신경계/우울증-번아웃-증후군/",
    "sub-수면장애.html": f"{WP_BASE_URL}/category/질환별-정보/정신-건강-신경계/수면장애-불면증/",
    "sub-치매.html": f"{WP_BASE_URL}/category/질환별-정보/정신-건강-신경계/치매-경도인지장애/",
    "sub-이명.html": f"{WP_BASE_URL}/category/질환별-정보/정신-건강-신경계/이명-어지럼증/",
    "sub-이명현훈.html": f"{WP_BASE_URL}/category/질환별-정보/정신-건강-신경계/이명-어지럼증/",
    
    # 소화기 질환
    "sub-위염.html": f"{WP_BASE_URL}/category/질환별-정보/소화기-질환/위염-위궤양/",
    "sub-위염위궤양.html": f"{WP_BASE_URL}/category/질환별-정보/소화기-질환/위염-위궤양/",
    "sub-위염역류식.html": f"{WP_BASE_URL}/category/질환별-정보/소화기-질환/위염-위궤양/",
    "sub-역류성식도염.html": f"{WP_BASE_URL}/category/질환별-정보/소화기-질환/역류성-식도염/",
    "sub-과민성대장증후군.html": f"{WP_BASE_URL}/category/질환별-정보/소화기-질환/과민성-대장증후군/",
    "sub-지방간.html": f"{WP_BASE_URL}/category/질환별-정보/소화기-질환/지방간-간기능-저하/",
    "sub-대장암.html": f"{WP_BASE_URL}/category/질환별-정보/소화기-질환/과민성-대장증후군/",
    
    # 안과/치과/기타
    "sub-백내장.html": f"{WP_BASE_URL}/category/질환별-정보/안과-치과-기타/백내장-녹내장/",
    "sub-녹내장.html": f"{WP_BASE_URL}/category/질환별-정보/안과-치과-기타/백내장-녹내장/",
    "sub-치주염.html": f"{WP_BASE_URL}/category/질환별-정보/안과-치과-기타/치주염-치아손실/",
    "sub-비만.html": f"{WP_BASE_URL}/category/질환별-정보/안과-치과-기타/비만-체형변화/",
}

# 카테고리 페이지 파일 목록
CATEGORY_FILES = [
    "category-심혈관질환.html",
    "category-당뇨병.html",
    "category-관절근골격계.html",
    "category-호르몬내분비.html",
    "category-정신건강신경계.html",
    "category-소화기질환.html",
    "category-안과치과기타.html",
]


def fix_subcategory_links_in_file(filepath):
    """카테고리 파일 내의 서브카테고리 링크를 WordPress URL로 수정"""
    if not os.path.exists(filepath):
        print(f"  ⚠️ 파일 없음: {filepath}")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes_made = 0
        
        # 모든 서브카테고리 링크 매핑 적용
        for old_link, new_link in SUBCATEGORY_MAPPING.items():
            # href="old_link" 패턴
            pattern1 = f'href="{re.escape(old_link)}"'
            replacement1 = f'href="{new_link}"'
            new_content = re.sub(pattern1, replacement1, content)
            if new_content != content:
                changes_made += len(re.findall(pattern1, content))
                content = new_content
        
        # 변경사항이 있으면 파일 저장
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ {filepath} - 서브카테고리 링크 수정 완료")
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
    print("🔗 카테고리 페이지의 서브카테고리 링크 수정")
    print("=" * 60)
    
    # 파일 수정
    print("\n📝 서브카테고리 링크 수정 중...\n")
    fixed_files = []
    
    for file in CATEGORY_FILES:
        if fix_subcategory_links_in_file(file):
            fixed_files.append(file)
    
    print(f"\n✅ 총 {len(fixed_files)}개 파일 수정 완료!")
    
    # FTP 업로드
    if fixed_files:
        print("\n📤 수정된 파일을 FTP로 업로드합니다...")
        upload_files_via_ftp(fixed_files)
    else:
        print("\n💡 변경된 파일이 없습니다.")
    
    print("\n" + "=" * 60)
    print("✅ 작업 완료!")
    print("=" * 60)


if __name__ == "__main__":
    main()

