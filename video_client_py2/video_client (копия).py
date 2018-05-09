from collections import deque
from datetime import datetime
import re
import urllib2
import json


DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'#Don`t touch it
NO_MOTION_PERIOD =  0.2#min
PLACE_ID = 'Magaz 28 st.Trututu' #Insert object.location
# LOG_FILE = 'd:/temp/test.txt' #Log file path
LOG_FILE = 'motion.txt'
URL = 'http://localhost:8000/video_api/recording/'

def send_msg(data):
    data = json.dumps(data)
    req = urllib2.Request(URL, data, {'Content-Type': 'application/json'})
    f = urllib2.urlopen(req)
    response = f.read()
    f.close()
    return response

getter = re.compile(r'^(?P<datetime>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}),'r' (?P<action>motion)$', re.I)

with open(LOG_FILE) as f:
    recent_motion = list(deque(f, 1))[0].strip('\n')
    print recent_motion
f.close()

result = getter.search(recent_motion).groupdict()
# result = getter.search(u'2018-03-11 15:32:56, Motion').groupdict()

last_motion = datetime.strptime(result['datetime'], DATETIME_FORMAT)
delta = datetime.now() - last_motion

print delta.total_seconds()>NO_MOTION_PERIOD*60
if delta.total_seconds()>NO_MOTION_PERIOD*60:
    data = {'place_id': PLACE_ID, 'time_start': result['datetime'], 'duration': int(delta.total_seconds())}
    r = send_msg(data)
    print r