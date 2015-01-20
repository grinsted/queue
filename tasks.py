from config import huey
import time

@huey.task()
def fetch(sceneid):
    print 'fetching: %s' % sceneid
    time.sleep(4)
    return "ok"
    