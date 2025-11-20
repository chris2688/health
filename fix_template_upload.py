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

def upload_to_correct_theme():
    """intro-template.php를 올바른 테마 폴더에 업로드"""
    print("=" * 60)
    print("📤 올바른 테마 폴더에 템플릿 업로드")
    print("=" * 60)
    
    try:
        # FTP 연결
        print(f"\n🔗 FTP 연결 중...")
        ftp = FTP()
        ftp.encoding = 'utf-8'
        ftp.connect(FTP_HOST, FTP_PORT, timeout=10)
        ftp.login(FTP_USER, FTP_PASS)
        print("✅ 연결 성공!")
        
        # generatepress 테마 폴더로 이동
        print("\n📁 GeneratePress 테마 폴더로 이동 중...")
        try:
            ftp.cwd("wp-content/themes/generatepress")
            print("  ✅ generatepress 폴더 접근 성공!")
        except:
            # 대안: twentytwentyfive (최신 WordPress 기본 테마)
            try:
                ftp.cwd("/www/wp-content/themes/twentytwentyfive")
                print("  ✅ twentytwentyfive 폴더 사용")
            except:
                print("  ❌ 테마 폴더 접근 실패")
                return False
        
        # 파일 업로드
        print(f"\n📤 intro-template.php 업로드 중...")
        with open("intro-template.php", "rb") as file:
            ftp.storbinary("STOR intro-template.php", file)
        
        print("✅ 업로드 완료!")
        
        # 현재 위치 확인
        current_path = ftp.pwd()
        print(f"\n📍 업로드 위치: {current_path}")
        
        # 파일 목록에서 확인
        files = ftp.nlst()
        if "intro-template.php" in files:
            print("  ✅ intro-template.php 파일 확인됨!")
        
        ftp.quit()
        
        print("\n" + "=" * 60)
        print("✅ 업로드 완료!")
        print("=" * 60)
        print("\n💡 다음 단계:")
        print("   1. WordPress 관리자 > 페이지 > 홈 (메인 로비)")
        print("   2. 오른쪽 사이드바에서 '페이지 속성' 찾기")
        print("   3. '템플릿' 드롭다운에서 '인트로 메인 페이지' 선택")
        print("   4. '업데이트' 버튼 클릭")
        print("\n🎉 완료되면 WordPress 헤더/푸터가 자동으로 표시됩니다!")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"\n❌ 오류: {e}")
        return False

if __name__ == "__main__":
    upload_to_correct_theme()
    print("\n⏳ 5초 후 종료...")
    import time
    time.sleep(5)

