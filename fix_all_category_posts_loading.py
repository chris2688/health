import os
import re
import sys
import io
from ftplib import FTP

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

CATEGORY_FILES = [
    "category-심혈관질환.html",
    "category-당뇨병.html",
    "category-관절근골격계.html",
    "category-호르몬내분비.html",
    "category-정신건강신경계.html",
    "category-소화기질환.html",
    "category-안과치과기타.html",
]


def fix_posts_loading(filepath):
    """글 불러오기 로직 수정 (REST API 실패 대비)"""
    if not os.path.exists(filepath):
        print(f"  ⚠️ 파일 없음: {filepath}")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 1. API URL을 더 많은 글을 가져오도록 수정
        content = re.sub(
            r"let apiUrl = 'https://health9988234\.mycafe24\.com/wp-json/wp/v2/posts\?per_page=12&_embed';",
            "let apiUrl = 'https://health9988234.mycafe24.com/wp-json/wp/v2/posts?per_page=50&_embed';",
            content
        )
        
        # 2. 카테고리 필터링 로직을 클라이언트 측으로 변경
        old_pattern = r'(let apiUrl = .*?;\s+const categoryIds = \[\];\s+if \(categorySlugs.*?if \(categoryIds\.length > 0\) \{\s+apiUrl \+= `&categories=\$\{categoryIds\.join\(.*?\)\}`;\s+\}\s+\}\s+const response = await fetch\(apiUrl\);.*?const posts = await response\.json\(\);)'
        
        new_code = '''let apiUrl = 'https://health9988234.mycafe24.com/wp-json/wp/v2/posts?per_page=50&_embed';
                
                const response = await fetch(apiUrl);
                if (!response.ok) {
                    console.warn('REST API 실패, 대체 방법 시도...');
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const posts = await response.json();
                
                // 카테고리 키워드로 필터링
                let filteredPosts = posts;
                if (categorySlugs && categorySlugs.length > 0) {
                    const keywords = categorySlugs.map(slug => slug.toLowerCase().replace(/-/g, ' '));
                    filteredPosts = posts.filter(post => {
                        const title = post.title.rendered.toLowerCase();
                        const content = post.content ? post.content.rendered.toLowerCase() : '';
                        
                        // 제목이나 내용에 키워드가 포함되어 있는지 확인
                        return keywords.some(keyword => {
                            const keywordParts = keyword.split(' ');
                            return keywordParts.some(part => 
                                title.includes(part) || content.includes(part)
                            );
                        });
                    });
                }'''
        
        # 기존 코드 패턴 찾기 및 교체
        pattern = r'(let apiUrl = .*?;\s+const categoryIds = \[\];.*?const posts = await response\.json\(\);)'
        
        if re.search(pattern, content, re.DOTALL):
            content = re.sub(pattern, new_code, content, flags=re.DOTALL)
        
        # 3. posts를 filteredPosts로 변경
        content = re.sub(
            r'if \(posts\.length === 0\)',
            'if (filteredPosts.length === 0)',
            content
        )
        
        content = re.sub(
            r'postsGrid\.innerHTML = posts\.map\(post =>',
            'const displayPosts = filteredPosts.slice(0, 12);\n                postsGrid.innerHTML = displayPosts.map(post =>',
            content
        )
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ {filepath} - 글 불러오기 로직 수정 완료")
            return True
        else:
            print(f"  ℹ️ {filepath} - 변경사항 없음 (이미 수정됨)")
            return False
            
    except Exception as e:
        print(f"  ❌ {filepath} - 오류: {e}")
        import traceback
        traceback.print_exc()
        return False


def upload_files_via_ftp(files):
    """FTP 업로드"""
    print("\n" + "=" * 60)
    print("📤 FTP 파일 업로드")
    print("=" * 60)
    
    FTP_HOST = "health9988234.mycafe24.com"
    FTP_USER = "health9988234"
    FTP_PASS = "ssurlf7904!"
    FTP_PORT = 21
    
    try:
        print(f"\n🔗 FTP 서버 연결 중...")
        ftp = FTP()
        ftp.encoding = 'utf-8'
        ftp.connect(FTP_HOST, FTP_PORT, timeout=10)
        print("✅ 연결 성공!")
        
        print(f"🔐 로그인 중...")
        ftp.login(FTP_USER, FTP_PASS)
        print("✅ 로그인 성공!")
        
        uploaded_count = 0
        print(f"\n📤 파일 업로드 시작...\n")
        
        for file in files:
            if os.path.exists(file):
                try:
                    print(f"  업로드 중: {file}...", end=" ")
                    with open(file, "rb") as f:
                        ftp.storbinary(f"STOR {file}", f)
                    print("✅ 완료")
                    uploaded_count += 1
                except Exception as e:
                    print(f"❌ 실패: {str(e)[:50]}")
        
        ftp.quit()
        print(f"\n✅ 총 {uploaded_count}개 파일 업로드 완료!")
        return True
            
    except Exception as e:
        print(f"\n❌ FTP 업로드 오류: {e}")
        return False


def main():
    """메인 실행"""
    print("=" * 60)
    print("🔧 카테고리 페이지 글 불러오기 로직 수정")
    print("=" * 60)
    print("\n💡 REST API가 작동하지 않을 경우를 대비하여")
    print("   모든 글을 가져온 후 클라이언트에서 필터링하도록 변경합니다.\n")
    
    print("📝 파일 수정 중...\n")
    fixed_files = []
    
    for file in CATEGORY_FILES:
        if fix_posts_loading(file):
            fixed_files.append(file)
    
    print(f"\n✅ 총 {len(fixed_files)}개 파일 수정 완료!")
    
    if fixed_files:
        print("\n📤 수정된 파일을 FTP로 업로드합니다...")
        upload_files_via_ftp(fixed_files)
    
    print("\n" + "=" * 60)
    print("✅ 작업 완료!")
    print("=" * 60)


if __name__ == "__main__":
    main()

