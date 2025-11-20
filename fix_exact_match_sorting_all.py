import os
import glob
import sys
import io

# UTF-8 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def fix_file(filepath):
    """파일의 정렬 로직 수정 - 정확 일치 우선 정렬 강화"""
    print(f"Processing: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 정렬 로직 수정
        old_sort = '''                // 정렬: 카테고리 정확 일치 > 카테고리 유사도 > 제목 유사도 > 점수 순
                filteredPosts.sort((a, b) => {
                    // 1순위: 카테고리 이름이 정확히 포함된 글 우선
                    if (a.hasExactCategoryMatch !== b.hasExactCategoryMatch) {
                        return b.hasExactCategoryMatch ? 1 : -1;
                    }
                    // 2순위: 카테고리 이름과 제목 유사도
                    if (Math.abs(a.categorySimilarity - b.categorySimilarity) > 0.1) {
                        return b.categorySimilarity - a.categorySimilarity;
                    }
                    // 3순위: 페이지 제목과 제목 유사도
                    if (Math.abs(a.titleSimilarity - b.titleSimilarity) > 0.1) {
                        return b.titleSimilarity - a.titleSimilarity;
                    }
                    // 4순위: 총 점수
                    return b.score - a.score;
                });'''
        
        new_sort = '''                // 정렬: 카테고리 정확 일치 > 페이지 제목 정확 일치 > 카테고리 유사도 > 제목 유사도 > 점수 순
                filteredPosts.sort((a, b) => {
                    // 1순위: 카테고리 이름이 정확히 포함된 글 우선
                    if (a.hasExactCategoryMatch && !b.hasExactCategoryMatch) {
                        return -1; // a가 앞에
                    }
                    if (!a.hasExactCategoryMatch && b.hasExactCategoryMatch) {
                        return 1; // b가 앞에
                    }
                    // 2순위: 페이지 제목이 정확히 포함된 글 우선
                    const aHasPageTitle = a.post.title.rendered.toLowerCase().includes(pageTitleLower) || 
                                         pageTitleLower.includes(a.post.title.rendered.toLowerCase());
                    const bHasPageTitle = b.post.title.rendered.toLowerCase().includes(pageTitleLower) || 
                                         pageTitleLower.includes(b.post.title.rendered.toLowerCase());
                    if (aHasPageTitle && !bHasPageTitle) {
                        return -1; // a가 앞에
                    }
                    if (!aHasPageTitle && bHasPageTitle) {
                        return 1; // b가 앞에
                    }
                    // 3순위: 카테고리 이름과 제목 유사도
                    if (Math.abs(a.categorySimilarity - b.categorySimilarity) > 0.05) {
                        return b.categorySimilarity - a.categorySimilarity;
                    }
                    // 4순위: 페이지 제목과 제목 유사도
                    if (Math.abs(a.titleSimilarity - b.titleSimilarity) > 0.05) {
                        return b.titleSimilarity - a.titleSimilarity;
                    }
                    // 5순위: 총 점수
                    return b.score - a.score;
                });'''
        
        if old_sort in content:
            content = content.replace(old_sort, new_sort)
            print(f"  ✅ 정렬 로직 강화")
        else:
            print(f"  ⚠️  정렬 로직을 찾을 수 없음")
            return False
        
        # 로그 메시지 업데이트
        old_log = "console.log(`📊 정렬 기준: 카테고리 이름 유사도 > 페이지 제목 유사도 > 점수`);"
        new_log = "console.log(`📊 정렬 기준: 카테고리 정확 일치 > 페이지 제목 정확 일치 > 카테고리 유사도 > 제목 유사도 > 점수`);"
        
        if old_log in content:
            content = content.replace(old_log, new_log)
            print(f"  ✅ 로그 메시지 업데이트")
        
        # 파일 저장
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✅ 완료!")
        return True
        
    except Exception as e:
        print(f"  ❌ 오류: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=" * 60)
    print("🔧 정확 일치 우선 정렬 강화")
    print("=" * 60)
    
    # news-main.html과 모든 sub-*.html 파일 처리
    target_files = ['news-main.html'] + glob.glob("sub-*.html")
    
    print(f"\n📁 총 {len(target_files)}개 파일")
    
    success_count = 0
    for file in target_files:
        if fix_file(file):
            success_count += 1
    
    print("\n" + "=" * 60)
    print(f"✅ 완료: {success_count}/{len(target_files)}개 파일")
    print("=" * 60)
    print("\n📝 개선사항:")
    print("  ✅ 카테고리 이름 정확 일치 우선 정렬 강화")
    print("  ✅ 페이지 제목 정확 일치 추가 고려")
    print("  ✅ 정렬 로직 명확화")

if __name__ == "__main__":
    main()

