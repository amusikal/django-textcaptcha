import logging
import urllib2
from hashlib import sha256, md5
from lxml import objectify
from django.conf import settings

CAPTCHA_TEST_KEY = '2sbwf7wsbomcc8ccw008gc0gk'
CAPTCHA_API_KEY = getattr(settings, 'CAPTCHA_API_KEY', CAPTCHA_TEST_KEY)
CAPTCHA_API_URL = 'http://textcaptcha.com/api/%s/'

def retrieve_textcaptcha(api_key=CAPTCHA_API_KEY):
    url = CAPTCHA_API_URL % api_key
    response = urllib2.urlopen(url)
    
    xmlstring = response.read()
    logging.debug("Got XML response '%s'" % xmlstring)

    captcha = objectify.fromstring(xmlstring)
    question = captcha.question.text.strip()
    answers = [each.text.strip() for each in captcha.findall('answer')]
    return question, answers
