from django import forms 
from .models import Book, Paper, Profile , Event
import bleach

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        
        fields= ['title','cover']

        labels = {'title': ''}

class PaperForm(forms.ModelForm):
    class Meta:
        model = Paper

        fields = ['title','paragraphs']

        labels = {'title' : '','paragraphs' : ''}

    def clean_paragraphs(self):
            """ Anti-XSS """
            
            text_user = self.cleaned_data.get('paragraphs')


            allowed_tags = [
                'p', 'b', 'i', 'u', 'em', 'strong', 'a', 
                'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                'ul', 'ol', 'li', 'br', 'span', 'div',
                'pre', 'code', 'table', 'tbody', 'tr', 'td', 'th' 
            ]

            allowed_attrs = {
                '*': ['class', 'style'], 
                'img': ['src', 'alt', 'width', 'height'] 
            }

   
            allowed_protocols = ['http', 'https', 'mailto']

    
            texto_limpo = bleach.clean(text_user, tags=allowed_tags,attributes=allowed_attrs, protocols=allowed_protocols, strip=True)

            return texto_limpo


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["profile_image", "banner_image"]


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        
        fields = ["title", "start_date", "end_date"]
        labels = {"title": "Título do Compromisso"}

        widgets = {"start_date": forms.DateInput(attrs={"type": "date"}), "end_date": forms.DateInput(attrs={"type": "date"}), }
