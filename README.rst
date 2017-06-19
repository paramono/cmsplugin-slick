.. image:: https://travis-ci.org/Atterratio/cmsplugin-slick.svg?branch=master
    :target: https://travis-ci.org/Atterratio/cmsplugin-slick
.. image:: https://codecov.io/gh/Atterratio/cmsplugin-slick/coverage.svg?branch=master
    :target: https://codecov.io/gh/Atterratio/cmsplugin-slick

===============
cmsplugin-slick
===============

Slick_ carousel plugin fo Django-CMS
.. _Slick: http://kenwheeler.github.io/slick/

.. image:: https://img.shields.io/badge/Donate-PayPal-blue.svg
   :target: https://www.paypal.me/Atterratio
.. image:: https://img.shields.io/badge/Donate-YaMoney-orange.svg
   :target: https://money.yandex.ru/to/410011005689134

INSTALLATION
============

* run :code:`pip install cmsplugin-slick` or :code:`pip install git+https://github.com/Atterratio/cmsplugin-slick.git`;
* add :code:`cmsplugin_slick` to your :code:`INSTALLED_APPS`;
* run :code:`manage.py migrate`;

Components and Usage
====================
Module :code:`Slick Carousel` contains the following plugins :code:`Carousel Plugin`, :code:`Plugins Wrapper`, :code:`Image Folder Carousel`

Carousel Plugin
---------------
Allow add Django-CMS plugin like one slide, ore multislide if plugin return not wrapped list of ellements, see my plugin :code:`Image Folder Carousel`

Plugins Wrapper
---------------
Allow wrapp several Django-CMS plugins like one slide. For example you can add :code:`image` and :code:`text` plugis, and text will be like caption for image.

Image Folder Carousel
---------------------
Returns images from :code:`filer` folder as carousel slides

Notes
=====
By default plugin used oficial slick CDN :code:`//cdn.jsdelivr.net/jquery.slick/1.6.0`,
if you want update version, you can put in :code:`static/cmsplugin_slick/slick`
folder of you project, prefered slick project files, or add :code:`SLICK_CDN` setting
in you progect :code:`settigs.py` file.
Local files have a higher priority its can be useful, if you thant change slick theme.