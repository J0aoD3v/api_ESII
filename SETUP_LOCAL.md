# Configuração do Servidor PHP Local

## Opção 1: Instalar PHP manualmente (Recomendado)

### 1. Download do PHP

1. Acesse: https://windows.php.net/download/
2. Baixe a versão **Thread Safe** (ex: `php-8.3.x-Win32-vs16-x64.zip`)
3. Extraia para `C:\php` (ou outra pasta de sua preferência)

### 2. Adicionar ao PATH

1. Abra "Variáveis de Ambiente" (Win + Pause > Configurações avançadas do sistema)
2. Em "Variáveis do Sistema", encontre `Path` e clique em "Editar"
3. Clique em "Novo" e adicione o caminho onde extraiu o PHP (ex: `C:\php`)
4. Clique OK em todas as janelas
5. **Feche e reabra o PowerShell**

### 3. Verificar instalação

```powershell
php --version
```

### 4. Rodar o servidor

```powershell
cd "C:\Users\Joao C\Documents\api_ESII"
php -S localhost:8000
```

A API estará disponível em: `http://localhost:8000/api.php`

---

## Opção 2: Usar XAMPP (Mais fácil, mas mais pesado)

### 1. Download do XAMPP

1. Acesse: https://www.apachefriends.org/
2. Baixe e instale o XAMPP
3. Inicie o Apache pelo painel de controle

### 2. Copiar arquivos

Copie o arquivo `api.php` para: `C:\xampp\htdocs\`

A API estará disponível em: `http://localhost/api.php`

---

## Opção 3: Usar Chocolatey (se tiver instalado)

```powershell
# Instalar PHP via Chocolatey
choco install php

# Depois de instalar, rodar o servidor
php -S localhost:8000
```

---

## Opção 4: Usar Docker (se tiver instalado)

```powershell
# Rodar PHP com Docker
docker run -d -p 8000:80 -v "${PWD}:/var/www/html" php:8.2-apache
```

---

## Depois de configurar

### Rodar o servidor local:

```powershell
php -S localhost:8000
```

### Atualizar o script de testes:

Edite `test_api.py` e mude a linha:

```python
API_URL = "http://136.248.121.230/api.php"
```

Para:

```python
API_URL = "http://localhost:8000/api.php"
```

### Executar os testes:

```powershell
python test_api.py
```
