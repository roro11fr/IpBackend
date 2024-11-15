from django.db import models

# Create your models here.
class Profesor(models.Model):
    ProfesorID = models.AutoField(primary_key=True)
    Nume = models.CharField(max_length=100)
    Prenume = models.CharField(max_length=100)
    DataNasterii = models.DateField()
    Specializare = models.CharField(max_length=100)
    Email = models.EmailField(max_length=100)
    Telefon = models.CharField(max_length=15)
    DataAngajarii = models.DateField()

    def __str__(self):
        return f"{self.Nume} {self.Prenume}"
    

    class Meta:
        db_table = 'Profesor'  # Indică explicit numele tabelului deja existent

