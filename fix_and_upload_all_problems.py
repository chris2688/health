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

def upload_all_problem_files():
    """문제가 있는 모든 파일 재업로드"""
    print("=" * 70)
    print("🔄 전체 파일 재업로드 (문제 해결)")
    print("=" * 70)
    
    # 모든 카테고리 및 서브 파일 업로드
    files_to_upload = []
    
    # 카테고리 파일 전체
    category_files = [
        'category-심혈관질환.html',
        'category-당뇨병.html',
        'category-관절근골격계.html',
        'category-소화기질환.html',
        'category-호르몬내분비.html',
        'category-정신건강신경계.html',
        'category-안과치과기타.html',
    ]
    files_to_upload.extend(category_files)
    
    # 서브 파일 전체 (문제가 있었던 파일 우선)
    priority_sub_files = [
        'sub-골다공증.html',
        'sub-갑상선.html',
        'sub-갱년기증후군.html',
        'sub-대사증후군.html',
    ]
    files_to_upload.extend(priority_sub_files)
    
    # 나머지 서브 파일
    other_sub_files = [f for f in os.listdir('.') 
                      if f.startswith('sub-') and f.endswith('.html') 
                      and f not in priority_sub_files]
    files_to_upload.extend(other_sub_files[:30])  # 처음 30개만
    
    # news-main.html 추가
    files_to_upload.append('news-main.html')
    
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
            target_dir = 'public_html'
        except:
            try:
                ftp.cwd('www')
                target_dir = 'www'
            except:
                target_dir = 'root'
        
        print(f"   📁 작업 디렉토리: {target_dir}\n")
        
        # 바이너리 모드 설정
        ftp.voidcmd('TYPE I')
        
        # 파일 업로드
        print("📤 파일 업로드 시작...\n")
        success_count = 0
        failed_files = []
        
        for filename in files_to_upload:
            if not os.path.exists(filename):
                print(f"   ⚠️  {filename} - 로컬에 파일이 없습니다")
                continue
            
            try:
                with open(filename, 'rb') as f:
                    ftp.storbinary(f'STOR {filename}', f)
                
                # 파일 크기 확인
                size = os.path.getsize(filename)
                size_kb = size / 1024
                
                if filename.startswith('category-'):
                    print(f"   📂 {filename} ({size_kb:.1f} KB)")
                elif filename in priority_sub_files:
                    print(f"   ⭐ {filename} ({size_kb:.1f} KB)")
                elif filename == 'news-main.html':
                    print(f"   📰 {filename} ({size_kb:.1f} KB)")
                else:
                    print(f"   📄 {filename} ({size_kb:.1f} KB)")
                success_count += 1
            except Exception as e:
                print(f"   ❌ {filename} - 오류: {e}")
                failed_files.append(filename)
        
        ftp.quit()
        
        print(f"\n✅ 총 {success_count}/{len(files_to_upload)}개 파일 업로드 완료!")
        
        if failed_files:
            print(f"\n❌ 실패한 파일 ({len(failed_files)}개):")
            for f in failed_files:
                print(f"   - {f}")
        
        print("\n" + "=" * 70)
        print("🔗 문제가 있었던 페이지 테스트")
        print("=" * 70)
        print("   1. 골다공증:")
        print("      https://health9988234.mycafe24.com/sub-골다공증.html")
        print("\n   2. 호르몬/내분비:")
        print("      https://health9988234.mycafe24.com/category-호르몬내분비.html")
        print("\n   3. 건강News:")
        print("      https://health9988234.mycafe24.com/news-main.html")
        print("\n   4. 관절/근골격계:")
        print("      https://health9988234.mycafe24.com/category-관절근골격계.html")
        print("=" * 70)
        print("\n💡 브라우저 캐시를 지우고 테스트해주세요:")
        print("   Ctrl+Shift+Del → 캐시 삭제 또는 Ctrl+F5 강력 새로고침")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ FTP 오류: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    upload_all_problem_files()

