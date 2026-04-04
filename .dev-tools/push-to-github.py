import sys, os, json, base64, glob, urllib.request, urllib.error
sys.stdout.reconfigure(encoding='utf-8')

# === CONFIGURATION ===
# Edit these before running:
docs_dir = './nick-fresh/docs'          # Path to your VitePress docs directory
token = 'YOUR_GITHUB_PAT_TOKEN_HERE'   # Fine-grained PAT token (Contents: Read and write)
repo = 'nick8638/nick-resources-deploy' # Your GitHub repo

api_base = f'https://api.github.com/repos/{repo}/contents'
headers = {'Authorization': f'Bearer {token}', 'Accept': 'application/vnd.github.v3+json'}

# Collect all files to push
files_to_push = []
for root, dirs, files in os.walk(docs_dir):
    # Skip .vitepress/dist and .git
    rel_root = os.path.relpath(root, docs_dir).replace('\\', '/')
    skip = False
    for part in ['.vitepress', '.git']:
        if part in rel_root:
            skip = True
            break
    if skip:
        continue
    for fname in files:
        full_path = os.path.join(root, fname)
        if rel_root == '.':
            rel_path = fname
        else:
            rel_path = rel_root + '/' + fname
        files_to_push.append((rel_path, full_path))

print(f'Files to push: {len(files_to_push)}')

success_count = 0
error_count = 0
error_files = []

for idx, (rel_path, full_path) in enumerate(files_to_push):
    api_url = f'{api_base}/{rel_path}'
    
    try:
        with open(full_path, 'rb') as f:
            content_b64 = base64.b64encode(f.read()).decode()
        
        # Get current sha
        req = urllib.request.Request(api_url, headers=headers)
        try:
            with urllib.request.urlopen(req) as resp:
                file_info = json.loads(resp.read())
                sha = file_info.get('sha', '')
        except urllib.error.HTTPError:
            sha = ''  # New file
        
        data = {
            'message': f'update: {rel_path}',
            'content': content_b64,
            'sha': sha,
            'branch': 'main'
        }
        
        req2 = urllib.request.Request(api_url,
            data=json.dumps(data).encode(),
            headers={**headers, 'Content-Type': 'application/json'},
            method='PUT')
        with urllib.request.urlopen(req2):
            success_count += 1
            
    except Exception as e:
        error_count += 1
        err_msg = str(e)[:100]
        error_files.append(rel_path)
        if error_count <= 5:
            print(f'Error [{rel_path}]: {err_msg}')

print(f'\n=== DONE ===')
print(f'Success: {success_count}')
print(f'Errors:  {error_count}')
if error_count > 5:
    print(f'Total error files: {len(error_files)}')
