import time
import json
import urllib.request

def get(url, timeout=5):
    return urllib.request.urlopen(url, timeout=timeout).read().decode()

def post(url, data):
    b = json.dumps(data).encode()
    req = urllib.request.Request(url, data=b, headers={"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=10).read().decode())

def wait_for_health(base, max_wait=10):
    end = time.time() + max_wait
    while time.time() < end:
        try:
            h = get(f"{base}/health", timeout=2)
            if 'ok' in h:
                return True
        except Exception:
            time.sleep(0.5)
    return False

if __name__ == '__main__':
    base = 'http://127.0.0.1:8001'
    print('Waiting for server health...')
    if not wait_for_health(base, max_wait=15):
        print('Server did not become healthy in time')
        raise SystemExit(1)

    print('Creating session...')
    s = post(f'{base}/session', {})
    sid = s['session_id']
    print('session_id=', sid)
    print('Sending chat message...')
    r = post(f'{base}/chat', {'session_id': sid, 'message': 'Hello from demo client'})
    print('response:', r.get('response'))
    print('history length:', len(r.get('history', [])))
    print('Demo complete')
