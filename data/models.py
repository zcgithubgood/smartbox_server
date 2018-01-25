# -*- coding:utf-8 -*-
__author__ = 'druid'


from django.db import connection, models

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class BetterCharField(models.Field):
    def __init__(self, length, *args, **kwargs):
        self.length = length
        super(BetterCharField, self).__init__(*args, **kwargs)
    def db_type(self, connection):
        return 'char(%s)' % self.length

class DeviceReqSup(models.Model):
    device_id = BetterCharField(8, verbose_name='设备ID')
    status = models.IntegerField(default=0, verbose_name='状态 0:未处理 1:已取走')
    intime = models.DateTimeField(auto_now=False, null=True, verbose_name='写入时间')
    modtime = models.DateTimeField(auto_now=False, null=True, verbose_name='更新时间')

    class Meta:
        db_table = 'device_request_support'

    def __unicode__(self):
        return u'%s %d %s %s' % (self.device_id, self.status, self.intime, self.modtime)

class DeviceBasicInfo(models.Model):
    device_id = BetterCharField(8, unique=True, verbose_name='设备ID')
    mobile = models.CharField(max_length=16, null=False, verbose_name='手机号')
    imsi = models.CharField(max_length=32, null=False, verbose_name='手机imsi')
    imei = models.CharField(max_length=32, null=False, verbose_name='手机imei')
    iccid = models.CharField(max_length=32, null=False, verbose_name='手机iccid')
    base_station = models.CharField(max_length=512, null=False, verbose_name='基站信息')
    serial_number = BetterCharField(16, default=0, verbose_name='产品序列号')
    hardware_ver = BetterCharField(16, null=False, verbose_name='硬件版本号')
    firmware_ver = BetterCharField(32, null=False, verbose_name='固件版本号')
    protocol_ver = BetterCharField(16, null=False, verbose_name='协议版本号')
    produce_time = models.DateTimeField(auto_now=True, verbose_name='生成信息时间')
    customize = BetterCharField(16, null=False, verbose_name='定制号')
    status = models.IntegerField(default=0, verbose_name='状态 0:初始化 1:出厂 2:被绑定')
    intime = models.DateTimeField(auto_now=False, null=True, verbose_name='写入时间')
    modtime = models.DateTimeField(auto_now=False, null=True, verbose_name='更新时间')

    class Meta:
        db_table = 'device_basic_info'

    def __unicode__(self):
        return u'%s %s %s %s %s %s %s %s %s %s %s %d %s %s' % (self.device_id, self.mobile, self.imsi, self.imei,
                self.iccid, self.base_station, self.serial_number, self.hardware_ver, self.firmware_ver,
                self.protocol_ver, self.produce_time, self.status, self.intime, self.modtime)


class DeviceStatusRel(models.Model):
    device_id = BetterCharField(8, primary_key=True, verbose_name='设备ID')
    power = models.IntegerField(default=0, verbose_name='外接电源状态')
    battery = models.IntegerField(default=0, verbose_name='电池剩余电量')
    sensor = models.IntegerField(default=0, verbose_name='传感器状态')
    comm = models.IntegerField(default=0, verbose_name='通讯状态')
    audio = models.IntegerField(default=0, verbose_name='音频模块的状态')
    power_light = models.IntegerField(default=0, verbose_name='电源灯状态')
    service_light = models.IntegerField(default=0, verbose_name='服务灯状态')
    bg_light = models.CharField(max_length=16, blank=True, null=False, verbose_name='背景灯状态')
    time_light = models.CharField(max_length=32, blank=True, null=False, verbose_name='时段灯状态')
    weight_change = models.CharField(max_length=16, blank=True, null=False, verbose_name='药箱重量状态')
    lack_med_status = models.IntegerField(default=0, verbose_name='补药提醒')
    intime = models.DateTimeField(auto_now=False, null=True, verbose_name='记录时间')
    modtime = models.DateTimeField(auto_now=False, null=True, verbose_name='修改时间')

    class Meta:
        db_table = 'device_status_realtime'

    def __unicode__(self):
        return u'%s %d %d %d %d %d %d %d %s %s %s %d %s %s' % (self.device_id, self.power, self.battery, self.sensor, self.comm,
                    self.audio, self.power_light, self.service_light, self.bg_light, self.time_light, self.weight_change,
                    self.lack_med_status, self.intime, self.modtime)

class DeviceStatusHis(models.Model):
    device_id = BetterCharField(8, verbose_name='设备ID')
    power = models.IntegerField(default=0, verbose_name='外接电源状态')
    battery = models.IntegerField(default=0, verbose_name='电池剩余电量')
    sensor = models.IntegerField(default=0, verbose_name='传感器状态')
    comm = models.IntegerField(default=0, verbose_name='通讯状态')
    audio = models.IntegerField(default=0, verbose_name='音频模块的状态')
    power_light = models.IntegerField(default=0, verbose_name='电源灯状态')
    service_light = models.IntegerField(default=0, verbose_name='服务灯状态')
    bg_light = models.CharField(max_length=16, blank=True, null=False, verbose_name='背景灯状态')
    time_light = models.CharField(max_length=32, blank=True, null=False, verbose_name='时段灯状态')
    weight_change = models.CharField(max_length=16, blank=True, null=False, verbose_name='药箱重量状态')
    lack_med_status = models.IntegerField(default=0, verbose_name='补药提醒')
    intime = models.DateTimeField(auto_now=False, null=True, verbose_name='记录时间')
    modtime = models.DateTimeField(auto_now=False, null=True, verbose_name='修改时间')

    class Meta:
        db_table = 'device_status_his'

    def __unicode__(self):
        return u'%s %d %d %d %d %d %d %d %s %s %s %d %s %s' % (self.device_id, self.power, self.battery, self.sensor, self.comm,
                    self.audio, self.power_light, self.service_light, self.bg_light, self.time_light, self.weight_change,
                    self.lack_med_status, self.intime, self.modtime)

class DeviceRecord(models.Model):
    device_id = BetterCharField(8, verbose_name='设备ID')
    cover_status = models.IntegerField(default=0, verbose_name='箱盖状态')
    open_time = models.DateTimeField(null=True, verbose_name='盒盖打开时间')
    close_time = models.DateTimeField(null=True, verbose_name='盒盖关闭时间')
    weights = models.CharField(max_length=64, blank=True, default=None, null=True, verbose_name='药盒重量')
    slot_weights = models.CharField(max_length=256, default=0, verbose_name='过滤前的原始重量')
    judge_levels = models.CharField(max_length=64, default=0, verbose_name='判断级别')
    intime = models.DateTimeField(auto_now=False, null=True, verbose_name='记录时间')
    modtime = models.DateTimeField(auto_now=False, null=True, verbose_name='修改时间')

    class Meta:
        db_table = 'device_record'

    def __unicode__(self):
        return u'%s %d %s %s %s %s %s %s' % (self.device_id, self.coverStatus, self.openTime, self.closeTime, self.weights,
                self.slot_weights, self.intime, self.modtime)

class DeviceOperation(models.Model):
    device_id = models.CharField(max_length=8, verbose_name='设备ID')
    op_type = models.IntegerField(default=0, verbose_name='操作类型')
    op_message = models.CharField(max_length=4096, verbose_name='操作信息')
    status = models.IntegerField(default=0, verbose_name='操作状态 0:未执行 1:已推送')
    intime = models.DateTimeField(null=True, verbose_name='记录时间')
    modtime = models.DateTimeField(null=True, verbose_name='修改时间')

    class Meta:
        db_table='device_operation'
        unique_together = ('device_id', 'op_type')

    def __unicode__(self):
        return u'%s %d %s %d %s %s' % (self.device_id, self.op_type, self.op_message, self.status, self.intime,
                self.modtime)

class DeviceOperationHis(models.Model):
    device_id = BetterCharField(8, verbose_name='设备ID')
    op_type = models.IntegerField(default=0, verbose_name='操作类型')
    op_message = models.CharField(max_length=4096, verbose_name='操作类型')
    status = models.IntegerField(default=0, verbose_name='操作状态 0:未执行 1:已推送')
    intime = models.DateTimeField(auto_now=False, null=True, verbose_name='记录时间')
    modtime = models.DateTimeField(auto_now=False, null=True, verbose_name='修改时间')

    class Meta:
        db_table = 'device_operation_his'

    def __unicode__(self):
        return u'%s %d %s %d %s %s' % (self.device_id, self.op_type, self.op_message, self.status, self.intime,
                self.modtime)

class DeviceOpResult(models.Model):
    device_id = BetterCharField(8, verbose_name='设备ID')
    device_op_id = models.IntegerField(default=0, verbose_name='操作id')
    op_type = models.IntegerField(default=0, verbose_name='异常类型')
    op_time = models.DateTimeField(null=True, verbose_name='操作时间')
    result = models.IntegerField(default=0, verbose_name='操作的结果')
    reason = models.CharField(max_length=100, verbose_name='失败原因')
    intime = models.DateTimeField(auto_now=False, null=True, verbose_name='记录时间')
    modtime = models.DateTimeField(auto_now=False, null=True, verbose_name='修改时间')

    class Meta:
        db_table = 'device_op_result'

    def __unicode__(self):
        return u'%s %d %d %s %d %s %s %s' % (self.device_id, self.device_op_id, self.type, self.timestamp, self.result,
                self.reason, self.intime, self.modtime)

class DeviceException(models.Model):
    device_id = BetterCharField(8, verbose_name='设备ID')
    type = models.IntegerField(default=0,verbose_name='异常类型')
    reason = models.CharField(max_length=2048, verbose_name='失败原因')
    intime = models.DateTimeField(auto_now=False, null=True, verbose_name='记录时间')
    modtime = models.DateTimeField(auto_now=False, null=True, verbose_name='修改时间')

    class Meta:
        db_table = 'device_exception'

    def __unicode__(self):
        return u'%s %d %s, %s, %s' % (self.device_id, self.type, self.reason, self.intime, self.modtime)

class Version(models.Model):
    ver_num = models.CharField(max_length=16, verbose_name='版本号')
    ver_type = models.IntegerField(default=0,verbose_name='版本类型 0:正式版 1:alpha版 2:beta版')
    customize = models.CharField(max_length=16, verbose_name='定制号')
    file_name = models.CharField(max_length=64, verbose_name='mcu文件名')
    ver_size = models.IntegerField(default=0,verbose_name='版本大小 单位字节')
    update_mode = models.IntegerField(default=0,verbose_name='升级方式 0:定时升级 1:强制升级')
    update_time = models.IntegerField(default=0,verbose_name='升级时间，距离0点的分钟数，默认凌晨2点')
    assign_devices = models.CharField(max_length=512,verbose_name='指定升级药箱 药箱ID使用逗号(,)分隔')
    status = models.IntegerField(default=0,verbose_name='状态 0:无效 1:有效')
    intime = models.DateTimeField(auto_now=False, verbose_name='记录时间')
    modtime = models.DateTimeField(auto_now=False, verbose_name='修改时间')
    #time_sign = models.CharField(max_length=16, verbose_name='时间戳 格式:1511271832')

    class Meta:
        db_table = 'device_mcu'

    def __unicode__(self):
        return u'%s %d %s %d %s %s' % (self.ver_num, self.ver_size, self.file_name, self.status, self.intime, self.modtime)

#用户信息
class UserInfo(models.Model):
    user_id = BetterCharField(10, verbose_name='用户ID', primary_key=True)
    device_id = BetterCharField(8, verbose_name = "药箱ID")
    user_name = models.CharField(max_length=16, null=True, default=0, verbose_name='用户名称')
    user_pwd = models.CharField(max_length=32, null=True, default=0, verbose_name='用户密码')
    user_sex = models.IntegerField(default=0, verbose_name='性别')
    user_mobile = BetterCharField(16, null=True, default=0, verbose_name = "手机")
    user_tel = BetterCharField(16, null=True, default=0, verbose_name = "电话")
    user_email = BetterCharField(32, null=True, default=0, verbose_name = "邮箱")
    pre_mobile = BetterCharField(16, null=True, default=0, verbose_name = "预留手机")
    pre_mobile_self = models.IntegerField(default=0, verbose_name='是否是本人手机号')
    buy_mobile = BetterCharField(16, null=True, default=0, verbose_name = "购买人手机号")
    buy_patient_relation = models.IntegerField(default=0, verbose_name='与患者关系')
    op_device_relation = models.IntegerField(default=0, verbose_name='操作药箱人与患者关系')

    #is_wechat = BetterCharField(1, verbose_name = "是否绑定微信")

    sicken_type = models.IntegerField(default=0, verbose_name='患病类型')
    sicken_age = models.IntegerField(default=0, verbose_name='病龄')
    health_info = models.CharField(max_length=512, null=True, default=0, verbose_name='健康信息')
    mor_time = models.IntegerField(default=0, verbose_name='早餐时间')
    midd_time = models.IntegerField(default=0, verbose_name='午餐时间')
    night_time = models.IntegerField(default=0, verbose_name='晚餐时间')
    midn_time = models.IntegerField(default=0, verbose_name='夜宵时间')
    remark = models.CharField(max_length=512, null=True, default=0, verbose_name='备注')
    device_status = models.IntegerField(default=0, verbose_name = "绑定药箱状态")

    voice_remind = models.IntegerField(default=0, verbose_name='语音提醒')
    light_remind = models.IntegerField(default=0, verbose_name='灯光提醒')
    supp_med_remind = models.IntegerField(default=0, verbose_name='缺药提醒')
    miss_med_remind = models.IntegerField(default=0, verbose_name='漏吃提醒')
    overturn_help = models.IntegerField(default=0, verbose_name='推倒呼救')
    help_a_mobile = models.CharField(max_length=16, null=True, default=0, verbose_name='呼救1电话')
    help_a_name = models.CharField(max_length=16, null=True, default=0, verbose_name='呼救1姓名')
    help_a_relation = models.CharField(max_length=16, null=True, default=0, verbose_name='呼救人1与患者关系')
    help_b_mobile = models.CharField(max_length=16, null=True, default=0, verbose_name='呼救2电话')
    help_b_name = models.CharField(max_length=16, null=True, default=0, verbose_name='呼救2姓名')
    help_b_relation = models.CharField(max_length=16, null=True, default=0, verbose_name='呼救人2与患者关系')

    inuser = models.CharField(max_length=16, null=True, default=0, verbose_name='创建人')
    moduser = models.CharField(max_length=16, null=True, default=0, verbose_name='修改人')
    intime = models.DateTimeField(auto_now=False, null=True, verbose_name='创建时间')
    modtime = models.DateTimeField(auto_now=False, null=True, verbose_name='修改时间')

    class Meta:
        db_table='user_info'

    #def __unicode__(self):
    #    return u'%s %s %s %s %s %s %s %s %s %s %d %s %s %s %d %d %d %d %s %s %s %s %s %s' % \
    #                    (self.user_id, self.device_id, self.user_name, self.user_pwd, self.user_mobile,
    #                       self.user_tel, self.user_email, self.is_self, self.is_wechat, self.sicken_age,
    #                       self.sicken_type, self.user_sex, self.health_info, self.mor_time, self.midd_time,
    #                       self.night_time, self.midn_time, self.remark, self.box_status, self.inuser, self.moduser,
    #                       self.intime, self.modtime
    #                       )

class DeviceActive(models.Model):
    device_id = BetterCharField(8, primary_key=True, verbose_name='设备ID')
    req_type = models.IntegerField(default=0, verbose_name = "请求类型")
    req_url = models.CharField(max_length=128, null=True, default=0, verbose_name='请求的url')
    req_time = models.DateTimeField(null=True, verbose_name='写入时间')

    class Meta:
        db_table = 'device_active'

    def __unicode__(self):
        return u'%s %d %s %s' % (self.device_id, self.req_type, self.req_url, self.req_time)

'''
class CallCenterUserInfo(models.Model):
    phone = models.CharField(max_length=20, primary_key=True, verbose_name='用户电话')
    device_id = models.CharField(max_length=100, verbose_name='药箱设备ID')
    user_name = models.CharField(max_length=100, verbose_name='用户姓名')
    op_man = models.CharField(max_length=100, verbose_name='操作规则')
    DM_type = models.CharField(max_length=100, verbose_name='糖尿病类型')
    medical_history = models.IntegerField(default=0, verbose_name='病史 /年')

    class Meta:
        db_table = 'center_user_info'

    def __unicode__(self):
        return u'%s %s %s %s %s %d' % (self.phone, self.device_id, self.user_name, self.op_man, self.DM_type, \
                                          self.medical_history)
'''

'''
class UserFeedback(models.Model):
    user_id = BetterCharField(10, verbose_name='用户ID')
    type = BetterCharField(2, verbose_name='问题类型')
    de = models.CharField(max_length=512, verbose_name='问题描述')
    status = BetterCharField(1, verbose_name='状态')
    inuser = models.CharField(max_length=16, verbose_name='创建人')
    moduser = models.CharField(max_length=16, verbose_name='修改人')
    intime = models.DateTimeField(null=True, verbose_name='创建时间')
    modtime = models.DateTimeField(null=True, verbose_name='修改时间')

    class Meta:
        db_table='T_USER_FEEDBACK'

    def __unicode__(self):
        return u'%s %s %s %s %s %s %s %s' % (self.user_id, self.type, self.de, self.status, self.inuser, self.moduser,
                             self.intime, self.modtime)
'''

'''
class UserMedicine(models.Model):
    user_name = BetterCharField(10, verbose_name = "用户ID")
    box_id = BetterCharField(8, verbose_name = "药箱ID")
    medicine = models.CharField(max_length=64, verbose_name='药品名称')
    dose = BetterCharField(1, verbose_name='用药量')
    site = BetterCharField(1, verbose_name='药箱位置')
    dose_type = BetterCharField(1, verbose_name='用餐服药时段')
    dose_time = models.IntegerField(default=0, verbose_name='用餐服药间隔时间')
    #morning = BetterCharField(2, verbose_name='早')
    morning = models.IntegerField(default=0, verbose_name='早')
    midday = models.IntegerField(default=0, verbose_name='中')
    night = models.IntegerField(default=0, verbose_name='晚')
    midnight = models.IntegerField(default=0, verbose_name='夜')
    status = models.IntegerField(default=0, verbose_name='状态')
    des = models.CharField(max_length=512, verbose_name='自动提示信息')
    remark = models.CharField(max_length=512, verbose_name='备注')
    inuser = models.CharField(max_length=16, verbose_name='创建人')
    moduser = models.CharField(max_length=16, verbose_name='修改人')
    intime = models.DateTimeField(null=True, verbose_name='创建时间')
    modtime = models.DateTimeField(null=True, verbose_name='修改时间')

    class Meta:
        db_table='T_USER_MEDICINE'

    def __unicode__(self):
        return u'%s %s %s %s %s %s %d %s %s %s %s %d %s %s %s %s %s %s' % \
                                    (self.user_name, self.box_id, self.medicine, self.dose, self.site, self.dose_type, \
                                   self.dose_time, self.morning, self.midday, self.night, self.midnight, self.status,  \
                                   self.des, self.remark, self.inuser, self.moduser, self.intime, self.modtime)
'''
'''
class MedicineLibrary(models.Model):
    medicine_id = BetterCharField(8, verbose_name = "药品ID")
    medicine_name = BetterCharField(32, verbose_name = "药名字")
    medicine_origin_name = BetterCharField(32, verbose_name = "药品名字")
    large_class = BetterCharField(32, verbose_name = "大类")
    small_class = BetterCharField(32, verbose_name = "小类")
    effect = BetterCharField(32, verbose_name = "作用")
    specifications = BetterCharField(32, verbose_name = "规格")
    company = BetterCharField(64, verbose_name = "公司名")

    piece_weight = models.IntegerField(default=0, verbose_name='每片重量(mg)')
    per_box_weight = models.IntegerField(default=0, verbose_name='每盒重量(mg)')

    number = BetterCharField(16, verbose_name = "次/天")
    dose = BetterCharField(16, verbose_name = "片/次")
    taking_time = BetterCharField(32, verbose_name = "建议服药时间")
    piece = models.IntegerField(default=0, verbose_name='片/板')
    board = models.IntegerField(default=0, verbose_name='板/月')
    weight_box_month = models.IntegerField(default=0, verbose_name='重量（1盒药）／月（mg）')
    weight_board_month = models.IntegerField(default=0, verbose_name='重量（1板药）／月（mg）')
    board_box = models.IntegerField(default=0, verbose_name='板／盒')
    net_weight = models.IntegerField(default=0, verbose_name='净重（1板不含包装）／盒（mg）')

    remarks = BetterCharField(255, verbose_name = "备注")
    adverse_reactions = BetterCharField(255, verbose_name = "不良反应")
    drug_conflict = BetterCharField(255, verbose_name = "药物冲突")


    class Meta:
        db_table='T_MEDICINE_LIBRARY'

    def __unicode__(self):
        return u'%s %s %s %s %s %s %s %s %d %d %s %s %s %s %s %s %s %s %s' % \
               (self.medicine_id, self.medicine_name, self.medicine_origin_name, self.large_class, self.small_class,
                self.effect, self.specifications, self.company, self.piece_weight, self.per_box_weight, self.number,
                self.dose, self.taking_time, self.piece, self.board, self.weight_box_month, self.weight_board_month,
                self.board_box, self.net_weight)
'''

#from south.modelsinspector import add_introspection_rules
'''
rules = [((BetterCharField,),
    [],
    {
        'to': ['rel.to', {'default': User}],
        'null': ['null', {'default': True}],
    },)]
'''
