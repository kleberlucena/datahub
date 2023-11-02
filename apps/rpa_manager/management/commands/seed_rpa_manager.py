from django.core.management import call_command
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils.timezone import now
from apps.rpa_manager.models import *
from apps.portal.models import *

from django.contrib.auth.models import Group
from django.db import transaction

class Command(BaseCommand):
    help = 'Insert seed data'
    
    def create_groups():
        groups_to_create = [
            "profile:rpa_manager",
            "profile:rpa_view",
            "profile:rpa_basic",
            "profile:rpa_advanced",
        ]

        with transaction.atomic():
            for group_name in groups_to_create:
                group, created = Group.objects.get_or_create(name=group_name)
                if created:
                    print(f'Grupo "{group_name}" criado com sucesso.')
                else:
                    print(f'Grupo "{group_name}" já existe.')
                    
    create_groups()

    def handle(self, *args, **options):
        
        entities = [
            'PMPB', 'PCPB', 'CBMPB', 'CPRM', 'CPR-I', 'CPR-II', 'CPR-III', 'SUPLAN', 
            'TJPB', 'MPPB', 'PC', 'IPC', 'SUDEMA', 'AESA', 'PF', 'DAL', 'CE', 'DSAS', 
            'CMG', 'QCG', '1º BPM', '2º BPM', '3º BPM', '4º BPM', '5º BPM', '6º BPM', 
            '7º BPM', '8º BPM', '9º BPM', '10º BPM', '11º BPM', '12º BPM', '13º BPM', 
            '14º BPM', '15º BPM', '1ª CIPM', '2ª CIPM', '3ª CIPM', '4ª CIPM', '5ª CIPM', 
            '6ª CIPM', '7ª CIPM', 'BEPTUR', 'COA', 'BOPE', 'BPAmb', 'BPTran', 'RPMont', 'Outra'
        ]

        natures_of_flights = [
            'Treinamento',
            'Policiamento ostensivo e investigativo',
            'Policiamento e vigilância em áreas de responsabilidade',
            'Ações de inteligência',
            'Apoio ao cumprimento de mandado judicial',
            'Controle de tumultos; distúrbios e motins',
            'Escoltas de dignitários, presos, valores e cargas',
            'Operações de busca terrestre e aquática',
            'Controle de tráfego rodoviário, ferroviário e urbano',
            'Aerolevantamento',
            'Solenidades e eventos',
            'Marketing institucional',
            'Levantamento operacional',
            'Desapropriação/reintegração',
            'Patrulhamento preventivo',
            'Patrulhamento de buscas',
            'Solenidades',
            'Festas populares',
            'Manifestações/movimentos',
            'Festas Juninas',
            'Controle de tráfego rodoviário e ferroviário',
            'Prevenção e combate a incêndio',
            'Patrulhamento urbano, rural, ambiental, litorâneo e de fronteiras',
            'Repressão ao contrabando e descaminho',
            'Gestão e execução de atividades de fiscalização',
            'Outra'
        ]

        cities_pb = [
            'Água Branca', 'Aguiar', 'Alagoa Grande', 'Alagoa Nova', 'Alagoinha', 'Alcantil', 'Algodão de Jandaíra', 
            'Alhandra', 'Amparo', 'Aparecida', 'Araçagi', 'Arara', 'Araruna', 'Areia', 'Areia de Baraúnas', 'Areial', 
            'Aroeiras', 'Assunção', 'Baía da Traição', 'Bananeiras', 'Baraúna', 'Barra de Santa Rosa', 'Barra de Santana', 
            'Barra de São Miguel', 'Bayeux', 'Belém', 'Belém do Brejo do Cruz', 'Bernardino Batista', 'Boa Ventura', 'Boa Vista', 
            'Bom Jesus', 'Bom Sucesso', 'Bonito de Santa Fé', 'Boqueirão', 'Borborema', 'Brejo do Cruz', 'Brejo dos Santos', 
            'Caaporã', 'Cabaceiras', 'Cabedelo', 'Cachoeira dos Índios', 'Cacimba de Areia', 'Cacimba de Dentro', 'Cacimbas', 
            'Caiçara', 'Cajazeiras', 'Cajazeirinhas', 'Caldas Brandão', 'Camalaú', 'Campina Grande', 'Capim', 'Caraúbas', 
            'Carrapateira', 'Casserengue', 'Catingueira', 'Catolé do Rocha', 'Caturité', 'Conceição', 'Condado', 'Conde', 
            'Congo', 'Coremas', 'Coxixola', 'Cruz do Espírito Santo', 'Cubati', 'Cuité', 'Cuité de Mamanguape', 'Cuitegi', 
            'Curral de Cima', 'Curral Velho', 'Damião', 'Desterro', 'Diamante', 'Dona Inês', 'Duas Estradas', 'Emas', 'Esperança', 
            'Fagundes', 'Frei Martinho', 'Gado Bravo', 'Guarabira', 'Gurinhém', 'Gurjão', 'Ibiara', 'Igaracy', 'Imaculada', 'Ingá', 
            'Itabaiana', 'Itaporanga', 'Itapororoca', 'Itatuba', 'Jacaraú', 'Jericó', 'João Pessoa', 'Joca Claudino (ex-Santarém)', 
            'Juarez Távora', 'Juazeirinho', 'Junco do Seridó', 'Juripiranga', 'Juru', 'Lagoa', 'Lagoa de Dentro', 'Lagoa Seca', 
            'Lastro', 'Livramento', 'Logradouro', 'Lucena', 'Mãe d\'Água', 'Malta', 'Mamanguape', 'Manaíra', 'Marcação', 'Mari', 
            'Marizópolis', 'Massaranduba', 'Mataraca', 'Matinhas', 'Mato Grosso', 'Matureia', 'Mogeiro', 'Montadas', 'Monte Horebe', 
            'Monteiro', 'Mulungu', 'Natuba', 'Nazarezinho', 'Nova Floresta', 'Nova Olinda', 'Nova Palmeira', 'Olho d\'Água', 
            'Olivedos', 'Ouro Velho', 'Parari', 'Passagem', 'Patos', 'Paulista', 'Pedra Branca', 'Pedra Lavrada', 'Pedras de Fogo', 
            'Pedro Régis', 'Piancó', 'Picuí', 'Pilar', 'Pilões', 'Pilõezinhos', 'Pirpirituba', 'Pitimbu', 'Pocinhos', 'Poço Dantas', 
            'Poço de José de Moura', 'Pombal', 'Prata', 'Princesa Isabel', 'Puxinanã', 'Queimadas', 'Quixaba', 'Remígio', 'Riachão', 
            'Riachão do Bacamarte', 'Riachão do Poço', 'Riacho de Santo Antônio', 'Riacho dos Cavalos', 'Rio Tinto', 'Salgadinho', 
            'Salgado de São Félix', 'Santa Cecília', 'Santa Cruz', 'Santa Helena', 'Santa Inês', 'Santa Luzia', 'Santa Rita', 
            'Santa Terezinha', 'Santana de Mangueira', 'Santana dos Garrotes', 'Santo André', 'São Bentinho', 'São Bento', 
            'São Domingos', 'São Domingos do Cariri', 'São Francisco', 'São João do Cariri', 'São João do Rio do Peixe', 
            'São João do Tigre', 'São José da Lagoa Tapada', 'São José de Caiana', 'São José de Espinharas', 'São José de Piranhas', 
            'São José de Princesa', 'São José do Bonfim', 'São José do Brejo do Cruz', 'São José do Sabugi', 'São José dos Cordeiros', 
            'São José dos Ramos', 'São Mamede', 'São Miguel de Taipu', 'São Sebastião de Lagoa de Roça', 'São Sebastião do Umbuzeiro', 
            'São Vicente do Seridó', 'Sapé', 'Serra Branca', 'Serra da Raiz', 'Serra Grande', 'Serra Redonda', 'Serraria', 'Sertãozinho', 
            'Sobrado', 'Solânea', 'Soledade', 'Sossêgo', 'Sousa', 'Sumé', 'Tacima (ex-Campo de Santana)', 'Taperoá', 'Tavares', 
            'Teixeira', 'Tenório', 'Triunfo', 'Uiraúna', 'Umbuzeiro', 'Várzea', 'Vieirópolis', 'Vista Serrana', 'Zabelê'
        ]
        
        def generateEntitiesOfFlighs(list_of_entities = []):
            if Entities.objects.count() == 0:
                for index in range(len(list_of_entities)):
                    Entities.objects.create(entity=list_of_entities[index])
        
        def generateCitiesByList(listOfCities = []):
            CitiesPB.objects.all().delete()
            count = 0
            if CitiesPB.objects.all().count() >= 223:
                return
            else:
                for index in range(len(listOfCities)):
                    count += 1
                    CitiesPB.objects.create(cities_pb=listOfCities[index])
                
    
        def generateNatureOfFlighs(list_of_natures = []):
            if FlightNature.objects.count() == 0:
                for index in range(len(list_of_natures)):
                    FlightNature.objects.create(nature=list_of_natures[index])

        def generateAircrafts():
            aircrafts = Aircraft.objects.count()
            
            if aircrafts == 0:
                aeronave1 = Aircraft.objects.create(
                    prefix="PP-001",
                    model="Mavic Enterprise",
                    brand="DJI",
                    location=CitiesPB.objects.get(cities_pb='João Pessoa'),
                    in_use=False,
                )
                
                aeronave2 = Aircraft.objects.create(
                    prefix="PP-002",
                    model="Phantom Pro",
                    brand="DJI",
                    location=CitiesPB.objects.get(cities_pb='Campina Grande'),
                    in_use=False,
                )
        
        def generateMilitaries():
            if Entity.objects.count() == 0:
                entity = Entity.objects.create(
                    name="PMPB",
                    father='Estado',
                    child_exists=False,
                    category=1,
                    hierarchy=9,
                    code="000"
                    )
            
            if Military.objects.count() == 0:
                military1 = Military.objects.create(
                    name="João Alves da Silva",
                    entity=Entity.objects.get(name="PMPB"),
                    nickname="Cb João",
                    admission_date="2000-10-26",  
                    birthdate="1980-01-01",  
                    register="1234567",  
                    activity_status="Ativo",  
                    cpf="879.926.080-89",  
                    genre="M",  
                    email="ze@example.com",  
                    father="Pai do Zé", 
                    mather="Mãe do Zé",  
                    place_of_birth="Cidade de Exemplo",  
                    marital_status="Solteiro(a)",  
                    phone="(83) 1234-5678",  
                    address="Rua Exemplo",  
                    number="123",  
                    complement="Apto 456",  
                    district="Bairro Exemplo",  
                    city="Cidade Exemplo",  
                    state="PB",  
                    zipcode="58000-000",  
                )
                
                military2 = Military.objects.create(
                    name="Henrique Elias",
                    entity=Entity.objects.get(name="PMPB"),
                    nickname="Sd Henrique",
                    admission_date="1980-10-26",  
                    birthdate="1980-01-01",  
                    register="1412589",  
                    activity_status="Ativo",  
                    cpf="070.269.390-17",  
                    genre="M",  
                    email="roro@example.com",  
                    father="Pai do Henrique", 
                    mather="Mãe do Henrique",  
                    place_of_birth="Cidade de Exemplo",  
                    marital_status="Solteiro(a)",  
                    phone="(11) 1234-7856",  
                    address="Rua Exemplo",  
                    number="123",  
                    complement="Apto 456",  
                    district="Bairro Exemplo",  
                    city="Cidade Exemplo",  
                    state="PB",  
                    zipcode="58000-000",  
                )
                
                military3 = Military.objects.create(
                    name="Fransisco Silva",
                    entity=Entity.objects.get(name="PMPB"),
                    nickname="Sgt Fransisco",
                    admission_date="1980-10-26",  
                    birthdate="1980-01-01",  
                    register="7412889",  
                    activity_status="Ativo",  
                    cpf="786.589.280-20",  
                    genre="M",  
                    email="roro@example.com",  
                    father="Pai do Fransisco", 
                    mather="Mãe do Fransisco",  
                    place_of_birth="Cidade de Exemplo",  
                    marital_status="Solteiro(a)",  
                    phone="(11) 1234-7856",  
                    address="Rua Exemplo",  
                    number="123",  
                    complement="Apto 456",  
                    district="Bairro Exemplo",  
                    city="Cidade Exemplo",  
                    state="PB",  
                    zipcode="58000-000",  
                )
                military4 = Military.objects.create(
                    name="Daniel Caldas",
                    entity=Entity.objects.get(name="PMPB"),
                    nickname="Cb Daniel",
                    admission_date="1980-10-26",  
                    birthdate="1980-01-01",  
                    register="7412689",  
                    activity_status="Ativo",  
                    cpf="300.700.030-09",  
                    genre="M",  
                    email="roro@example.com",  
                    father="Pai do Daniel", 
                    mather="Mãe do Daniel",  
                    place_of_birth="Cidade de Exemplo",  
                    marital_status="Solteiro(a)",  
                    phone="(11) 1234-7856",  
                    address="Rua Exemplo",  
                    number="123",  
                    complement="Apto 456",  
                    district="Bairro Exemplo",  
                    city="Cidade Exemplo",  
                    state="PB",  
                    zipcode="58000-000",  
                )

        
        def generateRiskAssessementData():
            if Situation.objects.count() == 0:
                situation1 = Situation.objects.create(
                    situation="Perda de Link"
                )
                situation2 = Situation.objects.create(
                    situation="Ventos de X nós"
                )
                situation3 = Situation.objects.create(
                    situation="Aeronaves Tripuladas"
            )
            
            probabilities = ["1", "2", "3", "4", "5"]
            severeties = ["A", "B", "C", "D", "E",]
            
            noProbabilities = Probability.objects.count() == 0
            noSeverities = Severity.objects.count() == 0
            
            if noProbabilities and noSeverities:
                for probability in probabilities:
                    Probability.objects.create(
                        probability=probability
                    )

                for severity in severeties:
                    Severity.objects.create(
                        severity=severity
                    )

        def populateModelsFieldsByList():
            generateCitiesByList(cities_pb)
            generateEntitiesOfFlighs(entities)
            generateNatureOfFlighs(natures_of_flights)
            generateAircrafts()
            generateMilitaries()
            generateRiskAssessementData()
            
            print("As seeds foram implantadas com sucesso!")
            
        populateModelsFieldsByList()