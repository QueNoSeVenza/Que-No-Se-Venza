from django.core.management.base import BaseCommand, CommandError
from donaciones.models import *
from datetime import datetime, timezone, timedelta

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'


    def handle(self, *args, **options):

        now = datetime.now(timezone.utc)
        interval =   timedelta(days=30)

        for med in MedicamentoDonado.objects.filter(stock = "Reservado"):
            if now-med.fecha_creacion >= interval:
                print(med.medicamento.nombre," donado hace 3 minutos o mas")
                med.stock = "Disponible"
                med.save()
            else:
                print(med.medicamento.nombre," donado hace menos de 3 minutos")

        for med in MedicamentoDonado.objects.all():
            if med.isDull():
                med.stock = "Vencido"
                med.save()

        self.stdout.write(self.style.SUCCESS('Success'))
