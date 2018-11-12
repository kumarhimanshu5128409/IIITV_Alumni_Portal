from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from cities_light.models import City, Country, Region


class Alumni(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(
        max_length=30,
        validators=[
            RegexValidator(r'^[(A-Z)|(a-z)|(\s)|(\-)]+$', ),
        ],
    )
    last_name = models.CharField(
        max_length=30,
        validators=[
            RegexValidator(r'^[(A-Z)|(a-z)|(\s)|(\-)]+$', ),
        ],
    )
    permanent_address = models.CharField(
        max_length=700,
        validators=[
            RegexValidator(r'^[(A-Z)|(a-z)|(0-9)|(\s)|(\-)|(\.)|(,)|(\:)]+$', ),
        ],
    )
    current_city = models.ForeignKey(City, null=True, blank=True, on_delete='SET_NULL')
    current_state = models.ForeignKey(Region, null=True, blank=True, on_delete='SET_NULL')
    current_country = models.ForeignKey(Country, null=True, blank=True, on_delete='SET_NULL')
    phone_number = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                r'^\s*(?:\+?(\d{1,3}))?([-. (]*(\d{3})[-. )]*)?'
                r'((\d{3})[-. ]*(\d{2,4})(?:[-.x ]*(\d+))?)\s*$',
                message="Please enter a valid phone number",
            ),
        ],
    )
    # EmailField automatically checks if email address is a valid format
    email = models.EmailField(max_length=45, unique=True)
    links = models.TextField(
        blank=True,
        validators=[
            RegexValidator(
                r'^(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+'
                r'[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+'
                r'[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))'
                r'[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9]\.[^\s]{2,})+$',
            ),
        ],
    )
    about = models.TextField(
        blank=True,
        validators=[
            RegexValidator(r'^[(A-Z)|(a-z)|(0-9)|(\s)|(\.)|(,)|(\-)|(!)]+$', ),
        ],
    )
    area_of_expertise = models.TextField(
        blank=True,
        validators=[
            RegexValidator(r'^[(A-Z)|(a-z)|(0-9)|(\s)|(\.)|(,)|(\-)|(!)]+$', ),
        ],
    )
    profile_pic = models.ImageField(blank=True, default='alumni/default_profile_pic.png', upload_to='alumni')

    user = models.OneToOneField(User, on_delete='CASCADE')

    def __str__(self):
        return '{0} {1}'.format(self.first_name, self.last_name)

