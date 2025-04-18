from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings


def home(request):
    # return HttpResponse("Hello WElcome to Pinaks 1st backend in django .......")
    return render(request, 'website/index.html')

def about(request):
    return render(request, 'website/about.html')

def contact(request):
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        message_content = request.POST.get('message', '')
        
        # Create message body
        full_message = f"""
        Name: {name}
        Email: {email}
        Phone: {phone}
        
        Message:
        {message_content}
        """
        
        # Try to send email
        try:
            # In production, this will send an actual email
            # In development, it will be printed to the console
            send_mail(
                subject=f'Contact Form Submission from {name}',
                message=full_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL],
                fail_silently=False,
            )
            # Add success message
            messages.success(request, "Thank you for your message! We'll get back to you soon.")
            return redirect('contact')
        except Exception as e:
            # Log the error in production
            print(f"Error sending email: {e}")
            # Add error message
            messages.error(request, "There was a problem sending your message. Please try again later.")
            
    # If GET request or after POST processing
    return render(request, 'website/contact.html')

def custom_page_not_found(request, exception):
    return render(request, 'website/404.html', status=404)