from datetime import date, datetime, timezone

from django.contrib.sitemaps import Sitemap as DjangoSitemap
from django.test import Client, RequestFactory
from lxml import etree

from django_sitemaps import Sitemap


NS = {
    "s": "http://www.sitemaps.org/schemas/sitemap/0.9",
    "xhtml": "http://www.w3.org/1999/xhtml",
}


def make_sitemap():
    request = RequestFactory().get("/sitemap.xml")
    return Sitemap(build_absolute_uri=request.build_absolute_uri)


def parse(sitemap):
    return etree.fromstring(sitemap.serialize())


def test_add():
    sitemap = make_sitemap()
    sitemap.add(
        "/en/",
        changefreq="weekly",
        lastmod=date(2026, 10, 24),
        priority=0.5,
        alternates={"en": "/en/", "de": "https://example.com/de/"},
    )
    sitemap.add("/minimal/", priority="")

    root = parse(sitemap)
    first, second = root.findall("s:url", NS)
    assert first.findtext("s:loc", namespaces=NS) == "http://testserver/en/"
    assert first.findtext("s:changefreq", namespaces=NS) == "weekly"
    assert first.findtext("s:lastmod", namespaces=NS) == "2026-10-24"
    assert first.findtext("s:priority", namespaces=NS) == "0.5"
    assert [
        (link.get("hreflang"), link.get("href"))
        for link in first.findall("xhtml:link", NS)
    ] == [("en", "http://testserver/en/"), ("de", "https://example.com/de/")]

    assert second.findtext("s:loc", namespaces=NS) == "http://testserver/minimal/"
    assert [child.tag for child in second] == [f"{{{NS['s']}}}loc"]


def test_response():
    sitemap = make_sitemap()
    sitemap.add("/a/", lastmod=datetime(2026, 10, 1, 12, tzinfo=timezone.utc))
    sitemap.add("/b/", lastmod=date(2026, 9, 1))

    response = sitemap.response()
    assert response["Content-Type"] == "application/xml"
    assert response["X-Robot-Tag"] == "noindex, noodp, noarchive"
    assert response["Last-Modified"] == "Thu, 01 Oct 2026 12:00:00 GMT"
    assert response.content.startswith(b"<?xml version='1.0' encoding='UTF-8'?>")

    sitemap.add("/c/")
    assert "Last-Modified" not in sitemap.response()


class PagesSitemap(DjangoSitemap):
    changefreq = "daily"

    def items(self):
        return ["/one/", "/two/"]

    def location(self, item):
        return item


def test_add_django_sitemap():
    sitemap = make_sitemap()
    sitemap.add_django_sitemap(PagesSitemap)
    sitemap.add_django_sitemap(PagesSitemap())

    root = parse(sitemap)
    assert [url.findtext("s:loc", namespaces=NS) for url in root] == [
        "http://testserver/one/",
        "http://testserver/two/",
    ] * 2
    assert {url.findtext("s:changefreq", namespaces=NS) for url in root} == {"daily"}
    assert root.find("s:url/s:priority", NS) is None


def test_robots_txt():
    response = Client().get("/robots.txt")
    assert response["Content-Type"] == "text/plain"
    assert response.content.decode() == (
        "User-agent: *\nSitemap: http://testserver/sitemap.xml\n"
    )
