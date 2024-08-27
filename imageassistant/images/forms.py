from images.models import Image

from django import forms


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
    width = forms.IntegerField()
    height = forms.IntegerField()

    def clean_width(self):
        width = self.cleaned_data.get('width')
        width = int(width)
        print(width)
        if width <= 0:
            raise forms.ValidationError('Width must be greater than 0')
        return width

    def clean_height(self):
        height = self.cleaned_data.get('height')
        height = int(height)
        print(height)
        if height <= 0:
            raise forms.ValidationError('Height must be greater than 0')
        return height
