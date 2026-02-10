import urllib.request, json, time, threading

req = urllib.request.Request('http://localhost:8000/api/start', method='POST')
urllib.request.urlopen(req)
print('Camera started')

# Trigger stream in background
def read_stream():
    try:
        r = urllib.request.urlopen('http://localhost:8000/api/live')
        r.read(2000000)  # read more frames
        r.close()
    except:
        pass

t = threading.Thread(target=read_stream)
t.start()

# Check status repeatedly to see detections grow
for i in range(4):
    time.sleep(5)
    r = urllib.request.urlopen('http://localhost:8000/api/status')
    s = json.loads(r.read())
    print(f"\n--- {(i+1)*5}s: Frames={s['pipeline_stats']['metrics']['total_frames']}, "
          f"Dets={s['pipeline_stats']['metrics']['total_detections']} ---")
    
    r2 = urllib.request.urlopen('http://localhost:8000/api/detections?since=0')
    d = json.loads(r2.read())
    classes = {}
    for x in d['detections']:
        c = x['class']
        if c not in classes:
            classes[c] = []
        classes[c].append(x['confidence'])
    
    for cls, confs in sorted(classes.items()):
        print(f"  {cls:15s}  seen {len(confs)}x  conf: {min(confs)}-{max(confs)}%")
