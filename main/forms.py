from django import forms
from main.models import Lifemark

CHOICES_STATE = (
    ('', ''),
    ('todo', 'todo'),
    ('working', 'working'),
    ('complete', 'complete'),
)


class LifemarkForm(forms.models.ModelForm):

    class Meta:
        model = Lifemark
        fields = '__all__'
        widgets = {
            'title': forms.fields.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter lifemark title',
            }),
            'link': forms.fields.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter related page link',
            }),
            'category': forms.fields.HiddenInput(),
            'is_complete': forms.fields.Select(
                choices=CHOICES_STATE,
                attrs={'class': 'form-control'},
            ),
            'due_datehour': forms.fields.HiddenInput(),
            'rating': forms.fields.TextInput(attrs={
                'class': 'form-control',
            }),
            'tags': forms.fields.TextInput(attrs={
                'class': 'form-control',
            }),
            'desc': forms.Textarea(attrs={
                'class': 'form-control',
            }),
            'image_url': forms.fields.TextInput(attrs={
                'class': 'form-control',
            }),
        }
        error_messages = {
            'title': {'required': "You need a valid title"}
        }

    def __init__(self, *args, **kwargs):
        super(LifemarkForm, self).__init__(*args, **kwargs)
