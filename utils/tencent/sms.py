# import ssl

from qcloudsms_py import SmsMultiSender, SmsSingleSender
from qcloudsms_py.httpclient import HTTPError
from django.conf import settings


appid = settings.TENCENT_SMS_APP_ID
appkey = settings.TENCENT_SMS_APP_KEY
sms_sign = settings.TENCENT_SMS_SIGN


def send_sms_single(phone_num, template_id, template_param_list):
    sender = SmsSingleSender(appid, appkey)
    try:
        response = sender.send_with_param(86, phone_num, template_id, template_param_list, sign=sms_sign)
    except HTTPError as e:
        response = {'result': 1000, 'errmsg': '网络异常，发送失败'}
    return response


def send_sms_multi(phone_num_list, template_id, param_list):
    sender = SmsMultiSender(appid, appkey)
    try:
        response = sender.send_with_param(86, phone_num_list, template_id, param_list, sign=sms_sign)
    except HTTPError as e:
        response = {'result': 1000, 'errmsg': "网络异常发送失败"}
    return response

