from django import forms


class LifemarkForm(forms.Form):
    title = forms.CharField(
        widget=forms.fields.TextInput(attrs={
            'placeholder': 'Enter lifemark title',
        })
    )
