from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    FormView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse
from blog.models import Post
from blog.forms import ContactForm, PostForm


class IndexView(TemplateView):
    """
    View to render the homepage of the blog, displaying the latest posts.
    """

    template_name = "blog/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = Post.objects.filter(status=True)[:10]
        return context


class PostListView(LoginRequiredMixin, ListView):
    """
    View to list all posts. Requires the user to be logged in.
    """

    model = Post
    paginate_by = 2
    context_object_name = "posts"


class PostDetailView(LoginRequiredMixin, DetailView):
    """
    View to display a single post in detail. Requires the user to be logged in.
    """

    model = Post
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ContactFormView(LoginRequiredMixin, FormView):
    """
    View to render and process a contact form. Requires the user to be logged in.
    """

    template_name = "blog/contact.html"
    form_class = ContactForm
    success_url = "/blog/contact/"

    def form_valid(self, form):
        messages.success(self.request, "Your message has been sent successfully.")
        return super().form_valid(form)


class PostCreateView(LoginRequiredMixin, CreateView):
    """
    View to create a new post. Requires the user to be logged in.
    """

    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("blog:post-detail", kwargs={"pk": self.object.pk})


class PostEditView(LoginRequiredMixin, UpdateView):
    """
    View to edit an existing post. Requires the user to be logged in.
    """

    model = Post
    form_class = PostForm
    success_url = "/blog/post/"

    def get_success_url(self):
        return reverse("blog:post-detail", kwargs={"pk": self.object.pk})


class PostDeleteView(LoginRequiredMixin, DeleteView):
    """
    View to delete a post. Requires the user to be logged in.
    """

    model = Post
    success_url = "/blog/post/"


class PostListApiView(TemplateView):
    """
    View to render a template that displays a list of published blog posts using an API
    """

    template_name = "blog/post_list_api.html"
