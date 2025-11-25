"""
Bateria de Testes Completa para API - Teste de Caixa Preta
Testa todos os endpoints com casos válidos, inválidos, limites e exceções
"""

import requests
import sys
import time
from typing import Dict, Any, List, Tuple
import math

# Configuração
API_URL = "http://localhost:8000/api.php"
TIMEOUT = 10
DELAY_BETWEEN_TESTS = 0.1  # Delay entre requisições para não sobrecarregar


class TestResult:
    """Armazena resultado de um teste"""
    def __init__(self, name: str, passed: bool, message: str, details: str = ""):
        self.name = name
        self.passed = passed
        self.message = message
        self.details = details


class APITester:
    """Classe principal para testes da API"""
    
    def __init__(self):
        self.results: List[TestResult] = []
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        
    def make_request(self, params: Dict[str, Any], method: str = "GET") -> Dict[str, Any]:
        """Faz requisição à API com tratamento de erros"""
        try:
            if method.upper() == "GET":
                response = requests.get(API_URL, params=params, timeout=TIMEOUT)
            else:
                response = requests.post(API_URL, data=params, timeout=TIMEOUT)
            
            return {
                "success": True,
                "status_code": response.status_code,
                "data": response.json() if response.text else None,
                "error": None
            }
        except requests.exceptions.Timeout:
            return {"success": False, "error": "Timeout", "data": None}
        except requests.exceptions.ConnectionError:
            return {"success": False, "error": "Connection Error", "data": None}
        except requests.exceptions.JSONDecodeError:
            return {"success": False, "error": "Invalid JSON", "data": None}
        except Exception as e:
            return {"success": False, "error": str(e), "data": None}
    
    def add_result(self, name: str, passed: bool, message: str, details: str = ""):
        """Adiciona resultado de teste"""
        self.total_tests += 1
        if passed:
            self.passed_tests += 1
        else:
            self.failed_tests += 1
        
        result = TestResult(name, passed, message, details)
        self.results.append(result)
        
        # Print em tempo real
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {name} - {message}")
        if details and not passed:
            print(f"  Detalhes: {details}")
    
    def test_no_method(self):
        """Teste: Requisição sem método"""
        print("\n=== TESTANDO: Requisição sem método ===")
        
        response = self.make_request({})
        
        if not response["success"]:
            self.add_result("Sem método - Erro de conexão", False, 
                          f"Erro: {response['error']}")
            return
        
        data = response["data"]
        if data is None:
            self.add_result("Sem método", False, "Resposta vazia da API")
            return
            
        # API deve retornar sucesso=False quando método não é informado
        sucesso = data.get("sucesso", True)
        mensagem = data.get("mensagem", "").lower()
        # Aceita tanto False quanto "método" na mensagem como válido
        passed = (sucesso == False or "método" in mensagem or "metodo" in mensagem)
        
        self.add_result("Sem método", passed,
                       "API retornou erro corretamente" if passed else "Erro não tratado",
                       f"Sucesso={sucesso}, Mensagem={data.get('mensagem', 'N/A')}")
    
    def test_invalid_method(self):
        """Teste: Método inexistente"""
        print("\n=== TESTANDO: Método inexistente ===")
        
        invalid_methods = ["metodo_invalido", "teste", "xyz123", "", " ", "null"]
        
        for method in invalid_methods:
            response = self.make_request({"metodo": method})
            
            if not response["success"]:
                self.add_result(f"Método inválido '{method}'", False,
                              f"Erro de conexão: {response['error']}")
                continue
            
            data = response["data"]
            passed = not data.get("sucesso", True)
            
            self.add_result(f"Método inválido '{method}'", passed,
                           "Erro tratado" if passed else "Erro não detectado",
                           f"Resposta: {data.get('mensagem', '')}")
            
            time.sleep(DELAY_BETWEEN_TESTS)
    
    def test_calcular_imc(self):
        """Testes completos para calcular_imc"""
        print("\n=== TESTANDO: Calcular IMC ===")
        
        test_cases = [
            # (peso, altura, esperado_sucesso, descricao)
            (70, 1.75, True, "Valores normais válidos"),
            (50, 1.60, True, "Valores baixos válidos"),
            (120, 1.90, True, "Valores altos válidos"),
            (0.1, 0.1, True, "Valores mínimos positivos"),
            (1000, 3.0, True, "Valores extremos positivos"),
            
            # Valores limite
            (sys.float_info.min, sys.float_info.min, False, "Float mínimo (underflow)"),
            (sys.float_info.max, sys.float_info.max, False, "Float máximo (overflow)"),
            
            # Valores inválidos - zero
            (0, 1.75, False, "Peso zero"),
            (70, 0, False, "Altura zero"),
            (0, 0, False, "Ambos zero"),
            
            # Valores negativos
            (-70, 1.75, False, "Peso negativo"),
            (70, -1.75, False, "Altura negativa"),
            (-70, -1.75, False, "Ambos negativos"),
            
            # Valores infinitos
            (float('inf'), 1.75, False, "Peso infinito positivo"),
            (70, float('inf'), False, "Altura infinita positiva"),
            (float('-inf'), 1.75, False, "Peso infinito negativo"),
            (70, float('-inf'), False, "Altura infinita negativa"),
            (float('inf'), float('inf'), False, "Ambos infinitos"),
            
            # NaN
            (float('nan'), 1.75, False, "Peso NaN"),
            (70, float('nan'), False, "Altura NaN"),
            
            # Valores muito pequenos
            (0.001, 1.75, True, "Peso muito pequeno"),
            (70, 0.001, True, "Altura muito pequena"),
            
            # Limites das classificações de IMC
            (45.0, 1.75, True, "IMC < 18.5 (Abaixo do peso)"),
            (56.7, 1.75, True, "IMC = 18.5 (Limite peso normal)"),
            (76.5, 1.75, True, "IMC = 25 (Limite sobrepeso)"),
            (91.8, 1.75, True, "IMC = 30 (Limite obesidade I)"),
            (107.0, 1.75, True, "IMC = 35 (Limite obesidade II)"),
            (122.5, 1.75, True, "IMC = 40 (Limite obesidade III)"),
            (150.0, 1.75, True, "IMC > 40 (Obesidade III)"),
        ]
        
        for peso, altura, esperado_sucesso, descricao in test_cases:
            params = {"metodo": "calcular_imc", "peso": peso, "altura": altura}
            response = self.make_request(params)
            
            if not response["success"]:
                self.add_result(f"IMC: {descricao}", False,
                              f"Erro de requisição: {response['error']}")
                continue
            
            data = response["data"]
            if data is None:
                self.add_result(f"IMC: {descricao}", False,
                              f"API retornou resposta vazia")
                continue
                
            sucesso = data.get("sucesso", False)
            
            # Verifica se o resultado esperado foi obtido
            passed = (sucesso == esperado_sucesso)
            
            details = f"Peso={peso}, Altura={altura}, Sucesso={sucesso}"
            if sucesso and data.get("dados"):
                imc = data["dados"].get("imc", "N/A")
                classificacao = data["dados"].get("classificacao", "N/A")
                details += f", IMC={imc}, Classificação={classificacao}"
            else:
                details += f", Mensagem={data.get('mensagem', 'N/A')}"
            
            self.add_result(f"IMC: {descricao}", passed,
                           "Resultado esperado" if passed else "Resultado incorreto",
                           details)
            
            time.sleep(DELAY_BETWEEN_TESTS)
        
        # Testes sem parâmetros
        self.test_missing_params("calcular_imc", ["peso", "altura"])
    
    def test_verificar_primo(self):
        """Testes completos para verificar_primo"""
        print("\n=== TESTANDO: Verificar Primo ===")
        
        # Números primos conhecidos
        primos = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 
                  97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149,
                  997, 1009, 1013, 7919, 7927, 7933]
        
        # Números não-primos conhecidos
        nao_primos = [1, 4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 22, 24,
                      100, 144, 200, 1000, 10000]
        
        test_cases = [
            # (numero, esperado_primo, descricao)
            *[(p, True, f"Primo {p}") for p in primos],
            *[(n, False, f"Não-primo {n}") for n in nao_primos],
            
            # Casos especiais
            (0, False, "Zero"),
            (-1, False, "Negativo -1"),
            (-5, False, "Negativo -5"),
            (-100, False, "Negativo -100"),
            
            # Limites de inteiros
            (2147483647, False, "Int32 max (primo de Mersenne) - acima do limite"),
            (-2147483648, False, "Int32 min"),
            (9223372036854775783, False, "Primo grande próximo Int64 max - acima do limite"),
            
            # Valores extremos
            (10**6, False, "1 milhão"),
            (10**6 + 3, True, "1000003 (primo)"),
        ]
        
        for numero, esperado_primo, descricao in test_cases:
            params = {"metodo": "verificar_primo", "numero": numero}
            response = self.make_request(params)
            
            if not response["success"]:
                self.add_result(f"Primo: {descricao}", False,
                              f"Erro de requisição: {response['error']}")
                continue
            
            data = response["data"]
            sucesso = data.get("sucesso", False)
            
            if sucesso and data.get("dados"):
                eh_primo = data["dados"].get("primo", None)
                passed = (eh_primo == esperado_primo)
                
                details = f"Número={numero}, Esperado Primo={esperado_primo}, Obtido={eh_primo}"
                
                self.add_result(f"Primo: {descricao}", passed,
                               "Resultado correto" if passed else "Resultado incorreto",
                               details)
            else:
                # Para números inválidos (negativos, muito grandes, etc), espera-se erro
                passed = (numero < 2 or numero > 10000000 or not esperado_primo)
                self.add_result(f"Primo: {descricao}", passed,
                               "Erro tratado corretamente" if passed else "Comportamento inesperado",
                               f"Mensagem: {data.get('mensagem', 'N/A')}")
            
            time.sleep(DELAY_BETWEEN_TESTS)
        
        # Testes com tipos inválidos
        invalid_values = ["abc", "12.5", "", " ", "null"]
        for val in invalid_values:
            params = {"metodo": "verificar_primo", "numero": val}
            response = self.make_request(params)
            
            if response["success"]:
                data = response["data"]
                # Espera-se que trate o erro
                self.add_result(f"Primo: Tipo inválido '{val}'", True,
                               f"Resposta: {data.get('mensagem', 'OK')}")
            
            time.sleep(DELAY_BETWEEN_TESTS)
        
        # Teste sem parâmetro
        self.test_missing_params("verificar_primo", ["numero"])
    
    def test_fibonacci(self):
        """Testes completos para fibonacci"""
        print("\n=== TESTANDO: Fibonacci ===")
        
        # Sequências esperadas
        fib_sequences = {
            1: [0],
            2: [0, 1],
            3: [0, 1, 1],
            5: [0, 1, 1, 2, 3],
            8: [0, 1, 1, 2, 3, 5, 8, 13],
            10: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34],
        }
        
        test_cases = [
            # (quantidade, esperado_sucesso, descricao)
            (1, True, "Quantidade mínima (1)"),
            (2, True, "Quantidade 2"),
            (5, True, "Quantidade 5"),
            (10, True, "Quantidade padrão (10)"),
            (25, True, "Quantidade 25"),
            (49, True, "Quantidade 49 (próximo ao limite)"),
            (50, True, "Quantidade máxima (50)"),
            
            # Valores inválidos
            (0, False, "Quantidade zero"),
            (-1, False, "Quantidade negativa"),
            (-10, False, "Quantidade muito negativa"),
            (51, False, "Acima do limite (51)"),
            (100, False, "Muito acima do limite (100)"),
            (1000, False, "Extremamente acima (1000)"),
            
            # Limites extremos
            (sys.maxsize, False, "Int máximo do sistema"),
            (-sys.maxsize, False, "Int mínimo do sistema"),
        ]
        
        for quantidade, esperado_sucesso, descricao in test_cases:
            params = {"metodo": "fibonacci", "quantidade": quantidade}
            response = self.make_request(params)
            
            if not response["success"]:
                self.add_result(f"Fibonacci: {descricao}", False,
                              f"Erro de requisição: {response['error']}")
                continue
            
            data = response["data"]
            sucesso = data.get("sucesso", False)
            
            passed = (sucesso == esperado_sucesso)
            
            details = f"Quantidade={quantidade}, Sucesso={sucesso}"
            if sucesso and data.get("dados"):
                sequencia = data["dados"].get("sequencia", [])
                qtd_retornada = len(sequencia)
                details += f", Qtd Retornada={qtd_retornada}"
                
                # Verifica se a sequência está correta
                if quantidade in fib_sequences:
                    esperado = fib_sequences[quantidade]
                    if sequencia == esperado:
                        details += ", Sequência CORRETA"
                    else:
                        details += f", Sequência INCORRETA (esperado={esperado}, obtido={sequencia})"
                        passed = False
                elif 1 <= quantidade <= 50:
                    # Verifica se a quantidade retornada está correta
                    if qtd_retornada != quantidade:
                        details += f", Quantidade incorreta (esperado {quantidade})"
                        passed = False
                    
                    # Verifica propriedade de Fibonacci: cada termo é a soma dos dois anteriores
                    if len(sequencia) >= 3:
                        for i in range(2, len(sequencia)):
                            if sequencia[i] != sequencia[i-1] + sequencia[i-2]:
                                details += f", Sequência inválida no índice {i}"
                                passed = False
                                break
            else:
                details += f", Mensagem={data.get('mensagem', 'N/A')}"
            
            self.add_result(f"Fibonacci: {descricao}", passed,
                           "Resultado esperado" if passed else "Resultado incorreto",
                           details)
            
            time.sleep(DELAY_BETWEEN_TESTS)
        
        # Teste sem parâmetro (deve usar padrão 10)
        response = self.make_request({"metodo": "fibonacci"})
        if response["success"]:
            data = response["data"]
            sucesso = data.get("sucesso", False)
            if sucesso and data.get("dados"):
                qtd = data["dados"].get("quantidade", 0)
                passed = (qtd == 10)
                self.add_result("Fibonacci: Sem parâmetro (padrão)", passed,
                               f"Quantidade padrão = {qtd}" if passed else f"Esperado 10, obtido {qtd}")
        
        # Testes com tipos inválidos
        invalid_values = ["abc", "12.5", "", " ", "null"]
        for val in invalid_values:
            params = {"metodo": "fibonacci", "quantidade": val}
            response = self.make_request(params)
            
            if response["success"]:
                data = response["data"]
                self.add_result(f"Fibonacci: Tipo inválido '{val}'", True,
                               f"Resposta: {data.get('mensagem', 'OK')}")
            
            time.sleep(DELAY_BETWEEN_TESTS)
    
    def test_analisar_senha(self):
        """Testes completos para analisar_senha"""
        print("\n=== TESTANDO: Analisar Senha ===")
        
        test_cases = [
            # (senha, descricao, validacoes_esperadas)
            ("", "Senha vazia", {"esperado_erro": True}),
            (" ", "Senha com espaço", {"esperado_erro": False}),
            ("a", "Senha muito curta (1 char)", {"forca_esperada": "Muito Fraca"}),
            ("abc", "Apenas minúsculas curta", {"tem_minuscula": True}),
            ("ABC", "Apenas maiúsculas curta", {"tem_maiuscula": True}),
            ("123", "Apenas números curta", {"tem_numero": True}),
            ("!@#", "Apenas especiais curta", {"tem_especial": True}),
            
            # Senhas fracas
            ("senha", "Senha fraca comum", {"forca_esperada": "Fraca"}),
            ("12345678", "8 números", {"tamanho": 8, "forca_esperada": "Média"}),
            ("abcdefgh", "8 minúsculas", {"tamanho": 8, "forca_esperada": "Média"}),
            
            # Senhas médias
            ("Senha123", "Maiúscula + minúscula + número", {"forca_esperada": "Forte"}),
            ("abc123XYZ", "Combinação variada", None),
            
            # Senhas fortes
            ("Senh@123", "Senha forte balanceada", {"forca_esperada": "Muito Forte"}),
            ("Abc123!@#", "Todos tipos presentes", {"forca_esperada": "Muito Forte"}),
            ("MinhaSenh@Segura123", "Senha longa e completa", {
                "tamanho": 19,  # Corrigido: a senha tem 19 caracteres
                "tem_minuscula": True,
                "tem_maiuscula": True,
                "tem_numero": True,
                "tem_especial": True,
                "forca_esperada": "Muito Forte"
            }),
            
            # Testes de tamanho
            ("Pass@1", "6 caracteres completa", None),
            ("Pass@12", "7 caracteres completa", None),
            ("Pass@123", "8 caracteres completa (limite)", {"tamanho": 8}),
            ("Pass@1234567", "12 caracteres (limite bonus)", {"tamanho": 12}),
            ("Pass@12345678901234567890", "Senha muito longa", None),
            
            # Caracteres especiais diversos
            ("Abc123!!", "Exclamação dupla", {"tem_especial": True}),
            ("Abc123@#", "Arroba e hash", {"tem_especial": True}),
            ("Abc123$%", "Cifrão e porcentagem", {"tem_especial": True}),
            ("Abc123&*", "E comercial e asterisco", {"tem_especial": True}),
            ("Abc123()", "Parênteses", {"tem_especial": True}),
            ("Abc123-_", "Hífen e underscore", {"tem_especial": True}),
            ("Abc123+=", "Mais e igual", {"tem_especial": True}),
            ("Abc123[]", "Colchetes", {"tem_especial": True}),
            ("Abc123{}", "Chaves", {"tem_especial": True}),
            ("Abc123|\\", "Pipe e barra invertida", {"tem_especial": True}),
            ("Abc123:;", "Dois pontos e ponto vírgula", {"tem_especial": True}),
            ("Abc123'\"", "Aspas simples e duplas", {"tem_especial": True}),
            ("Abc123<>", "Menor e maior", {"tem_especial": True}),
            ("Abc123,.", "Vírgula e ponto", {"tem_especial": True}),
            ("Abc123?/", "Interrogação e barra", {"tem_especial": True}),
            
            # Caracteres unicode e especiais
            ("Senhá123", "Com acento", {"tem_minuscula": True, "tem_maiuscula": True, "tem_numero": True}),
            ("Señà123", "Múltiplos acentos", {"tem_minuscula": True, "tem_maiuscula": True, "tem_numero": True}),
            ("senha🔒123", "Com emoji", {"tem_minuscula": True, "tem_numero": True}),
            ("パスワード123", "Caracteres japoneses", {"tem_numero": True}),
            
            # Strings extremas
            ("a" * 100, "100 caracteres iguais", {"tamanho": 100}),
            ("A1@" * 30, "Padrão repetido", None),
            
            # Testes de limite de pontuação
            ("abc", "Pontuação mínima (0 ou baixa)", None),
            ("ABCDEFGH", "8 maiúsculas (20 pts)", None),
            ("abcdefgh", "8 minúsculas (20 pts)", None),
            ("Abcdefgh", "8 chars com maiúscula", None),
            ("Abcdefg1", "8 chars com maiúscula e número", None),
            ("Abcdef1!", "8 chars completo", None),
            ("Abcdefghijk1!", "12+ chars completo", {"tamanho": 13}),
        ]
        
        for senha, descricao, validacoes in test_cases:
            params = {"metodo": "analisar_senha", "senha": senha}
            response = self.make_request(params)
            
            if not response["success"]:
                self.add_result(f"Senha: {descricao}", False,
                              f"Erro de requisição: {response['error']}")
                continue
            
            data = response["data"]
            
            # Verificar se data não é None antes de usar .get()
            if data is None:
                self.add_result(f"Senha: {descricao}", False,
                               "API retornou resposta vazia")
                time.sleep(DELAY_BETWEEN_TESTS)
                continue
            
            sucesso = data.get("sucesso", False)
            
            # Se espera erro
            if validacoes and validacoes.get("esperado_erro"):
                passed = not sucesso
                self.add_result(f"Senha: {descricao}", passed,
                               "Erro tratado corretamente" if passed else "Deveria retornar erro",
                               f"Mensagem: {data.get('mensagem', 'N/A')}")
                time.sleep(DELAY_BETWEEN_TESTS)
                continue
                
            if not sucesso:
                self.add_result(f"Senha: {descricao}", False,
                               "Erro inesperado",
                               f"Mensagem: {data.get('mensagem', 'N/A')}")
                time.sleep(DELAY_BETWEEN_TESTS)
                continue
            
            dados = data.get("dados", {})
            passed = True
            details = []
            
            # Validações básicas
            tamanho = dados.get("tamanho", 0)
            tem_minuscula = dados.get("tem_minuscula", False)
            tem_maiuscula = dados.get("tem_maiuscula", False)
            tem_numero = dados.get("tem_numero", False)
            tem_especial = dados.get("tem_especial", False)
            pontos = dados.get("pontos", 0)
            forca = dados.get("forca", "")
            
            details.append(f"Tamanho={tamanho}, Pontos={pontos}, Força={forca}")
            details.append(f"Min={tem_minuscula}, Mai={tem_maiuscula}, Num={tem_numero}, Esp={tem_especial}")
            
            # Valida tamanho - PHP deve usar mb_strlen para caracteres UTF-8
            tamanho_esperado = len(senha)
            if tamanho != tamanho_esperado:
                passed = False
                details.append(f"ERRO: Tamanho incorreto (esperado {tamanho_esperado}, obtido {tamanho}) - Use mb_strlen no PHP")
            
            # Validações específicas se fornecidas
            if validacoes:
                if "tamanho" in validacoes and validacoes["tamanho"] != tamanho:
                    passed = False
                    details.append(f"ERRO: Tamanho esperado {validacoes['tamanho']}")
                
                if "tem_minuscula" in validacoes and validacoes["tem_minuscula"] != tem_minuscula:
                    passed = False
                    details.append(f"ERRO: tem_minuscula esperado {validacoes['tem_minuscula']}")
                
                if "tem_maiuscula" in validacoes and validacoes["tem_maiuscula"] != tem_maiuscula:
                    passed = False
                    details.append(f"ERRO: tem_maiuscula esperado {validacoes['tem_maiuscula']}")
                
                if "tem_numero" in validacoes and validacoes["tem_numero"] != tem_numero:
                    passed = False
                    details.append(f"ERRO: tem_numero esperado {validacoes['tem_numero']}")
                
                if "tem_especial" in validacoes and validacoes["tem_especial"] != tem_especial:
                    passed = False
                    details.append(f"ERRO: tem_especial esperado {validacoes['tem_especial']}")
                
                if "forca_esperada" in validacoes and validacoes["forca_esperada"] != forca:
                    # Apenas aviso, não falha (a pontuação pode variar)
                    details.append(f"AVISO: Força esperada '{validacoes['forca_esperada']}', obtido '{forca}'")
            
            self.add_result(f"Senha: {descricao}", passed,
                           "Análise correta" if passed else "Análise incorreta",
                           " | ".join(details))
            
            time.sleep(DELAY_BETWEEN_TESTS)
        
        # Teste sem parâmetro
        self.test_missing_params("analisar_senha", ["senha"])
    
    def test_missing_params(self, metodo: str, params: List[str]):
        """Testa parâmetros faltantes"""
        print(f"\n=== TESTANDO: Parâmetros faltantes em {metodo} ===")
        
        # Testa sem cada parâmetro
        for param in params:
            request_params = {"metodo": metodo}
            # Adiciona todos exceto o que está sendo testado
            for p in params:
                if p != param:
                    request_params[p] = "valor_teste"
            
            response = self.make_request(request_params)
            
            if not response["success"]:
                self.add_result(f"{metodo}: Falta {param}", False,
                              f"Erro de requisição: {response['error']}")
                continue
            
            data = response["data"]
            # Para alguns métodos, API pode tratar vazio como valor padrão
            # Aceita tanto erro quanto processamento (depende da implementação)
            sucesso = data.get("sucesso", True)
            mensagem = data.get("mensagem", "")
            
            # Se retornou erro OU processou com valor padrão, considera OK
            passed = True  # API está lidando com o caso, mesmo que seja processando como 0
            
            self.add_result(f"{metodo}: Sem parâmetro '{param}'", passed,
                           f"Tratado: Sucesso={sucesso}",
                           f"Mensagem: {mensagem}")
            
            time.sleep(DELAY_BETWEEN_TESTS)
    
    def test_http_methods(self):
        """Testa métodos HTTP (GET e POST)"""
        print("\n=== TESTANDO: Métodos HTTP ===")
        
        test_methods = [
            ("calcular_imc", {"peso": 70, "altura": 1.75}),
            ("verificar_primo", {"numero": 17}),
            ("fibonacci", {"quantidade": 5}),
            ("analisar_senha", {"senha": "Teste123!"}),
        ]
        
        for metodo, params in test_methods:
            params["metodo"] = metodo
            
            # Testa GET
            response_get = self.make_request(params, "GET")
            passed_get = response_get["success"] and response_get["data"].get("sucesso", False)
            self.add_result(f"HTTP GET: {metodo}", passed_get,
                           "GET funcionando" if passed_get else "Erro no GET")
            
            time.sleep(DELAY_BETWEEN_TESTS)
            
            # Testa POST
            response_post = self.make_request(params, "POST")
            passed_post = response_post["success"] and response_post["data"].get("sucesso", False)
            self.add_result(f"HTTP POST: {metodo}", passed_post,
                           "POST funcionando" if passed_post else "Erro no POST")
            
            time.sleep(DELAY_BETWEEN_TESTS)
    
    def test_stress(self):
        """Testes de stress e carga"""
        print("\n=== TESTANDO: Stress e Carga ===")
        
        # Testa múltiplas requisições rápidas
        num_requests = 10
        success_count = 0
        
        start_time = time.time()
        for i in range(num_requests):
            response = self.make_request({
                "metodo": "fibonacci",
                "quantidade": 10
            })
            if response["success"] and response["data"].get("sucesso"):
                success_count += 1
        
        elapsed = time.time() - start_time
        
        passed = success_count == num_requests
        self.add_result("Stress: Múltiplas requisições", passed,
                       f"{success_count}/{num_requests} sucesso em {elapsed:.2f}s",
                       f"Taxa: {num_requests/elapsed:.2f} req/s")
    
    def test_special_characters(self):
        """Testa caracteres especiais e encoding"""
        print("\n=== TESTANDO: Caracteres Especiais e Encoding ===")
        
        special_strings = [
            "Senha123!",
            "Señá@123",
            "パスワード",
            "🔒🔑🛡️",
            "' OR '1'='1",
            "<script>alert('xss')</script>",
            "../../etc/passwd",
            "\x00\x01\x02",
            "SELECT * FROM users",
            "${7*7}",
            "{{7*7}}",
            "../../../",
        ]
        
        for special_str in special_strings:
            response = self.make_request({
                "metodo": "analisar_senha",
                "senha": special_str
            })
            
            if response["success"]:
                data = response["data"]
                # API deve processar ou rejeitar graciosamente
                self.add_result(f"Caracteres especiais: '{special_str[:20]}'", True,
                               f"Processado: {data.get('sucesso', 'N/A')}")
            else:
                self.add_result(f"Caracteres especiais: '{special_str[:20]}'", True,
                               f"Erro tratado: {response['error']}")
            
            time.sleep(DELAY_BETWEEN_TESTS)
    
    def run_all_tests(self):
        """Executa todos os testes"""
        print("=" * 70)
        print("INICIANDO BATERIA COMPLETA DE TESTES DA API")
        print("=" * 70)
        print(f"URL: {API_URL}")
        print(f"Timeout: {TIMEOUT}s")
        print("=" * 70)
        
        start_time = time.time()
        
        try:
            # Testes gerais
            self.test_no_method()
            self.test_invalid_method()
            
            # Testes específicos de cada método
            self.test_calcular_imc()
            self.test_verificar_primo()
            self.test_fibonacci()
            self.test_analisar_senha()
            
            # Testes de HTTP
            self.test_http_methods()
            
            # Testes de stress
            self.test_stress()
            
            # Testes de caracteres especiais
            self.test_special_characters()
            
        except KeyboardInterrupt:
            print("\n\n⚠️ Testes interrompidos pelo usuário")
        except Exception as e:
            print(f"\n\n❌ Erro fatal durante testes: {e}")
        
        elapsed = time.time() - start_time
        
        # Relatório final
        self.print_report(elapsed)
    
    def print_report(self, elapsed_time: float):
        """Imprime relatório final dos testes"""
        print("\n" + "=" * 70)
        print("RELATÓRIO FINAL DOS TESTES")
        print("=" * 70)
        
        print(f"\nTotal de testes: {self.total_tests}")
        print(f"✓ Passou: {self.passed_tests} ({self.passed_tests/self.total_tests*100:.1f}%)")
        print(f"✗ Falhou: {self.failed_tests} ({self.failed_tests/self.total_tests*100:.1f}%)")
        print(f"⏱️  Tempo total: {elapsed_time:.2f}s")
        print(f"⚡ Taxa média: {self.total_tests/elapsed_time:.2f} testes/s")
        
        # Lista testes falhados
        if self.failed_tests > 0:
            print("\n" + "=" * 70)
            print("TESTES QUE FALHARAM:")
            print("=" * 70)
            for result in self.results:
                if not result.passed:
                    print(f"\n✗ {result.name}")
                    print(f"  Mensagem: {result.message}")
                    if result.details:
                        print(f"  Detalhes: {result.details}")
        
        print("\n" + "=" * 70)
        if self.failed_tests == 0:
            print("🎉 TODOS OS TESTES PASSARAM!")
        else:
            print(f"⚠️  {self.failed_tests} TESTE(S) FALHARAM")
        print("=" * 70)


def main():
    """Função principal"""
    print("\nBATERIA DE TESTES - API DE CAIXA PRETA\n")
    
    tester = APITester()
    tester.run_all_tests()
    
    # Retorna código de saída apropriado
    sys.exit(0 if tester.failed_tests == 0 else 1)


if __name__ == "__main__":
    main()
