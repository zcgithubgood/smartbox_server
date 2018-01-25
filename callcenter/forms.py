# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.forms.formsets import BaseFormSet, formset_factory


#from bootstrap3.tests import TestForm

RADIO_CHOICES = (
    ('1', 'Radio 1'),
    ('2', 'Radio 2'),
)

MEDIA_CHOICES = (
    ('Audio', (
        ('vinyl', 'Vinyl'),
        ('cd', 'CD'),
    )
    ),
    ('Video', (
        ('vhs', 'VHS Tape'),
        ('dvd', 'DVD'),
    )
    ),
    ('unknown', 'Unknown'),
)

TOPIC_CHOICES = (
        ('leve1', '早餐'),
        ('leve2', '中餐'),
        ('leve3', '晚餐'),
        ('leve4', '夜宵'),
)

OPMAN_CHOICES = (
    ('本人操作','本人操作'),
    ('子女代操作','子女代操作'),
    ('朋友代操作','朋友代操作'),
    ('邻居代操作','邻居代操作'),
    ('同事代操作','同事代操作'),
    ('病友代操作','病友代操作'),
    ('医生或护士代操作','医生或护士代操作'),
    ('非本人操作','非本人操作'),
)

DM_TYPE = (
    ('糖尿病2型','糖尿病2型'),
    ('糖尿病1型','糖尿病1型'),
    ('妊娠糖尿病','妊娠糖尿病'),
    ('无病史','无病史')
)

OP_BOX = (
    ('1','绑定手机号'),
    ('2','解绑手机号'),
    ('.0','无操作'),
    ('4','下载音频'),
    ('5', '设置音量'),
    ('6', '设置灯光'),
    ('7', '补充药提醒'),
)

PERIOD = (
    ('1',(u'早上')),
    ('2',(u'中午')),
    ('3', (u'晚上')),
    ('4', (u'夜里'))
)

MEALS = (
    ('1', '饭前'),
    ('2', '饭中'),
    ('3', '饭后'),
)

'''
class FilesForm(forms.Form):
    text1 = forms.CharField()
    file1 = forms.FileField()
    file2 = forms.FileField(required=False)
    file3 = forms.FileField(widget=forms.ClearableFileInput)
    file4 = forms.FileField(required=False, widget=forms.ClearableFileInput)
    email = forms.EmailField(required=False)
    website = forms.URLField()

class ContactForm(FilesForm):
    pass

class ContactBaseFormSet(BaseFormSet):
    def add_fields(self, form, index):
        super(ContactBaseFormSet, self).add_fields(form, index)

    def clean(self):
        super(ContactBaseFormSet, self).clean()
        raise forms.ValidationError("This error was added to show the non form errors styling")

ContactFormSet = formset_factory(FilesForm, formset=ContactBaseFormSet,
                                 extra=2,
                                 max_num=4)#,
                                 #validate_max=True)
                                 #validatemax=True)
'''

'''
class ArticleForm(forms.Form):
    title = forms.CharField()
    pub_date = forms.DateField()

    def clean(self):
        cleaned_data = super(ArticleForm, self).clean()
        raise forms.ValidationError("This error was added to show the non field errors styling.")
        return cleaned_data
'''

class ContactUserInfoForm(forms.Form):
    op_box = forms.ChoiceField(choices=OP_BOX,label='操作药箱')
    user_iphone = forms.CharField(label='手机号',min_length=5, max_length=12, required=True,
                                  error_messages={"required"   : u"请输入手机号",
                                                "min_length" : "电话号码长度为5-12个字符",
                                                "max_length" : "电话号码长度为5-12个字符"})
    box_id = forms.CharField(label='药箱ID',min_length=5,max_length=15, help_text ="可以扫描药箱下面的二维码",
                                  error_messages={"required"   : u"请输入药箱ID",
                                                "min_length" : "药箱ID长度为5-15个字符",
                                                "max_length" : "药箱ID长度为5-15个字符"})
    user_name = forms.CharField(label='用户姓名',max_length=100,required=False)
    op_man = forms.ChoiceField(choices=OPMAN_CHOICES,label='操作规则')
    DM_type = forms.ChoiceField(choices=DM_TYPE,label='糖尿病类型')
    medical_history = forms.CharField(label='病史 /年',max_length=10, required=False, help_text="年的整数倍，最多30年，最少1年")

    #user_id = forms.CharField(label='用户ID',max_length=100, error_messages={'required': '请输入用户ID'},
    #                        help_text="用户注册时的ID")

    #topic = forms.ChoiceField(choices=TOPIC_CHOICES,label='提醒规则')
    #email = forms.EmailField(required=False)
    #email = forms.EmailField(required=False, label='Your e‐mail address')
    #message = forms.CharField()
    #message = forms.CharField(widget=forms.Textarea)

    #return user_iphone

    def clean_message(self):
        '''
        message = self.cleaned_data['user_iphone']
        num_words = len(message.split())
        print "num_words:"
        print num_words
        if num_words < 4:
            raise forms.ValidationError("电话号码不对啊!")
        '''
        self.clean()
        return message


        #def clean(self):
        '''
        user_iphone = self.cleaned_data['user_iphone']
        print user_iphone
        num_words = len(user_iphone)    #len(user_iphone.split())
        print num_words
        if num_words < 11 or num_words > 15:
            raise forms.ValidationError("电话号码错误!")
        #return user_iphone
        '''

    #    super(ContactUserInfoForm, self).clean()
    #    raise forms.ValidationError("This error was added to show the non form errors styling.")

class ContactConfigForm(forms.Form):
    user_iphone = forms.CharField(label='手机号',min_length=5, max_length=12, required=True,
                                  error_messages={"required"   : u"请输入用户手机号或固定电话",
                                                "min_length" : "密码长度为5-12个字符",
                                                "max_length" : "密码长度为5-12个字符"})
    box_id = forms.CharField(label='药箱ID',min_length=5,max_length=15, required=True, help_text ="可以扫描药箱下面的二维码",
                                  error_messages={"required"   : u"请输入药箱ID",
                                                "min_length" : "密码长度为5-15个字符",
                                                "max_length" : "密码长度为5-15个字符"})
    #config = forms.ComboField(label='邮箱', fields=[forms.CharField(label='药箱ID', max_length=20), forms.EmailField()])
    #config = forms.ComboField(label='配置信息', widget=user_iphone)
    #foo_select = forms.ModelMultipleChoiceField(queryset=None)
    #test1 = forms.ComboField(label='Repository Admin',error_messages={'required':'Enter repository admin'})
    #period = forms.ComboField(label = '时段',widget=forms.CheckboxSelectMultiple(
    #        choices=PERIOD), required=False, initial=['morning'])
    #tank = forms.IntegerField(widget=forms.HiddenInput(), initial=123)
    #test2 = forms.FilePathField(label='test2', path='/Users/smartbox/百度云同步盘/chunyu/code/smartbox')
    #test3 = forms.MultipleChoiceField(choices=OPMAN_CHOICES)
    slot1_medicine_name = forms.CharField(label='第一个药仓--药名', max_length=64, required=False,
                                          error_messages={"max_length" : "密码长度为1-64个字符"})

    slot1_meals = forms.ChoiceField(choices=MEALS,label='第一个药仓--用餐时间', required=False)
    slot1_mealstime = forms.IntegerField(label='第一个药仓--饭前/饭后几分钟', required=False, help_text='单位 /分',
                                         min_value=0, max_value=30,
                                         error_messages={"min_value"    :u"数值最小是0",
                                                         "max_value"   :u"数值最大是30"})
    slot1_piece = forms.IntegerField(label='第一个药仓--片数', required=False, help_text='单位 /片')
    #slot1_period = forms.ChoiceField(choices=PERIOD,label='第一个药仓--用餐时段', required=False)
    #slot1_moning = forms.IntegerField(label='第一个药仓--早上服药时间',required=False,
    #                                   help_text="05:00-11:00,请输入1010表示10点10分", min_value=0, max_value=2359,
    #                                  error_messages={"min_value"    :u"数值最小是0000",
    #                                                  "max_value"   :u"数值最大是2359"})

    slot1_moning = forms.DateTimeField(label='第一个药仓--早上服药时间', required=False,
                                       help_text="00:00-10:59,请输入10:10表示10点10分", input_formats=['%H:%M'])

    slot1_noon = forms.DateTimeField(label='第一个药仓--中午服药时间', required=False,
                                     help_text="11:00-15:59", input_formats=['%H:%M'])
    slot1_evening = forms.DateTimeField(label='第一个药仓--晚上服药时间', required=False,
                                        help_text="16:00-19:59", input_formats=['%H:%M'])
    slot1_nigh = forms.DateTimeField(label='第一个药仓--夜里服药时间', required=False,
                                     help_text="20:00-23:59", input_formats=['%H:%M'])


    slot2_medicine_name = forms.CharField(label='第二个药仓--药名', max_length=64, required=False,
                                          error_messages={"max_length" : "密码长度为1-64个字符"})
    slot2_meals = forms.ChoiceField(choices=MEALS,label='第二个药仓--用餐时间', required=False)
    slot2_mealstime = forms.IntegerField(label='第二个药仓--饭前/饭后几分钟', required=False, help_text='单位 /分',
                                         min_value=0, max_value=30,
                                         error_messages={"min_value"    :u"数值最小是0",
                                                         "max_value"   :u"数值最大是30"})
    slot2_piece = forms.IntegerField(label='第二个药仓--片数', required=False, help_text='单位 /片')
    #slot2_period = forms.ChoiceField(choices=PERIOD,label='第二个药仓--用餐时段', required=False)
    slot2_moning = forms.DateTimeField(label='第二个药仓--早上服药时间', required=False,
                                       help_text="00:00-10:59,请输入10:10表示10点10分", input_formats=['%H:%M'])
    slot2_noon = forms.DateTimeField(label='第二个药仓--中午服药时间', required=False,
                                     help_text="11:00-15:59", input_formats=['%H:%M'])
    slot2_evening = forms.DateTimeField(label='第二个药仓--晚上服药时间', required=False,
                                        help_text="16:00-19:59", input_formats=['%H:%M'])
    slot2_nigh = forms.DateTimeField(label='第二个药仓--夜里服药时间', required=False,
                                     help_text="20:00-23:59", input_formats=['%H:%M'])

    slot3_medicine_name = forms.CharField(label='第三个药仓--药名', max_length=64, required=False,
                                          error_messages={"max_length" : "密码长度为1-64个字符"})
    slot3_meals = forms.ChoiceField(choices=MEALS,label='第三个药仓--用餐时间', required=False)
    slot3_mealstime = forms.IntegerField(label='第三个药仓--饭前/饭后几分钟', required=False, help_text='单位 /分',
                                         min_value=0, max_value=30,
                                         error_messages={"min_value"    :u"数值最小是0",
                                                         "max_value"   :u"数值最大是30"})
    slot3_piece = forms.IntegerField(label='第三个药仓--片数', required=False, help_text='单位 /片')
    #slot3_period = forms.ChoiceField(choices=PERIOD,label='第三个药仓--用餐时段', required=False)
    slot3_moning = forms.DateTimeField(label='第三个药仓--早上服药时间', required=False,
                                       help_text="00:00-10:59,请输入10:10表示10点10分", input_formats=['%H:%M'])
    slot3_noon = forms.DateTimeField(label='第三个药仓--中午服药时间', required=False,
                                     help_text="11:00-15:59", input_formats=['%H:%M'])
    slot3_evening = forms.DateTimeField(label='第三个药仓--晚上服药时间', required=False,
                                        help_text="16:00-19:59", input_formats=['%H:%M'])
    slot3_nigh = forms.DateTimeField(label='第三个药仓--夜里服药时间', required=False,
                                     help_text="20:00-23:59", input_formats=['%H:%M'])


    slot4_medicine_name = forms.CharField(label='第四个药仓--药名', max_length=64, required=False,
                                          error_messages={"max_length" : "密码长度为1-64个字符"})
    slot4_meals = forms.ChoiceField(choices=MEALS,label='第四个药仓--用餐时间', required=False)
    slot4_mealstime = forms.IntegerField(label='第四个药仓--饭前/饭后几分钟', required=False, help_text='单位 /分',
                                         min_value=0, max_value=30,
                                         error_messages={"min_value"    :u"数值最小是0",
                                                         "max_value"   :u"数值最大是30"})
    slot4_piece = forms.IntegerField(label='第四个药仓--片数', required=False, help_text='单位 /片')
    #slot4_period = forms.ChoiceField(choices=PERIOD,label='第四个药仓--用餐时段', required=False)
    slot4_moning = forms.DateTimeField(label='第四个药仓--早上服药时间', required=False,
                                       help_text="00:00-10:59,请输入10:10表示10点10分", input_formats=['%H:%M'])
    slot4_noon = forms.DateTimeField(label='第四个药仓--中午服药时间', required=False,
                                     help_text="11:00-15:59", input_formats=['%H:%M'])
    slot4_evening = forms.DateTimeField(label='第四个药仓--晚上服药时间', required=False,
                                        help_text="16:00-19:59", input_formats=['%H:%M'])
    slot4_nigh = forms.DateTimeField(label='第四个药仓--夜里服药时间', required=False,
                                     help_text="20:00-23:59", input_formats=['%H:%M'])



    def clean_message(self):
        self.clean()
        return message


class UploadFileForm(forms.Form):
    #title=forms.CharField(label="mcu文件名", max_length=50)
    version = forms.CharField(label="版本号", max_length=50, required=False)

    def clean_message(self):
        self.clean()
        return message


class AdUplaodFileForm(forms.Form):
    box_id = forms.CharField(label='药箱ID',min_length=6,max_length=10, required=True, help_text ="可以扫描药箱下面的二维码",
                                  error_messages={"required"   : u"请输入药箱ID",
                                                "min_length" : "密码长度为6-10个字符",
                                                "max_length" : "密码长度为6-10个字符"})
    text = forms.CharField(label='广告内容', max_length=4096, required=False,
                                  error_messages={"max_length" : "内容长度为1-2048个字符"})

    def clean_message(self):
        self.clean()
        return message
