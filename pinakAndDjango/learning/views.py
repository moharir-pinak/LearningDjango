from django.shortcuts import render
from django.http import HttpResponse
from .models import CharVarity
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.core.files.images import ImageFile
from django.core.files.base import ContentFile
import os
import base64
import requests
from io import BytesIO
from django.conf import settings
import random
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.urls import reverse, reverse_lazy

# Create your views here.
def add_dummy_courses():
    # Only add dummy courses if none exist
    if CharVarity.objects.count() == 0:
        try:
            # List of courses to add
            dummy_courses = [
                {
                    'name': 'Python for Beginners',
                    'description': 'Learn Python from scratch with practical exercises and projects. This course is perfect for complete beginners.',
                    'price': 1499.00,
                    'type': 'py',
                    'instructor': 'John Smith',
                    'duration': '12 hours',
                    'level': 'Beginner',
                    'image_url': 'https://img.freepik.com/free-vector/gradient-python-logo_23-2150213200.jpg',
                    'rating': 4.8,
                    'students_enrolled': 12583,
                    'is_featured': True
                },
                {
                    'name': 'Advanced JavaScript',
                    'description': 'Master JavaScript with this comprehensive course covering ES6+, async/await, closures, and more.',
                    'price': 2499.00,
                    'type': 'js',
                    'instructor': 'Sarah Johnson',
                    'duration': '15 hours',
                    'level': 'Advanced',
                    'image_url': 'https://img.freepik.com/free-vector/javascript-abstract-concept-illustration_335657-3702.jpg',
                    'rating': 4.7,
                    'students_enrolled': 8245,
                    'is_featured': True
                },
                {
                    'name': 'Web Development Bootcamp',
                    'description': 'A comprehensive bootcamp covering HTML, CSS, JavaScript, and responsive design principles.',
                    'price': 1999.00,
                    'type': 'html',
                    'instructor': 'David Wilson',
                    'duration': '20 hours',
                    'level': 'Intermediate',
                    'image_url': 'https://img.freepik.com/free-vector/web-development-programmer-engineering-coding-website-augmented-reality-interface-screens-developer-project-engineer-programming-software-application-design-cartoon-illustration_107791-3863.jpg',
                    'rating': 4.9,
                    'students_enrolled': 15420,
                    'is_featured': True
                },
                {
                    'name': 'React.js Masterclass',
                    'description': 'Learn to build modern, reactive web applications with React.js, hooks, context API and Redux.',
                    'price': 2999.00,
                    'type': 'react',
                    'instructor': 'Emily Chen',
                    'duration': '18 hours',
                    'level': 'Intermediate',
                    'image_url': 'https://miro.medium.com/v2/resize:fit:1200/1*y6C4nSvy2Woe0m7bWEn4BA.png',
                    'rating': 4.6,
                    'students_enrolled': 7845,
                    'is_featured': False
                },
                {
                    'name': 'Django Web Framework',
                    'description': 'Build powerful web applications with Django, the Python web framework for perfectionists with deadlines.',
                    'price': 2199.00,
                    'type': 'django',
                    'instructor': 'Michael Rodriguez',
                    'duration': '16 hours',
                    'level': 'Intermediate',
                    'image_url': 'https://miro.medium.com/v2/resize:fit:678/1*DGnzHHkfYMuN7Wvdk8j6TA.png',
                    'rating': 4.5,
                    'students_enrolled': 5632,
                    'is_featured': False
                },
                {
                    'name': 'Machine Learning Fundamentals',
                    'description': 'Introduction to machine learning algorithms, data preprocessing, and model evaluation using Python and scikit-learn.',
                    'price': 3499.00,
                    'type': 'ml',
                    'instructor': 'Dr. Alexandra Patel',
                    'duration': '22 hours',
                    'level': 'Advanced',
                    'image_url': 'https://img.freepik.com/free-vector/gradient-machine-learning-infographic_23-2149379688.jpg',
                    'rating': 4.9,
                    'students_enrolled': 6789,
                    'is_featured': True
                }
            ]
            
            # Get the media root
            media_root = settings.MEDIA_ROOT
            os.makedirs(os.path.join(media_root, 'learningimages'), exist_ok=True)
            
            # Add courses
            for course_data in dummy_courses:
                course = CharVarity(
                    name=course_data['name'],
                    description=course_data['description'],
                    price=course_data['price'],
                    type=course_data['type'],
                    instructor=course_data['instructor'],
                    duration=course_data['duration'],
                    level=course_data['level'],
                    rating=course_data['rating'],
                    students_enrolled=course_data['students_enrolled'],
                    is_featured=course_data['is_featured'],
                    date=timezone.now()
                )
                
                # Download image and save it
                try:
                    response = requests.get(course_data['image_url'])
                    if response.status_code == 200:
                        img_name = f"{course_data['type']}_{random.randint(1000, 9999)}.jpg"
                        img_path = os.path.join('learningimages', img_name)
                        img_fullpath = os.path.join(media_root, img_path)
                        
                        with open(img_fullpath, 'wb') as f:
                            f.write(response.content)
                        
                        course.image = img_path
                except Exception as e:
                    print(f"Error downloading image for {course_data['name']}: {e}")
                    # Provide a fallback image
                    course.image = f"learningimages/default_{course_data['type']}.jpg"
                
                course.save()
            
            print(f"Added {len(dummy_courses)} dummy courses to the database.")
        except Exception as e:
            print(f"Error adding dummy courses: {e}")

def learning(request):
    # Add dummy courses if none exist
    add_dummy_courses()
    
    # Get all courses
    learnings = CharVarity.objects.all() 
    return render(request, 'learning/index.html',{'learnings': learnings})

def learning_detail(request, pk):
    learning = get_object_or_404(CharVarity, pk=pk)
    return render(request, 'learning/learning_detail.html', {'learning': learning})
    
def learning_form(request):
    return render(request,'learning/learning_forms.html')

def contact(request):
    """View function for handling contact form"""
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        message_content = request.POST.get('message', '')
        
        # Form validation
        if name and email and message_content:
            # Prepare email message
            subject = f"Contact Form: {name}"
            message = f"Name: {name}\nEmail: {email}\nPhone: {phone}\n\nMessage:\n{message_content}"
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [settings.CONTACT_EMAIL if hasattr(settings, 'CONTACT_EMAIL') else settings.DEFAULT_FROM_EMAIL]
            
            try:
                # Send email
                send_mail(subject, message, from_email, recipient_list)
                messages.success(request, "Thank you for your message! We'll get back to you soon.")
            except BadHeaderError:
                messages.error(request, "Invalid header found. Please try again.")
            except Exception as e:
                messages.error(request, f"There was an error sending your message. Please try again later.")
                if settings.DEBUG:
                    print(f"Email error: {str(e)}")
        else:
            messages.error(request, "Please fill in all required fields.")
            
        # Redirect to contact page
        return redirect('contact')
            
    return render(request, 'website/contact.html')