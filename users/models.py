from django.db import models
from django.contrib.auth.models import User


class Practice(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="default.png", upload_to="profile_pics")
    f_psychology = models.DecimalField(
        default=0.0, max_digits=7, decimal_places=2
    )
    f_prepregnancy = models.DecimalField(
        default=0.5, max_digits=7, decimal_places=2
    )
    f_research = models.DecimalField(
        default=0.0, max_digits=7, decimal_places=2
    )
    f_placenta = models.DecimalField(
        default=0.9, max_digits=7, decimal_places=1
    )
    f_medication = models.DecimalField(
        default=0.7, max_digits=7, decimal_places=2
    )
    f_fetus = models.DecimalField(default=0.3, max_digits=7, decimal_places=2)
    f_communication = models.DecimalField(
        default=0.7, max_digits=7, decimal_places=2
    )
    f_risks = models.DecimalField(default=0.9, max_digits=7, decimal_places=2)
    f_breastfeed = models.DecimalField(
        default=0.3, max_digits=7, decimal_places=2
    )
    f_bleeding = models.DecimalField(
        default=0.6, max_digits=7, decimal_places=2
    )
    f_tools = models.DecimalField(default=0.2, max_digits=7, decimal_places=2)

    def __str__(self):
        return f"{self.user.username}'s Practice Content"
