from django.contrib import admin
from .models import CharVarity, CourseReview, CourseEnrollment, InstructorProfile

# Register your models here.

class CourseReviewAdmin(admin.TabularInline):
    model = CourseReview
    extra = 2
    
class CourseEnrollmentInline(admin.TabularInline):
    model = CourseEnrollment.courses.through
    extra = 1

class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'price')
    list_filter = ('type',)
    search_fields = ('name', 'description')
    inlines = [CourseReviewAdmin]

class CourseEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'date')
    exclude = ('courses',)

class InstructorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'expertise', 'years_of_experience')

# Register models with their admin classes
admin.site.register(CharVarity, CourseAdmin)
admin.site.register(CourseEnrollment, CourseEnrollmentAdmin)
admin.site.register(InstructorProfile, InstructorProfileAdmin)
# CourseReview is registered as an inline in CourseAdmin
