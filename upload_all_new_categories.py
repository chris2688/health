import os
from ftplib import FTP
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# FTP 설정
FTP_HOST = "health9988234.mycafe24.com"
FTP_USER = "health9988234"
FTP_PASSWORD = "ssurlf7904!"

def upload_all_new_files():
    """새로 생성된 모든 카테고리 및 서브 페이지 업로드"""
    print("=" * 70)
    print("🚀 전체 카테고리 FTP 업로드")
    print("=" * 70)
    
    # 업로드할 파일 목록
    files_to_upload = [
        # 카테고리 파일
        'category-관절근골격계.html',
        'category-소화기질환.html',
        'category-호르몬내분비.html',
        'category-정신건강신경계.html',
        'category-안과치과기타.html',
        
        # 관절/근골격계 서브 파일
        'sub-퇴행성관절염.html',
        'sub-허리디스크목디스크.html',
        'sub-골다공증.html',
        'sub-오십견.html',
        
        # 소화기 질환 서브 파일
        'sub-위염위궤양.html',
        'sub-역류성식도염.html',
        'sub-과민성대장증후군.html',
        'sub-지방간.html',
        
        # 호르몬/내분비 서브 파일
        'sub-갑상선.html',
        'sub-갱년기증후군.html',
        'sub-대사증후군.html',
        
        # 정신건강/신경계 서브 파일
        'sub-우울증번아웃.html',
        'sub-수면장애불면증.html',
        'sub-치매경도인지장애.html',
        'sub-이명어지럼증.html',
        
        # 안과/치과/기타 서브 파일
        'sub-백내장녹내장.html',
        'sub-치주염치아손실.html',
        'sub-비만체형변화.html',
    ]
    
    print(f"\n📝 총 {len(files_to_upload)}개 파일 업로드 예정\n")
    
    try:
        # FTP 연결
        print("🔌 FTP 서버 연결 중...")
        ftp = FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASSWORD)
        ftp.encoding = 'utf-8'
        print("   ✅ FTP 연결 성공\n")
        
        # 디렉토리 확인
        try:
            ftp.cwd('public_html')
            print("   📁 작업 디렉토리: public_html\n")
        except:
            try:
                ftp.cwd('www')
                print("   📁 작업 디렉토리: www\n")
            except:
                print("   📁 작업 디렉토리: root\n")
        
        # 바이너리 모드 설정
        ftp.voidcmd('TYPE I')
        
        # 파일 업로드
        print("📤 파일 업로드 시작...\n")
        success_count = 0
        category_count = 0
        sub_count = 0
        
        for filename in files_to_upload:
            if not os.path.exists(filename):
                print(f"   ⚠️  {filename} - 파일을 찾을 수 없습니다")
                continue
            
            try:
                with open(filename, 'rb') as f:
                    ftp.storbinary(f'STOR {filename}', f)
                
                if filename.startswith('category-'):
                    print(f"   📂 {filename}")
                    category_count += 1
                elif filename.startswith('sub-'):
                    print(f"   📄 {filename}")
                    sub_count += 1
                else:
                    print(f"   ✅ {filename}")
                success_count += 1
            except Exception as e:
                print(f"   ❌ {filename} - 오류: {e}")
        
        ftp.quit()
        
        print(f"\n✅ 총 {success_count}/{len(files_to_upload)}개 파일 업로드 완료!")
        print(f"   - 카테고리: {category_count}개")
        print(f"   - 서브 페이지: {sub_count}개")
        
        print("\n" + "=" * 70)
        print("🎉 전체 카테고리 업로드 완료!")
        print("=" * 70)
        print("\n📋 완성된 구조:")
        print("   🦴 관절/근골격계 질환 (4개 서브)")
        print("   🫁 소화기 질환 (4개 서브)")
        print("   ⚗️ 호르몬/내분비 질환 (3개 서브)")
        print("   🧠 정신건강/신경계 (4개 서브)")
        print("   👁️ 안과/치과/기타 (3개 서브)")
        print("\n🌐 테스트:")
        print("   https://health9988234.mycafe24.com")
        print("   → 각 카테고리 카드 클릭")
        print("   → 서브 카테고리 확인")
        print("   → WordPress 글 매핑 확인")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ FTP 오류: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    upload_all_new_files()

