# Modelo de Entidades Organizacionais

## Objetivo dos atributos:

* entity_code
  * Código de origem dos sistemas de origem dos usuários, deve seguir o padrão adotado nesse sistema (<código do tipo>-<código da unidade>), por exemplo uma string no formato "0-1000";
  * O objetivo é viabilizar o cadastro de códigos de diferentes entidades sem choque de valores, além de viabilizar o correto cadastro de níveis através do campo entidade_pai.
  

* name
  * Nome de identificação da entidade;
  * Deve respeitar o nome de origem do sistema integrado.


* entity_father
  * Código da entidade pai;
  * Deve ser do tipo string;
  * O objetivo desse atributo é viabilizar os níveis hierárquicos das subunidades;
  * Deve ser cadastrado uma string em branco ("") no caso não existir nível superior.


* type
  * Deve classificar a origem da Unidade, planejamos dividir intenamente em 'Ostensivo' e 'Inteligência'. Se houver unidades de endidades externas, estas deverão ser com seu próprio tipo;
  * O objetivo desse choice é podem separar o código das unidades, viabilizar a inserção de outras corporações e manter organizada a distribuição de usuários.


* hierarchy
  * Deve indicar qual nível a organização está dentro da entidade cadastrada;
  * Tem um valor padrão 0 (não classificado), indicando a falta dessa análise;
  * O objetivo desse atributo é viabilizar o filtro de cadastros e estatísticas conforme o tipo de unidade e possíveis buscas recursivas para estatíticas maiores.
  

[Voltar a documentação inicial](./index.md)