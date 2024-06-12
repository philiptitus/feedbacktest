import os
import django

# Setup Django environment
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yourproject.settings')  # replace 'yourproject' with the name of your Django project
# django.setup()

from feedbackhub.models import Category  # adjust the import according to your app name

# List of realistic categories
categories = [
    "User Interface", "Performance", "Security", "Usability", "Customer Support", 
    "Documentation", "Features", "Bug Reports", "Compatibility", "Accessibility", 
    "Design", "Navigation", "Responsiveness", "Error Handling", "Notifications", 
    "Account Management", "Payment System", "Integrations", "Data Privacy", 
    "Onboarding", "Content Quality", "Mobile Experience", "Search Functionality", 
    "Updates and Patches", "Customization", "Reliability", "Speed", "User Experience", 
    "Technical Support", "Feedback Mechanism"
]

# Create categories in the database
for name in categories:
    Category.objects.create(name=name)

print("30 real-life categories created successfully.")
