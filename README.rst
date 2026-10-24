===============
django-sitemaps
===============

``sitemap.xml`` generation using lxml_ with support for alternates_. It
uses Python 3's keyword-only arguments for self-documenting code.


Why not ``django.contrib.sitemaps``?
====================================

Django's sitemaps framework didn't support alternates when this package
was written. Django 3.2 added ``i18n``, ``languages`` and ``alternates``,
but alternate URLs are still derived by activating each language and
reversing the same object's URL. django-sitemaps instead lets you pass
arbitrary alternate URLs for each entry, e.g. when languages live on
different domains. URLs are added one-by-one from a regular view, without
having to write ``Sitemap`` classes. Existing Django sitemaps can still be
included using ``add_django_sitemap``.


Installation
============

Simply ``pip install django-sitemaps``. The package consists of a single
python module, ``django_sitemaps``, containing the single class; there's no
additional configuration necessary.


Usage
=====

View::

    from app.pages.sitemaps import PagesSitemap

    def sitemap(request):
        sitemap = Sitemap(
            # All URLs are passed through build_absolute_uri.
            build_absolute_uri=request.build_absolute_uri,
        )

        # URLs can be added one-by-one. The only required argument
        # is the URL. All other arguments are keyword-only arguments.
        for p in Page.objects.active():
            url = p.get_absolute_url()
            sitemap.add(
                url,
                changefreq='weekly',
                priority=0.5,
                lastmod=p.modification_date,
                alternates={
                    code: urljoin(domain, url)
                    for code, domain in PAGE_DOMAINS[p.language].items()
                },
            )

        # Adding conventional Django sitemaps is supported. Pass either
        # the class or an instance. Their URLs are also passed through
        # build_absolute_uri, so django.contrib.sites isn't required.
        sitemap.add_django_sitemap(PagesSitemap)

        # You could get the serialized XML...
        # ... = sitemap.serialize([pretty_print=False])
        # ... or use the ``response`` helper to return a
        # ready-made ``HttpResponse``:
        return sitemap.response(
            # pretty_print is False by default
            pretty_print=settings.DEBUG,
        )

Some browsers display the sitemap as plain text because the
``xhtml:link`` alternates use a different namespace and no stylesheet
is attached. The response is still valid XML served as
``application/xml``; search engines don't mind.

URLconf::

    from django.urls import path
    from django_sitemaps import robots_txt
    from app.views import sitemap

    urlpatterns = [
        path('sitemap.xml', sitemap),
        path('robots.txt', robots_txt(timeout=86400)),
        ...
    ]

The ``robots_txt`` function returns a view which can be used to generate
a ``robots.txt`` file containing sitemap URLs. The default sitemap only
contains::

    User-agent: *
    Sitemap: <protocol>://<host>/sitemap.xml

The list of sitemap URLs may be overridden by setting ``sitemaps``::

    from django.urls import reverse_lazy

    urlpatterns = [
        path('robots.txt', robots_txt(
            timeout=86400,
            sitemaps=[
                '/sitemap.xml',
                reverse_lazy('articles-sitemap'),
                ...,
            ],
        )),
    ]


.. _alternates: https://support.google.com/webmasters/answer/2620865?hl=en
.. _lxml: http://lxml.de/
