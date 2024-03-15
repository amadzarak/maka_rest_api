from django.db import models

# Create your models here.
class User(models.Model):
    uid = models.CharField(max_length=100, primary_key=True)
    created_at = models.DateTimeField
    credits = models.IntegerField
    fcmTokens = models.CharField(null=True)
    recieve_promotions = models.CharField(null=True)

    
class Profile(models.Model):
    user= models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    interesting = models.CharField()
    birthday = models.DateField(null=True)
    gender = models.TextField(null=True)
    nickName = models.CharField()
    occupation = models.CharField()
    orientation = models.CharField()
    relationship_status = models.CharField()
    active = models.BooleanField(null=True, default=True)
    

class GuestContacts(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.SET_NULL)
    phone = models.CharField(null=True)
    email = models.CharField(null=True)
    facebook = models.CharField(null=True)
    instagram = models.CharField(null=True)
    x = models.CharField(null=True)
    tiktok = models.CharField(null=True)
    linkedin = models.CharField(null=True)
    snapchat =models.CharField(null=True)
    zip_code = models.IntegerField(null=True) 

class ConversationStarters(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField()

class Address(models.Model):
    address_line_1 = models.TextField()
    address_line_2 = models.TextField()
    city = models.TextField()
    state = models.TextField()
    zip = models.TextField()


class PointOfContact(models.Model):
    first_name = models.TextField()
    middle_name = models.TextField()
    last_name = models.TextField()
    phone = models.TextField()
    email = models.TextField()
    

class Venue(models.Model):
    address = models.ForeignKey(Address, on_delete=models.DO_NOTHING)
    venue_name = models.TextField()
    owner = models.TextField()
    point_of_contact = models.ManyToManyField(PointOfContact)

class EventType(models.Model):
    name = models.TextField()
    description = models.TextField()

class Event(models.Model):
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    require_tickets = models.BooleanField()
    password_protected = models.BooleanField()
    visibility = models.CharField(max_length=200, null=True)
    cost = models.FloatField()
    type = models.ForeignKey(EventType, null=True, on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, null=True, on_delete=models.CASCADE)

class EventDate(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True)
    is_multi_day = models.BooleanField()
    start_time = models.TimeField()
    end_time = models.TimeField()

class EventUser(models.Model):
    ROLES = (
        ('H', 'Host'),
        ('C', 'Creator'),
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=1, choices=ROLES)

class EventCheckIn(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    check_in_time = models.DateTimeField()
    guest_type = models.CharField(max_length=200)
    is_host = models.BooleanField()

class Transaction(models.Model):
    transaction_time = models.TimeField()
    transaction_date = models.DateField()
    transaction_type = models.TextField() #TextChoices? Include Free, Compensated, Won, Paid
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

class UserInteraction(models.Model):
    target = models.ForeignKey(User, on_delete=models.CASCADE, related_name="target")
    actor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="actor")
    interaction_type = models.TextField()
    interaction_time = models.DateTimeField()
    event = models.ForeignKey(Event, on_delete=models.DO_NOTHING)

class Ticket(models.Model):
    #For ticket endpoints i suppose there can be multiple methods of acquiring the users information to pass into this field
    # Get user by phone etc etc.
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    event = models.ForeignKey(Event, on_delete=models.DO_NOTHING)