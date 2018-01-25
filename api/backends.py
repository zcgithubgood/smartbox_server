__author__ = 'druid'


import pytz

class RequestMeta:
    def __init__(self, request):
        self.device_id = request.GET.get('id', "");
        self.imsi = request.GET.get('imsi', "")


def read_post_data(request):
    f = request.FILES["data"];
    #f = request.POST["data"]
    buf = "".join(f.chunks())
    return buf


import datetime

def unix_time(dt):
    epoch = pytz.utc.localize(datetime.datetime.utcfromtimestamp(0))
    #print "dt:"
    #print dt
    #print "epoch:"
    #print epoch
    delta = dt - epoch
    return delta.total_seconds()

def unix_time_millis(dt):
    return unix_time(dt) * 1000.0
