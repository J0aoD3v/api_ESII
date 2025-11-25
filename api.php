<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST');

// Captura o método e parâmetros
$metodo = $_GET['metodo'] ?? $_POST['metodo'] ?? null;

// Função auxiliar para resposta JSON
function resposta($sucesso, $dados, $mensagem = '') {
    echo json_encode([
        'sucesso' => $sucesso,
        'dados' => $dados,
        'mensagem' => $mensagem
    ], JSON_UNESCAPED_UNICODE);
    exit;
}

// Validação do método
if (!$metodo) {
    resposta(false, null, 'Parâmetro "metodo" não informado');
}

// MÉTODO 1: Calculadora de IMC
if ($metodo === 'calcular_imc') {
    $peso = floatval($_GET['peso'] ?? $_POST['peso'] ?? 0);
    $altura = floatval($_GET['altura'] ?? $_POST['altura'] ?? 0);
    
    if ($peso <= 0 || $altura <= 0) {
        resposta(false, null, 'Peso e altura devem ser maiores que zero');
    }
    
    $imc = $peso / ($altura * $altura);
    $classificacao = '';
    
    if ($imc < 18.5) $classificacao = 'Abaixo do peso';
    elseif ($imc < 25) $classificacao = 'Peso normal';
    elseif ($imc < 30) $classificacao = 'Sobrepeso';
    elseif ($imc < 35) $classificacao = 'Obesidade grau I';
    elseif ($imc < 40) $classificacao = 'Obesidade grau II';
    else $classificacao = 'Obesidade grau III';
    
    resposta(true, [
        'imc' => round($imc, 2),
        'classificacao' => $classificacao
    ], 'IMC calculado com sucesso');
}

// MÉTODO 2: Verificar se número é primo
if ($metodo === 'verificar_primo') {
    $numero = intval($_GET['numero'] ?? $_POST['numero'] ?? 0);
    
    if ($numero < 2) {
        resposta(true, ['primo' => false], 'Números menores que 2 não são primos');
    }
    
    $primo = true;
    for ($i = 2; $i <= sqrt($numero); $i++) {
        if ($numero % $i == 0) {
            $primo = false;
            break;
        }
    }
    
    resposta(true, [
        'numero' => $numero,
        'primo' => $primo
    ], $primo ? 'O número é primo' : 'O número não é primo');
}

// MÉTODO 3: Gerar sequência Fibonacci
if ($metodo === 'fibonacci') {
    $quantidade = intval($_GET['quantidade'] ?? $_POST['quantidade'] ?? 10);
    
    if ($quantidade < 1) {
        resposta(false, null, 'Quantidade deve ser maior que zero');
    }
    
    if ($quantidade > 50) {
        resposta(false, null, 'Quantidade máxima é 50');
    }
    
    $fib = [0, 1];
    for ($i = 2; $i < $quantidade; $i++) {
        $fib[$i] = $fib[$i-1] + $fib[$i-2];
    }
    
    $sequencia = array_slice($fib, 0, $quantidade);
    
    resposta(true, [
        'quantidade' => $quantidade,
        'sequencia' => $sequencia
    ], 'Sequência Fibonacci gerada com sucesso');
}

// MÉTODO 4: Analisar força de senha
if ($metodo === 'analisar_senha') {
    $senha = $_GET['senha'] ?? $_POST['senha'] ?? '';
    
    if (empty($senha)) {
        resposta(false, null, 'Senha não informada');
    }
    
    $tamanho = strlen($senha);
    $tem_minuscula = preg_match('/[a-z]/', $senha);
    $tem_maiuscula = preg_match('/[A-Z]/', $senha);
    $tem_numero = preg_match('/[0-9]/', $senha);
    $tem_especial = preg_match('/[^a-zA-Z0-9]/', $senha);
    
    $pontos = 0;
    if ($tamanho >= 8) $pontos += 20;
    if ($tamanho >= 12) $pontos += 10;
    if ($tem_minuscula) $pontos += 20;
    if ($tem_maiuscula) $pontos += 20;
    if ($tem_numero) $pontos += 20;
    if ($tem_especial) $pontos += 10;
    
    $forca = 'Muito Fraca';
    if ($pontos >= 80) $forca = 'Muito Forte';
    elseif ($pontos >= 60) $forca = 'Forte';
    elseif ($pontos >= 40) $forca = 'Média';
    elseif ($pontos >= 20) $forca = 'Fraca';
    
    resposta(true, [
        'tamanho' => $tamanho,
        'tem_minuscula' => $tem_minuscula ? true : false,
        'tem_maiuscula' => $tem_maiuscula ? true : false,
        'tem_numero' => $tem_numero ? true : false,
        'tem_especial' => $tem_especial ? true : false,
        'pontos' => $pontos,
        'forca' => $forca
    ], 'Senha analisada com sucesso');
}

// Método não encontrado
resposta(false, null, 'Método "' . $metodo . '" não encontrado. Métodos disponíveis: calcular_imc, verificar_primo, fibonacci, analisar_senha');
?>