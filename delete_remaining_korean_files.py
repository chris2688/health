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

def delete_korean_files():
    """서버의 한글 파일명 파일들 삭제"""
    print("=" * 70)
    print("🗑️  서버의 한글 파일명 파일 삭제")
    print("=" * 70)
    
    # 삭제할 한글 파일명 목록
    korean_files = [
        # Food 카테고리
        'food-질환별식단.html',
        'food-피해야할과일.html',
        'food-모르면독이된다.html',
        
        # Exercise 카테고리
        'exercise-질환별운동가이드.html',
        'exercise-운동팁.html',
        
        # Lifestyle 카테고리
        'lifestyle-생활습관.html',
        'lifestyle-생활습관바꾸기팁.html',
    ]
    
    print(f"\n📝 {len(korean_files)}개 한글 파일 삭제 예정\n")
    
    try:
        ftp = FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASSWORD)
        print("✅ FTP 연결 성공\n")
        
        # 디렉토리 이동
        try:
            ftp.cwd('public_html')
        except:
            try:
                ftp.cwd('www')
            except:
                pass
        
        deleted_count = 0
        not_found_count = 0
        
        for filename in korean_files:
            try:
                ftp.delete(filename)
                print(f"✅ {filename} - 삭제 완료")
                deleted_count += 1
            except Exception as e:
                if '550' in str(e) or 'No such file' in str(e):
                    print(f"ℹ️  {filename} - 서버에 없음")
                    not_found_count += 1
                else:
                    print(f"❌ {filename} - 삭제 실패: {e}")
        
        ftp.quit()
        
        print(f"\n✅ {deleted_count}개 파일 삭제 완료!")
        print(f"ℹ️  {not_found_count}개 파일은 서버에 없었음")
        
        print("\n" + "=" * 70)
        print("🎉 한글 파일 정리 완료!")
        print("=" * 70)
        print("\n이제 모든 파일이 영문으로 작동합니다:")
        print("\n✅ exercise-guide.html (질환별운동가이드)")
        print("✅ exercise-tips.html (운동팁)")
        print("✅ food-diet-guide.html (질환별식단)")
        print("✅ food-avoid-fruits.html (피해야할과일)")
        print("✅ food-warnings.html (모르면독이된다)")
        print("✅ lifestyle-habits.html (생활습관)")
        print("✅ lifestyle-tips.html (생활습관바꾸기팁)")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ 오류: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    delete_korean_files()

