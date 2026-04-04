import zipfile, xml.etree.ElementTree as ET, sys, os, re, glob, json
sys.stdout.reconfigure(encoding='utf-8')

# ===== Step 1: Parse the docx to get replacement map =====
docx = r'C:\Users\Administrator\WorkBuddy\20260404071608\网盘转存名单.docx'
with zipfile.ZipFile(docx) as z:
    with z.open('word/document.xml') as f:
        content = f.read().decode('utf-8')
        ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        root = ET.fromstring(content)
        texts = root.findall('.//w:t', ns)

all_text = []
for t in texts:
    text = (t.text or '').strip()
    if text:
        all_text.append(text)

data_start = None
for i, t in enumerate(all_text):
    if t.isdigit() and i > 10:
        if i + 3 < len(all_text) and all_text[i+2].startswith('http'):
            data_start = i
            break

replacements = {}  # old_url -> new_url
deletions = set()   # old_urls to delete

if data_start is not None:
    i = data_start
    while i + 3 < len(all_text):
        no = all_text[i]
        name = all_text[i+1]
        old_url = all_text[i+2]
        new_link = all_text[i+3]

        if old_url.startswith('http'):
            if '删除' in str(new_link):
                deletions.add(old_url)
            elif new_link.startswith('http'):
                replacements[old_url] = new_link

        i += 4

print(f'Parsed: {len(replacements)} replacements, {len(deletions)} deletions')

# ===== Step 2: Apply to all .md files in nick-fresh/docs (excluding dist) =====
docs_dir = r'C:\Users\Administrator\WorkBuddy\20260404071608\nick-fresh\docs'
files_modified = 0
total_replacements_made = 0
total_deletions_made = 0

for md_file in glob.glob(os.path.join(docs_dir, '**', '*.md'), recursive=True):
    # Skip dist directory
    if '\\.vitepress\\' in md_file or md_file.endswith('\\dist\\'):
        continue

    try:
        with open(md_file, 'r', encoding='utf-8') as f:
            original_content = f.read()

        content = original_content
        changes_made = False

        # First handle deletions - remove lines containing these URLs
        for del_url in deletions:
            # Match lines that contain this URL (with or without surrounding text)
            # Pattern: any line containing this URL and possibly the 869hr.uk suffix
            pattern = r'.*' + re.escape(del_url) + r'.*\n?'
            new_content = re.sub(pattern, '', content)
            if new_content != content:
                content = new_content
                total_deletions_made += 1
                changes_made = True

        # Then handle replacements
        for old_url, new_url in replacements.items():
            if old_url in content:
                count = content.count(old_url)
                content = content.replace(old_url, new_url)
                total_replacements_made += count
                changes_made = True

                # Also clean up "超过100T资料总站网站-doc.869hr.uk" suffix if present after the link
                # This might be attached to the resource name part
                content = content.replace('-超过100T资料总站网站-doc.869hr.uk', '')

        if changes_made:
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(content)
            files_modified += 1
            rel_path = md_file.replace(docs_dir, '')
            print(f'  Modified: {rel_path}')

    except Exception as e:
        print(f'  Error processing {md_file}: {e}')

print(f'\n=== RESULTS ===')
print(f'Files modified: {files_modified}')
print(f'Total replacements: {total_replacements_made}')
print(f'Total lines deleted: {total_deletions_made}')
