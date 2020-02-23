from django.db import models
from django.contrib.auth.models import User



class Practice(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField(default='default.jpg', upload_to='profile_pics')
	# features = models.TextField(default='{""Psychological Distress"": 0.0, ""Pre-Pregnancy"": 0.07317073170731707, ""Research"": 0.0, ""Retained Placenta"": 0.2926829268292683, ""Administer Medication"": 0.12195121951219512, ""Fetal"": 0.0975609756097561, ""Communication"": 0.0, ""Breastfeeding"": 0.0, ""Assess Risks"": 0.0, ""Post-Natal Complications: Bleeding"": 0.24390243902439024, ""Tool Knowledge"": 0.17073170731707318}')
	f_psychology = models.DecimalField(default=0.0, max_digits=7, decimal_places=2)
	f_prepregnancy = models.DecimalField(default=0.0, max_digits=7, decimal_places=2)
	f_research = models.DecimalField(default=0.0, max_digits=7, decimal_places=2)
	f_placenta = models.DecimalField(default=0.0, max_digits=7, decimal_places=1)
	f_medication = models.DecimalField(default=0.0, max_digits=7, decimal_places=2)
	f_fetus = models.DecimalField(default=0.0, max_digits=7, decimal_places=2)
	f_communication = models.DecimalField(default=0.0, max_digits=7, decimal_places=2)
	f_risks = models.DecimalField(default=0.0, max_digits=7, decimal_places=2)
	f_breastfeed = models.DecimalField(default=0.0, max_digits=7, decimal_places=2)
	f_bleeding = models.DecimalField(default=0.0, max_digits=7, decimal_places=2)
	f_tools = models.DecimalField(default=0.0, max_digits=7, decimal_places=2)


	# recommended_articles = models.

	# insert much more logic here for the practice scenario
	# add all the other fields we want


	def __str__(self):
		return f"{self.user.username}'s Practice Content"

