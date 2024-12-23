from django.db import models
from django.contrib.auth.models import User

class FoodLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the User model
    meal_name = models.CharField(max_length=100)  # Name of the meal
    calories = models.FloatField(default=0.0)  # Calories in the meal
    protein = models.FloatField(default=0.0)  # Add default value
    fats = models.FloatField(default=0.0)
    date = models.DateField(auto_now_add=True)  # Date of the log

    def __str__(self):
        return f"{self.user.username} - {self.meal_name} ({self.calories} cal)"

class WaterLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    amount = models.FloatField()  # Water intake in liters

    def __str__(self):
        return f"{self.user.username} - {self.amount} L on {self.date}"

class Goal(models.Model):
    GOAL_CHOICES = [
        ('reduce', 'Reduce Weight'),
        ('maintain', 'Maintain Weight'),
        ('increase', 'Increase Calories'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)  # One user, one goal
    goal_type = models.CharField(max_length=10, choices=GOAL_CHOICES, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Goal"
    
class Profile(models.Model):
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

    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to the User model
    age = models.PositiveIntegerField(null=True, blank=True)  # Optional field
    height = models.FloatField(null=True, blank=True)  # Height in cm
    weight = models.FloatField(null=True, blank=True)  # Weight in kg
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    exercise_level = models.CharField(max_length=10, choices=EXERCISE_LEVEL_CHOICES, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    