import os
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 수정할 파일 목록
ALL_FILES = [
    "food-main.html",
    "exercise-main.html",
    "lifestyle-main.html",
    "news-main.html",
    "category-심혈관질환.html",
    "category-당뇨병.html",
    "category-관절근골격계.html",
    "category-호르몬내분비.html",
    "category-정신건강신경계.html",
    "category-소화기질환.html",
    "category-안과치과기타.html",
    "food-피해야할과일.html",
    "food-질환별식단.html",
    "food-모르면독이된다.html",
    "exercise-질환별운동가이드.html",
    "exercise-운동팁.html",
    "lifestyle-생활습관.html",
    "lifestyle-생활습관바꾸기팁.html",
]


def fix_media_queries_direct(filepath):
    """미디어 쿼리 구조 직접 수정"""
    if not os.path.exists(filepath):
        print(f"  ⚠️ 파일 없음: {filepath}")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        original_lines = lines.copy()
        new_lines = []
        i = 0
        in_media_query = False
        media_brace_count = 0
        
        while i < len(lines):
            line = lines[i]
            
            # 미디어 쿼리 시작 감지
            if '@media (max-width: 768px)' in line:
                in_media_query = True
                media_brace_count = 0
                new_lines.append(line)
                i += 1
                continue
            
            # 미디어 쿼리 안에서
            if in_media_query:
                # 중괄호 카운트
                media_brace_count += line.count('{')
                media_brace_count -= line.count('}')
                
                # 빈 CSS 블록 제거
                if '.main-nav.active' in line and i + 1 < len(lines):
                    # 다음 몇 줄 확인
                    next_lines = ''.join(lines[i:min(i+10, len(lines))])
                    if re.match(r'\.main-nav\.active\s*\{[^}]*?\}', next_lines, re.DOTALL):
                        # 빈 블록이면 건너뛰기
                        brace_count = 0
                        skip_to = i
                        for j in range(i, min(i+20, len(lines))):
                            brace_count += lines[j].count('{')
                            brace_count -= lines[j].count('}')
                            if brace_count == 0 and '{' in lines[j]:
                                skip_to = j + 1
                                break
                        i = skip_to
                        continue
                
                # 미디어 쿼리 닫힘
                if media_brace_count == 0 and '}' in line:
                    in_media_query = False
                    new_lines.append(line)
                    i += 1
                    continue
                
                new_lines.append(line)
                i += 1
            else:
                # 미디어 쿼리 밖
                # 미디어 쿼리 밖에 있는 모바일 전용 스타일 제거
                # .health-cards-grid { grid-template-columns: 1fr; } 같은 것
                if '.health-cards-grid' in line and 'grid-template-columns: 1fr' in ''.join(lines[i:i+5]):
                    # 이 블록이 미디어 쿼리 밖에 있는지 확인
                    # 미디어 쿼리 밖이면 제거
                    # 하지만 미디어 쿼리 안에 있는 것은 유지
                    # 일단 건너뛰기
                    brace_count = 0
                    skip_to = i
                    for j in range(i, min(i+10, len(lines))):
                        brace_count += lines[j].count('{')
                        brace_count -= lines[j].count('}')
                        if brace_count == 0 and '{' in lines[j]:
                            skip_to = j + 1
                            break
                    i = skip_to
                    continue
                
                new_lines.append(line)
                i += 1
        
        content = ''.join(new_lines)
        
        # 추가 정리: 빈 CSS 블록 제거
        content = re.sub(
            r'\.main-nav\.active\s*\{\s*\}',
            '',
            content,
            flags=re.MULTILINE
        )
        
        if content != ''.join(original_lines):
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ {filepath} - 미디어 쿼리 수정 완료")
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
    print("🔧 모든 파일 미디어 쿼리 구조 직접 수정")
    print("=" * 60)
    print("\n💡 수정 사항:")
    print("   1. 빈 CSS 블록 제거")
    print("   2. 미디어 쿼리 밖의 모바일 스타일 제거\n")
    
    print("📝 파일 수정 중...\n")
    fixed_files = []
    
    for file in ALL_FILES:
        if fix_media_queries_direct(file):
            fixed_files.append(file)
    
    print(f"\n✅ 총 {len(fixed_files)}개 파일 수정 완료!")
    print("=" * 60)


if __name__ == "__main__":
    main()

