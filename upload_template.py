import sys
import io
from ftplib import FTP
import os

# UTF-8 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# FTP 정보
FTP_HOST = "health9988234.mycafe24.com"
FTP_USER = "health9988234"
FTP_PASS = "ssurlf7904!"
FTP_PORT = 21

def upload_template():
    """intro-template.php를 테마 폴더에 업로드"""
    print("=" * 60)
    print("📤 WordPress 템플릿 업로드")
    print("=" * 60)
    
    # 파일 확인
    if not os.path.exists("intro-template.php"):
        print("❌ intro-template.php 파일을 찾을 수 없습니다!")
        return False
    
    print(f"\n파일 크기: {os.path.getsize('intro-template.php')} bytes")
    
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
        
        # 현재 디렉토리
        current_dir = ftp.pwd()
        print(f"\n📂 현재 디렉토리: {current_dir}")
        
        # wp-content/themes 폴더로 이동
        print("\n📁 테마 폴더 찾는 중...")
        
        theme_paths = [
            "wp-content/themes",
            "/www/wp-content/themes"
        ]
        
        theme_found = False
        for path in theme_paths:
            try:
                ftp.cwd(path)
                print(f"  ✅ {path} 접근 성공!")
                theme_found = True
                break
            except:
                try:
                    ftp.cwd(current_dir)
                except:
                    pass
        
        if not theme_found:
            print("  ❌ 테마 폴더를 찾을 수 없습니다")
            return False
        
        # 테마 목록 확인
        print("\n📋 테마 목록:")
        themes = ftp.nlst()
        for theme in themes:
            print(f"   - {theme}")
        
        # 첫 번째 테마 폴더 사용
        if themes:
            active_theme = themes[0]  # 보통 첫 번째가 활성 테마
            print(f"\n✅ '{active_theme}' 테마 사용")
            
            try:
                ftp.cwd(active_theme)
                print(f"  ✓ {active_theme} 폴더로 이동")
            except:
                print(f"  ❌ {active_theme} 폴더 접근 실패")
                return False
            
            # 파일 업로드
            print(f"\n📤 intro-template.php 업로드 중...")
            with open("intro-template.php", "rb") as file:
                ftp.storbinary("STOR intro-template.php", file)
            
            print("✅ 업로드 완료!")
            
            # 연결 종료
            ftp.quit()
            
            print("\n" + "=" * 60)
            print("✅ 템플릿 업로드 완료!")
            print("=" * 60)
            print("\n💡 다음 단계:")
            print("   1. WordPress 관리자 > 페이지 > 홈 (메인 로비)")
            print("   2. 오른쪽 사이드바 > 페이지 속성 > 템플릿")
            print("   3. '인트로 메인 페이지' 선택")
            print("   4. 업데이트 클릭")
            print("\n🎉 그러면 WordPress 헤더가 자동으로 표시됩니다!")
            print("=" * 60)
            return True
        else:
            print("❌ 테마를 찾을 수 없습니다")
            return False
            
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        return False

if __name__ == "__main__":
    upload_template()
    print("\n⏳ 5초 후 종료...")
    import time
    time.sleep(5)

