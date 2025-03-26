from django import forms
from .models import Story
from django.core.validators import FileExtensionValidator

class ImageUploadForm(forms.Form):
    image = forms.ImageField(
        label='Lung Tissue Image',
        widget=forms.FileInput(attrs={'accept': 'image/*'}),
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )
    
class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['name', 'role', 'story']



