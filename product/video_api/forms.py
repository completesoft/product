from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User

class VideoRecordFilterForm(forms.Form):
    date_at = forms.DateField(label='c', required=False, widget=forms.DateInput(attrs={'class':'form-control input-sm'}))
    date_to = forms.DateField(label='по', required=False, widget=forms.DateInput(attrs={'class':'form-control input-sm'}))
    place_id = forms.CharField(label='Магазин', max_length=20, required=False, widget=forms.TextInput(attrs={'class':'form-control input-sm'}))

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('date_at') and cleaned_data.get('date_to'):
            if cleaned_data['date_at'] > cleaned_data['date_to']:
                msg = 'Не правильный диапазон дат'
                self.add_error('date_at', msg)

    def filter_set(self):
        preset = {'time_start__date__gte': 'date_at', 'time_start__date__lte': 'date_to', 'place_id__icontains': 'place_id'}
        args = {k:self.cleaned_data[v] for k, v in preset.items() if v in self.changed_data and v in self.cleaned_data}
        return args