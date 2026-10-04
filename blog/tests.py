"""Dərs 8 - Django test client ilə səhifə və template yoxlamaları."""

from datetime import datetime
from pathlib import Path
import re

from django.test import SimpleTestCase
from django.urls import reverse

from .data import CATEGORIES, POSTS


class Lesson8PageTests(SimpleTestCase):
    def test_all_page_routes_have_shared_layout(self):
        pages = [
            "/", "/posts/", "/posts/1/", "/categories/",
            "/categories/oyunlar/", "/about/", "/contact/",
            "/author/murad/", "/author/xyz/", "/latest/", "/stats/",
        ]
        for url in pages:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, "/static/css/style.css")
                self.assertContains(response, 'aria-label="Əsas menyu"')
                self.assertContains(response, "STEP IT Academy · Python Web Development")

    def test_author_two_cards_and_unknown_author_empty(self):
        response = self.client.get(reverse("blog:author_posts", args=["murad"]))
        self.assertContains(response, '<article class="post-card">', count=2)
        self.assertContains(response, "Minecraft-da redstone")
        self.assertContains(response, "FIFA-da ən yaxşı taktika")

        unknown = self.client.get(reverse("blog:author_posts", args=["xyz"]))
        self.assertEqual(unknown.status_code, 200)
        self.assertContains(unknown, "Bu müəllifin hələ postu yoxdur.")
        self.assertNotContains(unknown, '<article class="post-card">')

    def test_latest_three_are_numbered_and_dated(self):
        response = self.client.get(reverse("blog:latest"))
        self.assertEqual(response.context["posts"], POSTS[-3:])
        for index, post in enumerate(POSTS[-3:], start=1):
            self.assertContains(response, f'<span class="list-index">{index}.</span>')
            self.assertContains(response, post["title"])
            self.assertContains(response, post["created_at"].strftime("%d.%m.%Y"))
        self.assertNotContains(response, "Python-da ilk addım")

    def test_stats_uses_lists_and_template_counts(self):
        response = self.client.get(reverse("blog:stats"))
        self.assertEqual(response.context["posts"], POSTS)
        self.assertEqual(response.context["categories"], CATEGORIES)
        self.assertContains(response, '<strong>5</strong>')
        self.assertContains(response, '<strong>3</strong>')

    def test_author_links_in_card_and_detail(self):
        self.assertContains(self.client.get("/"), 'href="/author/nigar/"')
        self.assertContains(self.client.get("/posts/1/"),
                            'href="/author/nigar/"')

    def test_active_menu_link(self):
        for url, label in [
            ("/", "Postlar"),
            ("/posts/1/", "Postlar"),
            ("/author/nigar/", "Postlar"),
            ("/latest/", "Son postlar"),
            ("/categories/", "Kateqoriyalar"),
            ("/categories/oyunlar/", "Kateqoriyalar"),
            ("/stats/", "Statistika"),
            ("/about/", "Haqqımızda"),
            ("/contact/", "Əlaqə"),
        ]:
            with self.subTest(url=url):
                content = self.client.get(url).content.decode()
                self.assertIn('class="active" aria-current="page">'
                              + label + '</a>', content)

    def test_contact_and_bonuses(self):
        contact = self.client.get("/contact/")
        self.assertContains(contact, '<ul class="list">')
        self.assertContains(contact, "info@example.com")
        self.assertContains(contact, "+994 50 123 45 67")
        self.assertContains(contact, f'© {datetime.now().year} STEP Blog')
        self.assertContains(self.client.get("/posts/1/"), "söz")

    def test_old_practice_pages_removed_and_missing_post_is_404(self):
        for url in ("/salam/", "/kvadrat/", "/posts/99/", "/categories/xyz/"):
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 404)

    def test_templates_use_named_urls_not_hardcoded_slash_links(self):
        root = Path(__file__).resolve().parent.parent / "templates"
        for template in root.rglob("*.html"):
            with self.subTest(template=template.name):
                text = template.read_text(encoding="utf-8")
                self.assertFalse(re.search(r'href\s*=\s*["\']/', text))

    def test_views_do_not_use_httpresponse(self):
        views = (Path(__file__).resolve().parent / "views.py").read_text(encoding="utf-8")
        self.assertNotIn("Http" + "Response", views)
