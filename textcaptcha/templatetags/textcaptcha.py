from django import template
from djtk.textcaptcha.models import Question

register = template.Library()

class GetTextCaptchaNode(template.Node):
    
    def __init__(self, varname):
        self.varname = varname

    def render(self, context):
        context[self.varname] = Question.objects.new_captcha()
        return ''

@register.tag(name='get_captcha')
def do_get_textcaptcha_question(parser, token):
    try:
        tag_name, varname = token.split_contents()
    except ValueError:
        varname = 'captcha'
    return GetTextCaptchaNode(varname)
