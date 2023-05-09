from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, ArticleScope


class ArticleScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        tag_name = []
        count = 0
        for form in self.forms:
            if form.cleaned_data.get('is_main'):
                count += 1
            if form.cleaned_data.get('tag').name in tag_name:
                raise ValidationError('Такой раздел уже есть в списке!')
            tag_name.append(form.cleaned_data.get('tag').name)
        if count == 0:
            raise ValidationError('Укажите основной раздел!')
        elif count > 1:
            raise ValidationError('Основным может быть только один раздел!')
        return super().clean()


class ArticleScopeInline(admin.TabularInline):
    model = ArticleScope
    formset = ArticleScopeInlineFormset
    extra = 0


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ArticleScopeInline]
