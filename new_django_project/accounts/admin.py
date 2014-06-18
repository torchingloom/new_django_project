# coding: utf-8

from django import forms
from django.core.exceptions import ValidationError
from django.contrib import admin
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm, UserCreationForm as BaseUserCreationForm
from django.contrib.auth.admin import UserAdmin, GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group
from new_django_project.accounts.models import User


class UserChangeForm(BaseUserChangeForm):
    class Meta(BaseUserChangeForm.Meta):
        model = User


class UserCreationForm(BaseUserCreationForm):
    class Meta(BaseUserCreationForm.Meta):
        model = User

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise ValidationError(self.error_messages['duplicate_username'])


class UserProfileAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm


# admin.site.unregister(AuthUser)
admin.site.register(User, UserProfileAdmin)


class GroupForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(
        label=u'Пользователи',
        queryset=User.objects.all(),
        required=False,
        widget=admin.widgets.FilteredSelectMultiple("users", is_stacked=False)
    )

    class Meta:
        model = Group
        widgets = {
            'permissions': admin.widgets.FilteredSelectMultiple("permissions", is_stacked=False),
        }


class GroupAdmin(BaseGroupAdmin):
    form = GroupForm

    def save_model(self, request, obj, form, change):
        super(GroupAdmin, self).save_model(request, obj, form, change)
        obj.user_set.clear()
        for user in form.cleaned_data['users']:
             obj.user_set.add(user)

    def get_form(self, request, obj=None, **kwargs):
        if obj:
            self.form.base_fields['users'].initial = [o.pk for o in obj.user_set.all()]
        else:
            self.form.base_fields['users'].initial = []
        return GroupForm

admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)