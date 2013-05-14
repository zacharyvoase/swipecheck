from django.conf import settings
from django.core.exceptions import SuspiciousOperation
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.util import RequestValidator
from urlobject import URLObject

from . import models


def validate_twilio_request(request):
    validator = RequestValidator(settings.TWILIO_AUTH_TOKEN)
    if 'HTTP_X_TWILIO_SIGNATURE' not in request.META:
        return False, "No X-Twilio-Signature header present"
    signature = request.META['HTTP_X_TWILIO_SIGNATURE']

    if 'CallSid' in request.POST:
        url = (URLObject(request.build_absolute_uri()).without_auth()
               .with_path(reverse('twilio-voice')))
        if url.scheme == 'https':
            url = url.without_port()
    elif 'SmsSid' in request.POST:
        url = (URLObject(request.build_absolute_uri())
               .with_path(reverse('twilio-sms')))
    else:
        return False, "Neither CallSid nor SmsSid found in request"

    valid = validator.validate(url, request.POST, signature)
    if not valid:
        return False, "Invalid signature"
    return True, None


@csrf_exempt
def sms_received(request):
    valid, reason = validate_twilio_request(request)
    if not valid:
        raise SuspiciousOperation("Invalid Twilio request: {0}".format(reason))
    models.Checkin.create(rfid=request.POST['Body'], from_number=request.POST['From'])
    return HttpResponse(status=204)
