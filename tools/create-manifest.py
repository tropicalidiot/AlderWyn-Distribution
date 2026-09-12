"""Print a manifest with the actual ZIP hash and size; never uploads anything.
python3 scripts/create-manifest.py USERNAME AlderWyn-Distribution 0.0.1 PATH_TO_ZIP > manifest.json
"""
import hashlib, json, pathlib, re, sys
owner, repo, version, filename = sys.argv[1:5]
if not re.fullmatch(r'[A-Za-z0-9_.-]+', owner) or not re.fullmatch(r'[A-Za-z0-9_.-]+', repo):
    raise SystemExit('Invalid owner or repository')
if not re.fullmatch(r'(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[A-Za-z0-9.-]+)?', version):
    raise SystemExit('Use a semantic game version without a v prefix')
path = pathlib.Path(filename)
expected = f'AlderWyn-mac-v{version}.zip'
if path.name != expected: raise SystemExit(f'Expected ZIP name: {expected}')
with path.open('rb') as source: digest = hashlib.file_digest(source, 'sha256').hexdigest()
print(json.dumps({'launcherVersion':'0.1.0', 'gameVersion':version,
    'platforms':{'macos':{'url':f'https://github.com/{owner}/{repo}/releases/download/v{version}/{expected}', 'sha256':digest, 'size':path.stat().st_size}},
    'patchNotes':{'version':version,'url':f'https://raw.githubusercontent.com/{owner}/{repo}/main/patchnotes/{version}.md'}}, indent=2))
