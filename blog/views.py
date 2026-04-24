from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from .models import MyBlog
from .forms import MyBlogForm


class BlogListView(ListView):
    """Список всех записей (только опубликованные для пользователей, все для админа)"""
    model = MyBlog
    template_name = "blog/blog_list.html"
    context_object_name = "posts"
    paginate_by = 10  # Пагинация по 10 записей на странице

    def get_queryset(self):
        # Для пользователей показываем только опубликованные
        # Для админа - все
        if self.request.user.is_staff:
            return MyBlog.objects.all().order_by('-created_at')
        return MyBlog.objects.filter(is_published=True).order_by('-created_at')


class BlogDetailView(DetailView):
    """Просмотр одной записи с увеличением счетчика просмотров"""
    model = MyBlog
    template_name = "blog/blog_detail.html"
    context_object_name = "post"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        # Увеличиваем счетчик просмотров только для опубликованных записей
        if obj.is_published or self.request.user.is_staff:
            obj.views_count += 1
            obj.save()
        return obj


class BlogCreateView(CreateView):
    """Создание новой записи"""
    model = MyBlog
    form_class = MyBlogForm
    template_name = "blog/blog_form.html"
    success_url = reverse_lazy('blog:blog_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Запись "{form.instance.name}" успешно создана!')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме.')
        return super().form_invalid(form)


class BlogUpdateView(UpdateView):
    """Редактирование записи"""
    model = MyBlog
    form_class = MyBlogForm
    template_name = "blog/blog_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Запись "{form.instance.name}" успешно обновлена!')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме.')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('blog:blog_detail', kwargs={'pk': self.object.pk})


class BlogDeleteView(DeleteView):
    """Удаление записи"""
    model = MyBlog
    template_name = "blog/blog_confirm_delete.html"
    success_url = reverse_lazy('blog:blog_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, f'Запись "{self.get_object().name}" успешно удалена!')
        return super().delete(request, *args, **kwargs)
