from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Story
from .forms import StoryForm
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import numpy as np
import cv2
from django.core.files.storage import default_storage
from django.conf import settings
from .forms import ImageUploadForm
import tensorflow as tf
import os
import logging


def register(request):
    if request.method == "POST":
        name = request.POST.get("name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not username:
            messages.error(request, "Username is required.")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return redirect("register")

        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = name.split()[0]  # Set first name
        user.last_name = " ".join(name.split()[1:])  # Set last name
        user.save()

        messages.success(request, "Registration successful. You can now log in.")
        return redirect("index")

    return render(request, "app1/register.html")

def index(request):
    if request.method == "POST":
        username= request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect("home")  # Redirect to a protected page
        else:
            messages.error(request, "Invalid email or password.")
            return redirect("index")

    return render(request, "app1/index.html")

@login_required
def account_view(request):
    # Render the account management page
    return render(request, "app1/account.html")

def logout_view(request):
    # Log out the user
    logout(request)
    return redirect("index")

@login_required
def home(request):
    return render(request, 'app1/home.html')

def symptom_checker(request):
    return render(request, 'app1/symptom_checker.html')

def lung_analysis(request):
    return render(request, 'app1/lung_analysis.html')

def community(request):
    stories = Story.objects.all().order_by('-created_at')
    return render(request, 'app1/community.html', {'stories': stories})

def share_story(request):
    if request.method == 'POST':
        form = StoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('community')
    else:
        form = StoryForm()
    return render(request, 'app1/share_story.html', {'form': form})




logger = logging.getLogger(__name__)

# Load model ONCE at startup
try:
    MODEL_PATH = os.path.join(settings.BASE_DIR, 'app1/models/lung_cancer_vgg16/lung_cancer_vgg16.keras')
    model = tf.keras.models.load_model(MODEL_PATH)
    logger.info("Model loaded successfully. Input shape: %s", model.input_shape)
except Exception as e:
    model = None
    logger.error("MODEL LOADING FAILED: %s", str(e))

@csrf_exempt
def classify_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        
        if not form.is_valid():
            return JsonResponse({'error': 'Invalid form submission'}, status=400)
        
        try:
            # 1. Save uploaded file
            image = form.cleaned_data['image']
            file_path = default_storage.save('temp/temp_img.jpg', image)
            img_path = os.path.join(settings.MEDIA_ROOT, file_path)
            
            # 2. Verify image
            if not os.path.exists(img_path):
                raise Exception("Image not saved correctly")
            
            # 3. Preprocess image (VGG16 specific)
            img = cv2.imread(img_path)
            if img is None:
                raise Exception("OpenCV couldn't read the image")
            
            img = cv2.resize(img, (224, 224))  # Standard VGG16 size
            img = img.astype('float32') / 255.0  # Normalize
            img = np.expand_dims(img, axis=0)  # Add batch dimension
            
            # 4. Predict
            preds = model.predict(img)
            class_idx = np.argmax(preds, axis=1)[0]
            confidence = float(np.max(preds)) * 100
            
            classes = {
                0: {'name': 'Adenocarcinoma', 'class': 'danger'},
                1: {'name': 'Normal', 'class': 'success'},
                2: {'name': 'Squamous Cell Carcinoma', 'class': 'danger'}
            }
            
            return JsonResponse({
                'result': classes[class_idx],
                'confidence': f"{confidence:.2f}%",
                'image_url': f"/media/{file_path}"
            })
            
        except Exception as e:
            logger.error("ANALYSIS FAILED: %s", str(e), exc_info=True)
            return JsonResponse({'error': str(e)}, status=500)
            
        finally:
            if os.path.exists(img_path):
                os.remove(img_path)
    
    return render(request, 'app1/lung_analysis.html', {'form': ImageUploadForm()})