from django import forms
from .models import ServiceApplication

class ApplicationSubmissionForm(forms.ModelForm):
    class Meta:
        model = ServiceApplication
        fields = ['applicant_name', 'applicant_phone', 'applicant_address', 'ward']
        widgets = {
            'applicant_name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500'}),
            'applicant_phone': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500'}),
            'applicant_address': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500', 'rows': 3}),
            'ward': forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500'}),
        }
