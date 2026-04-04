import zipfile, xml.etree.ElementTree as ET, sys, json
sys.stdout.reconfigure(encoding='utf-8')

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

# Find data start: first digit-only entry after position 10 that starts a 4-element group
data_start = None
for i, t in enumerate(all_text):
    if t.isdigit() and i > 10:
        if i + 3 < len(all_text) and all_text[i+2].startswith('http'):
            data_start = i
            break

replacements = []
deletions = []
skipped = []

if data_start is not None:
    i = data_start
    while i + 3 < len(all_text):
        no = all_text[i]
        name = all_text[i+1]
        old_url = all_text[i+2]
        new_link = all_text[i+3]

        if not old_url.startswith('http'):
            i += 4
            continue

        if '删除' in str(new_link):
            deletions.append((no, name[:50], old_url))
        elif new_link.startswith('http'):
            replacements.append((no, name[:50], old_url, new_link))
        else:
            skipped.append((no, name[:50], old_url))

        i += 4

print(f'=== SUMMARY ===')
print(f'Replacements (new URL): {len(replacements)}')
print(f'Deletions (mark delete): {len(deletions)}')
print(f'Skipped (empty/no action): {len(skipped)}')

if replacements:
    print(f'\n=== REPLACEMENTS ({len(replacements)}) ===')
    for no, name, old, new in replacements:
        print(f'[{no}] {name}')
        print(f'    OLD: {old}')
        print(f'    NEW: {new}')

if deletions:
    print(f'\n=== DELETIONS ({len(deletions)}) ===')
    for no, name, old in deletions:
        print(f'[{no}] {name} -> {old}')

if skipped:
    print(f'\n=== SKIPPED ({len(skipped)}) - need attention ===')
    for no, name, old in skipped[:20]:
        print(f'[{no}] {name}')
    if len(skipped) > 20:
        print(f'  ... and {len(skipped)-20} more')
