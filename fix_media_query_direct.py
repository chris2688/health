import os
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 수정할 파일 목록
ALL_FILES = [
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


def fix_file(filepath):
    """미디어 쿼리 구조 직접 수정"""
    if not os.path.exists(filepath):
        print(f"  ⚠️ 파일 없음: {filepath}")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        original_lines = lines.copy()
        
        # 미디어 쿼리 시작과 끝 찾기
        media_start = None
        media_end = None
        
        for i, line in enumerate(lines):
            if '@media (max-width: 768px)' in line:
                media_start = i
            elif media_start is not None and line.strip() == '}' and i > media_start:
                # 중괄호 개수로 정확한 끝 찾기
                brace_count = 0
                for j in range(media_start, i + 1):
                    brace_count += lines[j].count('{')
                    brace_count -= lines[j].count('}')
                if brace_count == 0:
                    media_end = i
                    break
        
        if media_start is not None and media_end is not None:
            # 미디어 쿼리 안에 .hero-heading과 .cards-grid가 있는지 확인
            media_content = ''.join(lines[media_start:media_end+1])
            
            if '.hero-heading' not in media_content or '.cards-grid' not in media_content:
                # 미디어 쿼리 안에 추가
                # .main-nav.active .mobile-close-btn 다음에 추가
                insert_pos = None
                for i in range(media_start, media_end):
                    if '.main-nav.active .mobile-close-btn' in lines[i]:
                        # 다음 } 찾기
                        for j in range(i, media_end):
                            if lines[j].strip() == '}':
                                insert_pos = j
                                break
                        break
                
                if insert_pos:
                    # .hero-heading과 .cards-grid 추가
                    new_lines = [
                        '            \n',
                        '            .hero-heading {\n',
                        '                font-size: 32px;\n',
                        '            }\n',
                        '            \n',
                        '            .cards-grid {\n',
                        '                grid-template-columns: 1fr;\n',
                        '                gap: 20px;\n',
                        '            }\n'
                    ]
                    lines[insert_pos:insert_pos] = new_lines
                    media_end += len(new_lines)
            
            # 미디어 쿼리 밖에 있는 .hero-heading과 .cards-grid 제거
            for i in range(media_end + 1, len(lines)):
                if '.hero-heading' in lines[i] or '.cards-grid' in lines[i]:
                    # 이 블록 전체 제거
                    block_start = i
                    block_end = i
                    brace_count = 0
                    for j in range(i, len(lines)):
                        brace_count += lines[j].count('{')
                        brace_count -= lines[j].count('}')
                        if brace_count == 0 and '{' in lines[j]:
                            block_end = j
                            # 다음 } 찾기
                            for k in range(j, len(lines)):
                                if lines[k].strip() == '}':
                                    block_end = k
                                    break
                            break
                    
                    # 블록 제거
                    if block_end > block_start:
                        del lines[block_start:block_end+1]
                        break
        
        # 중복된 닫는 괄호 제거
        # 미디어 쿼리 다음에 바로 }가 있는 경우 제거
        if media_end is not None and media_end + 1 < len(lines):
            if lines[media_end + 1].strip() == '}':
                del lines[media_end + 1]
        
        if lines != original_lines:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            print(f"  ✅ {filepath} - 수정 완료")
            return True
        else:
            print(f"  ℹ️ {filepath} - 변경사항 없음")
            return False
            
    except Exception as e:
        print(f"  ❌ {filepath} - 오류: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """메인 실행"""
    print("=" * 60)
    print("🔧 미디어 쿼리 구조 직접 수정")
    print("=" * 60)
    print("\n💡 수정 사항:")
    print("   1. 미디어 쿼리 구조 정리")
    print("   2. PC에서 정상 작동 확인\n")
    
    print("📝 파일 수정 중...\n")
    fixed_files = []
    
    for file in ALL_FILES:
        if fix_file(file):
            fixed_files.append(file)
    
    print(f"\n✅ 총 {len(fixed_files)}개 파일 수정 완료!")
    print("=" * 60)


if __name__ == "__main__":
    main()

