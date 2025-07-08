from django import forms
from .models import Label


class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        exclude = ['csv_data', 'labeled_by', 'label_time']
        widgets = {
            'label_type': forms.RadioSelect,
            'abnormal_subtype': forms.RadioSelect,
        }
        

    def __init__(self, *args, **kwargs):
        self.csv_data = kwargs.pop('csv_data', None)
        self.user = kwargs.pop('user', None)
        super(LabelForm, self).__init__(*args, **kwargs)


    def clean(self):
        cleaned_data = super().clean()
        label_type = cleaned_data.get('label_type')
        abnormal_subtype = cleaned_data.get('abnormal_subtype')

        if label_type == 'abnormal' and not abnormal_subtype:
            self.add_error('abnormal_subtype', 'Please select the category of the Abnormal character.')
        return cleaned_data
    
    def save(self, commit=True):
        label_instance = super().save(commit=False)
        if self.csv_data:
            label_instance.csv_data = self.csv_data
        if self.user:
            label_instance.labeled_by = self.user
        if commit:
            label_instance.save()
        return label_instance