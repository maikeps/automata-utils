UFSC
CTC - INE


Douglas Martins - 13104674
Maike de Paula Santos - 13100763


02/10/2015


Automaton
determinize - determiniza o automato;
generate_grammar - gera uma gramática a partir do automato;
generate_regular_expression - gera uma expressão regular a partir do automato.
￼￼
Grammar
generate_automaton - gera um automato a partir da gramática;


RegularExpression
generate_automaton - gera um automato a partir da expressão regular.


Requisitos:
É necessário ter python3 instalado no computador.


Como executar o programa:
Na linha de comando do terminal execute ./main.py, a partir de então você pode carregar um arquivo, que pode ser um automato, uma gramática ou uma expressão regular, usando o comando load <pasta/nomeDoArquivo>.


Com o arquivo carregado você pode converter ele. 


São aceita as seguintes conversões:
NOME         |         ENTRADA         ->         SAIDA
-------------------------------------------------------------------------------
deterministic         |        AFND                 ->         AFD
grammar        |        AFD                 ->        GRAMATICA
re                 |        AFD                 ->        ER
automaton        |        GRAMATICA         ->         AFD
automaton        |        ER                 ->         AFD


Conversões são feitas pelo comando convert <NOME>, elas são feitas da variavel current para a conversion. Ao fazer uma conversão, você pode vê-la com o comando print conversion, ou então salvar, save conversion <pastaDestino/nomeDoArquivo>.
Você também pode jogar o valor de conversion em current, com o comando refresh.