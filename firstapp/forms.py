from django import forms
from django.core.exceptions import ValidationError

from firstapp.models import UserProfile


def word_validator(comment):
    if len(comment) < 4:
        raise ValidationError("not enough words")


def comment_validator(comment):
    keywords = [u"发票", u"钱"]
    for keyword in keywords:
        if keyword in comment:
            raise ValidationError("Your comment contains invalid words,please check it again.")


class CommentForm(forms.Form):
    name = forms.CharField(max_length=50)
    comment = forms.CharField(
        widget=forms.Textarea(),
        error_messages={
            "required": 'wow, such words'
        },
        validators=[word_validator, comment_validator]
    )


class MyinfoForm(forms.Form):
    full_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': '你的真实姓名'}),
        max_length=100, label='姓名', required=False)
    gender = forms.ChoiceField((('0', '男'), ('1', '女')))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': '********'}),
        max_length=100, label='密码', required=False)
    avatar = forms.ImageField(label='修改头像', required=False)