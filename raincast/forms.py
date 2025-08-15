from django import forms
from datetime import date, timedelta


class PredictionForm(forms.Form):
    location = forms.CharField(
        max_length=120,
        label="Location",
        help_text="Enter your location",
    )
    date_ = forms.DateField(
        label="Date",
        widget=forms.DateInput(attrs={"type": "date"})
    )

    lat = forms.CharField(required=False, widget=forms.HiddenInput())
    lon = forms.CharField(required=False, widget=forms.HiddenInput())

    def clean_date_(self):
        date_ = self.cleaned_data["date_"]
        today = date.today()

        if date_ < today:
            raise forms.ValidationError("Date is in the past")
        if date_ > today + timedelta(days=14):
            raise forms.ValidationError("Please choose a date within the next 14 days.")
        return date_