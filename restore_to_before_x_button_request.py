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


def restore_file(filepath):
    """파일을 X 버튼 요청 이전 상태로 복구"""
    if not os.path.exists(filepath):
        print(f"  ⚠️ 파일 없음: {filepath}")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 1. 깨진 mobile-close-btn CSS 수정
        content = re.sub(
            r'/\* 모바일 닫기 버튼 \*/\s*ppx;[^}]*?\}',
            '''/* 모바일 닫기 버튼 */
        .mobile-close-btn {
            display: none;
            background: none;
            border: none;
            color: white;
            font-size: 24px;
            cursor: pointer;
            padding: 8px 12px;
            position: absolute;
            top: 15px;
            right: 15px;
            z-index: 1001;
            line-height: 1;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            transition: all 0.3s;
        }
        
        .mobile-close-btn:hover {
            background: rgba(255,255,255,0.2);
            transform: rotate(90deg);
        }''',
            content,
            flags=re.DOTALL
        )
        
        # 2. 모든 중복된 모바일 미디어 쿼리 제거 및 단순화
        # 애니메이션 제거 (opacity, transform, transition, max-height 등)
        # 단순한 display: none/flex만 사용
        
        # 중복된 @media 블록 제거
        media_blocks = list(re.finditer(r'@media\s*\(max-width:\s*768px\)\s*\{', content))
        if len(media_blocks) > 1:
            # 첫 번째는 유지, 나머지는 제거
            # header-content가 포함된 첫 번째 미디어 쿼리만 유지
            first_header_media = None
            for i, match in enumerate(media_blocks):
                start = match.start()
                if i < len(media_blocks) - 1:
                    end = media_blocks[i+1].start()
                else:
                    end = content.find('</style>', start)
                    if end == -1:
                        end = len(content)
                
                block_content = content[start:end]
                if '.header-content' in block_content and first_header_media is None:
                    first_header_media = i
                    break
            
            # 첫 번째 이후의 중복 제거
            if first_header_media is not None and len(media_blocks) > first_header_media + 1:
                # 첫 번째 블록의 끝 찾기
                first_start = media_blocks[first_header_media].start()
                brace_count = 0
                first_block_end = first_start
                for i in range(first_start, len(content)):
                    if content[i] == '{':
                        brace_count += 1
                    elif content[i] == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            first_block_end = i + 1
                            break
                
                # 두 번째 header-content 미디어 쿼리 찾아서 제거
                for i in range(first_header_media + 1, len(media_blocks)):
                    start = media_blocks[i].start()
                    if i < len(media_blocks) - 1:
                        end = media_blocks[i+1].start()
                    else:
                        end = content.find('</style>', start)
                        if end == -1:
                            end = len(content)
                    
                    block_content = content[start:end]
                    if '.header-content' in block_content:
                        # 이 블록 제거
                        brace_count = 0
                        block_end = start
                        for j in range(start, len(content)):
                            if content[j] == '{':
                                brace_count += 1
                            elif content[j] == '}':
                                brace_count -= 1
                                if brace_count == 0:
                                    block_end = j + 1
                                    break
                        content = content[:start] + content[block_end:]
                        break
        
        # 3. 모바일 미디어 쿼리에서 애니메이션 제거 및 단순화
        # 패턴: @media (max-width: 768px) { ... .main-nav { ... } ... }
        mobile_nav_simple = """
            .main-nav {
                display: none;
                position: absolute;
                top: 100%;
                left: 0;
                right: 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                flex-direction: column;
                padding: 20px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.2);
                z-index: 1000;
            }
            
            .main-nav.active {
                display: flex;
            }
            
            .nav-item {
                padding: 15px 20px;
                text-align: center;
            }
            
            .mobile-menu-btn {
                display: block;
            }
            
            .main-nav.active .mobile-close-btn {
                display: block;
            }
"""
        
        # 모바일 미디어 쿼리에서 main-nav 관련 부분 교체
        if '@media (max-width: 768px)' in content:
            # .main-nav 스타일 부분 찾아서 교체
            pattern = r'(@media\s*\(max-width:\s*768px\)[^}]*?\.header-content[^}]*?\}[^}]*?\.logo-image[^}]*?\}[^}]*?)(\.main-nav[^}]*?\}[^}]*?\.main-nav\.active[^}]*?\}[^}]*?\.nav-item[^}]*?\}[^}]*?\.mobile-menu-btn[^}]*?\}[^}]*?\.mobile-close-btn[^}]*?\}[^}]*?\.main-nav\.active[^}]*?\.mobile-close-btn[^}]*?\}[^}]*?)(\.main-nav\.active\s*~\s*\.mobile-close-btn[^}]*?\}[^}]*?)?'
            
            content = re.sub(
                pattern,
                r'\1' + mobile_nav_simple,
                content,
                flags=re.DOTALL
            )
            
            # 애니메이션 관련 속성 제거
            content = re.sub(
                r'opacity:\s*0;[^}]*?transform:\s*translateY\([^)]*\);[^}]*?transition:[^}]*?max-height:\s*0;[^}]*?overflow:\s*hidden;',
                '',
                content
            )
            content = re.sub(
                r'opacity:\s*1;[^}]*?transform:\s*translateY\([^)]*\);[^}]*?max-height:\s*\d+px;',
                '',
                content
            )
            content = re.sub(
                r'opacity:\s*0;[^}]*?transform:\s*translateY\([^)]*\);[^}]*?transition:[^}]*?',
                '',
                content
            )
            content = re.sub(
                r'opacity:\s*1;[^}]*?transform:\s*translateY\([^)]*\);',
                '',
                content
            )
            content = re.sub(
                r'opacity:\s*1;[^}]*?transform:\s*scale\([^)]*\);',
                '',
                content
            )
        
        # 4. HTML 구조 확인 및 수정
        # X 버튼이 메뉴 안에 있어야 함
        if '<nav class="main-nav" id="mainNav">' in content:
            # nav 안에 X 버튼이 없으면 추가
            if '<button class="mobile-close-btn" id="mobileCloseBtn">✕</button>' not in content or '<nav class="main-nav" id="mainNav">' not in content.split('<button class="mobile-close-btn" id="mobileCloseBtn">✕</button>')[0]:
                # nav 안에 X 버튼 추가
                content = re.sub(
                    r'(<nav class="main-nav" id="mainNav">)',
                    r'\1\n                <button class="mobile-close-btn" id="mobileCloseBtn">✕</button>',
                    content
                )
            
            # nav 밖에 있는 X 버튼 제거
            content = re.sub(
                r'(</nav>\s*)(<button class="mobile-close-btn" id="mobileCloseBtn">✕</button>)',
                r'\1',
                content
            )
        
        # 5. JavaScript 확인
        if 'mobileCloseBtn' not in content or 'addEventListener' not in content.split('mobileCloseBtn')[1] if 'mobileCloseBtn' in content else True:
            # JavaScript 추가
            if '</script>' in content:
                close_js = '''
        document.getElementById('mobileCloseBtn').addEventListener('click', function() {
            document.getElementById('mainNav').classList.remove('active');
        });'''
                # 이미 있는지 확인
                if 'mobileCloseBtn' not in content or 'addEventListener' not in content:
                    content = re.sub(
                        r'(</script>)',
                        close_js + '\n    \1',
                        content,
                        count=1
                    )
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ {filepath} - 복구 완료")
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
    print("🔧 X 버튼 요청 이전 상태로 복구")
    print("=" * 60)
    print("\n💡 복구 사항:")
    print("   1. 깨진 CSS 수정")
    print("   2. 중복 미디어 쿼리 제거")
    print("   3. 애니메이션 제거 (단순 메뉴)")
    print("   4. X 버튼: 메뉴 안에 위치")
    print("   5. PC: 햄버거 바 숨김\n")
    
    print("📝 파일 수정 중...\n")
    fixed_files = []
    
    for file in ALL_FILES:
        if restore_file(file):
            fixed_files.append(file)
    
    print(f"\n✅ 총 {len(fixed_files)}개 파일 복구 완료!")
    print("=" * 60)


if __name__ == "__main__":
    main()

