# -*- coding:utf-8 -*-
__author__ = 'druid'
from django.contrib import admin
#from data.models import BoxReserve, BoxBasicInfo, BoxStatus, BoxRecord, BoxOperation, BoxOpResult, BoxException
from data.models import *

class DeviceReqSupAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'status', 'intime', 'modtime')

class DeviceBasicInfoAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'mobile', 'imsi', 'imei', 'iccid', 'base_station', 'serial_number', 'hardware_ver',
                    'firmware_ver', 'protocol_ver', 'produce_time', 'customize', 'status', 'intime', 'modtime')

    #search_fields = ('device_id')

class DeviceStatusRelAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'power', 'battery', 'sensor', 'comm', 'audio', 'power_light', 'service_light',
                    'bg_light', 'time_light', 'weight_change', 'lack_med_status', 'intime', 'modtime')

class DeviceStatusHisAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'power', 'battery', 'sensor', 'comm', 'audio', 'power_light', 'service_light',
                    'bg_light', 'time_light', 'weight_change', 'lack_med_status', 'intime', 'modtime')

class DeviceRecordAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'cover_status', 'open_time', 'close_time', 'weights', 'slot_weights', 'judge_levels', 'intime', 'modtime')

class DeviceOperationAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'op_type', 'op_message', 'status', 'intime', 'modtime')

class DeviceOperationHisAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'op_type', 'op_message', 'status', 'intime', 'modtime')

class DeviceOpResultAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'device_op_id', 'op_type', 'op_time', 'result', 'reason', 'intime', 'modtime')

class DeviceExceptionAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'type', 'reason', 'intime', 'modtime')

class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'device_id', 'user_name', 'user_pwd', 'user_sex', 'user_mobile', 'user_tel', 'user_email',
                    'pre_mobile', 'pre_mobile_self', 'buy_mobile', 'buy_patient_relation', 'op_device_relation',
                    #'is_wechat', 
		            'sicken_type', 'sicken_age', 'health_info', 'mor_time',  'midd_time', 'night_time',
                    'midn_time', 'remark', 'device_status', 'voice_remind', 'light_remind', 'supp_med_remind',
                    'miss_med_remind', 'overturn_help', 'help_a_mobile', 'help_a_name', 'help_a_relation', 'help_b_mobile',
                    'help_b_name', 'help_b_relation', 'inuser', 'moduser', 'intime', 'modtime')

class DeviceActiveAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'req_type', 'req_url', 'req_time')

class VersionAdmin(admin.ModelAdmin):
    list_display = ('ver_num', 'ver_type', 'customize', 'file_name', 'ver_size', 'update_mode', 'update_time', 'assign_devices',
                    'status') 

#class UserFeedbackAdmin(admin.ModelAdmin):
#    list_display = ('user_id', 'type', 'de', 'status', 'inuser', 'moduser', 'intime', 'modtime')

#class UserMedicineAdmin(admin.ModelAdmin):
#    list_display = ('user_name', 'box_id', 'medicine', 'dose', 'site', 'dose_type', 'dose_time', 'morning', 'midday',
#                    'night', 'midnight', 'status', 'des', 'remark', 'inuser', 'moduser', 'intime', 'modtime')


#class CallCenterUserInfoAdmin(admin.ModelAdmin):
#    list_display = ('phone', 'device_id', 'user_name', 'op_man', 'DM_type', 'medical_history')


admin.site.register(DeviceReqSup, DeviceReqSupAdmin)
admin.site.register(DeviceBasicInfo, DeviceBasicInfoAdmin)
admin.site.register(DeviceStatusRel, DeviceStatusRelAdmin)
admin.site.register(DeviceStatusHis, DeviceStatusHisAdmin)
admin.site.register(DeviceRecord, DeviceRecordAdmin)
admin.site.register(DeviceOperation, DeviceOperationAdmin)
admin.site.register(DeviceOperationHis, DeviceOperationHisAdmin)
admin.site.register(DeviceOpResult, DeviceOpResultAdmin)
admin.site.register(DeviceException, DeviceExceptionAdmin)
admin.site.register(Version, VersionAdmin)
admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(DeviceActive, DeviceActiveAdmin)

#admin.site.register(UserFeedback, UserFeedbackAdmin)
#admin.site.register(UserMedicine, UserMedicineAdmin)
#admin.site.register(MedicineLibrary)
#admin.site.register(CallCenterUserInfo, CallCenterUserInfoAdmin)
