# -*- coding: utf-8 -*-
from datetime import datetime
from .models import *

def getMatchs(entity):

	if entity.__class__.__name__ == "Pedido":
		MedicamentoDonado.objects.filter(medicamento=entity.medicamento)

