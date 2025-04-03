from django import forms


class DateRangeForm(forms.Form):
    """
    Form to represent a span of multiple days using start and end dates.
    """
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Start Date",
        required=True
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="End Date",
        required=True
    )

    def clean(self):
        """
        Custom validation to ensure that the end date is not before the start date.

        Returns
        -------
        cleaned_data : dict
            date range form data with start and end dates validated.
        """
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            if end_date < start_date:
                raise forms.ValidationError("End date cannot be earlier than start date.")

        return cleaned_data
