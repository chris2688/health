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

def upload_file():
    """FTP를 통해 intro.html 업로드"""
    print("=" * 60)
    print("📤 FTP 파일 업로드 시작")
    print("=" * 60)
    
    # 파일 확인
    if not os.path.exists("intro.html"):
        print("❌ intro.html 파일을 찾을 수 없습니다!")
        return False
    
    print(f"\n파일 크기: {os.path.getsize('intro.html')} bytes")
    
    try:
        # FTP 연결
        print(f"\n🔗 FTP 서버 연결 중: {FTP_HOST}...")
        ftp = FTP()
        ftp.encoding = 'utf-8'
        
        # 다양한 호스트 시도
        hosts = [
            FTP_HOST,
            f"ftp.{FTP_HOST}",
            "ftp.cafe24.com",
            "health9988234.cafe24.com"
        ]
        
        connected = False
        for host in hosts:
            try:
                print(f"  시도 중: {host}...")
                ftp.connect(host, FTP_PORT, timeout=10)
                connected = True
                print(f"  ✅ {host} 연결 성공!")
                break
            except Exception as e:
                print(f"  ❌ {host} 실패: {str(e)[:50]}")
                continue
        
        if not connected:
            print("\n❌ 모든 FTP 서버 연결 실패")
            print("\n💡 수동 업로드 방법:")
            print("   1. cafe24 관리자 페이지 로그인")
            print("   2. 나의 서비스 관리 > FTP 관리")
            print("   3. FileZilla 등의 FTP 프로그램 사용")
            print(f"   4. intro.html 파일을 public_html/ 폴더에 업로드")
            return False
        
        # 로그인
        print(f"\n🔐 로그인 중: {FTP_USER}...")
        ftp.login(FTP_USER, FTP_PASS)
        print("✅ 로그인 성공!")
        
        # 현재 디렉토리 확인
        current_dir = ftp.pwd()
        print(f"\n📂 현재 디렉토리: {current_dir}")
        
        # 디렉토리 목록 확인
        print("\n📋 파일 목록:")
        try:
            files = ftp.nlst()
            for f in files[:10]:  # 처음 10개만 표시
                print(f"   - {f}")
            if len(files) > 10:
                print(f"   ... 외 {len(files)-10}개")
        except:
            print("   (목록을 가져올 수 없습니다)")
        
        # public_html 또는 www 폴더로 이동 시도
        target_dirs = ["public_html", "www", "htdocs", "web"]
        uploaded_path = None
        
        for target_dir in target_dirs:
            try:
                ftp.cwd(target_dir)
                print(f"\n✅ {target_dir} 폴더로 이동 성공!")
                
                # 파일 업로드
                print("\n📤 intro.html 업로드 중...")
                with open("intro.html", "rb") as file:
                    ftp.storbinary("STOR intro.html", file)
                
                uploaded_path = f"{target_dir}/intro.html"
                print(f"✅ 업로드 완료: {uploaded_path}")
                break
            except Exception as e:
                print(f"❌ {target_dir} 폴더 접근 실패: {str(e)[:50]}")
                # 루트로 돌아가기
                try:
                    ftp.cwd(current_dir)
                except:
                    pass
                continue
        
        if not uploaded_path:
            # 루트 디렉토리에 업로드 시도
            print("\n💡 루트 디렉토리에 업로드 시도...")
            try:
                with open("intro.html", "rb") as file:
                    ftp.storbinary("STOR intro.html", file)
                uploaded_path = "intro.html"
                print(f"✅ 업로드 완료: {uploaded_path}")
            except Exception as e:
                print(f"❌ 루트 업로드 실패: {e}")
        
        # 연결 종료
        ftp.quit()
        
        if uploaded_path:
            print("\n" + "=" * 60)
            print("✅ 업로드 완료!")
            print("=" * 60)
            print("\n🌐 접속 URL:")
            print(f"   https://{FTP_HOST}/intro.html")
            print("\n💡 다음 단계:")
            print("   1. 위 URL로 접속해서 확인")
            print("   2. WordPress 메인 페이지에서 리디렉션 설정")
            print("=" * 60)
            return True
        else:
            print("\n❌ 업로드 실패")
            return False
            
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        print("\n💡 해결 방법:")
        print("   1. FTP 정보가 정확한지 확인")
        print("   2. cafe24 관리자 페이지에서 FTP 계정 확인")
        print("   3. 방화벽이 FTP 포트(21)를 차단하는지 확인")
        return False

if __name__ == "__main__":
    upload_file()
    print("\n⏳ 5초 후 종료...")
    import time
    time.sleep(5)

