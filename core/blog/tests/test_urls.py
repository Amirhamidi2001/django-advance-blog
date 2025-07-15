from django.test import SimpleTestCase
from django.urls import reverse, resolve
from blog import views


class BlogURLTests(SimpleTestCase):
    def test_blog_root_url_resolves_to_templateview(self):
        view = resolve("/blog/")
        self.assertEqual(view.func.view_class.__name__, "TemplateView")

    def test_index_url_resolves(self):
        url = reverse("blog:index")
        view = resolve(url)
        self.assertEqual(view.func.view_class, views.IndexView)

    def test_contact_url_resolves(self):
        url = reverse("blog:contact")
        view = resolve(url)
        self.assertEqual(view.func.view_class, views.ContactFormView)

    def test_post_list_url_resolves(self):
        url = reverse("blog:post-list")
        view = resolve(url)
        self.assertEqual(view.func.view_class, views.PostListView)

    def test_post_detail_url_resolves(self):
        url = reverse("blog:post-detail", kwargs={"pk": 1})
        view = resolve(url)
        self.assertEqual(view.func.view_class, views.PostDetailView)

    def test_post_create_url_resolves(self):
        url = reverse("blog:post-create")
        view = resolve(url)
        self.assertEqual(view.func.view_class, views.PostCreateView)

    def test_post_edit_url_resolves(self):
        url = reverse("blog:post-edit", kwargs={"pk": 1})
        view = resolve(url)
        self.assertEqual(view.func.view_class, views.PostEditView)

    def test_post_delete_url_resolves(self):
        url = reverse("blog:post-delete", kwargs={"pk": 1})
        view = resolve(url)
        self.assertEqual(view.func.view_class, views.PostDeleteView)

    def test_api_v1_url_is_included(self):
        view = resolve("/blog/api/v1/")
        self.assertTrue(view)
