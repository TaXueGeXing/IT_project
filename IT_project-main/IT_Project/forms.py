from django import forms
from .models import Transaction, CarPost, Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['buyer', 'seller', 'car_post', 'price_agreed', 'status']
        widgets = {
            'status': forms.Select(choices=Transaction.STATUS_CHOICES),
        }

    def __init__(self, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        # Additional form customization can go here
        self.fields['car_post'].queryset = CarPost.objects.all()
        self.fields['buyer'].queryset = User.objects.all()
        self.fields['seller'].queryset = User.objects.all()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required. Add a valid email address.")
    phone_number = forms.CharField(required=True, max_length=15, help_text="Required.")

    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'password1', 'password2', )

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.phone_number = self.cleaned_data['phone_number']
        if commit:
            user.save()
        return user

class EditProfileForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(required=True, max_length=15)

    class Meta:
        model = User
        fields = ('email', 'phone_number')

class CarPostForm(forms.ModelForm):
    class Meta:
        model = CarPost
        fields = ['title', 'description', 'make', 'model', 'year', 'mileage', 'price']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']