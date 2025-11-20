import os
import glob
import re
import sys
import io

# UTF-8 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 개선된 키워드 매핑 (더 정확하고 중복 허용)
IMPROVED_KEYWORD_MAP = {
    # 심혈관 질환 (cardiovascular)
    '고혈압': 'cardiovascular',
    '고지혈증': 'cardiovascular',
    '콜레스테롤': 'cardiovascular',
    '심근경색': 'cardiovascular',
    '협심증': 'cardiovascular',
    '뇌졸중': 'cardiovascular',
    '동맥경화': 'cardiovascular',
    '심장': 'cardiovascular',
    
    # 당뇨병 (diabetes)
    '당뇨': 'diabetes',
    '공복혈당': 'diabetes',
    '인슐린': 'diabetes',
    '혈당': 'diabetes',
    '당뇨병': 'diabetes',
    '당뇨합병증': 'diabetes',
    
    # 관절/근골격계 (musculoskeletal)
    '관절염': 'musculoskeletal',
    '퇴행성관절염': 'musculoskeletal',
    '오십견': 'musculoskeletal',
    '유착성관절낭염': 'musculoskeletal',
    '허리디스크': 'musculoskeletal',
    '목디스크': 'musculoskeletal',
    '골다공증': 'musculoskeletal',
    '관절': 'musculoskeletal',
    '근골격': 'musculoskeletal',
    
    # 소화기 질환 (digestive)
    '위염': 'digestive',
    '위궤양': 'digestive',
    '역류성식도염': 'digestive',
    '역류': 'digestive',
    '식도염': 'digestive',
    '과민성대장증후군': 'digestive',
    '대장': 'digestive',
    '지방간': 'digestive',
    '간기능': 'digestive',
    '소화기': 'digestive',
    
    # 호르몬/내분비 (endocrine)
    '갑상선': 'endocrine',
    '갱년기': 'endocrine',
    '갱년기증후군': 'endocrine',
    '대사증후군': 'endocrine',
    '호르몬': 'endocrine',
    '내분비': 'endocrine',
    
    # 정신 건강/신경계 (neuroscience)
    '우울증': 'neuroscience',
    '번아웃': 'neuroscience',
    '수면장애': 'neuroscience',
    '불면증': 'neuroscience',
    '치매': 'neuroscience',
    '경도인지장애': 'neuroscience',
    '이명': 'neuroscience',
    '어지럼증': 'neuroscience',
    '현훈': 'neuroscience',
    '정신건강': 'neuroscience',
    '신경계': 'neuroscience',
    
    # 안과/치과/기타 (eyes-dental)
    '백내장': 'eyes-dental',
    '녹내장': 'eyes-dental',
    '치주염': 'eyes-dental',
    '치아손실': 'eyes-dental',
    '치주질환': 'eyes-dental',
    '비만': 'eyes-dental',
    '체형변화': 'eyes-dental',
}

def fix_title_alignment(filepath):
    """페이지 제목 중앙정렬 CSS 추가"""
    print(f"Processing: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # .page-title 스타일 찾기
        page_title_pattern = r'\.page-title\s*\{[^}]*\}'
        page_title_match = re.search(page_title_pattern, content)
        
        if page_title_match:
            # text-align: center 추가
            page_title_style = page_title_match.group(0)
            if 'text-align' not in page_title_style:
                # 마지막 } 앞에 text-align 추가
                new_style = page_title_style[:-1] + '    text-align: center;\n}'
                content = content.replace(page_title_style, new_style)
                print(f"  ✅ 제목 중앙정렬 추가")
            else:
                # 이미 있으면 수정
                content = re.sub(
                    r'text-align:\s*[^;]+;',
                    'text-align: center;',
                    content
                )
                print(f"  ✅ 제목 중앙정렬 수정")
        else:
            # .page-title 스타일이 없으면 추가
            # </style> 전에 추가
            page_title_css = '''
        .page-title {
            text-align: center;
        }
'''
            if '</style>' in content:
                content = content.replace('</style>', page_title_css + '</style>')
                print(f"  ✅ 제목 중앙정렬 CSS 추가")
        
        # .page-header도 중앙정렬
        page_header_pattern = r'\.page-header\s*\{[^}]*\}'
        page_header_match = re.search(page_header_pattern, content)
        
        if page_header_match:
            page_header_style = page_header_match.group(0)
            if 'text-align' not in page_header_style:
                new_style = page_header_style[:-1] + '    text-align: center;\n}'
                content = content.replace(page_header_style, new_style)
        
        # 키워드 매핑 개선
        old_keyword_map_pattern = r"const keywordMap = \{.*?\};"
        
        # 개선된 키워드 맵 생성
        keyword_map_js = "const keywordMap = {\n"
        for keyword, slug in IMPROVED_KEYWORD_MAP.items():
            keyword_map_js += f"                    '{keyword}': '{slug}',\n"
        keyword_map_js += "                };"
        
        if re.search(old_keyword_map_pattern, content, re.DOTALL):
            content = re.sub(old_keyword_map_pattern, keyword_map_js, content, flags=re.DOTALL)
            print(f"  ✅ 키워드 매핑 개선")
        
        # 파일 저장
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
        
    except Exception as e:
        print(f"  ❌ 오류: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=" * 60)
    print("🎯 제목 중앙정렬 및 카테고리 매핑 개선")
    print("=" * 60)
    
    # news-main.html과 모든 sub-*.html 파일 처리
    target_files = ['news-main.html'] + glob.glob("sub-*.html")
    
    print(f"\n📁 총 {len(target_files)}개 파일")
    
    success_count = 0
    for file in target_files:
        if fix_title_alignment(file):
            success_count += 1
    
    print("\n" + "=" * 60)
    print(f"✅ 완료: {success_count}/{len(target_files)}개 파일")
    print("=" * 60)
    print("\n📝 개선사항:")
    print("  ✅ 페이지 제목 중앙정렬")
    print("  ✅ 키워드 매핑 개선 (더 정확하고 중복 허용)")
    print("  ✅ 역류성 식도염 → digestive (소화기 질환)")

if __name__ == "__main__":
    main()

