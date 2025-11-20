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

def verify_and_reupload():
    """서버 파일 확인 및 재업로드"""
    print("=" * 70)
    print("🔍 서버 파일 확인 및 재업로드")
    print("=" * 70)
    
    # 문제 파일들
    problem_files = [
        'sub-골다공증.html',
        'category-호르몬내분비.html',
        'category-관절근골격계.html',
        'news-main.html',
    ]
    
    try:
        # FTP 연결
        print("\n🔌 FTP 서버 연결 중...")
        ftp = FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASSWORD)
        print("   ✅ FTP 연결 성공")
        
        # 디렉토리 이동
        try:
            ftp.cwd('public_html')
            target_dir = 'public_html'
        except:
            try:
                ftp.cwd('www')
                target_dir = 'www'
            except:
                target_dir = 'root'
        
        print(f"   📁 작업 디렉토리: {target_dir}")
        
        # 바이너리 모드
        ftp.voidcmd('TYPE I')
        
        # 서버의 모든 HTML 파일 목록 가져오기 (바이너리 모드로)
        print("\n📋 서버의 HTML 파일 목록 확인 중...\n")
        try:
            # MLSD로 파일 목록 가져오기 (더 안정적)
            files_on_server = []
            try:
                for item in ftp.mlsd():
                    if item[0].endswith('.html'):
                        files_on_server.append(item[0])
            except:
                # MLSD가 안되면 NLST 사용
                ftp.encoding = 'latin-1'  # 인코딩 변경
                all_files = ftp.nlst()
                ftp.encoding = 'utf-8'
                files_on_server = [f for f in all_files if f.endswith('.html')]
            
            print(f"   서버에 {len(files_on_server)}개 HTML 파일 발견")
            
            # 문제 파일들 확인
            print("\n🔍 문제 파일 확인:\n")
            for filename in problem_files:
                if filename in files_on_server:
                    # 파일 크기 확인
                    try:
                        ftp.voidcmd('TYPE I')
                        size = ftp.size(filename)
                        size_kb = size / 1024 if size else 0
                        print(f"   ✅ {filename} - 존재 ({size_kb:.1f} KB)")
                    except:
                        print(f"   ⚠️  {filename} - 존재하지만 크기 확인 실패")
                else:
                    print(f"   ❌ {filename} - 서버에 없음")
            
        except Exception as e:
            print(f"   ⚠️  파일 목록 확인 실패: {e}")
        
        # 모든 파일 강제 재업로드
        print("\n📤 모든 파일 강제 재업로드 시작...\n")
        success_count = 0
        
        for filename in problem_files:
            if not os.path.exists(filename):
                print(f"   ⚠️  {filename} - 로컬에 파일이 없습니다")
                continue
            
            try:
                # 기존 파일 삭제 시도
                try:
                    ftp.delete(filename)
                    print(f"   🗑️  {filename} - 기존 파일 삭제")
                except:
                    pass
                
                # 파일 업로드
                with open(filename, 'rb') as f:
                    ftp.storbinary(f'STOR {filename}', f)
                
                # 업로드 확인
                try:
                    size = ftp.size(filename)
                    local_size = os.path.getsize(filename)
                    if size == local_size:
                        print(f"   ✅ {filename} - 업로드 성공 및 검증 완료 ({size/1024:.1f} KB)")
                    else:
                        print(f"   ⚠️  {filename} - 업로드되었으나 크기 불일치 (서버:{size}, 로컬:{local_size})")
                except:
                    print(f"   ✅ {filename} - 업로드 완료 (검증 불가)")
                
                success_count += 1
            except Exception as e:
                print(f"   ❌ {filename} - 업로드 실패: {e}")
        
        ftp.quit()
        
        print(f"\n✅ {success_count}/{len(problem_files)}개 파일 재업로드 완료!")
        
        print("\n" + "=" * 70)
        print("🔗 테스트 URL (직접 접속해서 확인):")
        print("=" * 70)
        print("\n1. 골다공증 (URL 인코딩):")
        print("   https://health9988234.mycafe24.com/sub-%EA%B3%A8%EB%8B%A4%EA%B3%B5%EC%A6%9D.html")
        print("\n2. 호르몬/내분비 (URL 인코딩):")
        print("   https://health9988234.mycafe24.com/category-%ED%98%B8%EB%A5%B4%EB%AA%AC%EB%82%B4%EB%B6%84%EB%B9%84.html")
        print("\n3. 관절/근골격계 (URL 인코딩):")
        print("   https://health9988234.mycafe24.com/category-%EA%B4%80%EC%A0%88%EA%B7%BC%EA%B3%A8%EA%B2%A9%EA%B3%84.html")
        print("\n4. 건강News:")
        print("   https://health9988234.mycafe24.com/news-main.html")
        print("\n" + "=" * 70)
        print("💡 여전히 안되면:")
        print("   1. 시크릿 모드에서 테스트")
        print("   2. 다른 브라우저에서 테스트")
        print("   3. 5분 정도 기다린 후 테스트 (서버 캐시)")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    verify_and_reupload()

