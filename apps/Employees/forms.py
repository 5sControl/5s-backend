from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from multiupload.fields import MultiFileField, MultiMediaField, MultiImageField

from apps.Employees.models import CustomUser


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

        widgets = {
            'email': forms.EmailInput(attrs={'class': 'input', 'placeholder': 'Email Address'})

        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'dataset', 'image']  # not attachments!

    files = MultiFileField(min_num=1, max_num=3, max_file_size=1024*1024*5)

    def save(self, commit=True):
        instance = super(ContactForm, self).save(commit)
        for each in self.cleaned_data['image']:
            CustomUser.objects.create(file=each, message=instance)

        return instance
