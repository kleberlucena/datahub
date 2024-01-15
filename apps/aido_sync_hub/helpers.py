import logging

from apps.portal import models as portal_models
from apps.portal import helpers as portal_helpers


# Get an instance of a logger
logger = logging.getLogger(__name__)


def sync_entity(model_data):
    message_response = {}
    
    entity = portal_models.Entity.objects.filter(name=model_data['name']).first()
    
    if not entity:
        entity, created = portal_models.Entity.objects.get_or_create(uuid_portal=model_data['uuid_portal'])        
    else: 
        entity.uuid_portal = model_data['uuid_portal']
    
    entity.name = model_data['name']
    entity.active = model_data['active']
    entity.child_exists = model_data['child_exists']
    entity.save()
    
    genders = model_data['gender']
    organizations = model_data['organization']
    
    entity.dad = portal_helpers.set_father_entity(entity, model_data['dad'])
    gender_response = portal_helpers.update_genders_entity(entity, genders)
    organization_response = portal_helpers.update_organizations_entity(entity, organizations)
    
    if gender_response and organization_response:
        logger.info('Sync Entity successfully updated')
        message_response["status"] = "success"
        message_response["completed"] = True
    else:
        message_response["completed"] = False
        if not gender_response:
            message_response["status"] = "fail"
            message_response["error"] = "Entity-related gender model was not correctly related"
        if not organization_response:
            message_response["status"] = "fail"
            message_response["error"] = "Organization model related to Entity was not listed correctly"
            
    return message_response


def sync_gender(model_data):
    message_response = {}
    
    gender, created = portal_models.Gender.objects.get_or_create(uuid_portal=model_data['uuid_portal'])
    
    gender.active = model_data['active']
    gender.name = model_data['name']
    gender.description = model_data['description']
    gender.save()
    
    message_response["status"] = "success"
    message_response["completed"] = True
            
    return message_response


def sync_organizational_hierarchy(model_data):
    message_response = {}
    
    organization_hierarchy, created = portal_models.OrganizationalHierarchy.objects.get_or_create(uuid_portal=model_data['uuid_portal'])
    
    organization_hierarchy.active = model_data['active']
    organization_hierarchy.name = model_data['name']
    organization_hierarchy.description = model_data['description']
    organization_hierarchy.save()
    
    message_response["status"] = "success"
    message_response["completed"] = True
            
    return message_response
            
            
def sync_military(model_data):
    message_response = {}
    
    military = portal_models.Military.objects.filter(
        cpf=model_data['cpf'], register=model_data['register']
    ).first()
    
    if not military:
        military, created = portal_models.Military.objects.get_or_create(uuid_portal=model_data['uuid_portal'])
    else: 
        military.uuid_portal = model_data['uuid_portal']
        
    military.active = model_data['active']                
    military.rank = model_data['rank']
    military.name = model_data['name']
    military.nickname = model_data['nickname']
    military.admission_date = model_data['admission_date']
    military.birthdate = model_data['birthdate']
    military.register = model_data['register']
    military.activity_status = model_data['activity_status']
    military.cpf = model_data['cpf']
    military.genre = model_data['genre']
    military.email = model_data['email']
    military.father = model_data['father']
    military.mather = model_data['mather']
    military.place_of_birth = model_data['place_of_birth']
    military.marital_status = model_data['marital_status']
    military.phone = model_data['phone']
    military.address = model_data['address']
    military.number = model_data['number']
    military.complement = model_data['complement']
    military.district = model_data['district']
    military.city = model_data['city']
    military.state = model_data['state']
    military.zipcode = model_data['zipcode']
    military.office = model_data['office']
    military.military_identity = model_data['military_identity']
    military.cnh = model_data['cnh']
    military.rg = model_data['rg']
    military.orgao_expeditor_rg = model_data['orgao_expeditor_rg']
    
    military.save()
    
    entity_response = portal_helpers.update_military_entity(military, model_data['entity'])
    image_response = portal_helpers.update_military_image(military, model_data['image'])
        
    if entity_response and image_response:
        logger.info('Sync military successfully updated')
        message_response["status"] = "success"
        message_response["completed"] = True
    else:
        message_response["completed"] = False
        if not entity_response:
            message_response["status"] = "fail"
            message_response["error"] = "Entity-related military model was not correctly related"
        if not image_response:
            message_response["status"] = "fail"
            message_response["error"] = "Image from military was not listed correctly"
    
    return message_response


def sync_enjoyer(model_data):
    message_response = {}
    
    enjoyer = portal_models.Enjoyer.objects.filter(username=model_data['username']).first()
        
    if not enjoyer:
        enjoyer, created = portal_models.Enjoyer.objects.get_or_create(
            uuid_portal=model_data['uuid_portal'],
            username=model_data['username'],
            first_name=model_data['first_name'],
            last_name=model_data['last_name'],
            email=model_data['email']
        )

    else: 
        enjoyer.uuid_portal = model_data['uuid_portal']
    
    enjoyer.active = model_data['active']
    enjoyer.username = model_data['username']
    enjoyer.first_name = model_data['first_name']
    enjoyer.last_name = model_data['last_name']
    enjoyer.full_name = model_data['full_name']
    enjoyer.email = model_data['email']
    enjoyer.uuid_portal = model_data['uuid_portal']
    enjoyer.birthdate = model_data['birthdate']
    enjoyer.phone = model_data['phone']
    
    enjoyer.save()
    
    entity_response = portal_helpers.update_enjoyer_entity(enjoyer, model_data['uuid_entity'])
    
    # TODO: Fazer os ajustes abaixo
    # enjoyer.function_ids 
    # enjoyer.situation_ids
    
    
    message_response["status"] = "success"
    message_response["completed"] = True
            
    return message_response
