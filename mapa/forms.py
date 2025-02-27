from django import forms
from .models import Profile
from .models import Sugestao
from .models import Resposta

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user', 'photo','plan']


class SugestaoForm(forms.ModelForm):
    class Meta:
        model = Sugestao
        fields = ['titulo', 'descricao']
       
       
class RespostaForm(forms.ModelForm):
    class Meta:
        model = Resposta
        fields = ['resposta']


    def __init__(self, *args, **kwargs):
        super(RespostaForm, self).__init__(*args, **kwargs)
        self.fields['resposta'].widget.attrs.update({'class': 'form-control', 'rows': 4})