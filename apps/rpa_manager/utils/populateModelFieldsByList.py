
from apps.rpa_manager.models import CidadesPB, NaturezaDeVoo, Entidades


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


"""The functions below are used to populate the models attributes, if you
need to insert values to these models, call the package inside a views.py file
and call one of these functions inside a view funcition. The lists above must be 
in the view file also and be passed to the functions by parameters.
"""

def generateCitiesByList(listOfCities = []):
    """ Only call this function if you have several new cities to add in the list.
        Preferably user django admin to add new cities.
    """
    CidadesPB.objects.all().delete()
    count = 0
    if CidadesPB.objects.all().count() >= 223:
        return
    else:
        for index in range(len(listOfCities)):
            count += 1
            CidadesPB.objects.create(cidades_pb=listOfCities[index])
        
    print(f"List of cities updated: {count}")
    
def generateNatureOfFlighs(list_of_natures = []):
    NaturezaDeVoo.objects.all().delete()
    
    for index in range(len(list_of_natures)):
        NaturezaDeVoo.objects.create(natureza=list_of_natures[index])
        
def generateEntitiesOfFlighs(list_of_entities = []):
    Entidades.objects.all().delete()
    
    for index in range(len(list_of_entities)):
        Entidades.objects.create(natureza=list_of_entities[index])
        