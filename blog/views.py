from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.utils.text import slugify
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView

from blog.forms import PostForm
from blog.models import Post
from mailing.services import clear_cache


class BlogCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'mailing/create.html'
    permission_required = 'post.add_post'
    success_url = reverse_lazy('blog:view')
    extra_context = {'title': 'Блог: Создание новой статьи'}

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            self.object.slug = slugify(self.object.name)
            self.object.user = self.request.user
            return super().form_valid(form)
        return super().form_invalid(form)


class BlogDetailView(DetailView):
    model = Post
    template_name = 'blog/blog_details.html'
    success_url = reverse_lazy('blog:view')
    slug_url_kwarg = 'slug'
    slug_field = 'slug'
    extra_context = {'timeout': settings.CACHE_TIMEOUT}

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = f'Блог: {self.object}'
        return context_data

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.view_count += 1
        self.object.save()
        return self.object


class BlogDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/blog_confirm_delete.html'
    permission_required = 'post.delete_post'
    success_url = reverse_lazy("blog:view")

    def form_valid(self, form):
        clear_cache('post', {self.object.id})
        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    permission_required = 'post.update_post'
    template_name = 'mailing/create.html'

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            self.object.slug = slugify(self.object.name)
            return super().form_valid(form)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = f'Редактирование: {self.object}'
        return context_data

    def get_success_url(self):
        return reverse_lazy('blog:detail', args=[self.kwargs.get('pk')])


class BlogListView(ListView):
    model = Post
    fields = ('name', 'desc', 'image')
    template_name = 'blog/blog_list.html'
    extra_context = {
        'title': 'Блог',
        'timeout': settings.CACHE_TIMEOUT
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_published=True)


def published_activity(request, pk):
    post_item = get_object_or_404(Post, pk=pk)
    if post_item.is_published:
        post_item.is_published = False
    else:
        post_item.is_published = True
    post_item.save()
    return redirect(reverse_lazy('blog:detail', args=[post_item.pk]))
