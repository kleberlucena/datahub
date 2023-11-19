import os
import logging


# Get an instance of a logger
logger = logging.getLogger(__name__)


def delete_image_with_variations(instance, field_name="image"):
    """
    Delete the main image and its variations.
    
    Args:
        instance: The Django model instance containing the image field.
        field_name (str): The name of the image field to be processed. Defaults to "image".
    """
    try:
        # Obter a imagem do modelo
        image_field = getattr(instance, field_name)
        
        if not image_field:
            return
        
        storage = image_field.storage
        image_name_without_extension = os.path.splitext(image_field.name)[0]
        
        # Variações para deletar
        variations = [
            'large',
            'medium',
            'thumbnail'
        ]

        # Deletar a imagem principal
        if storage.exists(image_field.name):
            storage.delete(image_field.name)

        # Deletar variações
        for variation in variations:
            variation_name = f"{image_name_without_extension}.{variation}.jpg"
            if storage.exists(variation_name):
                storage.delete(variation_name)
    except Exception as e:
        logger.error(f'[Base] in helpers_image - error on method delete_image_with_variations: {e}')
        
# Uso:
# delete_image_with_variations(enjoyer_instance)
