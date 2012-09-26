from django.db import models

class Sites (models.Model):
	""" A site is a logical representation of the physical location at which
	recording take place."""

	name = models.CharField (max_length = 200)
	location = models.CharField (max_length = 50)


	def __unicode__ (self):
		""" Simple name representation for sites """
		return self.name + ', ' + self.location


 	class Meta:
 		app_label= 'search'