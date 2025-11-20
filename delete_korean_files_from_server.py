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
        # 카테고리
        'category-심혈관질환.html',
        'category-당뇨병.html',
        'category-관절근골격계.html',
        'category-소화기질환.html',
        'category-호르몬내분비.html',
        'category-정신건강신경계.html',
        'category-안과치과기타.html',
        
        # 서브 페이지들
        'sub-고혈압.html',
        'sub-고지혈증.html',
        'sub-협심증심근경색.html',
        'sub-동맥경화.html',
        'sub-뇌졸중.html',
        'sub-당뇨.html',
        'sub-공복혈당장애.html',
        'sub-당뇨병합병증.html',
        'sub-퇴행성관절염.html',
        'sub-허리디스크목디스크.html',
        'sub-골다공증.html',
        'sub-오십견.html',
        'sub-관절염.html',
        'sub-위염위궤양.html',
        'sub-역류성식도염.html',
        'sub-과민성대장증후군.html',
        'sub-지방간.html',
        'sub-위염.html',
        'sub-갑상선.html',
        'sub-갱년기증후군.html',
        'sub-대사증후군.html',
        'sub-갱년기.html',
        'sub-우울증번아웃.html',
        'sub-수면장애불면증.html',
        'sub-치매경도인지장애.html',
        'sub-이명어지럼증.html',
        'sub-우울증.html',
        'sub-수면장애.html',
        'sub-치매.html',
        'sub-불안장애.html',
        'sub-백내장녹내장.html',
        'sub-치주염치아손실.html',
        'sub-비만체형변화.html',
        'sub-백내장.html',
        'sub-녹내장.html',
        'sub-치주질환.html',
        'sub-비만.html',
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
        print("\n이제 한글 URL로 접속하면 404 오류가 발생합니다.")
        print("영문 URL만 정상 작동합니다:")
        print("\n✅ 골다공증: https://health9988234.mycafe24.com/sub-osteoporosis.html")
        print("✅ 허리디스크: https://health9988234.mycafe24.com/sub-disc-herniation.html")
        print("✅ 퇴행성관절염: https://health9988234.mycafe24.com/sub-degenerative-arthritis.html")
        print("✅ 오십견: https://health9988234.mycafe24.com/sub-frozen-shoulder.html")
        print("✅ 호르몬/내분비: https://health9988234.mycafe24.com/category-endocrine.html")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ 오류: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    delete_korean_files()

