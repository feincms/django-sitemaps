Change log
==========

Next version
~~~~~~~~~~~~

2.1 (2026-10-24)
~~~~~~~~~~~~~~~~

- Updated the README: ``path()`` in URLconf examples, the current
  ``add_django_sitemap`` signature and a comparison with
  ``django.contrib.sitemaps``.
- Added tests and a GitHub Actions workflow running them.
- Added a workflow publishing releases to PyPI using trusted publishing.
- Added the missing package description.


`2.0.2`_ (2025-11-06)
~~~~~~~~~~~~~~~~~~~~~

.. _2.0.2: https://github.com/matthiask/django-sitemaps/compare/2.0.1...2.0.2

- Converted the package to hatchling and ruff.


`2.0.1`_ (2022-01-25)
~~~~~~~~~~~~~~~~~~~~~

.. _2.0.1: https://github.com/matthiask/django-sitemaps/compare/1.1...2.0.1

- Fixed cases where empty priority tags were added if priority was an
  empty string (which is always the default case with Django sitemaps).
- Added pre-commit, switched to a declarative setup, etc.
- Made ``add_django_sitemap`` always build URLs using ``build_absolute_uri``
  too to avoid problems when using ``django.contrib.sites``.


`1.1`_ (2018-04-11)
~~~~~~~~~~~~~~~~~~~

.. _1.1: https://github.com/matthiask/django-sitemaps/compare/1.0...1.1

- Added the ``lxml`` dependency to ``install_requires``.
- Added documentation.
- Added the ``robots_txt`` view for easily adding a ``/robots.txt``
  view returning sitemap URLs.


`1.0`_ (2017-03-29)
~~~~~~~~~~~~~~~~~~~

.. _1.0: https://github.com/matthiask/django-sitemaps/commit/df0841349

- Initial release!
