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

def upload_all_files():
    """모든 HTML 파일 업로드 및 .htaccess 설정"""
    print("=" * 60)
    print("🚀 전체 사이트 업로드 및 메인 페이지 설정")
    print("=" * 60)
    
    # 업로드할 파일 목록
    html_files = [f for f in os.listdir('.') if f.endswith('.html')]
    
    # 주요 파일 우선 업로드
    priority_files = ['index-v3.html', 'index-v2.html', 'intro.html']
    category_files = [f for f in html_files if f.startswith('category-')]
    sub_files = [f for f in html_files if f.startswith('sub-')]
    main_files = [f for f in html_files if 'main' in f]
    other_files = [f for f in html_files if f not in priority_files + category_files + sub_files + main_files]
    
    upload_order = priority_files + category_files + sub_files + main_files + other_files
    
    print(f"\n📝 총 {len(upload_order)}개 HTML 파일 업로드 예정")
    print(f"   - 우선 파일: {len(priority_files)}개")
    print(f"   - 카테고리 파일: {len(category_files)}개")
    print(f"   - 서브 파일: {len(sub_files)}개")
    print(f"   - 메인 파일: {len(main_files)}개")
    print(f"   - 기타 파일: {len(other_files)}개\n")
    
    try:
        # FTP 연결
        print("🔌 FTP 서버 연결 중...")
        ftp = FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASSWORD)
        ftp.encoding = 'utf-8'
        print("   ✅ FTP 연결 성공\n")
        
        # 디렉토리 찾기
        try:
            ftp.cwd('public_html')
            target_dir = 'public_html'
            print("   📁 작업 디렉토리: public_html\n")
        except:
            try:
                ftp.cwd('www')
                target_dir = 'www'
                print("   📁 작업 디렉토리: www\n")
            except:
                target_dir = 'root'
                print("   📁 작업 디렉토리: root\n")
        
        # 바이너리 모드 설정
        ftp.voidcmd('TYPE I')
        
        # 1. HTML 파일 업로드
        print("📤 HTML 파일 업로드 시작...\n")
        success_count = 0
        
        for filename in upload_order:
            if not os.path.exists(filename):
                continue
            try:
                with open(filename, 'rb') as f:
                    ftp.storbinary(f'STOR {filename}', f)
                
                # 주요 파일은 강조 표시
                if filename in priority_files:
                    print(f"   ⭐ {filename}")
                else:
                    print(f"   ✅ {filename}")
                success_count += 1
            except Exception as e:
                print(f"   ❌ {filename} - 오류: {e}")
        
        print(f"\n✅ {success_count}/{len(upload_order)}개 HTML 파일 업로드 완료!\n")
        
        # 2. .htaccess 파일 생성 및 업로드
        print("=" * 60)
        print("📝 .htaccess 파일 생성 중...")
        print("=" * 60)
        
        htaccess_content = """# WordPress 기본 설정 유지
# BEGIN WordPress
<IfModule mod_rewrite.c>
RewriteEngine On
RewriteRule ^index\\.php$ - [L]
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule . /index.php [L]
</IfModule>
# END WordPress

# 커스텀 HTML 페이지 설정
<IfModule mod_rewrite.c>
RewriteEngine On

# 메인 도메인 → index-v3.html로 리디렉션
RewriteCond %{REQUEST_URI} ^/$
RewriteRule ^$ /index-v3.html [L]

# HTML 파일 직접 접근 허용
RewriteCond %{REQUEST_FILENAME} -f
RewriteCond %{REQUEST_URI} \\.html$
RewriteRule .* - [L]

# WordPress REST API 및 관리자 페이지 접근 허용
RewriteCond %{REQUEST_URI} ^/wp-json/ [OR]
RewriteCond %{REQUEST_URI} ^/wp-admin/ [OR]
RewriteCond %{REQUEST_URI} ^/wp-login\\.php [OR]
RewriteCond %{REQUEST_URI} ^/wp-content/
RewriteRule .* - [L]
</IfModule>

# CORS 설정 (REST API용)
<IfModule mod_headers.c>
    Header set Access-Control-Allow-Origin "*"
    Header set Access-Control-Allow-Methods "GET, POST, OPTIONS"
    Header set Access-Control-Allow-Headers "Content-Type"
</IfModule>

# UTF-8 인코딩 설정
AddDefaultCharset UTF-8

# 캐시 설정
<IfModule mod_expires.c>
    ExpiresActive On
    ExpiresByType text/html "access plus 1 hour"
    ExpiresByType text/css "access plus 1 week"
    ExpiresByType application/javascript "access plus 1 week"
    ExpiresByType image/png "access plus 1 month"
    ExpiresByType image/jpeg "access plus 1 month"
</IfModule>
"""
        
        # 로컬에 .htaccess 파일 생성
        with open('.htaccess', 'w', encoding='utf-8') as f:
            f.write(htaccess_content)
        
        print("\n.htaccess 내용:")
        print("-" * 60)
        print(htaccess_content)
        print("-" * 60)
        
        # .htaccess 업로드
        print("\n📤 .htaccess 파일 업로드 중...")
        try:
            with open('.htaccess', 'rb') as f:
                ftp.storbinary('STOR .htaccess', f)
            print("   ✅ .htaccess 업로드 완료!")
        except Exception as e:
            print(f"   ❌ .htaccess 업로드 실패: {e}")
        
        ftp.quit()
        
        print("\n" + "=" * 60)
        print("🎉 전체 사이트 설정 완료!")
        print("=" * 60)
        print("\n✅ 메인 도메인: https://health9988234.mycafe24.com")
        print("   → index-v3.html로 리디렉션됩니다")
        print("\n✅ WordPress 관리자: https://health9988234.mycafe24.com/wp-admin")
        print("   → 글 작성/관리용으로 계속 사용 가능")
        print("\n✅ REST API: https://health9988234.mycafe24.com/wp-json/wp/v2/posts")
        print("   → 글 내용 매핑용으로 작동 중")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    upload_all_files()

