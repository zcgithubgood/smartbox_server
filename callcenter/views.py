# Create your views here.
# -*- coding:utf-8 -*-
from django.shortcuts import render_to_response
import datetime
import cPickle


from django.core.files.storage import default_storage
from django.db.models.fields.files import FieldFile
from django.views.generic import FormView
from django.views.generic.base import TemplateView
from django.contrib import messages
from .forms import ContactConfigForm, ContactUserInfoForm, UploadFileForm, AdUplaodFileForm

from data.models import *
from django.template import RequestContext
from django.http import HttpResponseRedirect
import json

# http://yuji.wordpress.com/2013/01/30/django-form-field-in-initial-data-requires-a-fieldfile-instance/
class FakeField(object):
    storage = default_storage


fieldfile = FieldFile(None, FakeField, 'dummy.txt')


#class HomePageView(TemplateView):
    #template_name = 'demo/home.html'

    #def get_context_data(self, **kwargs):
    #    context = super(HomePageView, self).get_context_data(**kwargs)
    #    messages.info(self.request, 'CallCenter系统.')
    #    return context


def contact_thanks(request):
    return render_to_response('contact_thanks.html')

def Signin(request):
    errors = []
    if 'user' in request.GET and 'passwd' in request.GET:
        user = request.GET['user']
        passwd = request.GET['passwd']
        print "user:%s, passwd:%s" % (user, passwd)

        if not user:
            errors.append('请输入手机/邮箱/用户')
        elif len(user) > 20:
            errors.append('请输入最多20个字符')
        else:
            if user == 'admin' and passwd == 'zc123':
            #return render_to_response('search_results.html')
                    return HttpResponseRedirect('demo/home.html')
            else:
                errors.append('账号或密码错误')
    else:
        errors.append('请输入账号')

    return render_to_response('demo/signin/index.html', {'errors': errors})

def HomePageView(request):
    errors = []
    if 'id' in request.GET:
        id = request.GET['id']
        print "id"
        print id

        if not id:
            errors.append('请输入药箱ID或者手机号')
        elif len(id) > 20:
            errors.append('请输入最多20个字符')
        else:
            #BasicInfo = DeviceBasicInfo.objects.filter(device_id=id)
            deviceRecord = DeviceRecord.objects.filter(device_id=id)
            #return render_to_response('search_results.html',{'BasicInfo':BasicInfo, 'device_id':id})
            return render_to_response('search_results.html',{'deviceRecord':deviceRecord, 'device_id':id})
    return render_to_response('demo/home.html', {'errors': errors})

#class DefaultFormsetView(FormView):
    #template_name = 'demo/formset.html'
    #template_name = 'demo/form.html'
    #form_class = ContactUserInfoForm

def UserInfoSetView(request):
    errors = []
    if request.method == 'POST':
        #print request.POST
        form = ContactUserInfoForm(request.POST)
        #print "1 ========="
        #print form
        if form.is_valid():
            cd = form.cleaned_data
            #print "2 ========="
            #print cd
            '''
            BoxResInfo = BoxReserve()
            BoxId = cd['box_id']
            Iphone = cd['user_iphone']
            SaveFlag = 0
            if BoxId:
                BoxResInfo.device_id = BoxId
                SaveFlag = 1

            if Iphone:
                BoxResInfo.phone = Iphone
                SaveFlag += 1

            if SaveFlag is 2:
            '''
            if cd['box_id'] and cd['user_iphone']:
                BoxBindInfo = BoxBind()
                BoxBindInfo.device_id = cd['box_id']
                BoxBindInfo.userid = cd['user_iphone']
                BoxBindInfo.save()

                if cd['op_box']:
                    BoxOp = BoxOperation()
                    BoxOp.device_id = cd['box_id']
                    BoxOp.type = cd['op_box']
                    BoxOp.save()
                user_info = CallCenterUserInfo()
                user_info.phone = cd['user_iphone']
                user_info.device_id = cd['box_id']
                if cd['user_name']:
                    user_info.user_name = cd['user_name']
                user_info.op_man = cd['op_man']
                user_info.DM_type = cd['DM_type']
                if cd['medical_history']:
                    user_info.medical_history = cd['medical_history']
                user_info.save()
                #return HttpResponseRedirect('/callcenter/thanks/')
                print "cd['op_box']"
                print cd['op_box']
                if cd['op_box'] == "1":
                    form = ContactConfigForm(
                        initial={'user_iphone': cd['user_iphone'], 'box_id':cd['box_id']}
                    )
                else:
                    return HttpResponseRedirect('/callcenter/thanks/')
    else:
        form = ContactUserInfoForm(
             initial={'user_iphone': ''}
        )
    return render_to_response('demo/form.html', {'form': form, 'errors': errors},
                              context_instance=RequestContext(request))


#class DefaultFormView(FormView):
    #template_name = 'demo/config_form.html'
    #form_class = ContactConfigForm

def DefaultFormView(request):
    errors = []
    if request.method == 'POST':
        #print request.POST
        form = ContactConfigForm(request.POST)
        #print "1 ========="
        #print form
        if form.is_valid():
            cd = form.cleaned_data
            BoxConfInfo = BoxConfig()

            #for (k,v) in cd.items():
            #    print '%s:%s' %(k, v)
            #print "list:"
            #print list(cd.items())
            BoxConfInfo.phone = cd['user_iphone']
            BoxConfInfo.device_id = cd['box_id']

            #type:3 配置药箱
            BoxOp = BoxOperation()
            BoxOp.device_id = BoxConfInfo.device_id
            BoxOp.type = 3
            BoxOp.save()

            BoxConfInfo.slot1_medicine_id = 0001
            if cd['slot1_medicine_name']:
                BoxConfInfo.slot1_medicine_name = cd['slot1_medicine_name']
            if cd['slot1_meals']:
                BoxConfInfo.slot1_meals = cd['slot1_meals']
            if cd['slot1_piece']:
                BoxConfInfo.slot1_piece = cd['slot1_piece']
            #print "cd['slot1_moning']:"
            #print cd['slot1_moning']
            if cd['slot1_moning']:
                #BoxConfInfo.slot1_moning = '%02d%02d' % (cd['slot1_moning'].hour, cd['slot1_moning'].minute)
                BoxConfInfo.slot1_moning = '%d' % (cd['slot1_moning'].hour*60 + cd['slot1_moning'].minute - cd['slot1_mealstime'])
            if cd['slot1_noon']:
                #BoxConfInfo.slot1_noon = '%02d%02d' % (cd['slot1_noon'].hour, cd['slot1_noon'].minute)
                BoxConfInfo.slot1_noon = '%d' % (cd['slot1_noon'].hour*60 + cd['slot1_noon'].minute - cd['slot1_mealstime'])
            if cd['slot1_evening']:
                #BoxConfInfo.slot1_evening = '%02d%02d' % (cd['slot1_evening'].hour, cd['slot1_evening'].minute)
                BoxConfInfo.slot1_evening = '%d' % (cd['slot1_evening'].hour*60 + cd['slot1_evening'].minute - cd['slot1_mealstime'])
            if cd['slot1_nigh']:
                #BoxConfInfo.slot1_nigh = '%02d%02d' % (cd['slot1_nigh'].hour, cd['slot1_nigh'].minute)
                BoxConfInfo.slot1_nigh = '%d' % (cd['slot1_nigh'].hour*60 + cd['slot1_nigh'].minute - cd['slot1_mealstime'])

            BoxConfInfo.slot2_medicine_id = 0002
            if cd['slot2_medicine_name']:
                BoxConfInfo.slot2_medicine_name = cd['slot2_medicine_name']
            if cd['slot2_meals']:
                BoxConfInfo.slot2_meals = cd['slot2_meals']
            if cd['slot2_piece']:
                BoxConfInfo.slot2_piece = cd['slot2_piece']
            #total*2 = (cd['slot2_moning'].hour * 60 + cd['slot2_moning'].minute) / 60 - cd['slot1_mealstime']
            if cd['slot2_moning']:
                #BoxConfInfo.slot2_moning = '%02d%02d' % (cd['slot2_moning'].hour, cd['slot2_moning'].minute)
                BoxConfInfo.slot2_moning = '%d' % (cd['slot2_moning'].hour*60 + cd['slot2_moning'].minute)
            if cd['slot2_noon']:
                #BoxConfInfo.slot2_noon = '%02d%02d' % (cd['slot2_noon'].hour, cd['slot2_noon'].minute)
                BoxConfInfo.slot2_noon = '%d' % (cd['slot2_noon'].hour*60 + cd['slot2_noon'].minute)
            if cd['slot2_evening']:
                #BoxConfInfo.slot2_evening = '%02d%02d' % (cd['slot2_evening'].hour, cd['slot2_evening'].minute)
                BoxConfInfo.slot2_evening = '%d' % (cd['slot2_evening'].hour*60 + cd['slot2_evening'].minute)
            if cd['slot2_nigh']:
                #BoxConfInfo.slot2_nigh = '%02d%02d' % (cd['slot2_nigh'].hour, cd['slot2_nigh'].minute)
                BoxConfInfo.slot2_nigh = '%d' % (cd['slot2_nigh'].hour*60 + cd['slot2_nigh'].minute)

            BoxConfInfo.slot3_medicine_id = 0003
            if cd['slot3_medicine_name']:
                BoxConfInfo.slot3_medicine_name = cd['slot3_medicine_name']
            if cd['slot3_meals']:
                BoxConfInfo.slot3_meals = cd['slot3_meals']
            if cd['slot3_piece']:
                BoxConfInfo.slot3_piece = cd['slot3_piece']
            if cd['slot3_moning']:
                #BoxConfInfo.slot3_moning = '%02d%02d' % (cd['slot3_moning'].hour, cd['slot3_moning'].minute)
                BoxConfInfo.slot3_moning = '%d' % (cd['slot3_moning'].hour*60 + cd['slot3_moning'].minute)
            if cd['slot3_noon']:
                #BoxConfInfo.slot3_noon = '%02d%02d' % (cd['slot3_noon'].hour, cd['slot3_noon'].minute)
                BoxConfInfo.slot3_noon = '%d' % (cd['slot3_noon'].hour*60 + cd['slot3_noon'].minute)
            if cd['slot3_evening']:
                #BoxConfInfo.slot3_evening = '%02d%02d' % (cd['slot3_evening'].hour, cd['slot3_evening'].minute)
                BoxConfInfo.slot3_evening = '%d' % (cd['slot3_evening'].hour*60 + cd['slot3_evening'].minute)
            if cd['slot3_nigh']:
                #BoxConfInfo.slot3_nigh = '%02d%02d' % (cd['slot3_nigh'].hour, cd['slot3_nigh'].minute)
                BoxConfInfo.slot3_nigh = '%d' % (cd['slot3_nigh'].hour*60 + cd['slot3_nigh'].minute)

            BoxConfInfo.slot4_medicine_id = 0004
            if cd['slot4_medicine_name']:
                BoxConfInfo.slot4_medicine_name = cd['slot4_medicine_name']
            if cd['slot4_meals']:
                BoxConfInfo.slot4_meals = cd['slot4_meals']
            if cd['slot4_piece']:
                BoxConfInfo.slot4_piece = cd['slot4_piece']
            if cd['slot4_moning']:
                #BoxConfInfo.slot4_moning = '%02d%02d' % (cd['slot4_moning'].hour, cd['slot4_moning'].minute)
                BoxConfInfo.slot4_moning = '%d' % (cd['slot4_moning'].hour*60 + cd['slot4_moning'].minute)
            if cd['slot4_noon']:
                #BoxConfInfo.slot4_noon = '%02d%02d' % (cd['slot4_noon'].hour, cd['slot4_noon'].minute)
                BoxConfInfo.slot4_noon = '%d' % (cd['slot4_noon'].hour*60 + cd['slot4_noon'].minute)
            if cd['slot4_evening']:
                #BoxConfInfo.slot4_evening = '%02d%02d' % (cd['slot4_evening'].hour, cd['slot4_evening'].minute)
                BoxConfInfo.slot4_evening = '%d' % (cd['slot4_evening'].hour*60 + cd['slot4_evening'].minute)
            if cd['slot4_nigh']:
                #BoxConfInfo.slot4_nigh = '%02d%02d' % (cd['slot4_nigh'].hour, cd['slot4_nigh'].minute)
                BoxConfInfo.slot4_nigh = '%d' % (cd['slot4_nigh'].hour*60 + cd['slot4_nigh'].minute)

            BoxConfInfo.save()
            return HttpResponseRedirect('/callcenter/thanks/')
    else:
        form = ContactConfigForm(
             initial={'user_iphone': '137'}
        )
    #if form.is_valid()
    return render_to_response('demo/form.html', {'form': form, 'errors': errors},
                              context_instance=RequestContext(request))


'''
class DefaultFormByFieldView(FormView):
    template_name = 'demo/form_by_field.html'
    form_class = ContactConfigForm


class FormHorizontalView(FormView):
    template_name = 'demo/form_horizontal.html'
    form_class = ContactConfigForm


class FormInlineView(FormView):
    template_name = 'demo/form_inline.html'
    form_class = ContactConfigForm


class FormWithFilesView(FormView):
    template_name = 'demo/form_with_files.html'
    form_class = ContactConfigForm

    def get_context_data(self, **kwargs):
        context = super(FormWithFilesView, self).get_context_data(**kwargs)
        context['layout'] = self.request.GET.get('layout', 'vertical')
        return context

    def get_initial(self):
        return {
            'file4': fieldfile,
        }

class PaginationView(TemplateView):
    template_name = 'demo/pagination.html'

    def get_context_data(self, **kwargs):
        context = super(PaginationView, self).get_context_data(**kwargs)
        lines = []
        for i in range(10000):
            lines.append('Line %s' % (i + 1))
        paginator = Paginator(lines, 10)
        page = self.request.GET.get('page')
        try:
            show_lines = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            show_lines = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            show_lines = paginator.page(paginator.num_pages)
        context['lines'] = show_lines
        return context


class MiscView(TemplateView):
    template_name = 'demo/misc.html'
'''

def MedicineLibraryFormView(request):
    errors = []
    if request.method == 'POST':
        #print request.POST
        #form = ContactConfigForm(request.POST)
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            filehandle = request.FILES['file']
            return excel.make_response(filehandle.get_sheet(), "csv")
    else:
        form = UploadFileForm(request.POST, request.FILES)
    return render_to_response('demo/form.html', {'form': form, 'errors': errors},
                              context_instance=RequestContext(request))


def current_datetime(request):
    now = datetime.datetime.now()
    return render_to_response('current_datetime.html', locals())

def bootstrap_test(request):
    return render_to_response('strap_test.html')

def handle_uploaded_file(f):
    destination = open('../download/box_mcu.bin', 'wb+')
    print "handle_uploaded_file"
    print destination.read()
    for chunk in f.chunks():
        destination.write(chunk)
        destination.close()

def UploadUpgrade(request):
    errors = []
    #print "1 +++++++++++++"
    #print request
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        print "2 +++++++++++++"
        print form
        if form.is_valid():
            print "3 +++++++++++++"
            file_name = request.FILES['file']
            if file_name:
                version = Version()
                version.ver_num = "1.0.0"
                version.ver_size = 123
                version.file_name = file_name
                version.status = 1
                version.save()

                handle_uploaded_file(request.FILES['file'])
                return HttpResponseRedirect('/callcenter/thanks/')
    else:
        form = UploadFileForm()
    return render_to_response('demo/upload.html', {'form': form, 'errors': errors},
                              context_instance=RequestContext(request))

def AdUpload(request):
    errors = []
    #print "1 +++++++++++++"
    #print request
    if request.method == 'POST':
        form = AdUplaodFileForm(request.POST, request.FILES)
        print "2 +++++++++++++"
        print form
        if form.is_valid():
            cd = form.cleaned_data
            print "3 +++++++++++++"

            #operation = DeviceOperation()

            try:
                flag = 0
                for operation in DeviceOperation.objects.filter(device_id=str(cd['box_id']), op_type=4):
                    #operation.device_id = str(cd['box_id'])
                    #operation.op_type = 4
                    message = {}
                    message['index'] = 1
                    print cd['text']
                    message['text'] = str(cd['text']).decode("utf-8") #cd['text'].encode('utf8')#.encode('gb2312')#str(cd['text'].encode('GBK'))
                    print "+++++++++++++++++++"
                    print message
                    operation.op_message = json.dumps(message)#cPickle.dumps(json.dumps(message))
                    operation.status = 0
                    print operation.op_message
                    operation.save(update_fields=['op_message','status'])
                    flag = 1
                    break

                if flag == 0:
                    operation = DeviceOperation()
                    message = {}
                    message['index'] = 1
                    message['text'] = str(cd['text']).encode('utf8')
                    operation.device_id = str(cd['box_id'])
                    operation.op_type = 4
                    operation.op_message = cd['text']#json.dumps(message)
                    operation.status = 0
                    operation.save()

            except DeviceOperation.DoesNotExist:
                pass

            return HttpResponseRedirect('/callcenter/thanks/')
    else:
        form = AdUplaodFileForm(
            initial={'text':u'床前明月光，疑是地上霜，举头望明月，我是小药箱'}
        )
    return render_to_response('demo/form.html', {'form': form, 'errors': errors},
                              context_instance=RequestContext(request))


from django.shortcuts import render
from django.views.decorators.cache import cache_page

@cache_page(60 * 15) # 秒数，这里指缓存 15 分钟，不直接写900是为了提高可读性
def index(request):
    # 读取数据库等 并渲染到网页
    return render(request, 'index.html', {'queryset':queryset})
