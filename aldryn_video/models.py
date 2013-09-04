# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms.models.pluginmodel import CMSPlugin

from aldryn_video.utils import get_embed_code


class OEmbedVideoPlugin(CMSPlugin):

    url = models.URLField(_('URL'), max_length=100)
    width = models.IntegerField(_('Width'), null=True, blank=True)
    height = models.IntegerField(_('Height'), null=True, blank=True)
    auto_play = models.BooleanField(_('auto play'), default=False)
    loop_video = models.BooleanField(_('loop'), help_text=_('when true, the video repeats itself when over.'), default=False)

    # cached oembed data
    html = models.TextField(blank=True)

    def __unicode__(self):
        return self.url

    def clean(self):
        extra = {}
        if self.width:
            extra['maxwidth'] = self.width
        if self.height:
            extra['maxheight'] = self.height
        if self.auto_play:
            extra['autoplay'] = 1
        if self.loop_video:
            extra['loop'] = 1
        try:
            self.html = get_embed_code(url=self.url, **extra)
        except Exception as e:
            raise ValidationError(e.message)
