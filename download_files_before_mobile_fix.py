import ftplib
import os
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# FTP 설정
FTP_HOST = "health9988234.mycafe24.com"
FTP_USER = "health9988234"
FTP_PASS = "ssurlf7904!"
FTP_PORT = 21

# 다운로드할 파일 목록
FILES_TO_DOWNLOAD = [
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
    "news-main.html",
    "food-피해야할과일.html",
    "food-질환별식단.html",
    "food-모르면독이된다.html",
    "exercise-질환별운동가이드.html",
    "exercise-운동팁.html",
    "lifestyle-생활습관.html",
    "lifestyle-생활습관바꾸기팁.html",
]


def download_file(ftp, remote_path, local_path):
    """FTP에서 파일 다운로드"""
    try:
        # 바이너리 모드로 전환
        ftp.voidcmd('TYPE I')
        with open(local_path, 'wb') as f:
            ftp.retrbinary(f'RETR {remote_path}', f.write)
        file_size = os.path.getsize(local_path)
        if file_size > 0:
            return True, file_size
        else:
            return False, "파일 크기가 0입니다"
    except Exception as e:
        return False, str(e)


def main():
    """메인 실행"""
    print("=" * 60)
    print("📥 워드프레스 서버에서 파일 다운로드")
    print("=" * 60)
    print("\n💡 모바일 메뉴 수정 전 상태로 복구하기 위해")
    print("   서버의 파일을 다운로드합니다.\n")
    
    try:
        # FTP 연결
        print("🔗 FTP 서버 연결 중...")
        ftp = ftplib.FTP()
        ftp.encoding = 'utf-8'
        ftp.connect(FTP_HOST, FTP_PORT, timeout=10)
        print("✅ 연결 성공!")
        
        # 로그인
        print("🔐 로그인 중...")
        ftp.login(FTP_USER, FTP_PASS)
        print("✅ 로그인 성공!")
        
        # 디렉토리 확인
        print("\n📂 현재 디렉토리 확인 중...")
        current_dir = ftp.pwd()
        print(f"   현재 디렉토리: {current_dir}")
        
        # 파일 목록 확인
        try:
            files = ftp.nlst()
            print(f"   파일 목록: {files[:10]}...")  # 처음 10개만 표시
        except:
            pass
        
        # 가능한 디렉토리 목록
        possible_dirs = ['/www', '/public_html', '/htdocs', '/web', '/']
        
        target_dir = None
        for dir_path in possible_dirs:
            try:
                ftp.cwd(dir_path)
                files = ftp.nlst()
                if 'index-v2.html' in files or any('index' in f.lower() for f in files):
                    target_dir = dir_path
                    print(f"✅ 타겟 디렉토리 찾음: {dir_path}")
                    break
            except:
                continue
        
        if not target_dir:
            print("⚠️ 타겟 디렉토리를 찾을 수 없습니다. 현재 디렉토리에서 시도합니다.")
            try:
                ftp.cwd('/')
            except:
                pass
        
        print("\n📥 파일 다운로드 시작...\n")
        
        downloaded = []
        failed = []
        
        for filename in FILES_TO_DOWNLOAD:
            try:
                print(f"  다운로드 중: {filename}...", end=" ")
                # 파일 존재 확인
                try:
                    ftp.size(filename)
                except:
                    print(f"❌ 파일 없음")
                    failed.append((filename, "파일이 서버에 없습니다"))
                    continue
                
                success, result = download_file(ftp, filename, filename)
                if success:
                    print(f"✅ 완료 ({result:,} bytes)")
                    downloaded.append(filename)
                else:
                    print(f"❌ 실패: {result}")
                    failed.append((filename, result))
            except Exception as e:
                print(f"❌ 오류: {e}")
                failed.append((filename, str(e)))
        
        ftp.quit()
        
        print("\n" + "=" * 60)
        print("✅ 다운로드 완료!")
        print("=" * 60)
        print(f"\n📊 다운로드 결과:")
        print(f"   ✅ 성공: {len(downloaded)}개")
        if failed:
            print(f"   ❌ 실패: {len(failed)}개")
            for filename, error in failed:
                print(f"      - {filename}: {error}")
        
        print("\n💡 파일이 로컬에 다운로드되었습니다.")
        print("   이제 이 파일들을 기반으로 수정을 시작할 수 있습니다.")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    main()

