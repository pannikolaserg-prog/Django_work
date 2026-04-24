from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
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

        if obj.is_published or self.request.user.is_staff:
            # Сохраняем старое значение просмотров
            old_views = obj.views_count

            # Увеличиваем счетчик
            obj.views_count += 1
            obj.save()

            # Проверяем, достигло ли число просмотров 100
            # и не отправляли ли уже поздравление
            if obj.views_count >= 100 and not obj.congratulation_sent:
                self.send_congratulation_email(obj)
                obj.congratulation_sent = True
                obj.save()

        return obj

    def send_congratulation_email(self, post):
        """Отправка поздравления на почту"""
        subject = f'🎉 Поздравление! Статья "{post.name}" достигла 100 просмотров!'

        message = f'''
        Здравствуйте!

        Поздравляем! Ваша статья "{post.name}" достигла {post.views_count} просмотров!

        Детали статьи:
        - Заголовок: {post.name}
        - Просмотров: {post.views_count}
        - Ссылка: http://127.0.0.1:8000{post.get_absolute_url()}
        - Дата создания: {post.created_at}

        Продолжайте в том же духе! 🚀

        С уважением,
        Ваш сайт
        '''

        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['your_email@gmail.com'],  # замените на свой email
                fail_silently=False,
            )
            print(f"Поздравление отправлено для статьи '{post.name}'")
        except Exception as e:
            print(f"Ошибка при отправке письма: {e}")


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
    success_url = reverse_lazy('blog:blog_list')  # ❌ СТАРОЕ (на список)

    # Нужно изменить на динамический URL:
    def get_success_url(self):
        """После успешного редактирования перенаправляем на страницу статьи"""
        return reverse_lazy('blog:blog_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Запись "{form.instance.name}" успешно обновлена!')
        return response


class BlogDeleteView(DeleteView):
    """Удаление записи"""
    model = MyBlog
    template_name = "blog/blog_confirm_delete.html"
    success_url = reverse_lazy('blog:blog_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, f'Запись "{self.get_object().name}" успешно удалена!')
        return super().delete(request, *args, **kwargs)
