from django.db import models
from django.template.defaultfilters import slugify

class Categoria(models.Model):
    titulo = models.CharField(max_length=40)

    def __str__(self):
        return self.titulo
    
class Produto(models.Model):
    nome = models.CharField(max_length=40, unique=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    quantidade = models.FloatField()
    preco_compra = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    slug = models.SlugField(unique=True, blank=True, null=True)


    def __str__(self) -> str:
        return self.nome
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)

        return super().save(*args, **kwargs)

    
    def gerar_desconto(self, desconto):
        return self.preco_venda - ((self.preco_venda * desconto) / 100)
    
    def lucro(self):
        lucro = self.preco_venda - self.preço_compra
        return (lucro * 100) / self.preço_compra
    

class Imagem(models.Model):
    imagem = models.ImageField(upload_to='imagem_produto/')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)