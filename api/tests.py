# -*- coding:utf-8 -*-
__author__ = 'druid'
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from cStringIO import StringIO
import datetime
from django.core.files.base import ContentFile

from django.test import TestCase, Client
from twisted.web import http
from api.backends import unix_time_millis, unix_time
from api.pb_utils import read_message_buf, write_multiple_messages
from data import box_pb2
from data.models import *
import pytz
import json
#from django.utils import timezone

class ApiTest(TestCase):
    def test_heartbeat(self):
        """
        测试heartbeat
        Epython manage.py test --settings=smartbox.settings_test api.ApiTest.test_heartbeat
        """
        c = Client()
        response = c.get("/api/v1/heartbeat/?device_id=66666666&imsi=460020240522205")
        self.assertEqual(http.OK, response.status_code)

        res = box_pb2.ResponseCode()
        input = StringIO(response.content)
        buf = read_message_buf(input)

        res.ParseFromString(buf)
        self.assertEqual(res.code, 0)

    def test_request(self):
        """
        测试request_service
        Epython manage.py test --settings=smartbox.settings_test api.ApiTest.test_request
        """
        c = Client()
        response = c.get("/api/v1/request/service/?device_id=66666666&imsi=460020240522205")

        res = box_pb2.ResponseCode()
        input = StringIO(response.content)
        buf = read_message_buf(input)

        res.ParseFromString(buf)
        self.assertEqual(res.code, 0)
        self.assertEqual(http.OK, response.status_code)

    def test_reserve(self):
        """
        测试获取预留信息。
        Epython manage.py test --settings=smartbox.settings_test api.ApiTest.test_reserve
        :return:
        """
        device_id = "66666666"
        mobile = "15912345678"

        user = UserInfo()
        user.pre_mobile = mobile
        user.save()

        reserve = box_pb2.ReserveInfo()
        reserve.phone = mobile
        io = StringIO()
        write_multiple_messages(io, reserve)
        io.seek(0)
        c = Client()
        f = ContentFile(io.read(), name="abc")
        response = c.post("/api/v1/reserve/?id=%s&imsi=460020240522205" % device_id, data={"data": f})

        self.assertEqual(http.OK, response.status_code)

        input = StringIO(response.content)
        res = box_pb2.ReserveInfo()
        res.ParseFromString(read_message_buf(input))
        print "++++++"
        print res.phone
        #self.assertEqual(res.phone, mobile)

    def test_reserve_wphone(self):
        """
        测试获取预留信息（没有预留电话的情况)
        Epython manage.py test --settings=smartbox.settings_test api.ApiTest.test_reserve_wphone
        :return:
        """
        device_id = "66666666"

        c = Client()
        response = c.get("/api/v1/reserve/?id=%s&imsi=460020240522205" % device_id)

        self.assertEqual(http.OK, response.status_code)

        input = StringIO(response.content)

        res = box_pb2.ResponseCode()
        res.ParseFromString(read_message_buf(input))
        self.assertEqual(res.code, 0)

        reserve = box_pb2.ReserveInfo()
        reserve.ParseFromString(read_message_buf(input))
        self.assertEqual(reserve.phone, '')

    def test_report_box_basic_info(self):
        #Epython manage.py test --settings=smartbox.settings_test api.ApiTest.test_report_box_basic_info
        device_id = "55555555"
        mobile = "15812345678"
        imsi = "460020240522205"
        imei = "123456"
        iccid = "1234567890"
        base_station = "12345678,87654321"
        serial_number = "287454020"
        hardware_ver = "1.0.0"
        firmware_ver = "2.1.1"#"boxmcu_2.1.1_0_common"
        protocol_ver = "3.0.0"
        produce_time = datetime.datetime.now()
        print produce_time
        produce_time = pytz.utc.localize(produce_time)
        print produce_time

        '''
        device = DeviceBasicInfo()
        device.device_id = device_id
        device.mobile = mobile
        device.imsi = imsi
        device.imei = imei
        device.iccid = iccid
        device.base_station = ",".join([str(x) for x in base_station])
        device.serial_number = serial_number
        device.hardware_ver = hardware_ver
        device.firmware_ver = firmware_ver
        device.protocol_ver = protocol_ver
        time = datetime.datetime.now()
        time = pytz.utc.localize(time)
        device.produce_time = int(unix_time(time))
        device.save()
        '''

        io = StringIO()
        basicInfo = box_pb2.BasicInfo()
        basicInfo.mobile = mobile
        basicInfo.imsi = imsi
        basicInfo.imei = imei
        basicInfo.iccid = iccid
        basicInfo.base_station.append(base_station)
        basicInfo.base_station.append("666666,777777")
        basicInfo.serial_number = serial_number
        basicInfo.hardware_ver = hardware_ver
        #basicInfo.firmware_ver = firmware_ver
        basicInfo.firmware_ver = firmware_ver
        basicInfo.protocol_ver = protocol_ver
        basicInfo.produce_time = int(unix_time(produce_time))
        print basicInfo.produce_time
        print "firmware_ver:%s" % firmware_ver
        slist = firmware_ver.split('_')

        print slist

        list_len = len(slist)

        print list_len
        if list_len >= 2:
            basicInfo.firmware_ver = slist[1]

        #if list_len >= 3:
        #    basicInfo.customize = slist[3]

        write_multiple_messages(io, basicInfo)
        io.seek(0)
        c = Client()
        f = ContentFile(io.read(), name="abc")
        response = c.post("/api/v1/box/info/basic/?id=%s&imsi=460020240522205" % device_id, data={"data": f})

        #print "111 ----------------------------------------------------------------------------"
        #print response
        #print "222 ----------------------------------------------------------------------------"
        #print "%x" % response

        self.assertEqual(response.status_code, http.OK)

        objects = DeviceBasicInfo.objects.all()
        self.assertEqual(1, len(objects))
        real = objects[0]
        self.assertEqual(device_id, real.device_id)
        self.assertEqual(imsi, real.imsi)
        self.assertEqual(imei, real.imei)
        self.assertEqual(iccid, real.iccid)
        #self.assertEqual(base_station, real.base_station)
        self.assertEqual(serial_number, real.serial_number)
        self.assertEqual(hardware_ver, real.hardware_ver)
        #self.assertEqual(firmware_ver, real.firmware_ver)
        self.assertEqual(protocol_ver, real.protocol_ver)
        #self.assertEqual((produce_time - real.produce_time).seconds, 0)

    def test_record(self):
        """
        测试药箱记录信息。
        Epython manage.py test --settings=smartbox.settings_test api.ApiTest.test_record
        :return:
        """
        device_id = "66666666"
        cover_status = 1
        open_time = datetime.datetime.now()
        open_time = pytz.utc.localize(open_time)
        close_time = datetime.datetime.now()
        close_time = pytz.utc.localize(close_time)

        Record = box_pb2.Record()

        Record.weight.append(200000)
        Record.weight.append(100000)
        Record.weight.append(12000)
        Record.weight.append(10000)

        #Record.slot_weights.append()

        Record.cover_status = int(cover_status)
        Record.open_time = int(unix_time(open_time))
        Record.close_time = int(unix_time(close_time))
        #Record.logged_time = int(unix_time(logged_time))

        io = StringIO()
        write_multiple_messages(io, Record)

        io.seek(0)
        c = Client()
        f = ContentFile(io.read(), name="abc")
        #print "here 1"
        #print f
        response = c.post("/api/v1/box/info/record/?id=%s&imsi=460020240522205" % device_id, data={'data': f})

        self.assertEqual(response.status_code, http.OK)

        objects = DeviceRecord.objects.all()
        self.assertEqual(1, len(objects))
        real = objects[0]
        self.assertEqual(cover_status, real.cover_status)
        self.assertEqual((open_time - real.open_time).seconds, 0)
        self.assertEqual((close_time - real.close_time).seconds, 0)
        self.assertEqual((open_time - real.open_time).seconds, 0)

    def test_status(self):
        """
        测试药箱状态信息。
        Epython manage.py test --settings=smartbox.settings_test api.ApiTest.test_status
        :return:
        """
        status = box_pb2.Status()
        device_id = "66666666"
        power = 1
        battery = 100
        sensor = 0
        comm = 1
        audio = 3
        service_light = 1

        status.power = power
        status.battery = battery
        status.sensor = sensor
        status.comm = comm
        status.audio = audio
        status.service_light = service_light
        status.remind = 1

        for i in range(0,4):
            status.bg_light.append(1)

        for i in range(0,16):
            status.time_light.append(1)

        io = StringIO()
        write_multiple_messages(io, status)

        io.seek(0)
        c = Client()
        f = ContentFile(io.read(), name="abc")
        response = c.post("/api/v1/box/info/status/?id=%s&imsi=460020240522205" % device_id, data={'data': f})
        self.assertEqual(response.status_code, http.OK)

    def test_op_conf(self):
        """
        测试获取药箱操作
        Epython manage.py test --settings=smartbox.settings_test api.ApiTest.test_op_conf
        """
        deviceid = "66666666"
        device = DeviceOperation()
        device.device_id = deviceid

        device.op_type = 3

        obj = {}
        if device.op_type == 1:
            obj = {'userid':'U222222222','bind':1}
        elif device.op_type == 3:
            #obj = [{"position":1,"dose_text":"四分之一片","schedules":[{"time":601,"meals":3,"period":1},{"time":915,"meals":3,"period":2},{"time":1001,"meals":1,"period":3},{"time":1201,"meals":1,"period":4}],"remind_threshold":25,"medicine_id":626,"medicine":"拜糖平","stweight": 30125},{"position":3,"dose_text":"半片","schedules":[{"time":603,"meals":3,"period":1},{"time":917,"meals":3,"period":2},{"time":1003,"meals":3,"period":3},{"time":1203,"meals":3,"period":4}],"remind_threshold":25,"medicine_id":660,"medicine":"糖适平","stweight": 25100},{"position":4,"dose_text”:”8片”,”schedules":[{"time":604,"meals":3,"period":1},{"time":918,"meals":3,"period":2},{"time":1004,"meals":1,"period":3},{"time":1204,"meals":2,"period":4}],"remind_threshold":25,"medicine_id":724,"medicine":"吗丁啉","stweight": 3775},{"position":2,"dose_text”:”2片”,”schedules":[{"time":602,"meals":1,"period":1},{"time":916,"meals":1,"period":2},{"time":1002,"meals":1,"period":3},{"time":1202,"meals":1,"period":4}],"remind_threshold":25,"medicine_id":676,"medicine":"降糖灵","stweight": 24700}]
            #obj = [{'position':4}]
            #obj = [{"position":1,"schedules":[{"time":601,"meals":3,"period":1,"dose_text":"1片"},{"time":952,"meals":3,"period":2},{"time":1031,"meals":1,"period":3},{"time":1201,"meals":1,"period":4}],"remind_threshold":25,"medicine_id":626,"medicine":"1号药仓","stweight": 30125,"level":1},{"position":2,"schedules":[{"time":601,"meals":3,"period":1,"dose_text":"1片"},{"time":1085,"meals":1,"period":3},{"time":1201,"meals":1,"period":4}],"remind_threshold":25,"medicine_id":626,"medicine":"2号药仓","stweight": 30125,"level":2},{"position":3,"schedules":[{"time":601,"1eals":3,"period":1,"dose_text":"1片"},{"time":953,"meals":3,"period":2},{"time":1085,"meals":1,"period":3}],"remind_threshold":25,"medicine_id":626,"medicine":"3号药仓","stweight": 30125,"level":1},{"position":4,"schedules":[{"time":601,"meals":3,"period":1,"dose_text":"1片"},{"time":953,"meals":3,"period":2},{"time":1086,"meals":1,"period":3}],"remind_threshold":25,"medicine_id":626,"medicine":"4号药仓","stweight": 30125,"level":1}]
            obj = [{"position":1,"schedules":[{"dose_text":"1片","time":470,"meals":1,"period":1},{"dose_text":"2片","time":728,"meals":1,"period":2},{"dose_text":"3片","time":1080,"meals":1,"period":3},{"dose_text":"4片","time":1210,"meals":1,"period":4}],"remind_threshold":25,"medicine_id":134012,"judge_level":2,"medicine":"头孢克洛分散片","stweight":1000},{"position":2,"schedules":[{"dose_text":"5片","time":390,"meals":1,"period":1},{"dose_text":"6片","time":724,"meals":1,"period":2},{"dose_text":"7片","time":1089,"meals":3,"period":3},{"dose_text":"8片","time":1205,"meals":1,"period":4}],"remind_threshold":25,"medicine_id":143451,"judge_level":2,"medicine":"拜唐苹","stweight":1000},{"position":3,"schedules":[{"dose_text":"1毫升","time":450,"meals":1,"period":1},{"dose_text":"1毫升","time":753,"meals":3,"period":2},{"dose_text":"1毫升","time":960,"meals":1,"period":3},{"dose_text":"1毫升","time":1201,"meals":1,"period":4}],"remind_threshold":25,"medicine_id":136061,"judge_level":2,"medicine":"来昔决南钐[153Sm]注射液","stweight":1000},{"position":4,"schedules":[{"dose_text":"41毫升","time":391,"meals":1,"period":1},{"dose_text":"42毫升","time":725,"meals":1,"period":2},{"dose_text":"43毫升","time":971,"meals":2,"period":3},{"dose_text":"44毫升","time":1208,"meals":1,"period":4}],"remind_threshold":25,"medicine_id":132624,"judge_level":2,"medicine":"咳感康口服液","stweight":1000},{"position":100,"schedules":[{"dose_text":"11片","time":390,"meals":1,"period":1},{"dose_text":"12片","time":750,"meals":1,"period":2},{"dose_text":"13片","time":1090,"meals":1,"period":3},{"dose_text":"14片","time":1206,"meals":1,"period":4}],"remind_threshold":25,"medicine_id":132024,"medicine":"吉加","stweight":1000},{"position":100,"schedules":[{"dose_text":"21毫升","time":390,"meals":1,"period":1},{"dose_text":"22毫升","time":726,"meals":1,"period":2},{"dose_text":"23毫升","time":1091,"meals":1,"period":3},{"dose_text":"24毫升","time":1207,"meals":1,"period":4}],"remind_threshold":25,"medicine_id":133449,"medicine":"复方盐酸甲麻黄碱糖浆","stweight":1000},{"position":100,"schedules":[{"dose_text":"31毫克","time":390,"meals":1,"period":1},{"dose_text":"32毫克","time":589,"meals":3,"period":2},{"dose_text":"33毫克","time":751,"meals":3,"period":3},{"dose_text":"34毫克","time":1111,"meals":3,"period":4}],"remind_threshold":25,"medicine_id":133885,"medicine":"大力药酒","stweight":1000},{"position":100,"schedules":[{"dose_text":"41片","time":571,"meals":3,"period":1},{"dose_text":"42片","time":727,"meals":2,"period":2},{"dose_text":"43片","time":972,"meals":3,"period":3},{"dose_text":"44片","time":1209,"meals":3,"period":4}],"remind_threshold":25,"medicine_id":133450,"medicine":"复方盐酸赖氨酸片","stweight":1000}]
        elif device.op_type == 4:
            obj = {'index':1,'text':'主人，为了激励您按时吃药，请用微信扫描药箱后的二维码，领取奖励，每个月都有机会抽取马尔代夫双人游机票，骗你我是小狗。'}
        elif device.op_type == 5:
            obj = {'volume':6}
        elif device.op_type == 6:
            #obj = {'backgrounds':'1,0,1,0'}
            obj = {'backgrounds':'1,0,1,0','power':'1','service':'1','timelights':'1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1'}
        elif device.op_type == 7:
            obj = {"oldverlength":50030,"updatetime":0,"updatemode":1}
        elif device.op_type == 8:
            obj = {'supplement':1,'forget':0,'sos':0}  

        device.status = 0
        device.op_message = json.dumps(obj)

        device.save()

        op = box_pb2.Operation()
        op.type = device.op_type
        op.op_id = 1000

        for operation in DeviceOperation.objects.filter(device_id=deviceid, status=0):
            op.type = operation.op_type
            if op.type == 1:
                message = json.loads(operation.op_message)
                op.bind.userid = message['userid']
                op.type = message['bind']
            elif op.type == 3:
                print json.loads(operation.op_message)
            elif op.type == 4:
                mes = json.loads(operation.op_message)
                for kmes, vmes in mes.items():
                    if kmes == "index":
                        op.audio.index = int(vmes)
                    if kmes == "text":
                        op.audio.text = str(vmes.encode('GBK'))
            elif op.type == 5:
                op.volume.volume = json.loads(operation.op_message)['volume']
            elif op.type == 6:
                mes = json.loads(operation.op_message)
                for kmes, vmes in mes.items():
                    if kmes == "power":
                        op.light.power = int(vmes)   #light.powerLight
                    if kmes == "service":
                        op.light.service = int(vmes) #light.serviceLight
                    if kmes == "backgrounds":
                        for bgLight in vmes.split(','):
                            op.light.backgrounds.append(int(bgLight))
                    if kmes == "timelights":
                        for timeLight in vmes.split(','):
                            op.light.timelights.append(int(timeLight))
            elif op.type == 8:
                mes = json.loads(operation.op_message)
                for kmes, vmes in mes.items():
                    if kmes == "userid":
                        op.funswitch.supplement = vmes
                    if kmes == "forget":
                        op.funswitch.forget = vmes
                    if kmes == "sos":
                        op.funswitch.sos = vmes

        io = StringIO()
        write_multiple_messages(io, op)
        io.seek(0)
        f = ContentFile(io.read(), name="abc")
        c = Client()
        print f
        response = c.post("/api/v1/op/?id=%s&imsi=460020240522205" % deviceid, data={'data': f})

        self.assertEqual(http.OK, response.status_code)

        res = box_pb2.ResponseCode()
        input = StringIO(response.content)
        buf = read_message_buf(input)
        print buf
        res.ParseFromString(buf)
        self.assertEqual(res.code, 0)

    def test_op_result(self):
        """
        测试药箱结果
        Epython manage.py test --settings=smartbox.settings_test api.ApiTest.test_op_result
        """
        device_id = "66666666"
        loggedTime = datetime.datetime.now()
        loggedTime = pytz.utc.localize(loggedTime)
        op_result = box_pb2.OpResult()
        op_result.op_id = 1000
        op_result.type = 1
        op_result.timestamp = int(unix_time(loggedTime))
        op_result.result = 0
        op_result.reason = u"19988"

        io = StringIO()
        write_multiple_messages(io, op_result)
        io.seek(0)
        c = Client()
        f = ContentFile(io.read(), name="abc")

        response = c.post("/api/v1/op/result/?id=%s&imsi=460020240522205" % device_id, data={"data": f})
        self.assertEqual(response.status_code, http.OK)

        #self.assertEqual(http.OK, response.status_code)
        #res = box_pb2.ResponseCode()
        #input = StringIO(response.content)
        #buf = read_message_buf(input)
        #res.ParseFromString(buf)
        #self.assertEqual(res.code, 0)

    def test_exception(self):
        """
        测试药箱异常
        Epython manage.py test --settings=smartbox.settings_test api.ApiTest.test_exception
        """
        device_id = "66666666"
        type = 5
        
        if type:
            Exception = box_pb2.Exception()
            Exception.type = int(type)
        if type == 1:
            for i in range(0,4):
                takens = Exception.takens.add()
                takens.medicine_id = 1+i
                takens.time = 360
        elif type == 2:
            Exception.power.reason = "hello 1"
        elif type == 3:
            Exception.signal.reason = "hello 2"
        elif type == 4:
            for i in range(0,4):
                scale = Exception.scales.add()
                scale.scaleid = 1+i
                scale.reason = "hello 3"
        elif type == 5:
            Exception.sos.reason = "hello 2"
            

        io = StringIO()
        write_multiple_messages(io, Exception)

        io.seek(0)
        c = Client()
        f = ContentFile(io.read(), name="abc")
        response = c.post("/api/v1/exception/?id=%s&imsi=460020240522205" % device_id, data={'data': f})

        self.assertEqual(response.status_code, http.OK)
        '''
        objects = Exception.objects.all()
        self.assertEqual(1, len(objects))
        real = objects[0]
        self.assertEqual(type, real.type)
        '''

    def test_upgrade(self):
        device_id = "66666666"

        """
        测试升级
        Epython manage.py test --settings=smartbox.settings_test api.ApiTest.test_upgrade
        """
        c = Client()
        response = c.get("/api/v1/upgrade/version/?id=%s&imsi=abc" % device_id)
        self.assertEqual(http.OK, response.status_code)

    def test_version(self):
        """
        测试版本管理
        Epython manage.py test --settings=smartbox.settings_test api.ApiTest.test_version
        """

        print "love baby!"
        for version in Version.objects.filter(status = 1):
            version_new = version.version_name
            print version_new
            for basic in DeviceBasicInfo.objects.all():
                print basic.hardware_ver

                if basic.hardware_ver < verson_new:
                    #for operation in DeviceOperation.objects.filter(device_id=basic.device_id, status=1):
                    device, created = DeviceOperation.objects.get_or_create(pk=basic.device_id, op_type=7)
                    message_dic = {}
                    message_dic['oldverlength'] = version.file_length
                    device.message = json.dumps(message_dic)
                    device.status = 0
                    device.save()



    def test_mysql(self):
        device_id = "123456"

        c = Client()
        response = c.get("/api/testmysql/?id=%s&imsi=abc" % device_id)
        self.assertEqual(http.OK, response.status_code)

