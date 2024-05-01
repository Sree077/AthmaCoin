from django import forms


class CodeForm(forms.Form):
    code = forms.IntegerField(max_value=999999, min_value=100000,
                              widget=forms.TextInput(attrs={'placeholder': 'Enter Your Coupon Code'}),
                              error_messages={'max_value': 'Enter a Valid Coupon Code', 'min_value': 'Enter a Valid Coupon Code', 'invalid': 'Enter a Valid Coupon Code'},
                              )