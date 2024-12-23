from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from .models import FoodLog, WaterLog, Goal
from .utils import get_nutrition
from .forms import UserDetailsForm
from datetime import date
from .models import Profile


def nutrition(request):
    return render(request, 'nutrition.html')
def about_author(request):
    return render(request, 'about.html')

def nutrition(request):
    social_links = {
        'facebook': 'https://www.facebook.com/your-profile',
        'twitter': 'https://twitter.com/your-profile',
        'instagram': 'https://www.instagram.com/your-profile',
        'linkedin': 'https://www.linkedin.com/in/nandakishor-p/',
        'github': 'https://github.com/Nandakishor-P',
    }
    return render(request, 'nutrition.html', {'social_links': social_links})

def signup(request):
    if request.method == 'POST':
        username = request.POST['username'].strip()
        email = request.POST['email'].strip()
        password = request.POST['password'].strip()

        # Validate username
        if not username.isalnum() or len(username) < 4 or len(username) > 12:
            messages.error(request, 'Username must be 4-12 characters long and contain only letters and numbers.')
            return render(request, 'signup.html')

        # Validate email
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Please enter a valid email address.')
            return render(request, 'signup.html')

        # Validate password
        if len(password) < 8 or len(password) > 20:
            messages.error(request, 'Password must be 4-12 characters long.')
            return render(request, 'signup.html')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose another one.')
            return render(request, 'signup.html')
        
        #to check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered. Please use a different email or log in.')
            return render(request, 'signup.html')


        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        login(request, user)
        messages.success(request, 'Sign-up successful!')
        return redirect('/dashboard')

    return render(request, 'signup.html')





def user_login(request):
    if request.method == 'POST':
        username = request.POST['username'].strip()
        password = request.POST['password'].strip()

        # Validate username
        if not username:
            messages.error(request, 'Please enter your username.')
            return render(request, 'login.html')

        # Validate password
        if not password:
            messages.error(request, 'Please enter your password.')
            return render(request, 'login.html')

        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            from .models import Profile  # Import Profile model
            Profile.objects.get_or_create(user=user)
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('/dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'login.html')

    return render(request, 'login.html')


@login_required
def log_food(request):
    """
    View to log multiple food items and their nutritional details.
    """
    if request.method == 'POST':
        num_items = int(request.POST.get('num_items', 0))  # Number of food items
        logged_items = []
        errors = []

        # Loop through each food item
        for i in range(1, num_items + 1):
            food_item = request.POST.get(f'food_item_{i}')  # e.g., "Apple"
            if food_item:
                # Fetch nutrition data from Edamam
                nutrition_data = get_nutrition(f"100g {food_item}")  # Default to 100g
                if nutrition_data:
                    # Save the food log in the database
                    food_log = FoodLog.objects.create(
                        user=request.user,
                        meal_name=food_item,
                        calories=nutrition_data['calories'],
                        protein=nutrition_data['protein'],
                        fats=nutrition_data['fats'],
                    )
                    logged_items.append(food_log)
                else:
                    errors.append(f"Could not fetch data for {food_item}. Please try again.")

        # Render the same page with success and error messages
        return render(request, 'log_food.html', {
            'success_message': f"Successfully logged {len(logged_items)} food items.",
            'errors': errors,
            'logged_items': logged_items,
        })
    

    food_logs = FoodLog.objects.filter(user=request.user).order_by('-date')
    print(food_logs) 
    return render(request, 'log_food.html', {'food_logs': food_logs})

@login_required
def track_water_intake(request):
    """
    Handles water intake logging and displays the user's water logs.
    """
    if request.method == 'POST':
        # Retrieve water intake from the POST data
        amount = float(request.POST.get('amount', 0))  # Input value in liters
        if amount > 0:
            # Create a new WaterLog entry and save it to the database
            WaterLog.objects.create(user=request.user, amount=amount)

        # Redirect to avoid resubmission
        return redirect('water-intake')

    # Handle GET requests by fetching water logs for the user
    water_logs = WaterLog.objects.filter(user=request.user).order_by('-date')
    return render(request, 'water-intake.html', {'water_logs': water_logs})


def calculate_daily_requirements(goal_type, age, height, weight, gender, exercise_level):
    # Basal Metabolic Rate (BMR) calculation
    if gender == 'M':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    # Adjust for activity level
    activity_multiplier = {
        'none': 1.2,
        'light': 1.375,
        'moderate': 1.55,
        'intense': 1.725,
    }
    daily_calories = bmr * activity_multiplier[exercise_level]

    # Adjust based on goal type
    if goal_type == 'reduce':
        daily_calories *= 0.8  # Reduce by 20%
    elif goal_type == 'increase':
        daily_calories *= 1.2  # Increase by 20%

    # Water intake (liters), protein (grams), fats (grams)
    daily_water = weight * 0.033
    daily_protein = weight * (1.6 if goal_type == 'increase' else 0.8)
    daily_fats = (daily_calories * 0.2) / 9

    return {
        'calories': round(daily_calories),
        'water': round(daily_water, 1),
        'protein': round(daily_protein, 1),
        'fats': round(daily_fats, 1),
    }

@login_required
def dashboard(request):
    """
    Dashboard to display user goals, intake, and recommendations dynamically.
    """
    user = request.user
    today = date.today()

    # Fetch user goals
    try:
        goal = Goal.objects.get(user=user)
    except Goal.DoesNotExist:
        goal = None

    # Fetch today's food logs
    food_logs = FoodLog.objects.filter(user=user, date=today)
    total_calories = sum(log.calories for log in food_logs)
    total_protein = sum(log.protein for log in food_logs)
    total_fats = sum(log.fats for log in food_logs)

    # Fetch today's water logs
    water_logs = WaterLog.objects.filter(user=user, date=today)
    total_water = sum(log.amount for log in water_logs)

    # Calculate daily requirements if goals exist
    if goal:
        user_details = {
            'age': user.profile.age,
            'height': user.profile.height,
            'weight': user.profile.weight,
            'gender': user.profile.gender,
            'exercise_level': user.profile.exercise_level,
        }
        daily_requirements = calculate_daily_requirements(
            goal.goal_type,
            **user_details
        )

        # Compare intake with requirements
        differences = {
            'calories': daily_requirements['calories'] - total_calories,
            'water': daily_requirements['water'] - total_water,
            'protein': daily_requirements['protein'] - total_protein,
            'fats': daily_requirements['fats'] - total_fats,
        }
    else:
        daily_requirements = None
        differences = None

    context = {
        'goal': goal,
        'food_logs': food_logs,
        'water_logs': water_logs,
        'daily_requirements': daily_requirements,
        'total_calories': total_calories,
        'total_water': total_water,
        'total_protein': total_protein,
        'total_fats': total_fats,
        'differences': differences,
    }
    return render(request, 'dashboard.html', context)


@login_required
def set_goals(request):
    """
    Allows users to input their details and set a fitness goal.
    """
    if request.method == 'POST':
        form = UserDetailsForm(request.POST)
        if form.is_valid():
            # Get user details from form
            age = form.cleaned_data['age']
            height = form.cleaned_data['height']
            weight = form.cleaned_data['weight']
            gender = form.cleaned_data['gender']
            exercise_level = form.cleaned_data['exercise_level']

            # Save or update user details in the profile
            profile, created = Profile.objects.get_or_create(user=request.user)
            profile.age = age
            profile.height = height
            profile.weight = weight
            profile.gender = gender
            profile.exercise_level = exercise_level
            profile.save()

            # Calculate daily requirements
            requirements = calculate_daily_requirements(
                'maintain', age, height, weight, gender, exercise_level
            )

            # Render goal setting page
            return render(request, 'goals.html', {
                'requirements': requirements,
            })
    else:
        form = UserDetailsForm()

    return render(request, 'input_details.html', {'form': form})

@login_required
def save_goals(request):
    """
    Saves the user's selected fitness goal.
    """
    if request.method == 'POST':
        goal_type = request.POST.get('goal')
        Goal.objects.update_or_create(
            user=request.user,
            defaults={'goal_type': goal_type},
        )
        return redirect('dashboard')
    
def display_goals(request):
    user = request.user
    # Assume user details are stored or retrieved elsewhere
    age = user.profile.age
    height = user.profile.height
    weight = user.profile.weight
    gender = user.profile.gender
    exercise_level = user.profile.exercise_level

    # Get user's goal type
    goal = Goal.objects.get(user=user)
    calculated_goals = calculate_daily_requirements(goal.goal_type, age, height, weight, gender, exercise_level)
    return render(request, 'goals.html', {'calculated_goals': calculated_goals})





