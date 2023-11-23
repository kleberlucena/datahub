import logging

from django.core import files

from base.helpers import helpers_images
from apps.portal import models, services


# Get an instance of a logger
logger = logging.getLogger(__name__)


def update_military_entity(military, entity_uuid):
    status = False
    try:
        if entity_uuid:
            entity = models.Entity.objects.get(uuid_portal=entity_uuid)
            military.entity = entity
        else:
            military.entity = None
        status = True
    except Exception as e:
        military.entity = None
        logger.error(f'[Military - helpers] update_military_entity - {e}')
    finally:
        military.save()
        return status
    

def update_military_image(military, image_url):
    status = False
    
    image_path = None
    if image_url:
        image_path, _ = services.get_enjoyer_image_file(image_url)
            
    try:
        if military.image:
            helpers_images.delete_image_with_variations(military, "image")
        military.image.save("{}.jpg".format(military.uuid_portal), files.File(open(image_path, 'rb')))
        status = True
    except Exception as e:
        military.image = None
        military.save()
        logger.error(f'[Military - helpers] update_military_image - {e}')
    finally:
        return status

def get_rank_military(self, military_id):
    try:
        rank = models.Military.objects.get(id=military_id).promotion.last().rank
    except:
        rank = ""
    finally: 
        return rank
    

def update_genders_entity(entity, gender_uuids):
    status = False
    try:
        genders = models.Gender.objects.filter(uuid_portal__in=gender_uuids)
        status = True
    except Exception as e:
        genders = []
        logger.error(f'[Entity - helpers] update_genders_entity --> Obs: As categorias foram removidas! - {e}')
    finally:
        entity.gender.set(genders)
        return status


def update_organizations_entity(entity, organization_uuid):
    status = False
    try:
        if organization_uuid:
            entity_organization = models.OrganizationalHierarchy.objects.get(uuid_portal=organization_uuid)
            entity.organization = entity_organization
        else:
            entity.organization = None
        status = True
    except Exception as e:
        entity.organization = None
        logger.error(f'[Entity - helpers] update_organizations_entit on entity: {entity} and organization_uuid: {organization_uuid} - {e}')
    finally:
        entity.save()
        return status
    

def set_father_entity(entity, father_uuid):
    try:
        if father_uuid:
            father_entity = models.Entity.objects.get(uuid_portal=father_uuid)
            entity.father = father_entity
        else:
            entity.father = None
    except Exception as e:
        entity.father = None
        logger.error(f'[Entity - helpers] set_father_entity - {e}')
    finally:
        entity.save()
