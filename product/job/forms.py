from django.forms import ModelForm
from django import forms
from .models import Person, Residence_address, Education, Experience
from django.contrib.auth.models import User
from .models import CvStatusName, CvState




class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = ['position', 'full_name', 'birthday', 'gender',
                  'registration',
                  'residenceBool',
                  'phone',
                  'civil_status',
                  'quant_children',
                  'passp_number', 'passp_issue', 'passp_date',
                  'army', 'army_id', 'driver_lic', 'car', 'advantage', 'disadvantage', 'convicted', 'illness',
                  'salary',
                  'ref1_full_name', 'ref1_position', 'ref1_workplace', 'ref1_phone',
                  'ref2_full_name', 'ref2_position', 'ref2_workplace', 'ref2_phone',
                  'source_about_as', 'add_details',
                  'start',
                  ]

    def save(self, location):
        person = super(PersonForm, self).save()
        person.fill_location = location
        person.save()
        return person




class ResidenceForm(ModelForm):
    class Meta:
        model = Residence_address
        fields = ['residence']

    def save(self, person):
        obj = super(ResidenceForm, self).save(commit=False)
        obj.person = person
        return obj.save()


class EducationForm(ModelForm):
    class Meta:
        model = Education
        fields = ['start_date', 'end_date', 'name_institute', 'qualification']

    start_date = forms.DateField(widget=forms.HiddenInput, required=False)
    end_date = forms.DateField(widget=forms.HiddenInput, required=False)

    def save(self, person):
        obj = super(EducationForm, self).save(commit=False)
        obj.person = person
        return obj.save()


class ExpirienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = [
            'exp_start_date',
            'exp_end_date',
            'workplace',
            'exp_position',
            'responsibility',
            'exp_salary',
            'reason_leaving'
        ]

    exp_start_date = forms.DateField(widget=forms.HiddenInput, required=False)
    exp_end_date = forms.DateField(widget=forms.HiddenInput, required=False)

    def save(self, person):
        obj = super(ExpirienceForm, self).save(commit=False)
        obj.person = person
        return obj.save()


#######################




def get_cvstate_choices():
    cvstate_choices = []
    for num in CvStatusName.objects.all().order_by('status'):
        cvstate_choices.append((num.status, num.get_status_display()))
    return cvstate_choices


class FilterCvListForm(forms.Form):
    date_at = forms.DateField(label='с', required=False, )
    date_to = forms.DateField(label='по', required=False)
    position = forms.CharField(label='Должность', max_length=20, required=False)
    full_name = forms.CharField(label='ФИО', max_length=20, required=False)
    cv_state = forms.MultipleChoiceField(label='Статус', choices=get_cvstate_choices, required=False, widget=forms.widgets.CheckboxSelectMultiple())


    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('date_at') and cleaned_data.get('date_to'):
            if cleaned_data['date_at'] > cleaned_data['date_to']:
                msg = 'Не правильный диапазон дат'
                self.add_error('date_at', msg)


    def filter_set(self):
        preset = {'fill_date__gte': 'date_at', 'fill_date__lte': 'date_to', 'position__icontains': 'position',
                  'full_name__icontains': 'full_name'}
        args = {k:self.cleaned_data[v] for k, v in preset.items() if v in self.changed_data and v in self.cleaned_data}
        return args


class CvPersonForm(PersonForm):

    def save(self, **kwargs):
        return ModelForm.save(self, **kwargs)


class CvEducationForm(EducationForm):
    pass

    def save(self, **kwargs):
        return ModelForm.save(self, **kwargs)


class CvExperienceForm(ExpirienceForm):
    pass

    def save(self, **kwargs):
        return ModelForm.save(self, **kwargs)


class CvResidenceForm(ResidenceForm):

    def save(self, *args, **kwargs):
        return super(CvResidenceForm, self).save(*args, **kwargs)

    def save_init(self):
        return ModelForm.save(self)


class CvStateForm(ModelForm):
    class Meta:
        model = CvState
        fields = ['status', 'user_responsible', 'comment']

    status = forms.ModelChoiceField(label='Статус', queryset=CvStatusName.objects.all())
    user_responsible = forms.ModelChoiceField(label='Передать в работу', queryset=User.objects.all())
