import json
import time

from flask import Flask, render_template

# huey stuff
from config import huey
import tasks

app = Flask(__name__)
app.status = []

def job_check():
    """ cleans the list of jobs for completed """
    # fixme: should requeue if failed, or warn, or ???
    completed = []
    for idx, obj in enumerate(app.status):
        result = obj[0].get() 
        print result
        if result == "ok":
            completed.append(idx)
    app.status = [i for j, i in enumerate(app.status) if j not in completed]

def job_submit(ref, task, **kwargs):
    app.status.append((ref, {"task": task, "args": kwargs, "timestamp": time.time()}))

def json_response(data=None, status="ok"):
    return json.dumps({"status": status, "data": data})

@app.route('/')
def index():
    return render_template('index.html', status=app.status)

@app.route('/fetch/<sceneid>')
def fetch(sceneid):
    # start the background job
    ref = tasks.fetch(sceneid)
    job_submit(ref, "fetch", sceneid=sceneid)
    return json_response()

@app.route('/status')
def status():
    job_check()
    active = map(lambda obj: obj[1], app.status)
    return json_response({"active": active, "timestamp": time.time()})


@app.route('/search/<partial>')
def search(partial):
    matches = ["abc", "cde", partial]
    return json_response({"matches": matches})




if __name__ == '__main__':
    app.debug = True
    app.run()