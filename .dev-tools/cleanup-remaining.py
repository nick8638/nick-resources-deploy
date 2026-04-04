import sys, os, re, glob
sys.stdout.reconfigure(encoding='utf-8')
docs_dir = r'C:\Users\Administrator\WorkBuddy\20260404071608\nick-fresh\docs'

count = 0
for md_file in glob.glob(os.path.join(docs_dir, '**', '*.md'), recursive=True):
    if '.vitepress' in md_file:
        continue
    
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    content = content.replace('-超过100T资料总站网站-doc.869hr.uk', '')
    
    if content != original:
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(content)
        count += 1
        rel_path = md_file.replace(docs_dir, '')
        print(f'Cleaned: {rel_path}')

# Fix robots.txt sitemap
robots_path = os.path.join(docs_dir, 'public', 'robots.txt')
if os.path.exists(robots_path):
    with open(robots_path, 'r', encoding='utf-8') as f:
        rc = f.read()
    new_rc = rc.replace('https://doc.869hr.uk/sitemap.xml', 'https://www.nick88.top/sitemap.xml')
    if new_rc != rc:
        with open(robots_path, 'w', encoding='utf-8') as f:
            f.write(new_rc)
        print('Fixed robots.txt sitemap -> https://www.nick88.top/sitemap.xml')

print(f'Total files cleaned: {count}')
