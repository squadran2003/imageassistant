from images.models import Image

from django import forms
from django.urls import reverse
from django.db import models


class ImageUploadForm(forms.ModelForm):
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


aspect_ratio_choices = [
    ('16:9', '16:9'),
    ('1:1', '1:1'),
    ('21:9', '21:9'),
    ('2:3', '2:3'),
    ('3:2', '3:2'),
    ('4:5', '4:5'),
    ('5:4', '5:4'),
    ('9:16', '9:16'),
    ('9:21', '9:21')
]


class PromptForm(forms.Form):
    # this should be a hidden field
    bot_field = forms.CharField(
        required=False, widget=forms.HiddenInput(
            attrs={'class': 'display:none;'}
        )
    )
    prompt = forms.CharField(
        required=True, widget=forms.Textarea(
           attrs={
                'class': "shadow appearance-none border rounded mt-2 min-h-20 mb-2 p-2 w-full  focus:outline-none focus:shadow-outline",
                "rows": 5,
                "cols": 40,
                "placeholder": "Tell us more about the image you want to generate",
                "style": "color:black"
            },
        )
    )
    aspect_ratio = forms.CharField(
        required=True,
        widget=forms.Select(
            choices=aspect_ratio_choices,
            attrs={
                'class': 'block appearance-none w-full border border-[#fffff] bg-[#ffff] py-3 px-4 pr-8 rounded leading-tight focus:outline-none focus:bg-[#ffff] focus:border-gray-500',
                'label': 'Aspect Ratio',
                'name': 'aspect_ratio'
            }, 
        ),
        empty_value='16:9'

    )
    confirm_your_a_human = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'mt-5',
                'type': 'checkbox',
                'required': 'required',
                'name': 'confirm_your_a_human',
                'placeholder': 'I am not a robot'
            }
        )
    )

    def clean_prompt(self):
        prompt = self.cleaned_data.get('prompt', None)
        if len(prompt) > 350:
            raise forms.ValidationError('Prompt must be less than 20 characters')
        if prompt is None or prompt == '':
            raise forms.ValidationError('Prompt is required')
        if len(prompt) > 350:
            raise forms.ValidationError('Prompt must be less than 20 characters')
        # check for xss javascript
        if '<script>' in prompt:
            raise forms.ValidationError('Invalid request')
        return prompt

    def clean_bot_field(self):
        bot_field = self.cleaned_data.get('bot_field')
        if bot_field:
            raise forms.ValidationError('Invalid request')
        if bot_field:
            raise forms.ValidationError('Invalid request')
        return bot_field
    
    def clean_confirm_your_a_human(self):
        confirm_your_a_human = self.cleaned_data.get('confirm_your_a_human', False)
        if not confirm_your_a_human:
            raise forms.ValidationError('Please confirm you are not a robot')
        return confirm_your_a_human
