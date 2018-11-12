# standard library
from functools import wraps

# Django
from django.shortcuts import render

# account can only be created if both passwords match
def match_password(password1, password2):
    return password1 == password2

