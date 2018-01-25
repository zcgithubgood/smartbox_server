import os
from django_cron import CronJobBase, Schedule
from data.models import *

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 10
    #RUN_AT_TIMES = ['00:01']

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    #schedule = Schedule(run_every_mins=RUN_EVERY_MINS, run_at_times=RUN_AT_TIMES)
    code = 'smartbox.my_cron_job'    # a unique code

    #homedir = os.getcwd()

    def do(self):
        # do your thing here
        print "love baby!"
        for version in Version.objects.filter(status = 1):
            verson_new = version.version_name
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
            break


