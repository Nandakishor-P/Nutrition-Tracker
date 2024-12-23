from django import forms

class UserDetailsForm(forms.Form):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    EXERCISE_LEVEL_CHOICES = [
        ('none', 'No Exercise'),
        ('light', 'Light Exercise'),
        ('moderate', 'Moderate Exercise'),
        ('intense', 'Intense Exercise'),
    ]

    age = forms.IntegerField(required=True, label="Age")
    height = forms.FloatField(required=True, label="Height (cm)")
    gender = forms.ChoiceField(choices=GENDER_CHOICES, label="Gender")
    weight = forms.FloatField(required=True, label="Weight (kg)")
    exercise_level = forms.ChoiceField(choices=EXERCISE_LEVEL_CHOICES, label="Exercise Level")
