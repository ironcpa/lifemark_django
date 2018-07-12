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
                'placeholder': 'Enter lifemark title',
            }),
            'link': forms.fields.URLInput(attrs={
                'placeholder': 'Enter related page link',
            }),
            'category': forms.fields.HiddenInput(),
            'is_complete': forms.fields.Select(choices=CHOICES_STATE),
            'due_datehour': forms.fields.HiddenInput(),
            'rating': forms.fields.TextInput(),
            'tags': forms.fields.TextInput(),
            'image_url': forms.fields.TextInput(),
        }
        error_messages = {
            'title': {'required': "You need a valid title"}
        }

    def __init__(self, *args, **kwargs):
        super(LifemarkForm, self).__init__(*args, **kwargs)
