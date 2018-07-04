from django import forms
from main.models import Lifemark
from main.models import TestModel


class LifemarkForm(forms.models.ModelForm):

    class Meta:
        model = Lifemark
        fields = '__all__'
        widgets = {
            'title': forms.fields.TextInput(attrs={
                'placeholder': 'Enter lifemark title',
            }),
            'link': forms.fields.URLInput(attrs={
                'placeholder': 'Enter related page link',
            }),
            'category': forms.fields.TextInput(attrs={
                'placeholder': 'Enter new or select from combo',
            }),
            'is_complete': forms.fields.TextInput(),
            'due_date': forms.fields.TextInput(),
            'rating': forms.fields.TextInput(),
            'tags': forms.fields.TextInput(),
            'image_url': forms.fields.TextInput(),
        }
        error_messages = {
            'title': {'required': "You need a valid title"}
        }

    def __init__(self, *args, **kwargs):
        super(LifemarkForm, self).__init__(*args, **kwargs)
        self.fields['link'].required = False
        self.fields['category'].required = False
        self.fields['is_complete'].required = False
        self.fields['due_date'].required = False
        self.fields['rating'].required = False
        self.fields['tags'].required = False
        self.fields['desc'].required = False
        self.fields['image_url'].required = False


class TestForm(forms.models.ModelForm):

    class Meta:
        model = TestModel
        fields = '__all__'
