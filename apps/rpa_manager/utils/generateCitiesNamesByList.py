
from apps.rpa_manager.models import CidadesPB

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
    
