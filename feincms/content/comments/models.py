# ------------------------------------------------------------------------
# coding=utf-8
# ------------------------------------------------------------------------
#
#  Created by Martin J. Laubach on 08.01.10.
#
# ------------------------------------------------------------------------

from django import forms
from django.contrib import comments
from django.contrib.comments.models import Comment
from django.db import models
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

# from feincms.admin.editor import ItemEditorForm

# ------------------------------------------------------------------------
class CommentsContent(models.Model):
    comments_enabled = models.BooleanField(_('enabled'), default=True, help_text=_('New comments may be added'))

    class Meta:
        abstract = True
        verbose_name = _('comments')
        verbose_name_plural = _('comments')

 #   @classmethod
 #   def initialize_type(cls):
 #       class CommentContentAdminForm(ItemEditorForm):
 #           def __init__(self, *args, **kwargs):
 #               parent = kwargs.get('instance', None)
 #               if parent is not None:
 #                   for c in Comment.objects.order_by('submit_date'):
 #                       self.base_fields['comment_%d' % c.id] = forms.BooleanField('comment')
 #               super(CommentContentAdminForm, self).__init__(*args, **kwargs)


 #       cls.feincms_item_editor_form = CommentContentAdminForm

    def render(self, **kwargs):
        parent_type = self.parent.__class__.__name__.lower()
        request = kwargs.get('request')

        # TODO: Check for translation extension before use!
        comment_page = self.parent.original_translation

        f = None
        if self.comments_enabled and request.POST:
            extra = request._feincms_appcontent_parameters.get('page_extra_path', ())
            if len(extra) > 0 and extra[0] == u"post-comment":
                from django.contrib.comments.views.comments import post_comment
                r = post_comment(request)
                if not isinstance(r, HttpResponseRedirect):
                    f = comments.get_form()(comment_page, data=request.POST)

        if f is None:
            f = comments.get_form()(comment_page)

        return render_to_string([
            'content/comments/%s.html' % parent_type,
            'content/comments/default-site.html',
            'content/comments/default.html',
            ], RequestContext(request, { 'content': self, 'feincms_page' : self.parent, 'parent': comment_page, 'form' : f }))

# ------------------------------------------------------------------------



# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
