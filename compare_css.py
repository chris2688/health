import re

# sub-diabetes.html과 category-cardiovascular.html의 CSS 비교

with open('sub-diabetes.html', 'r', encoding='utf-8') as f:
    sub_content = f.read()

with open('category-cardiovascular.html', 'r', encoding='utf-8') as f:
    cat_content = f.read()

# CSS 추출
sub_css_match = re.search(r'<style>(.*?)</style>', sub_content, re.DOTALL)
cat_css_match = re.search(r'<style>(.*?)</style>', cat_content, re.DOTALL)

if sub_css_match and cat_css_match:
    sub_css = sub_css_match.group(1)
    cat_css = cat_css_match.group(1)
    
    # body 스타일 비교
    print("=== BODY 스타일 비교 ===")
    sub_body = re.search(r'body \{([^}]+)\}', sub_css)
    cat_body = re.search(r'body \{([^}]+)\}', cat_css)
    print("sub-diabetes body:", sub_body.group(1) if sub_body else "없음")
    print("category body:", cat_body.group(1) if cat_body else "없음")
    
    # .site-main 스타일 비교
    print("\n=== .site-main 스타일 비교 ===")
    sub_main = re.search(r'\.site-main \{([^}]+)\}', sub_css)
    cat_main = re.search(r'\.site-main \{([^}]+)\}', cat_css)
    print("sub-diabetes .site-main:", sub_main.group(1) if sub_main else "없음")
    print("category .site-main:", cat_main.group(1) if cat_main else "없음")
    
    # .back-button 스타일 비교
    print("\n=== .back-button 스타일 비교 ===")
    sub_back = re.search(r'\.back-button \{([^}]+)\}', sub_css)
    cat_back = re.search(r'\.back-button \{([^}]+)\}', cat_css)
    print("sub-diabetes .back-button:", sub_back.group(1) if sub_back else "없음")
    print("category .back-button:", cat_back.group(1) if cat_back else "없음")
    
    print("\n비교 완료!")

