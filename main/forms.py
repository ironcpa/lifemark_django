import re
from django import forms
from main.models import Lifemark

CHOICES_STATE = (
    ('', ''),
    ('todo', 'todo'),
    ('working', 'working'),
    ('complete', 'complete'),
)

DATEHOUR_PATTERN = re.compile('\d{4}-\d{2}-\d{2} \d{2}')


class LifemarkForm(forms.models.ModelForm):
    geo_lat = forms.DecimalField(required=False, widget=forms.fields.HiddenInput())
    geo_lon = forms.DecimalField(required=False, widget=forms.fields.HiddenInput())

    class Meta:
        model = Lifemark
        fields = '__all__'
        exclude = ('c_geo_lat', 'c_geo_lon', 'u_geo_lat', 'u_geo_lon',)
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
            'state': forms.fields.Select(
                choices=CHOICES_STATE,
                attrs={'class': 'form-control'},
            ),
            'due_datehour': forms.fields.HiddenInput(),
            'rating': forms.fields.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '0 to 5 xs(xxxxx)'
            }),
            'tags': forms.fields.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter multiple tags with space separator'
            }),
            'desc': forms.Textarea(attrs={
                'class': 'form-control',
            }),
            'image_url': forms.fields.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter image url'
            }),
        }
        error_messages = {
            'title': {'required': "You need a valid title"}
        }

    def __init__(self, *args, **kwargs):
        super(LifemarkForm, self).__init__(*args, **kwargs)

    def clean_due_datehour(self):
        data = self.cleaned_data['due_datehour']
        if data and not DATEHOUR_PATTERN.match(data):
            raise forms.ValidationError(f"Invalid date hour format: {data}")

        return data
