from collections import deque
from datetime import datetime
import re
from urllib2 import Request, urlopen, URLError
import json
from BaseHTTPServer import BaseHTTPRequestHandler as RS


DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'#Don`t touch it
NO_MOTION_PERIOD = 10 #min
PLACE_ID = 'Magaz 28 st.Trututu' #Insert object.location
LOG_FILE = 'd:/temp/test.txt' #Log file path
URL = 'http://localhost:8000/video_api/recording/'


def send_msg(data):
    data = json.dumps(data)
    req = Request(URL, data, {'Content-Type': 'application/json'})
    try:
        response = urlopen(req)
    except URLError as e:
        if hasattr(e, 'reason'):
            fail = 'We failed to reach a server. Reason: %s.'%(e.reason)
            if hasattr(e, 'read'):
                fail = fail+'Description: %s.'%(e.read())
            return fail
        elif hasattr(e, 'code'):
            return 'The server couldn\'t fulfill the request. Error code: %s'%(RS.responses[e.code][1])
    else:
        response.close()
    return RS.responses[response.code][1]


def get_last_action(log_file):
    try:
        with open(log_file) as f:
            recent_motion = list(deque(f, 1))[0].rstrip()
            print recent_motion
            getter = re.compile(r'^(?P<datetime>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}), 'r'(?P<action>(No )?Motion)$', re.I)
            result = getter.search(recent_motion).groupdict()
    except (IOError, IndexError, AttributeError) as e:
        print e
        return None
    else:
        f.close()
    return result


last_act = get_last_action(LOG_FILE)

# s1 var use in original script. All string under this comment mast be after s1 var.
if last_act and last_act['action']=='No Motion' and s1=='Motion':
    time = datetime.strptime(last_act['datetime'], DATETIME_FORMAT)
    delta = datetime.now() - time
    if delta.total_seconds()>NO_MOTION_PERIOD*60:
        data = {'place_id': PLACE_ID, 'time_start': last_act['datetime'], 'duration': int(delta.total_seconds())}
        r = send_msg(data)
        print r
else:
    print 'Nothing todo'