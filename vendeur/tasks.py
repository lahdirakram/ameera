from django.utils.crypto import get_random_string
from .models import test
import string
from celery import shared_task

@shared_task
def create_random(total):
    for i in range(total):
        bb = 'user_{}'.format(get_random_string(10, string.ascii_letters))
        test.objects.create(aa=bb)
        
    return '{} random users created with success!'.format(total)
