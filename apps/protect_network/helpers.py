from . import models


def update_all_spots():
    # Obtem todos os spots em lotes
    spots = models.Spot.objects.iterator()
    # Itera sobre cada spot
    for spot in spots:
        # Atualiza o update_score para cada spot
        spot._update_score()