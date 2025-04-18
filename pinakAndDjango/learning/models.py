from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

# Create your models here.

class CharVarity(models.Model):
    """Main course model - demonstrates relationships in reverse direction"""
    LEARNING_TYPES_CHOICES = [
        ('py', 'Python'),
        ('java', 'Java'),
        ('cpp', 'C++'),
        ('js', 'JavaScript'),
        ('html', 'HTML'),
        ('css', 'CSS'),
        ('sql', 'SQL'),
        ('react', 'React'),
        ('django', 'Django'),
        ('node', 'Node.js'),
        ('ml', 'Machine Learning'),
        ('ai', 'Artificial Intelligence'),
    ]

    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='learningimages/')
    date = models.DateTimeField(default=timezone.now)
    type = models.CharField(max_length=10, choices=LEARNING_TYPES_CHOICES)
    description = models.TextField(default='')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    instructor = models.CharField(max_length=100, default='Admin')
    duration = models.CharField(max_length=20, default='10 hours')
    level = models.CharField(max_length=20, default='Beginner')
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.5)
    students_enrolled = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    # reviews - accessed via reviews related_name from CourseReview
    # enrollments - accessed via enrollments related_name from CourseEnrollment
    
    def __str__(self):
        return self.name
    
    
# One-to-Many relationship example
class CourseReview(models.Model):
    """One-to-Many: One course can have many reviews"""
    course = models.ForeignKey(CharVarity, on_delete=models.CASCADE, related_name='reviews')
    review = models.TextField()
    rating = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f'{self.user.username} rated {self.course.name} {self.rating} stars'
    
    
# Many-to-Many relationship example
class CourseEnrollment(models.Model):
    """Many-to-Many: Users can enroll in multiple courses, courses can have multiple users"""
    name = models.CharField(max_length=50)
    courses = models.ManyToManyField(CharVarity, related_name='enrollments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f'{self.user.username} enrolled in {self.name}'


# One-to-One relationship example
class InstructorProfile(models.Model):
    """One-to-One: Extends the User model with instructor-specific information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='instructor_profile')
    bio = models.TextField()
    expertise = models.CharField(max_length=100)
    years_of_experience = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f'Instructor: {self.user.username}'

# 
# Self-referential relationship example
# class Category(models.Model):
    # """Self relationship: Categories can have parent categories"""
    # name = models.CharField(max_length=50)
    # parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')
    # 
    # def __str__(self):
        # return self.name
# 
# 
# ManyToMany with through model example
# class Prerequisites(models.Model):
    # """Many-to-Many with a custom through model: Allows adding metadata to the relationship"""
    # basic_course = models.ForeignKey(CharVarity, on_delete=models.CASCADE, related_name='advanced_courses')
    # advanced_course = models.ForeignKey(CharVarity, on_delete=models.CASCADE, related_name='prerequisite_courses')
    # required = models.BooleanField(default=True)  # Is this prerequisite required or recommended?
    # 
    # def __str__(self):
        # return f'{self.basic_course.name} is prerequisite for {self.advanced_course.name}'
# 

# Generic Foreign Key example
# class Tag(models.Model):
    # """Generic relationship: Tags can be related to any model (courses, reviews, etc.)"""
    # name = models.CharField(max_length=50)
    # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # object_id = models.PositiveIntegerField()
    # content_object = GenericForeignKey('content_type', 'object_id')
    
    def __str__(self):
        return self.name


 
    

