from images.models import Image

from django import forms
from django.urls import reverse


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image.size > 1024 * 1024 * 5:
            raise forms.ValidationError('Image file too large ( > 1mb )')
        endwith = image.name.split('.')[-1]
        if endwith not in ['jpg', 'jpeg', 'png', 'JPG', 'JPEG', 'PNG']:
            raise forms.ValidationError('Image file type is not supported')
        if len(image.name) > 450:
            raise forms.ValidationError("Image file name too long")
        return image


class ImageResizeForm(forms.Form):
    width = forms.IntegerField(
        required=False, widget=forms.TextInput(
            attrs={'class': "validate"}
        )
    )
    height = forms.IntegerField(
        required=False, 
        widget=forms.TextInput(attrs={'class': "validate"}
        )
    )

    def clean_width(self):
        width = self.cleaned_data.get('width')
        if width is None or width == '':
            raise forms.ValidationError('Width is required')
        width = int(width)
        if width <= 0 or width > 1000:
            raise forms.ValidationError('Width must be greater than 0 and less than 1000')
        return width

    def clean_height(self):
        height = self.cleaned_data.get('height')
        if height is None or height == '':
            raise forms.ValidationError('Height is required')
        height = int(height)
        if height <= 0 or height > 800:
            raise forms.ValidationError('Height must be greater than 0 and less than 800')
        return height


class CroppingForm(forms.Form):
    x = forms.FloatField(
        required=True, widget=forms.TextInput(
            attrs={'class': "validate", "type": "hidden"}
        )
    )
    y = forms.FloatField(
        required=True, widget=forms.TextInput(
            attrs={'class': "validate", "type": "hidden"}
        )
    )
    width = forms.FloatField(
        required=True, widget=forms.TextInput(
            attrs={'class': "validate", "type": "hidden"}
        )
    )
    height = forms.FloatField(
        required=True, widget=forms.TextInput(
            attrs={'class': "validate", "type": "hidden"}
        )
    )

    def clean_x(self):
        x = self.cleaned_data.get('x')
        if x is None or x == '':
            raise forms.ValidationError('X is required')
        x = int(x)
        if x < 0:
            raise forms.ValidationError('X must be greater than or equal to 0')
        return x

    def clean_y(self):
        y = self.cleaned_data.get('y')
        if y is None or y == '':
            raise forms.ValidationError('Y is required')
        y = int(y)
        if y < 0:
            raise forms.ValidationError('Y must be greater than or equal to 0')
        return y

    def clean_width(self):
        width = self.cleaned_data.get('width')
        if width is None or width == '':
            raise forms.ValidationError('Width is required')
        width = int(width)
        if width <= 0:
            raise forms.ValidationError('Width must be greater than 0')
        return width

    def clean_height(self):
        height = self.cleaned_data.get('height')
        if height is None or height == '':
            raise forms.ValidationError('Height is required')
        height = int(height)
        if height <= 0:
            raise forms.ValidationError('Height must be greater than 0')
        return height