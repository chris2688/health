import os
import glob
import sys
import io

# UTF-8 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def improve_file(filepath):
    """핵심 키워드 필터링 개선 - 일반 의학 용어 제외"""
    print(f"Processing: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 이미 수정된 코드가 있으면 스킵
        if 'commonMedicalTerms' in content:
            print(f"  ⏭️  이미 수정된 코드가 있음, 스킵")
            return False
        
        # 핵심 키워드 추출 부분 수정
        old_keyword_extraction = '''                // 각 포스트의 관련성 점수 계산 (카테고리 이름과 제목 유사도 우선)
                const pageTitleLower = pageTitle.toLowerCase();
                const pageTitleWords = pageTitleLower.split(/[\\s\\-\\(\\)\\/]+/).filter(w => w.length > 1);
                
                // 핵심 키워드 추출 (페이지 제목의 주요 단어, 3글자 이상)
                const coreKeywords = pageTitleWords.filter(w => w.length > 2);'''
        
        new_keyword_extraction = '''                // 각 포스트의 관련성 점수 계산 (카테고리 이름과 제목 유사도 우선)
                const pageTitleLower = pageTitle.toLowerCase();
                const pageTitleWords = pageTitleLower.split(/[\\s\\-\\(\\)\\/]+/).filter(w => w.length > 1);
                
                // 일반적인 의학 용어 제외 목록
                const commonMedicalTerms = ['증후군', '장애', '질환', '병', '염', '증', '증상', '합병증', '관리', '예방', '치료', '가이드', '정보'];
                
                // 핵심 키워드 추출 (페이지 제목의 고유한 단어만, 3글자 이상, 일반 의학 용어 제외)
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
        
        if old_keyword_extraction in content:
            content = content.replace(old_keyword_extraction, new_keyword_extraction)
            print(f"  ✅ 핵심 키워드 추출 개선")
        else:
            print(f"  ⚠️  핵심 키워드 추출 부분을 찾을 수 없음")
            return False
        
        # 핵심 키워드 점수 감소 강화
        old_penalty = '''                    // 핵심 키워드가 하나도 없으면 점수 감소
                    if (coreKeywords.length > 0 && matchedCoreKeywords === 0) {
                        score = Math.max(0, score * 0.3); // 점수 대폭 감소
                    }'''
        
        new_penalty = '''                    // 핵심 키워드가 하나도 없으면 점수 대폭 감소 (거의 제외)
                    if (coreKeywords.length > 0 && matchedCoreKeywords === 0) {
                        score = Math.max(0, score * 0.1); // 점수 대폭 감소 (90% 감소)
                    }'''
        
        if old_penalty in content:
            content = content.replace(old_penalty, new_penalty)
            print(f"  ✅ 핵심 키워드 점수 감소 강화")
        
        # 필터링 로직 강화
        old_filter = '''                // 관련성 점수가 너무 낮은 글 필터링 (최소 50점 이상)
                const filteredPosts = postsWithScore.filter(({ score }) => score >= 50);'''
        
        new_filter = '''                // 관련성 점수가 너무 낮은 글 필터링 (최소 50점 이상)
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
        
        if old_filter in content:
            content = content.replace(old_filter, new_filter)
            print(f"  ✅ 필터링 로직 강화")
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
    print("🔧 핵심 키워드 필터링 개선")
    print("=" * 60)
    
    # news-main.html은 제외 (최신순 정렬이므로)
    target_files = glob.glob("sub-*.html")
    
    print(f"\n📁 총 {len(target_files)}개 파일")
    
    success_count = 0
    for file in target_files:
        if improve_file(file):
            success_count += 1
    
    print("\n" + "=" * 60)
    print(f"✅ 완료: {success_count}/{len(target_files)}개 파일")
    print("=" * 60)
    print("\n📝 개선사항:")
    print("  ✅ 일반 의학 용어 제외 (증후군, 장애, 질환 등)")
    print("  ✅ 핵심 키워드 필터링 강화")
    print("  ✅ 핵심 키워드가 없는 글 자동 제외")

if __name__ == "__main__":
    main()

