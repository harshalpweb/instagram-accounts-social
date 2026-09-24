"""Publish only the approved September 25 release with exact-hash media."""
import argparse,hashlib,json,os,subprocess,sys,time
from datetime import datetime,timezone
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
import ig_common as ig
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
STATE=HERE/'receipts.json'
BASE=ig.graph_base()
CONFIG={'harshal':('HYPE_TINGLES','harshalbuilds'),'anime':('ANIME_EKAYA','anime.ekaya'),'nuvarel':('NUVAREL','nuvarel_')}
def now(): return datetime.now(timezone.utc).isoformat(timespec='seconds')
def epoch(stamp): return datetime.fromisoformat(stamp.replace('Z','+00:00')).timestamp()
def remaining_gap(last,clock=None): return max(0,120-((clock if clock is not None else time.time())-last))
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def validate(release):
 assert set(release['accounts'])==set(CONFIG),'Wrong account set'
 ids=[p['id'] for pieces in release['accounts'].values() for p in pieces]
 assert len(ids)==9 and len(set(ids))==9,'Post IDs must be globally unique'
 for key,items in release['accounts'].items():
  assert len(items)==3 and [p['type'] for p in items]==['REELS','CAROUSEL','REELS']
  assert len({p['id'] for p in items})==3
  for p in items:
   assert len(p['assets'])==(5 if p['type']=='CAROUSEL' else 1)
   assert p['caption'].strip() and p['qa_verdict']=='PASS'
   for a in p['assets']:
    path=(ROOT/a['path']).resolve();assert path.is_relative_to(HERE.resolve()),'Asset outside batch'
    assert path.exists() and sha(path)==a['sha256'],'Asset hash mismatch'
def save(state,commit=False):
 STATE.write_text(json.dumps(state,indent=2),encoding='utf-8')
 if commit:
  rel=str(STATE.relative_to(ROOT)).replace('\\','/')
  subprocess.run(['git','add','--',rel],cwd=ROOT,check=True)
  staged=subprocess.check_output(['git','diff','--cached','--name-only'],cwd=ROOT,text=True).splitlines()
  assert not staged or staged==[rel],f'Unexpected staged paths: {staged}'
  if staged:
   subprocess.run(['git','commit','-m','Record Sep25 batch publication state','--',rel],cwd=ROOT,check=True,stdout=subprocess.DEVNULL)
   subprocess.run(['git','pull','--rebase','origin','master'],cwd=ROOT,check=True,stdout=subprocess.DEVNULL)
   subprocess.run(['git','push','origin','HEAD:master'],cwd=ROOT,check=True)
def get(account,path,params=None): return ig.api_get(path,account['token'],params=params,base=BASE)
def post(account,path,data): return ig.api_post(path,account['token'],data=data,base=BASE)
def recent(account): return get(account,account['id']+'/media',{'fields':'id,caption,permalink,timestamp,media_type','limit':50}).get('data',[])
def match(items,caption): return [p for p in items if p.get('caption','').strip()==caption.strip()]
def poll(account,ident):
 end=time.monotonic()+600
 while time.monotonic()<end:
  result=get(account,ident,{'fields':'status_code'})
  code=result.get('status_code')
  if code=='FINISHED': return
  if code in ('ERROR','EXPIRED','PUBLISHED'): raise RuntimeError(f'Container {ident}: {code}')
  time.sleep(3)
 raise RuntimeError(f'Processing timeout {ident}; not republished')
def verify_post(account,media_id,piece):
 actual=get(account,media_id,{'fields':'id,caption,permalink,timestamp,media_type,children{id,media_type}'})
 expected='CAROUSEL_ALBUM' if piece['type']=='CAROUSEL' else 'VIDEO'
 assert actual.get('media_type')==expected,(actual.get('media_type'),expected)
 assert actual.get('caption','').strip()==piece['caption'].strip(),'Caption mismatch'
 if piece['type']=='CAROUSEL':
  children=actual.get('children',{}).get('data',[])
  assert len(children)==5 and all(c.get('media_type')=='IMAGE' for c in children),'Not a five-image carousel'
 assert actual.get('permalink'),'Missing live permalink'
 return actual
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--dry-run',action='store_true');args=ap.parse_args()
 release=json.loads((HERE/'release.json').read_text(encoding='utf-8-sig'));validate(release)
 if args.dry_run: print('Release schema, scope, account order and all asset hashes PASS');return
 assert release['approved'] is True,'Release not cleared'
 assert os.environ.get('GITHUB_REF_NAME')=='master','Default branch required'
 state=json.loads(STATE.read_text()) if STATE.exists() else {'batch':'2026-09-25-distinct-voices','posts':{}}
 accounts={};last={}
 for key,(suffix,expected) in CONFIG.items():
  token=os.environ['IG_ACCESS_TOKEN_'+suffix];ident=os.environ['IG_USER_ID_'+suffix];ig.register_secret(token)
  account={'token':token,'id':ident};profile=get(account,ident,{'fields':'id,username'})
  assert profile['username']==expected,f'Wrong target identity for {key}'
  accounts[key]=account;items=recent(account);account['recent']=items
  last[key]=max([epoch(p['timestamp']) for p in items if p.get('timestamp')]+[p.get('acknowledged_epoch',epoch(p['acknowledged_at'])+1) for p in state['posts'].values() if p.get('account')==key and p.get('acknowledged_at')]+[0])
  print('Verified target @'+expected,flush=True)
 # Three waves: each account Reel A -> native carousel -> Reel B.
 for wave in range(3):
  for key,account in accounts.items():
   piece=release['accounts'][key][wave];pid=piece['id'];receipt=state['posts'].setdefault(pid,{'account':key,'status':'new'})
   assert receipt['account']==key,'Receipt account mismatch'
   if receipt.get('status')=='published':
    verify_post(account,receipt['media_id'],piece);print('Already published; skipped '+pid,flush=True);continue
   matches=match(recent(account),piece['caption'])
   if len(matches)>1: raise RuntimeError('Ambiguous existing caption: '+pid)
   if matches:
    actual=verify_post(account,matches[0]['id'],piece);receipt.update(status='published',media_id=actual['id'],permalink=actual['permalink'],posted_at=actual['timestamp'],reconciled=True);last[key]=max(last[key],epoch(actual['timestamp']));save(state,True);continue
   if receipt.get('status')=='publishing': raise RuntimeError('Uncertain earlier publication; operator reconciliation required for '+pid)
   raw=f"https://raw.githubusercontent.com/{os.environ['GITHUB_REPOSITORY']}/{os.environ['GITHUB_SHA']}"
   if not receipt.get('container_id'):
    if piece['type']=='REELS':
     payload={'media_type':'REELS','video_url':raw+'/'+piece['assets'][0]['path'],'caption':piece['caption'],'share_to_feed':'true'}
     receipt['container_id']=post(account,account['id']+'/media',payload)['id'];save(state)
    else:
     children=receipt.setdefault('children',[])
     for asset in piece['assets'][len(children):]:
      children.append(post(account,account['id']+'/media',{'image_url':raw+'/'+asset['path'],'is_carousel_item':'true'})['id']);save(state)
     for ident in children: poll(account,ident)
     receipt['container_id']=post(account,account['id']+'/media',{'media_type':'CAROUSEL','children':','.join(children),'caption':piece['caption']})['id'];save(state)
   poll(account,receipt['container_id'])
   for other in recent(account):
    if other.get('timestamp'):last[key]=max(last[key],epoch(other['timestamp']))
   delay=remaining_gap(last[key])
   while delay>0:
    print(f'Waiting {delay:.1f}s to preserve two-minute @{CONFIG[key][1]} interval',flush=True);time.sleep(min(delay,30));delay=remaining_gap(last[key])
   receipt.update(status='publishing',publish_intent_at=now());save(state,True)
   # Never automatically retry a media_publish request with an uncertain result.
   response=post(account,account['id']+'/media_publish',{'creation_id':receipt['container_id']})
   receipt.update(status='published',media_id=response['id'],acknowledged_at=now(),acknowledged_epoch=time.time());last[key]=time.time();save(state,True)
   actual=verify_post(account,response['id'],piece);receipt.update(permalink=actual['permalink'],posted_at=actual['timestamp'],verified=True)
   save(state,True);print('PUBLISHED '+pid+' '+actual['permalink'],flush=True)
 print('All nine posts published and verified.',flush=True)
if __name__=='__main__':
 try:main()
 except Exception as exc:
  print('STOP: '+ig.redact(exc),file=sys.stderr,flush=True);raise SystemExit(1)
