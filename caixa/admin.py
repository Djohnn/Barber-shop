from django.contrib import admin
from .models import Caixa, Desconto, Sangria

# Register your models here.
admin.site.register(Caixa)
admin.site.register(Sangria)
admin.site.register(Desconto)
