from django.db import models

class noticias(models.Model):
    id = models.IntegerField(primary_key=True)
    titulo = models.TextField()
    link = models.TextField()
    body = models.TextField()
    
    
#    titulo = models.TextField(primary_key=True)
