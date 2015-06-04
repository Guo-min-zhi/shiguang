from django.db import models
from users.models import User

# Create your models here.

class Shiguang(models.Model):
	"""docstring for Shiguang"""
	# name
	name = models.CharField(max_length=100)
	# description
	description = models.TextField(max_length=1000)
	# create time
	create_time = models.DateTimeField(auto_now_add=True)

	# start time
	start_time = models.DateTimeField(null=True, blank=True)
	# end time
	end_time = models.DateTimeField(null=True, blank=True)
	# tag one
	LIFE = 'LIFE'
	WORK = 'WORK'
	FIRST_LEVEL_TAG = (
		(LIFE, 'life'),
		(WORK, 'work'),
	)
	first_level_tag = models.CharField(max_length=100,choices=FIRST_LEVEL_TAG)
	# tag two

	# tag three

	# cover
	cover = models.ImageField(upload_to='covers')
	# user, foreign key
	user = models.ForeignKey(User)
