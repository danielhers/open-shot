import re
from django import forms
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext as _
from user.models import Profile

unicode_username = forms.RegexField(label=_("Username"), max_length=30,
        regex=re.compile(r'^(?u)[ \w.@+-]{4,}$', re.U),
        help_text = _("Required. 4-30 characters (only letters, numbers spaces and @/./+/-/_ characters)."),
        error_message = _("Required. 4-30 characters (only letters, numbers spaces and @/./+/-/_ characters)."))

class ProfileAdmin(admin.StackedInline):
    model = Profile
    extra = 0
    max_num = 1

# Overrides django.contrib.auth.forms.UserCreationForm and changes 
# username to accept a wider range of character in the username. 
class UserCreationForm(UserCreationForm):
    username = unicode_username

# Overrides django.contrib.auth.forms.UserChangeForm and changes 
# username to accept a wider range of character in the username. 
class UserChangeForm(UserChangeForm): 
    username = unicode_username

class UnicodeUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    inlines = [ProfileAdmin, ]
    list_filter = ('is_superuser', 'is_staff', 'profile__is_editor', 'profile__is_candidate', 'is_active', 'date_joined', 'profile__locality')

admin.site.unregister(User)
admin.site.register(User, UnicodeUserAdmin)
