import re

from django import forms
from django.conf import settings
from django.core.exceptions import SuspiciousOperation
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from twilio.util import RequestValidator
from urlobject import URLObject

from . import models


RFID_RE = re.compile(r'^[A-F0-9]+$', re.I)


class RFIDForm(forms.Form):
    rfid = forms.CharField(max_length=40, label="RFID")

    def clean_rfid(self):
        rfid = self.cleaned_data['rfid']
        if not RFID_RE.match(rfid):
            raise forms.ValidationError(
                "RFID may only contain hex chars (0-9, A-F)")
        return rfid.upper()


def list_rfids(request):
    if not request.foursquare.is_authenticated:
        return redirect('/login/')
    if request.method == 'POST':
        add_rfid_form = RFIDForm(request.POST)
        if add_rfid_form.is_valid():
            request.foursquare.user.rfids.get_or_create(
                rfid=add_rfid_form.cleaned_data['rfid'].upper())
            return redirect('/')
    else:
        add_rfid_form = RFIDForm()
    return render(request, 'rfids_list.html', {
        'user': request.foursquare.user,
        'add_rfid_form': add_rfid_form})


def delete_rfid(request):
    if not request.foursquare.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = RFIDForm(request.POST)
        if form.is_valid():
            rfid = form.cleaned_data['rfid']
            request.foursquare.user.rfids.filter(rfid=rfid).delete()
    return redirect('/')


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
