from django.contrib import admin
from navigation.models import *
from importcsv.models import *

admin.site.register(PageRegistre)
admin.site.register(TransactionSoiree)
admin.site.register(TransactionAbonnement)
admin.site.register(BudgetSoiree)
admin.site.register(Abonnement)
admin.site.register(Recapitulatif)
admin.site.register(CreditRecapitulatif)
admin.site.register(DebitRecapitulatif)
admin.site.register(Credit)
admin.site.register(Billetterie)
admin.site.register(Debit)
admin.site.register(Soiree)
admin.site.register(SoireeVide)
admin.site.register(Representation)
admin.site.register(Animation)
admin.site.register(Personne)
admin.site.register(Piece)
admin.site.register(Role)
