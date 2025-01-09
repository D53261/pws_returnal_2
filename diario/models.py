from django.db import models

# Create your models here.
class Pessoa(models.Model):
    nome = models.CharField(max_length=100)
    foto = models.ImageField(upload_to='foto')
    user = models.ForeignKey('Usuario', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nome
    

class Diario(models.Model):
    titulo = models.CharField(max_length=100)
    tags = models.TextField()
    texto = models.TextField()
    user = models.ForeignKey('Usuario', on_delete=models.CASCADE, null=True, blank=True)
    pessoas = models.ManyToManyField(Pessoa, null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
    
    def get_tags(self):
        return self.tags.split(',') if self.tags else []
    
    def set_tags(self, list_tags, reset=False):

        if not reset:
            existing_tags = set(self.get_tags())
            list_tags = existing_tags.union(set(list_tags))

        self.tags = ','.join(list_tags)

class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    senha = models.CharField(max_length=100)

    def __str__(self):
        return self.nome