from django import forms
from main.models import Lifemark


class LifemarkForm(forms.models.ModelForm):

    class Meta:
        model = Lifemark
        '''
        fields = (
            'title',
            'link',
            'category',
            'is_complete',
            'due_date',
            'rating',
            'tags',
            'desc',
            'image_url',
        )
        '''
        fields = '__all__'
        widgets = {
            'title': forms.fields.TextInput(attrs={
                'placeholder': 'Enter lifemark title',
            }),
        }
        error_messages = {
            'title': {'required': "You need a valid title"}
        }

    def __init__(self, *args, **kwargs):
        super(LifemarkForm, self).__init__(*args, **kwargs)
        self.fields['category'].required = False
        self.fields['is_complete'].required = False
        self.fields['desc'].required = False
