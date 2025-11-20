import os
import glob
import sys
import io

# UTF-8 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def fix_file(filepath):
    """페이지 제목도 정확 일치 체크에 포함"""
    print(f"Processing: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 이미 수정된 코드가 있으면 스킵
        if 'pageTitleNoSpace' in content and 'postTitleNoSpace' in content and '페이지 제목이 글 제목에 정확히 포함' in content:
            print(f"  ⏭️  이미 수정된 코드가 있음, 스킵")
            return False
        
        # 카테고리 이름 정확 일치 체크 부분 수정
        old_check = '''                    // 1. 카테고리 이름과 제목 유사도 (최우선) - 가장 높은 점수
                    let maxCategorySimilarity = 0;
                    let hasExactCategoryMatch = false;
                    categoryNames.forEach(catName => {
                        const catNameLower = catName.toLowerCase();
                        const catNameNoSpace = catNameLower.replace(/\\s+/g, '');
                        const postTitleNoSpace = postTitleLower.replace(/\\s+/g, '');
                        
                        // 카테고리 이름이 제목에 정확히 포함되어 있는지 확인 (공백 무시)
                        if (postTitleNoSpace.includes(catNameNoSpace) || catNameNoSpace.includes(postTitleNoSpace)) {
                            hasExactCategoryMatch = true;
                            maxCategorySimilarity = 1.0; // 정확히 일치하면 최고 점수
                        } else {
                            const similarity = calculateSimilarity(catName, postTitle);
                            if (similarity > maxCategorySimilarity) {
                                maxCategorySimilarity = similarity;
                            }
                        }
                    });'''
        
        new_check = '''                    // 1. 카테고리 이름과 제목 유사도 (최우선) - 가장 높은 점수
                    let maxCategorySimilarity = 0;
                    let hasExactCategoryMatch = false;
                    
                    // 페이지 제목도 카테고리 이름으로 사용 (공백 제거)
                    const pageTitleNoSpace = pageTitleLower.replace(/\\s+/g, '');
                    const postTitleNoSpace = postTitleLower.replace(/\\s+/g, '');
                    
                    // 페이지 제목이 글 제목에 정확히 포함되어 있는지 확인
                    if (postTitleNoSpace.includes(pageTitleNoSpace) || pageTitleNoSpace.includes(postTitleNoSpace)) {
                        hasExactCategoryMatch = true;
                        maxCategorySimilarity = 1.0;
                    }
                    
                    // 카테고리 이름도 확인
                    categoryNames.forEach(catName => {
                        const catNameLower = catName.toLowerCase();
                        const catNameNoSpace = catNameLower.replace(/\\s+/g, '');
                        
                        // 카테고리 이름이 제목에 정확히 포함되어 있는지 확인 (공백 무시)
                        if (postTitleNoSpace.includes(catNameNoSpace) || catNameNoSpace.includes(postTitleNoSpace)) {
                            hasExactCategoryMatch = true;
                            maxCategorySimilarity = 1.0; // 정확히 일치하면 최고 점수
                        } else {
                            const similarity = calculateSimilarity(catName, postTitle);
                            if (similarity > maxCategorySimilarity) {
                                maxCategorySimilarity = similarity;
                            }
                        }
                    });'''
        
        if old_check in content:
            content = content.replace(old_check, new_check)
            print(f"  ✅ 페이지 제목 정확 일치 체크 추가")
        else:
            print(f"  ⚠️  카테고리 체크 부분을 찾을 수 없음")
            return False
        
        # 디버깅 로그 추가
        old_log = '''                console.log(`Filtered posts: ${filteredPosts.length} out of ${posts.length} (min score: 50)`);
                console.log(`Core keywords: ${coreKeywords.join(', ')}`);
                console.log(`Category names: ${categoryNames.join(', ')}`);
                console.log(`📊 정렬 기준: 카테고리 정확 일치 > 페이지 제목 정확 일치 > 카테고리 유사도 > 제목 유사도 > 점수`);'''
        
        new_log = '''                console.log(`Filtered posts: ${filteredPosts.length} out of ${posts.length} (min score: 50)`);
                console.log(`Core keywords: ${coreKeywords.join(', ')}`);
                console.log(`Category names: ${categoryNames.join(', ')}`);
                console.log(`Page title: ${pageTitle}`);
                console.log(`📊 정렬 기준: 카테고리 정확 일치 > 페이지 제목 정확 일치 > 카테고리 유사도 > 제목 유사도 > 점수`);
                // 디버깅: 정확 일치 글 확인
                filteredPosts.forEach((item, idx) => {
                    if (item.hasExactCategoryMatch) {
                        console.log(`✅ 정확 일치 [${idx}]: ${item.post.title.rendered} (점수: ${item.score}, 카테고리 유사도: ${item.categorySimilarity})`);
                    }
                });'''
        
        if old_log in content:
            content = content.replace(old_log, new_log)
            print(f"  ✅ 디버깅 로그 추가")
        
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
    print("🔧 페이지 제목 정확 일치 체크 추가")
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
    print("  ✅ 페이지 제목도 정확 일치 체크에 포함")
    print("  ✅ 디버깅 로그 추가")

if __name__ == "__main__":
    main()

