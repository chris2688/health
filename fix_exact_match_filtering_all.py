import os
import glob
import sys
import io

# UTF-8 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def fix_file(filepath):
    """페이지 제목 정확 일치 필터링 강화"""
    print(f"Processing: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 이미 수정된 코드가 있으면 스킵
        if '페이지 제목 정확 일치 확인 (최우선 - 점수와 무관하게 통과)' in content:
            print(f"  ⏭️  이미 수정된 코드가 있음, 스킵")
            return False
        
        # 1. 페이지 제목 정확 일치 체크 강화
        old_exact_check = '''                    // 페이지 제목이 글 제목에 정확히 포함되어 있는지 확인
                    if (postTitleNoSpace.includes(pageTitleNoSpace) || pageTitleNoSpace.includes(postTitleNoSpace)) {
                        hasExactCategoryMatch = true;
                        maxCategorySimilarity = 1.0;
                    }'''
        
        new_exact_check = '''                    // 페이지 제목이 글 제목에 정확히 포함되어 있는지 확인 (양방향 체크 강화)
                    if (postTitleNoSpace.includes(pageTitleNoSpace) || 
                        pageTitleNoSpace.includes(postTitleNoSpace) ||
                        postTitleLower.includes(pageTitleLower) ||
                        pageTitleLower.includes(postTitleLower)) {
                        hasExactCategoryMatch = true;
                        maxCategorySimilarity = 1.0;
                    }'''
        
        if old_exact_check in content:
            content = content.replace(old_exact_check, new_exact_check)
            print(f"  ✅ 페이지 제목 정확 일치 체크 강화")
        
        # 2. 필터링 로직 개선 - 페이지 제목 정확 일치 최우선
        old_filter = '''                // 관련성 점수가 너무 낮은 글 필터링 (최소 50점 이상)
                // 핵심 키워드가 있는 경우, 핵심 키워드가 하나도 매칭되지 않은 글은 제외
                // 단, 페이지 제목 정확 일치나 카테고리 정확 일치가 있으면 예외
                const filteredPosts = postsWithScore.filter(({ score, post, hasExactCategoryMatch }) => {
                    if (score < 50) return false;
                    
                    // 정확 일치가 있으면 통과
                    if (hasExactCategoryMatch) return true;
                    
                    // 페이지 제목 정확 일치 확인
                    const postTitleLower = post.title.rendered.toLowerCase();
                    const postTitleNoSpace = postTitleLower.replace(/\\s+/g, '');
                    const pageTitleNoSpace = pageTitleLower.replace(/\\s+/g, '');
                    if (postTitleNoSpace.includes(pageTitleNoSpace) || pageTitleNoSpace.includes(postTitleNoSpace)) {
                        return true;
                    }
                    
                    // 핵심 키워드가 있고, 핵심 키워드가 하나도 매칭되지 않으면 제외
                    if (coreKeywords.length > 0) {
                        const hasCoreKeyword = coreKeywords.some(keyword => postTitleLower.includes(keyword) || postTitleNoSpace.includes(keyword.replace(/\\s+/g, '')));
                        if (!hasCoreKeyword) return false;
                    }
                    
                    return true;
                });'''
        
        new_filter = '''                // 관련성 점수가 너무 낮은 글 필터링 (최소 50점 이상)
                // 핵심 키워드가 있는 경우, 핵심 키워드가 하나도 매칭되지 않은 글은 제외
                // 단, 페이지 제목 정확 일치나 카테고리 정확 일치가 있으면 예외
                const filteredPosts = postsWithScore.filter(({ score, post, hasExactCategoryMatch }) => {
                    const postTitleLower = post.title.rendered.toLowerCase();
                    const postTitleNoSpace = postTitleLower.replace(/\\s+/g, '');
                    const pageTitleNoSpace = pageTitleLower.replace(/\\s+/g, '');
                    
                    // 페이지 제목 정확 일치 확인 (최우선 - 점수와 무관하게 통과)
                    if (postTitleNoSpace.includes(pageTitleNoSpace) || pageTitleNoSpace.includes(postTitleNoSpace)) {
                        return true;
                    }
                    
                    // 정확 일치가 있으면 통과
                    if (hasExactCategoryMatch) return true;
                    
                    // 점수 체크
                    if (score < 50) return false;
                    
                    // 핵심 키워드가 있고, 핵심 키워드가 하나도 매칭되지 않으면 제외
                    if (coreKeywords.length > 0) {
                        const hasCoreKeyword = coreKeywords.some(keyword => {
                            const keywordNoSpace = keyword.replace(/\\s+/g, '');
                            return postTitleLower.includes(keyword) || 
                                   postTitleNoSpace.includes(keywordNoSpace) ||
                                   keywordNoSpace.includes(postTitleNoSpace) ||
                                   postTitleNoSpace.includes(keywordNoSpace);
                        });
                        if (!hasCoreKeyword) return false;
                    }
                    
                    return true;
                });'''
        
        if old_filter in content:
            content = content.replace(old_filter, new_filter)
            print(f"  ✅ 필터링 로직 개선 (페이지 제목 정확 일치 최우선)")
        else:
            print(f"  ⚠️  필터링 부분을 찾을 수 없음")
            return False
        
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
    print("🔧 페이지 제목 정확 일치 필터링 강화")
    print("=" * 60)
    
    # news-main.html은 제외 (최신순 정렬이므로)
    target_files = glob.glob("sub-*.html")
    
    print(f"\n📁 총 {len(target_files)}개 파일")
    
    success_count = 0
    for file in target_files:
        if fix_file(file):
            success_count += 1
    
    print("\n" + "=" * 60)
    print(f"✅ 완료: {success_count}/{len(target_files)}개 파일")
    print("=" * 60)
    print("\n📝 개선사항:")
    print("  ✅ 페이지 제목 정확 일치 체크 강화 (양방향)")
    print("  ✅ 페이지 제목 정확 일치 시 점수와 무관하게 통과")
    print("  ✅ 핵심 키워드 매칭 로직 개선")

if __name__ == "__main__":
    main()

