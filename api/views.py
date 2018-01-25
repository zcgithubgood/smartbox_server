# -*- coding:utf-8 -*-
__author__ = 'druid'

# Create your views here.
from cStringIO import StringIO
import datetime
from django.http import HttpResponse, StreamingHttpResponse
#import struct
from twisted.web import http
from api.backends import RequestMeta, read_post_data
from api.pb_utils import write_multiple_messages, read_message_buf
from data import box_pb2
from data.box_pb2 import ResponseCode, ReserveInfo
from data.models import *

from api.backends import unix_time_millis, unix_time
import pytz
import json
from django.db import connection

PB_MIMETYPE = "application/x-protobuf"
#PB_MIMETYPE ＝ "text/HTML"

#debug
import logging, sys

logging.basicConfig(format="%(filename)s:%(funcName)s:%(message)s",level=logging.DEBUG,stream=sys.stderr)

def response_pb(*pb_instances):
    #cs = {}
    #cs.update(csrf(request))

    c = StringIO()
    write_multiple_messages(c, *pb_instances)
    c.seek(0)

    return HttpResponse(content=c.read(),
                        mimetype=PB_MIMETYPE,
                        status=http.OK)

def heartbeat(request):
    """
    长连接请求，返回长连接指令:
    0
    :param request:
    :return:
    """
    meta = RequestMeta(request)

    heart_beat = box_pb2.HeartBeat()
    calibrated_time = datetime.datetime.now()
    #print calibrated_time
    #print "int"
    calibrated_time = pytz.utc.localize(calibrated_time)
    #print "calibrated_time:"
    #print calibrated_time
    heart_beat.calibrated_time = int(unix_time(calibrated_time))
    #print "heart ++++++++++++++++"
    #print heart_beat.calibrated_time

    rc = ResponseCode()
    rc.code = 0
    return response_pb(rc, heart_beat)

def request_service(request):
    """
    请求客服支持:
    0
    :param request:
    :return:
    """
    meta = RequestMeta(request)
    device = DeviceReqSup()
    device.device_id = meta.device_id
    device.status = 0

    device.save()

    error = ResponseCode()
    error.code = 0
    return response_pb(error)

def reserve(request):
    """
    获得预留电话信息。
    :param request:
    :return:
    """
    meta = RequestMeta(request)
    pre_mobile = None

    try:
        for user in UserInfo.objects.filter(device_id=meta.device_id):
            if int(user.pre_mobile):
                pre_mobile = user.pre_mobile
                break

    except UserInfo.DoesNotExist:
        pass
    reserve_info = ReserveInfo()
    if pre_mobile:
        reserve_info.phone = pre_mobile

    #print "reserve_info.phonez:%s" % reserve_info.phone
    error = ResponseCode()
    error.code = 0

    return response_pb(error, reserve_info)

def basic_info(request):
    """
    获得药箱的基本信息。
    :param request:
    :return:
    """
    meta = RequestMeta(request)
    if request.method == 'POST':
        buf = read_post_data(request)
        #print buf
        basic = box_pb2.BasicInfo()
        basic.ParseFromString(read_message_buf(StringIO(buf)))
        #print "basic +++++++++++++"
        #print basic 
        device, created = DeviceBasicInfo.objects.get_or_create(device_id=meta.device_id)
        #device = DeviceBasicInfo()
        #device = DeviceBasicInfo.objects.filter(device_id=meta.device_id)
        #device = DeviceBasicInfo.objects.get(device_id=meta.device_id)
        #device.device_id = meta.device_id
        #device.mobile = basic.mobile
        #print basic.mobile
        device.imsi = basic.imsi
        device.imei = basic.imei
        device.iccid = basic.iccid
        #device.base_station = "/".join([str(x) for x in basic.base_station])
        base_arr = []
        for base_cell in basic.base_station:
            #print base_cell
            base_dic = {}
            base_dic['base_st'] = str(base_cell)
            #print base_dic
            base_arr.append(base_dic)
            base = json.dumps(base_arr)
            device.base_station = base
            #print device.base_station

	    print "firmware_ver:%s" % basic.firmware_ver
        device.serial_number = basic.serial_number
        device.hardware_ver = basic.hardware_ver
        #device.firmware_ver = basic.firmware_ver
        device.protocol_ver = basic.protocol_ver

        #boxmcu_1.0.08_0_common
        slist = basic.firmware_ver.split('_')

        list_len = len(slist)

        if list_len == 1:
                device.firmware_ver = basic.firmware_ver
        else:
            if list_len >= 2:
                device.firmware_ver = slist[1]

            if list_len >= 3:
                device.customize = slist[3]

        #print "_+_+_+_+_+_+_+_+_+_"
        #print basic.produce_time
        #if basic.produce_time:
            #device.produce_time = datetime.datetime.fromtimestamp(basic.produce_time)
        #else:
        #    produce_time = datetime.datetime.now()
        #    produce_time = pytz.utc.localize(produce_time)
        #    device.produce_time = int(unix_time(produce_time))
        device.status = 1
        device.save()
        #print "device.id"
        #print device.id

        error = ResponseCode()
        error.code = 0
	
        return response_pb(error)
    else:
        return HttpResponse(content="OK")

def box_status(request):
    """
    获得药箱状态信息，并且将信息记录到历史状态信息表中。
    :param request:
    :return:
    """
    meta = RequestMeta(request)
    if request.method == 'POST':
        buf = read_post_data(request)
        status = box_pb2.Status()
        status.ParseFromString(read_message_buf(StringIO(buf)))
        #print "1 status +++++++++++++"
        #print status
        device, created = DeviceStatusRel.objects.get_or_create(pk=meta.device_id)
        device_his = DeviceStatusHis()
        device_his.device_id = meta.device_id
        device.power = device_his.power = status.power
        device.battery = device_his.battery = status.battery
        device.sensor  = device_his.sensor = status.sensor
        device.comm = device_his.comm = status.comm
        device.audio = device_his.audio = status.audio
        device.service_light = device_his.service_light = status.service_light
        device.bg_light = device_his.bg_light = ",".join([str(x) for x in status.bg_light])
        device.time_light = device_his.time_light = ",".join([str(x) for x in status.time_light])
        #print status.weight_status
        device.weight_change = device_his.weight_change = ",".join([str(x) for x in status.weight_status])
        #device.loggedTime = datetime.datetime.fromtimestamp(status.loggedTime)
        device.lack_med_status = device_his.lack_med_status = status.remind
        device.save()
        device_his.save()

        error = ResponseCode()
        error.code = 0

        return response_pb(error)
    else:
        return HttpResponse(content="OK")

def box_record(request):
    """
    获得药箱记录信息。
    :param request:
    :return:
    """
    meta = RequestMeta(request)
    if request.method == 'POST':
        buf = read_post_data(request)
        record = box_pb2.Record()
        record.ParseFromString(read_message_buf(StringIO(buf)))
        device = DeviceRecord()
        device.device_id = meta.device_id
        device.weights = ",".join([str(x) for x in record.weight])
        device.cover_status = record.cover_status
        #print "record.open_time:"
        #print record.open_time
        #print "record.close_time:"
        #print record.close_time
        device.open_time = datetime.datetime.fromtimestamp(record.open_time)
        device.close_time = datetime.datetime.fromtimestamp(record.close_time)
        #device.loggedTime = datetime.datetime.fromtimestamp(record.loggedTime)
        #logging.debug("entering")

        weights_arr = []
        level_arr = []
        for weights in record.slot_weights:
            weights_dic = {}
            level_dic = {}
            level_dic['pos'] = weights_dic['pos'] = weights.position
            weights_dic['wei'] = ",".join([str(x) for x in weights.weight])
            level_dic['level'] = weights.grade
            weights_arr.append(weights_dic)
            level_arr.append(level_dic)
        weights = json.dumps(weights_arr)
        #print reason
        device.slot_weights = weights
        device.judge_levels = json.dumps(level_arr)
        device.save()

        error = ResponseCode()
        error.code = 0
        return response_pb(error)
    else:
        return HttpResponse(content="OK")

def get_box_operation(request):
    """
    请求药箱操作指令。
    :param request:
    :return:
    """
    meta = RequestMeta(request)
    op = box_pb2.Operation()
    op.type = 0
    try:
        for operation in DeviceOperation.objects.filter(device_id=meta.device_id, status=0):
            op.type = operation.op_type
            if op.type:
                message = operation.op_message
                #操作历史表1片
                op_his = DeviceOperationHis()
                op_his.device_id = operation.device_id
                op_his.op_type = operation.op_type
                op_his.op_message = message
                op_his.status = 1#operation.status
                op_his.save()
                op.op_id = op_his.id
                #print "op.op_id:%d" % op.op_id

            if op.type == 1:
                mes = json.loads(message)
                for kmes, vmes in mes.items():
                    if kmes == "userid":
                        op.bind.userid = vmes
                    if kmes == "bind":
                        if vmes:
                            #bind
                            op.type = 1
                        else:
                            op.type = 2

            #elif op.type == 2:
            #    mes = json.loads(message)
            #    for kmes, vmes in mes.items():
            #        if kmes == "userid":
            #                if operation.op_message:
            #                    op.unbind.userid = vmes

            elif op.type == 3:
                #print "1 +++++++++++++++++++++++++++++++"
                #print "op.type %s" % op.type
                mess = json.loads(message)
                #print mess
                #for mes in mess:
                length = len(mess)
                #print length
                for i in range(0, length):
                    #print mes['position']
                    #if mes['position']:
                    print "2 +++++++++++++++++++++++++++++++"
                    print i, mess[i]
                    config = op.config.add()
                    for kmes, vmes in mess[i].items():
                        #print "%s-------%s"%(kmes, vmes)
                        if kmes == "position":
                            config.position = int(vmes)
                        if kmes == "medicine":
                            config.medicine = str(vmes.encode('GBK'))
                        if kmes == "medicine_id":
                            config.medicine_id = int(vmes)
                            #print config.medicine_id
                        if kmes == "stweight":
                            config.stweight = int(vmes)

                        #if kmes == "dose_text":
                            #print vmes
                        #    config.dose_text = str(vmes.encode('GBK'))
                        #if kmes == "pieces":
                        #    config.pieces = int(vmes)
                        #if kmes == "meals":
                        #    config.meals = int(vmes)
                        if kmes == "remind_threshold":
                            config.remind_threshold = int(vmes)
                        if kmes == "judge_level":
                            config.grade = int(vmes)
                        if kmes == "schedules":
                            #print "3 +++++++"
                            #print vmes
                            for vm in vmes:
                                #print "4 +++++++"
                                #print vm
                                schedules = config.schedules.add()
                                for ks,vs in vm.items():
                                    #print "%s: %s"%(ks, vs)
                                    if ks == "period":
                                        schedules.period = int(vs)
                                    if ks == "time":
                                        schedules.time = int(vs)
                                    if ks == "meals":
                                        schedules.meals = int(vs)
                                    if ks == "dose_text":
                                        schedules.dose_text = str(vs.encode('GBK'))

            elif op.type == 4:
                #print "op.type %s" % op.type
                mes = json.loads(message)
                for kmes, vmes in mes.items():
                    if kmes == "index":
                        op.audio.index = int(vmes)
                    if kmes == "text":
                        op.audio.text = str(vmes.encode('GBK'))
            elif op.type == 5:
                mes = json.loads(message)
                for kmes, vmes in mes.items():
                    if kmes == "volume":
                        op.volume.volume = vmes
            elif op.type == 6:
                #print "op.type %s" % op.type
                mes = json.loads(message)
                for kmes, vmes in mes.items():
                    if kmes == "power":
                        op.light.power = int(vmes)	#light.powerLight
                    if kmes == "service":
                        op.light.service = int(vmes)	#light.serviceLight
                    if kmes == "backgrounds":
                        for bgLight in vmes.split(','):
                            op.light.backgrounds.append(int(bgLight))
                    if kmes == "timelights":
                        for timeLight in vmes.split(','):
                            op.light.timelights.append(int(timeLight))

            elif op.type == 7:
                #print "op.type %s" % op.type
                mes = json.loads(message)
                for kmes, vmes in mes.items():
                    if kmes == "oldverlength":
                        op.upgrade.oldverlength = int(vmes)
                    if kmes == "updatetime":
                        op.upgrade.updatetime = int(vmes)
                    if kmes == "updatemode":
                        op.upgrade.updatemode = int(vmes)

            elif op.type == 8:
                mes = json.loads(message)
                for kmes, vmes in mes.items():
                    if kmes == "supplement":
                        op.funswitch.supplement = vmes
                    if kmes == "forget":
                        op.funswitch.forget = vmes
                    if kmes == "sos":
                        op.funswitch.sos = vmes

            if op.type:
                operation.status = 1
                operation.save(update_fields=['status'])
            break

    except DeviceOperation.DoesNotExist:
        pass

    error = ResponseCode()
    error.code = 0
    print "5++++++++++++++++++++++++++"
    print op
    return response_pb(error, op)

def op_result(request):
    """
    汇报操作结果
    POST
    :param request:
    :return:
    """
    meta = RequestMeta(request)
    if request.method == 'POST':

        for operation in DeviceOperation.objects.filter(device_id=meta.device_id, status=0):
            operation.status = 1    #操作状态 0:未执行 1:已推送
            #print operation.status

        #print "+++++++++++"
        buf = read_post_data(request)
        result = box_pb2.OpResult()
        result.ParseFromString(read_message_buf(StringIO(buf)))
        device = DeviceOpResult()
        device.device_id = meta.device_id

        device.op_type = result.type
        device.device_op_id = result.op_id

        device.op_id = result.op_id
        device.op_time = datetime.datetime.fromtimestamp(result.timestamp)
        device.result = result.result
        device.reason = result.reason
        device.save()

        error = ResponseCode()
        error.code = 0
        return response_pb(error)

    else:
        return HttpResponse(content="OK")

def exception(request):
    """
    0：无异常
    1：超时未服药
    2：断电异常
    3：通信异常
    4：称异常
    :param request:
    :return:
    """
    meta = RequestMeta(request)
    if request.method == 'POST':
        buf = read_post_data(request)
        #print "1 exception++++++++++++++++"
        #print buf
        excp = box_pb2.Exception()
        excp.ParseFromString(read_message_buf(StringIO(buf)))

        #device, created = DeviceException.objects.get_or_create(device_id=meta.device_id)
        #print "2 exception++++++++++++++++"
        #print excp
        if excp.type:
            device= DeviceException()
            device.device_id = meta.device_id
            device.type = excp.type
            if device.type == 1:
                #print "漏药"
                reason_arr = []
                for taken in excp.takens:
                    reason_dic = {}
                    reason_dic['pos'] = taken.position
                    reason_dic['med_id'] = taken.medicine_id
                    reason_dic['time'] = taken.time
                    reason_arr.append(reason_dic)
                reason = json.dumps(reason_arr)
                #print reason
                device.reason = reason

            elif device.type == 2:
                #print "断电异常"
                #device.reason = excp.power.reason.decode('GBK')
                #print excp.power.reason
                device.reason = excp.power.reason

            elif device.type == 3:
                #print "通信异常"
                #device.reason = excp.signal.reason.decode('GBK')
                device.reason = excp.signal.reason

            elif device.type == 4:
                #print "称异常"
                reason_arr = []
                for scale in excp.scales:
                    reason_dic = {}
                    reason_dic['scaleid'] = scale.scaleid
                    #reason_dic['reason'] = scale.reason.decode('GBK')
                    reason_dic['reason'] = scale.reason
                    reason_arr.append(reason_dic)
                reason = json.dumps(reason_arr)
                #print reason
                device.reason = reason
            elif device.type == 5:
                #print "sos"
                device.reason = excp.sos.reason

            device.save()

        error = ResponseCode()
        error.code = 0
        return response_pb(error)
    else:
        return HttpResponse(content="OK")

def upgrade(request, ver):
    """
    获取更新信息
    :param request:
           ver: 客户端传过来的固件版本号。
    :return:
    """

    meta = RequestMeta(request)
    '''
    if ver == "v1":
        file = '/download/version1/leuart_transmit_dvk.bin'
    elif ver == "v2":
        file = '/download/version2/leuart_transmit_dvk.bin'
    else:
        return HttpResponse("error")

    with open(file) as f:
        c = f.read()

    #print "++++\n"
    return HttpResponse(content=c,
                        mimetype="text/html",
                        status=http.OK)
    )
    '''

    device, created = DeviceBasicInfo.objects.get_or_create(device_id=meta.device_id)
    print "firmware_ver:%s, customize:%s" % (device.firmware_ver, device.customize)

    cursor = connection.cursor()
    try:
        cursor.execute("select * from device_mcu where status=1 and customize='common' order by ver_num desc limit 1")
        mcu_row = cursor.fetchone()
    finally:
        cursor.close()

    #print "1+++++++++++"
    #print ver
    #print "mcu_row:%s, len:%d" % (mcu_row, len(mcu_row))
    if ver == "version":
        #file_name = '/home/ubuntu/product/static_work/mcu/' + mcu_row[4]
        #print mcu_row[4]
        if len(mcu_row) >= 4:
            #file_name = '/Users/smartbox/product/static_work/mcu/' + mcu_row[4]
            #file_name = '/home/ubuntu/product/static_work/mcu/' + mcu_row[4]
            file_name = '/home/baybox/produce/static_work/install_files/mcu' + mcu_row[4]
    else:
        return HttpResponse("error")

    #print file_name

    def file_iterator(file_name, chunk_size=5120000):
        with open(file_name) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    return HttpResponse(content=file_iterator(file_name),
                        mimetype="text/html",
                        status=http.OK)

def testmysql(request):

    meta = RequestMeta(request)
    print meta.device_id

    #try:
    for medlib in UserMedicine.objects.filter(box_id=meta.device_id):
        print medlib.medicine
        print medlib.morning

    #except medlib.DoesNotExist:
    #    pass

    #return HttpResponse("Hello Qxl")
    return HttpResponse(content="OK")

