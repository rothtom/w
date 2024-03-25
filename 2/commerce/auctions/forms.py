from django import forms

class BidForm(forms.Form):
    value = forms.DecimalField(label="Your bid here", decimal_places=2, step_size=0.01, max_digits=14, min_value=0)
