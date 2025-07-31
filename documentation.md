# ZPYRO — Manual da Linguagem (v0.1 Chaos Edition)

# 📦 VARIÁVEIS

# ✅ Declaração
As variáveis são declaradas com a palavra-chave let, da seguinte forma:

bash
Copy
Edit
let nome_variavel = valor;
ZPyro suporta 4 tipos básicos:

Inteiro (Integer)

Decimal (Float)

Texto (String)

Booleano (Bool)

# 🔄 Sobrescrever
Você pode alterar o valor de uma variável já existente assim:

ini
Copy
Edit
nome_variavel = novo_valor;
⚠️ Não esqueça:
⚠️ Declarar uma variável que já existe gera erro

⚠️ Sobrescrever uma variável que não existe também gera erro

⚠️ Toda instrução deve terminar com ;

# 🖨️ SAÍDA
A saída é feita com o comando:

exit valor;
Você pode imprimir diretamente:

Números com operações: exit 10 + 5 * 2;

Textos concatenados: exit "Olá, " + nome;

Variáveis: exit resultado;

# ⚠️ Não esqueça:
⚠️ Sempre finalize com ;

⚠️ Se usar variáveis, elas devem estar definidas

# 🧩 FUNÇÕES
As funções são definidas assim:

zpyro
Copy
Edit
def nome_funcao(arg1, arg2) {
    // corpo da função
}

# ⚠️ Atenção:
As funções estão em fase de reparo. O parser já reconhece corretamente a estrutura e os retornos (return valor;), mas a chamada da função ainda está temporariamente desativada para priorizar uma versão mais estável.

# 🔀 CONDICIONAIS (if, else)
Você pode usar lógica condicional assim:

zpyro
Copy
Edit
if (x == 10) {
    // instruções
} else {
    // instruções
}

# ⚠️ Ainda em fase de depuração.
A estrutura está pronta, mas está desativada por enquanto.


🧪 BUG CONHECIDO
# ⚠️ Importante:
Existe um problema atual em que, ao declarar uma segunda variável, o parser não encontra corretamente o token necessário para criar o nó.

Estamos cientes e trabalhando na correção.
Obrigado pela compreensão!

# 🚀 Próxima versão
A próxima geração da ZPyro vai ser:

Totalmente modular

Com estrutura orientada a objetos

Seguindo padrões consistentes

Com suporte a chamadas de função e escopos reais

