import os
import glob
import sys
import io

# UTF-8 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def fix_file(filepath):
    """핵심 키워드 추출 개선 - 페이지 제목 전체도 사용"""
    print(f"Processing: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 이미 수정된 코드가 있으면 스킵
        if '페이지 제목 전체를 공백 제거하여 핵심 키워드로 사용' in content:
            print(f"  ⏭️  이미 수정된 코드가 있음, 스킵")
            return False
        
        # 핵심 키워드 추출 부분 수정
        old_extraction = '''                // 핵심 키워드 추출 (페이지 제목의 고유한 단어만, 3글자 이상, 일반 의학 용어 제외)
                const coreKeywords = pageTitleWords.filter(w => 
                    w.length > 2 && 
                    !commonMedicalTerms.some(term => w.includes(term) || term.includes(w))
                );
                
                // 핵심 키워드가 없으면 페이지 제목의 첫 번째 단어 사용 (3글자 이상인 경우)
                if (coreKeywords.length === 0 && pageTitleWords.length > 0) {
                    const firstWord = pageTitleWords[0];
                    if (firstWord.length > 2) {
                        coreKeywords.push(firstWord);
                    }
                }'''
        
        new_extraction = '''                // 핵심 키워드 추출 (페이지 제목의 고유한 단어만, 3글자 이상, 일반 의학 용어 제외)
                let coreKeywords = pageTitleWords.filter(w => 
                    w.length > 2 && 
                    !commonMedicalTerms.some(term => w.includes(term) || term.includes(w))
                );
                
                // 핵심 키워드가 없으면 페이지 제목의 첫 번째 단어 사용 (3글자 이상인 경우)
                if (coreKeywords.length === 0 && pageTitleWords.length > 0) {
                    const firstWord = pageTitleWords[0];
                    if (firstWord.length > 2) {
                        coreKeywords.push(firstWord);
                    }
                }
                
                // 핵심 키워드가 여전히 없으면 페이지 제목 전체를 공백 제거하여 핵심 키워드로 사용
                if (coreKeywords.length === 0) {
                    const pageTitleNoSpace = pageTitleLower.replace(/\\s+/g, '');
                    if (pageTitleNoSpace.length > 2) {
                        coreKeywords.push(pageTitleNoSpace);
                    }
                }'''
        
        if old_extraction in content:
            content = content.replace(old_extraction, new_extraction)
            print(f"  ✅ 핵심 키워드 추출 개선")
        else:
            print(f"  ⚠️  핵심 키워드 추출 부분을 찾을 수 없음")
            return False
        
        # 필터링 로직 개선
        old_filter = '''                // 관련성 점수가 너무 낮은 글 필터링 (최소 50점 이상)
                // 핵심 키워드가 있는 경우, 핵심 키워드가 하나도 매칭되지 않은 글은 제외
                const filteredPosts = postsWithScore.filter(({ score, post }) => {
                    if (score < 50) return false;
                    
                    // 핵심 키워드가 있고, 핵심 키워드가 하나도 매칭되지 않으면 제외
                    if (coreKeywords.length > 0) {
                        const postTitleLower = post.title.rendered.toLowerCase();
                        const hasCoreKeyword = coreKeywords.some(keyword => postTitleLower.includes(keyword));
                        if (!hasCoreKeyword) return false;
                    }
                    
                    return true;
                });'''
        
        new_filter = '''                // 관련성 점수가 너무 낮은 글 필터링 (최소 50점 이상)
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
        
        if old_filter in content:
            content = content.replace(old_filter, new_filter)
            print(f"  ✅ 필터링 로직 개선")
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
    print("🔧 핵심 키워드 추출 및 필터링 개선")
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
    print("  ✅ 페이지 제목 전체를 핵심 키워드로 사용 (핵심 키워드가 없을 때)")
    print("  ✅ 정확 일치 글은 필터링 예외 처리")
    print("  ✅ 핵심 키워드 매칭 시 공백 제거 버전도 확인")

if __name__ == "__main__":
    main()

