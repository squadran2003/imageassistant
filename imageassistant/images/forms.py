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
        return image