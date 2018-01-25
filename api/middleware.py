# -*- coding:utf-8 -*-
#项目 zqxt 文件名 api/middleware.py

import datetime
import pytz
from api.backends import RequestMeta
from django.http import HttpResponse
from api.backends import unix_time
from data.models import *

class BlockedIpMiddleware(object):
    def process_request(self, request):
        #print "1 +++++++++++++++++"
        #print request.META

        meta = RequestMeta(request)
        #print meta.device_id
        if meta.device_id != "":
            #print request.get_full_path()
            device, created = DeviceActive.objects.get_or_create(pk=meta.device_id)
            #print int(meta.device_id)

            host = request.META.get('HTTP_HOST', 'unknown')
            path = request.META.get('PATH_INFO', 'unknown')
            query = request.META.get('QUERY_STRING', 'unknown')
            str = host+path+query
            #print "2 +++++++++++++++++"
            #print "%s %s %s %s" % (host, path, query, str)

            if path == "/api/v1/heartbeat/":
                device.req_type = 1
            elif path == "/api/v1/request/service/":
                device.req_type = 2
            elif path == "/api/v1/reserve/":
                device.req_type = 3
            elif path == "/api/v1/box/info/basic/":
                device.req_type = 4
            elif path == "/api/v1/box/info/record/":
                device.req_type = 5
            elif path == "/api/v1/box/info/status/":
                device.req_type = 6
            elif path == "/api/v1/op/":
                device.req_type = 7
            elif path == "/api/v1/op/result/":
                device.req_type = 8
            elif path == "/api/v1/exception/":
                device.req_type = 9
            elif path == "/api/v1/upgrade/v1/":
                device.req_type = 10

            device.req_url = str #request.META['HTTP_REFERER']
            req_time = datetime.datetime.now()
            req_time = pytz.utc.localize(req_time)
            device.req_time =  datetime.datetime.fromtimestamp(int(unix_time(req_time)))

            device.save()
        #if request.META['REMOTE_ADDR'] in getattr(request, "BLOCKED_IPS", []):
        #    return http.HttpResponseForbidden('<h1>Forbidden</h1>')

        #return HttpResponse("Your browser is %s" % str)
