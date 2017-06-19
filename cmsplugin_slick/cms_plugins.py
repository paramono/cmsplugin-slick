import json
import os
from django.contrib import admin
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.templatetags import static
from django.contrib.staticfiles import finders


from filer.models.imagemodels import Image

from .models import SlickCarousel, SlickCarouselBreakpoint, SlickCarouselElementWrapper, SlickCaroselImageFolder


class SlickCarouselBreakpointInline(admin.StackedInline):
    model = SlickCarouselBreakpoint
    extra = 0


class SlickCarouselPlugin(CMSPluginBase):
    """
    Main carousel plugin that parent for others plugin.
    Supossed one plugin - one slide, or support plugins that get list of ellements, see my filler folder galery
    """
    model = SlickCarousel
    render_template = "cmsplugin_slick/carousel.djhtml"
    module = _('Slick Carousel')
    name = _('Carousel Plugin')
    allow_children = True
    inlines = [SlickCarouselBreakpointInline,]

    fieldsets = (
        (None, {'fields': (
                'title',
                'default_style',
                'infinite',
                'speed',
                ('dots', 'arrows'),
                ('slides_to_show', 'slides_to_scroll'),
        )}),

        ('Autoplay', {
            'classes': ('collapse',),
            'fields': (
                ('autoplay', 'autoplay_speed'),
                ('pause_on_hover', 'pause_on_dots_hover'),
        )}),

        ('Others Settings', {
            'classes': ('collapse',),
            'fields':(
                'fade',
                ('center_mode', 'center_padding'),
                'variable_width',
                ('vertical', 'rigth_to_left'),
        )}),

        ('Advanced', {
            'classes': ('collapse',),
            'fields': (
                'classes',
            ),
        }),
    )

    def render(self, context, instance, placeholder):
        context = super(SlickCarouselPlugin, self).render(context, instance, placeholder)
        slick_dict = {'infinite': instance.infinite, 'speed': instance.speed,
                      'dots': instance.dots, 'arrows': instance.arrows,
                      'slidesToShow': instance.slides_to_show, 'slidesToScroll': instance.slides_to_scroll,
                      'autoplay': instance.autoplay, 'autoplaySpeed': instance.autoplay_speed,
                      'pauseOnHover': instance.pause_on_hover, 'pauseOnDotsHover': instance.pause_on_dots_hover,
                      'fade': instance.fade,
                      'centerMode': instance.center_mode, 'centerPadding': instance.center_padding,
                      'variableWidth': instance.variable_width,'vertical': instance.vertical,
                      'rtl': instance.rigth_to_left}

        if instance.breakpoints.all():
            responsive = []
            for breakpoint in instance.breakpoints.all():
                responsive.append({'breakpoint': breakpoint.breakpoint,
                                   'settings': {'slidesToShow': breakpoint.slides_to_show,
                                                'slidesToScroll': breakpoint.slides_to_scroll}
                                   })

            slick_dict.update({'responsive': responsive})

        slick_settings = json.dumps(slick_dict)

        try:
            os.path.isfile(finders.find('cmsplugin_slick/slick/slick.min.js'))
            
            slick_js = static('cmsplugin_slick/slick/slick.min.js')
        except:
            try:
                slick_js = '{}/slick.js'.format(settings.SLICK_CDN)
            except:
                slick_js = '//cdn.jsdelivr.net/jquery.slick/1.6.0/slick.min.js'

        try:
            os.path.isfile(finders.find('cmsplugin_slick/slick/slick.css'))
            
            slick_css = static('cmsplugin_slick/slick/slick.css')
        except:
            try:
                slick_css = '{}/slick.css'.format(settings.SLICK_CDN)
            except:
                slick_css = '//cdn.jsdelivr.net/jquery.slick/1.6.0/slick.css'

        try:
            os.path.isfile(finders.find('cmsplugin_slick/slick/slick-theme.css'))
            
            slick_theme = static('cmsplugin_slick/slick/slick-theme.css')
        except:
            try:
                slick_theme = '{}/slick-theme.css'.format(settings.SLICK_CDN)
            except:
                slick_theme = '//cdn.jsdelivr.net/jquery.slick/1.6.0/slick-theme.css'

        context.update({'slick_settings': slick_settings,
                        'slick_js': slick_js, 'slick_css': slick_css, 'slick_theme': slick_theme})

        return context


class SlickCarouselElementWrapperPlugin(CMSPluginBase):
    """
    Include all child plugin as one slide
    """
    model = SlickCarouselElementWrapper
    render_template = "cmsplugin_slick/element_wrapper.djhtml"
    module = _('Slick Carousel')
    name = _('Plugins Wrapper')
    #require_parent = True
    parent_classes = ['SlickCarouselPlugin', ]
    allow_children = True


class SlickCarouselImageFolderPlugin(CMSPluginBase):
    model = SlickCaroselImageFolder
    render_template = "cmsplugin_slick/folder_carousel.djhtml"
    module = _('Slick Carousel')
    name = _('Image Folder Carousel')
    #require_parent = True
    parent_classes = ['SlickCarouselPlugin', ]

    def get_folder_images(self, folder, user):
        qs_files = folder.files.instance_of(Image)
        if user.is_staff:
            return qs_files
        else:
            return qs_files.filter(is_public=True)

    def render(self, context, instance, placeholder):
        context = super(SlickCarouselImageFolderPlugin, self).render(context, instance, placeholder)
        user = context['request'].user

        if instance.folder_id:
            folder_images = self.get_folder_images(instance.folder, user)
        else:
            folder_images = Image.objects.none()

        context.update({'folder_images': sorted(folder_images)})

        return context


plugin_pool.register_plugin(SlickCarouselPlugin)
plugin_pool.register_plugin(SlickCarouselElementWrapperPlugin)
plugin_pool.register_plugin(SlickCarouselImageFolderPlugin)