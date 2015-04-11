# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms import TextAreaField
from wtforms.validators import DataRequired


class MediaCommentForm(Form):
    content = TextAreaField(
        u'评论',
        validators=[DataRequired(message=u'这个字段是必填的')])
