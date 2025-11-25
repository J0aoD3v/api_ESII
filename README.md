# Documentação API - Teste de Caixa Preta

## Visão Geral

Esta API REST foi desenvolvida para demonstrar e validar técnicas de teste de caixa preta. Ela oferece quatro métodos diferentes que podem ser testados utilizando diversas estratégias de teste.

**URL Base:** `http://136.248.121.230/api.php`

**URL Alternativa (Local):** `http://localhost/api.php`

**Métodos HTTP Suportados:** GET, POST

**Formato de Resposta:** JSON

---

## 🚀 Configuração Rápida do Servidor Local

### Opção 1: PHP Manual (Recomendado)

1. Baixe PHP em https://windows.php.net/download/ (versão Thread Safe)
2. Extraia para `C:\php`
3. Adicione ao PATH do sistema
4. Execute: `php -S localhost:8000`

### Opção 2: XAMPP

1. Baixe em https://www.apachefriends.org/
2. Instale e inicie o Apache
3. Copie `api.php` para `C:\xampp\htdocs\`

### Opção 3: Chocolatey

```powershell
choco install php
php -S localhost:8000
```

### Opção 4: Docker

```powershell
docker run -d -p 8000:80 -v "${PWD}:/var/www/html" php:8.2-apache
```

**Após configurar**, atualize a URL no `test_api.py` para `http://localhost:8000/api.php`

---

## Estrutura de Resposta

Todas as respostas da API seguem o seguinte formato JSON:

```json
{
  "sucesso": true/false,
  "dados": {...},
  "mensagem": "Mensagem descritiva"
}
```

- **sucesso**: Booleano indicando se a operação foi bem-sucedida
- **dados**: Objeto contendo os dados retornados (ou null em caso de erro)
- **mensagem**: Mensagem descritiva sobre o resultado da operação

---

## Métodos Disponíveis

### 1. Calculadora de IMC

Calcula o Índice de Massa Corporal (IMC) e retorna a classificação correspondente.

**Endpoint:** `?metodo=calcular_imc`

**Parâmetros:**

- `peso` (float, obrigatório): Peso em quilogramas (deve ser > 0)
- `altura` (float, obrigatório): Altura em metros (deve ser > 0)

**Exemplo de Requisição:**

```
GET http://136.248.121.230/api.php?metodo=calcular_imc&peso=70&altura=1.75
```

**Exemplo de Resposta (Sucesso):**

```json
{
  "sucesso": true,
  "dados": {
    "imc": 22.86,
    "classificacao": "Peso normal"
  },
  "mensagem": "IMC calculado com sucesso"
}
```

**Classificações de IMC:**

- IMC < 18.5: Abaixo do peso
- 18.5 ≤ IMC < 25: Peso normal
- 25 ≤ IMC < 30: Sobrepeso
- 30 ≤ IMC < 35: Obesidade grau I
- 35 ≤ IMC < 40: Obesidade grau II
- IMC ≥ 40: Obesidade grau III

**Casos de Erro:**

- Peso ou altura menor ou igual a zero

---

### 2. Verificar Número Primo

Verifica se um número inteiro é primo.

**Endpoint:** `?metodo=verificar_primo`

**Parâmetros:**

- `numero` (int, obrigatório): Número inteiro a ser verificado

**Exemplo de Requisição:**

```
GET http://136.248.121.230/api.php?metodo=verificar_primo&numero=17
```

**Exemplo de Resposta (Sucesso):**

```json
{
  "sucesso": true,
  "dados": {
    "numero": 17,
    "primo": true
  },
  "mensagem": "O número é primo"
}
```

**Regras:**

- Números menores que 2 não são considerados primos
- O algoritmo verifica divisibilidade até a raiz quadrada do número

---

### 3. Gerar Sequência Fibonacci

Gera uma sequência de Fibonacci com a quantidade especificada de termos.

**Endpoint:** `?metodo=fibonacci`

**Parâmetros:**

- `quantidade` (int, opcional): Quantidade de números na sequência (padrão: 10)
  - Mínimo: 1
  - Máximo: 50

**Exemplo de Requisição:**

```
GET http://136.248.121.230/api.php?metodo=fibonacci&quantidade=8
```

**Exemplo de Resposta (Sucesso):**

```json
{
  "sucesso": true,
  "dados": {
    "quantidade": 8,
    "sequencia": [0, 1, 1, 2, 3, 5, 8, 13]
  },
  "mensagem": "Sequência Fibonacci gerada com sucesso"
}
```

**Casos de Erro:**

- Quantidade menor que 1
- Quantidade maior que 50

---

### 4. Analisar Força de Senha

Analisa a força de uma senha com base em critérios de segurança.

**Endpoint:** `?metodo=analisar_senha`

**Parâmetros:**

- `senha` (string, obrigatório): Senha a ser analisada

**Exemplo de Requisição:**

```
GET http://136.248.121.230/api.php?metodo=analisar_senha&senha=Senh@123
```

**Exemplo de Resposta (Sucesso):**

```json
{
  "sucesso": true,
  "dados": {
    "tamanho": 8,
    "tem_minuscula": true,
    "tem_maiuscula": true,
    "tem_numero": true,
    "tem_especial": true,
    "pontos": 90,
    "forca": "Muito Forte"
  },
  "mensagem": "Senha analisada com sucesso"
}
```

**Critérios de Pontuação:**

- Tamanho ≥ 8 caracteres: +20 pontos
- Tamanho ≥ 12 caracteres: +10 pontos adicionais
- Contém letras minúsculas: +20 pontos
- Contém letras maiúsculas: +20 pontos
- Contém números: +20 pontos
- Contém caracteres especiais: +10 pontos

**Classificação de Força:**

- 0-19 pontos: Muito Fraca
- 20-39 pontos: Fraca
- 40-59 pontos: Média
- 60-79 pontos: Forte
- 80+ pontos: Muito Forte

**Casos de Erro:**

- Senha não informada ou vazia

---

## Exemplos de Uso

### Usando cURL

```bash
# Calcular IMC
curl "http://136.248.121.230/api.php?metodo=calcular_imc&peso=80&altura=1.80"

# Verificar número primo
curl "http://136.248.121.230/api.php?metodo=verificar_primo&numero=23"

# Gerar Fibonacci
curl "http://136.248.121.230/api.php?metodo=fibonacci&quantidade=15"

# Analisar senha
curl "http://136.248.121.230/api.php?metodo=analisar_senha&senha=MinhaSenha123!"
```

### Usando JavaScript (Fetch API)

```javascript
// Exemplo: Calcular IMC
fetch("http://136.248.121.230/api.php?metodo=calcular_imc&peso=70&altura=1.75")
  .then((response) => response.json())
  .then((data) => console.log(data))
  .catch((error) => console.error("Erro:", error));

// Exemplo: Verificar primo (POST)
fetch("http://136.248.121.230/api.php", {
  method: "POST",
  headers: {
    "Content-Type": "application/x-www-form-urlencoded",
  },
  body: "metodo=verificar_primo&numero=17",
})
  .then((response) => response.json())
  .then((data) => console.log(data));
```

### Usando Python (Requests)

```python
import requests

# Exemplo: Calcular IMC
response = requests.get('http://136.248.121.230/api.php', params={
    'metodo': 'calcular_imc',
    'peso': 70,
    'altura': 1.75
})
print(response.json())

# Exemplo: Analisar senha
response = requests.post('http://136.248.121.230/api.php', data={
    'metodo': 'analisar_senha',
    'senha': 'Senh@123'
})
print(response.json())
```

---

## Tratamento de Erros

### Método não informado

**Requisição:**

```
GET http://136.248.121.230/api.php
```

**Resposta:**

```json
{
  "sucesso": false,
  "dados": null,
  "mensagem": "Parâmetro \"metodo\" não informado"
}
```

### Método não encontrado

**Requisição:**

```
GET http://136.248.121.230/api.php?metodo=metodo_invalido
```

\*\*Resposta:

```json
{
  "sucesso": false,
  "dados": null,
  "mensagem": "Método \"metodo_invalido\" não encontrado. Métodos disponíveis: calcular_imc, verificar_primo, fibonacci, analisar_senha"
}
```

---

## Técnicas de Teste de Caixa Preta Recomendadas

Esta API foi projetada para ser testada usando as seguintes técnicas:

### 1. Particionamento de Equivalência

- Dividir os valores de entrada em classes válidas e inválidas
- Exemplo: Para o IMC, testar valores positivos, negativos e zero

### 2. Análise de Valor Limite

- Testar valores nos limites das classes de equivalência
- Exemplo: Para Fibonacci, testar com quantidade = 1, 50, 51

### 3. Tabela de Decisão

- Útil para o método de análise de senha
- Combinar diferentes características (maiúscula, minúscula, número, especial)

### 4. Teste de Transição de Estado

- Testar diferentes sequências de chamadas à API

### 5. Teste de Casos de Uso

- Simular cenários reais de uso da API

---

## Configuração e Instalação

### Requisitos

- PHP 7.0 ou superior
- Servidor web (Apache, Nginx, etc.)

### Instalação

1. Clone ou faça download dos arquivos da API
2. Coloque o arquivo `api.php` no diretório do servidor web
3. Certifique-se de que o PHP está configurado corretamente
4. Acesse a API através da URL configurada

### Testando a Instalação

```bash
curl "http://136.248.121.230/api.php?metodo=fibonacci&quantidade=5"
```

Se a resposta retornar a sequência Fibonacci, a API está funcionando corretamente.

---

## 📝 Mensagens de Resposta Completas

### Método: calcular_imc (10 validações)

- ❌ Valores infinitos: `"Peso e altura devem ser valores numéricos finitos"`
- ❌ Valores NaN: `"Peso e altura não podem ser NaN (Not a Number)"`
- ❌ Overflow (> 1e100): `"Valores muito grandes (overflow). Use valores razoáveis."`
- ❌ Underflow (< 1e-100): `"Valores extremamente pequenos (underflow). Use valores razoáveis."`
- ❌ Valores ≤ 0: `"Peso e altura devem ser maiores que zero"`
- ✅ Sucesso: `"IMC calculado com sucesso"`

### Método: verificar_primo (6 validações)

- ❌ Número < 2: `"Números menores que 2 não são primos"`
- ❌ Número > 10.000.000: `"Número muito grande para verificação (limite: 10.000.000). Operação causaria timeout."`
- ⏱️ Timeout: `"Timeout ao verificar número primo (processamento muito longo)"`
- ✅ É primo: `"O número é primo"`
- ✅ Não é primo: `"O número não é primo"`

### Método: fibonacci (3 validações)

- ❌ Quantidade < 1: `"Quantidade deve ser maior que zero"`
- ❌ Quantidade > 50: `"Quantidade máxima é 50"`
- ✅ Sucesso: `"Sequência Fibonacci gerada com sucesso"`

### Método: analisar_senha (2 validações)

- ❌ Senha vazia: `"Senha não informada"`
- ✅ Sucesso: `"Senha analisada com sucesso"`

**Total de validações implementadas: 21 condições diferentes**

---

## Notas de Implementação

- ✅ Todos os métodos aceitam tanto **GET** quanto **POST**
- ✅ **CORS habilitado** (`Access-Control-Allow-Origin: *`) - permite acesso de qualquer origem
- ✅ Respostas sempre em formato **JSON com codificação UTF-8**
- ✅ **Validação de entrada** implementada em todos os métodos
- ✅ **Sem dependências externas** ou banco de dados
- ✅ Todos os parâmetros podem ser enviados via query string (GET) ou corpo da requisição (POST)

---

## Códigos de Erro Detalhados

### Erros Gerais

- `"Parâmetro 'metodo' não informado"`: O parâmetro obrigatório 'metodo' não foi fornecido
- `"Método '[nome]' não encontrado"`: O método especificado não existe na API

### Erros Específicos por Método

**Calcular IMC:**

- `"Peso e altura devem ser maiores que zero"`: Valores inválidos (≤ 0) para peso ou altura

**Fibonacci:**

- `"Quantidade deve ser maior que zero"`: Valor menor que 1 foi fornecido
- `"Quantidade máxima é 50"`: Limite de 50 números foi excedido

**Analisar Senha:**

- `"Senha não informada"`: O parâmetro senha está vazio ou não foi fornecido

---

## Licença

Este projeto foi desenvolvido para fins educacionais e de demonstração de técnicas de teste de software.
