from django import forms
import re


class ContactForm(forms.Form):
    email = forms.EmailField(
        required=True, widget=forms.EmailInput(
            attrs={
                "class": "shadow appearance-none border rounded mt-2 min-h-20 mb-2 p-2 w-full text-[#fff] focus:outline-none focus:shadow-outline",
                "placeholder": "Your email address"
            }
        )
    )
    message = forms.CharField(
        required=True, widget=forms.Textarea(
            attrs={
                'class': "shadow appearance-none border rounded mt-2 min-h-20 mb-2 p-2 w-full text-white focus:outline-none focus:shadow-outline",
                "placeholder": "Please send us a message if you are having issues or have any questions."
            }
        )
    )
    bot_field = forms.CharField(
        required=False, widget=forms.HiddenInput(
            attrs={'class': 'display:none;'}
        )
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

    def clean_email(self):
        email = self.cleaned_data.get('email', None)
        if not email:
            raise forms.ValidationError("Email is required")
        if re.match(r"[^@]+@[^@]+\.[^@]+", email) is None:
            raise forms.ValidationError("Email is invalid")
        return email

    def clean_message(self):
        message = self.cleaned_data.get('message', None)
        if not message or len(message) < 10:
            raise forms.ValidationError("Message is too short. Please explain in more detail.")
        return message

    def clean_confirm_your_a_human(self):
        confirm_your_a_human = self.cleaned_data.get('confirm_your_a_human', None)
        if not confirm_your_a_human:
            raise forms.ValidationError("Please confirm you are not a robot.")
        return confirm_your_a_human

    def clean_bot_field(self):
        bot_field = self.cleaned_data.get('bot_field', None)
        if bot_field:
            raise forms.ValidationError("You are a bot.")
        return bot_field