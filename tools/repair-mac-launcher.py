"""Create and verify a development-signed launcher using Apple's native tools.
Run manually on macOS or through the manual packaging check workflow.
Does not notarize, strip quarantine, or change Gatekeeper settings.
"""
import hashlib, json, os, pathlib, plistlib, subprocess, sys, time, urllib.request

rid, expected_hash = sys.argv[1:3]
assert sys.platform == 'darwin', 'Native macOS signing is required'
assert rid in ('osx-x64', 'osx-arm64')
assert os.uname().machine == {'osx-x64':'x86_64','osx-arm64':'arm64'}[rid]
root=pathlib.Path.cwd()/'mac-package';root.mkdir(exist_ok=False)
old=root/'original.zip'
url=f'https://github.com/tropicalidiot/AlderWyn-Distribution/releases/download/v0.1.0/AlderWyn-Launcher-v0.1.0-{rid}.zip'
urllib.request.urlretrieve(url,old)
assert hashlib.sha256(old.read_bytes()).hexdigest()==expected_hash, 'Original release hash mismatch'
subprocess.run(['/usr/bin/ditto','-x','-k',str(old),str(root)],check=True)
app=root/'AlderWyn Launcher.app';contents=app/'Contents';host=contents/'MacOS/AlderWyn.Launcher'
metadata=plistlib.loads((contents/'Info.plist').read_bytes());metadata['CFBundleVersion']='2'
(contents/'Info.plist').write_bytes(plistlib.dumps(metadata))
entitlements=root/'Launcher.entitlements'
entitlements.write_bytes(plistlib.dumps({'com.apple.security.cs.allow-jit':True}))
# macOS treats MacOS/ as nested executable code. Put managed assemblies and
# data in Resources/, native libraries in Frameworks/, and retain relative
# links so .NET still finds its neighboring files without custom probing.
(contents/'Frameworks').mkdir(exist_ok=True)
for path in sorted((contents/'MacOS').iterdir()):
    if path == host or path.is_symlink():continue
    if path.is_file():
        with path.open('rb') as f:magic=f.read(4)
        is_native=magic in (b'\xcf\xfa\xed\xfe',b'\xfe\xed\xfa\xcf',b'\xca\xfe\xba\xbe')
    else:is_native=False
    if is_native and path.suffix != '.dylib':continue
    directory='Frameworks' if is_native else 'Resources'
    destination=contents/directory/path.name
    path.rename(destination)
    path.symlink_to('../'+directory+'/'+path.name, target_is_directory=destination.is_dir())
    if is_native:
        (contents/'Resources'/path.name).symlink_to('../Frameworks/'+path.name)
native=[]
for path in sorted(app.rglob('*')):
    if not path.is_file() or path.is_symlink():continue
    with path.open('rb') as f:magic=f.read(4)
    if magic in (b'\xcf\xfa\xed\xfe',b'\xfe\xed\xfa\xcf',b'\xca\xfe\xba\xbe'):
        path.chmod(0o755)
        if path != host:subprocess.run(['/usr/bin/codesign','--force','--sign','-',str(path)],check=True)
        native.append(path)
subprocess.run(['/usr/bin/codesign','--force','--sign','-','--entitlements',str(entitlements),str(app)],check=True)
subprocess.run(['/usr/bin/codesign','--verify','--deep','--strict','--verbose=2',str(app)],check=True)
output=pathlib.Path.cwd()/'verified-output';output.mkdir()
# Exercise the actual Mac runtime and native rendering libraries.
subprocess.run([str(host),'--render',str(output/'direct-launch.png')],check=True,timeout=90)
assert (output/'direct-launch.png').stat().st_size>10000
# Exercise LaunchServices separately, using the same app entry point as Finder.
subprocess.run(['/usr/bin/open','-n','-a',str(app),'--args','--render',str(output/'launchservices.png')],check=True)
for _ in range(180):
    image=output/'launchservices.png'
    if image.exists() and image.stat().st_size>10000 and image.read_bytes().endswith(b'\x00\x00\x00\x00IEND\xaeB\x60\x82'):break
    time.sleep(.5)
assert image.exists() and image.read_bytes().endswith(b'\x00\x00\x00\x00IEND\xaeB\x60\x82'), 'LaunchServices did not finish the render'
# Resource seals must still verify after launch.
subprocess.run(['/usr/bin/codesign','--verify','--deep','--strict',str(app)],check=True)
archive=output/f'AlderWyn-Launcher-v0.1.0-{rid}-macfix1.zip'
subprocess.run(['/usr/bin/ditto','-c','-k','--sequesterRsrc','--keepParent',str(app),str(archive)],check=True)
# Verify the ZIP after an actual Mac extraction, including relative links.
roundtrip=root/'roundtrip'
subprocess.run(['/usr/bin/ditto','-x','-k',str(archive),str(roundtrip)],check=True)
subprocess.run(['/usr/bin/codesign','--verify','--deep','--strict',str(roundtrip/app.name)],check=True)
digest=hashlib.sha256(archive.read_bytes()).hexdigest()
report={'rid':rid,'macOS':subprocess.check_output(['sw_vers','-productVersion'],text=True).strip(),'cpu':os.uname().machine,'bundleBuild':'2','nativeBinariesSigned':len(native),'appleCodesignStrictVerification':True,'nativeDirectLaunch':True,'launchServicesRender':True,'sha256':digest,'bytes':archive.stat().st_size,'signature':'ad-hoc development signature','developerID':False,'notarized':False,'browserQuarantineGatekeeperAcceptanceTested':False}
(output/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report),flush=True)
