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

// Validacao do metodo
if (!$metodo) {
    resposta(false, null, 'Parametro "metodo" nao informado');
}

// MÉTODO 1: Calculadora de IMC
if ($metodo === 'calcular_imc') {
    $peso = floatval($_GET['peso'] ?? $_POST['peso'] ?? 0);
    $altura = floatval($_GET['altura'] ?? $_POST['altura'] ?? 0);
    
    // Validar valores infinitos e NaN
    if (!is_finite($peso) || !is_finite($altura)) {
        resposta(false, null, 'Peso e altura devem ser valores numericos finitos');
    }
    
    if (is_nan($peso) || is_nan($altura)) {
        resposta(false, null, 'Peso e altura nao podem ser NaN (Not a Number)');
    }
    
    // Validar overflow (valores extremamente grandes)
    if ($peso > 1e100 || $altura > 1e100) {
        resposta(false, null, 'Valores muito grandes (overflow). Use valores razoaveis.');
    }
    
    // Validar underflow (valores extremamente pequenos proximos de zero)
    if (($peso > 0 && $peso < 1e-100) || ($altura > 0 && $altura < 1e-100)) {
        resposta(false, null, 'Valores extremamente pequenos (underflow). Use valores razoaveis.');
    }
    
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
        resposta(true, ['numero' => $numero, 'primo' => false], 'Numeros menores que 2 nao sao primos');
    }
    
    // Limitar numeros muito grandes para evitar timeout
    if ($numero > 10000000) {
        resposta(false, null, 'Numero muito grande para verificacao (limite: 10.000.000). Operacao causaria timeout.');
    }
    
    // Casos especiais otimizados
    if ($numero == 2) {
        resposta(true, ['numero' => $numero, 'primo' => true], 'O numero e primo');
    }
    
    if ($numero % 2 == 0) {
        resposta(true, ['numero' => $numero, 'primo' => false], 'O numero nao e primo');
    }
    
    // Verificação com timeout manual
    $tempo_inicio = microtime(true);
    $timeout = 5; // 5 segundos
    $primo = true;
    
    for ($i = 3; $i <= sqrt($numero); $i += 2) {
        // Verificar timeout a cada 1000 iteracoes
        if ($i % 1000 == 1 && (microtime(true) - $tempo_inicio) > $timeout) {
            resposta(false, null, 'Timeout ao verificar numero primo (processamento muito longo)');
        }
        
        if ($numero % $i == 0) {
            $primo = false;
            break;
        }
    }
    
    resposta(true, [
        'numero' => $numero,
        'primo' => $primo
    ], $primo ? 'O numero e primo' : 'O numero nao e primo');
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
    ], 'Sequencia Fibonacci gerada com sucesso');
}

// MÉTODO 4: Analisar força de senha
if ($metodo === 'analisar_senha') {
    $senha = $_GET['senha'] ?? $_POST['senha'] ?? '';
    
    if (empty($senha)) {
        resposta(false, null, 'Senha nao informada');
    }
    
    // Contar caracteres UTF-8 corretamente (compatível com ou sem mbstring)
    if (function_exists('mb_strlen')) {
        $tamanho = mb_strlen($senha, 'UTF-8');
    } else {
        // Fallback: contar caracteres UTF-8 sem mbstring
        $tamanho = strlen(utf8_decode($senha));
    }
    
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

// Metodo nao encontrado
resposta(false, null, 'Metodo "' . $metodo . '" nao encontrado. Metodos disponiveis: calcular_imc, verificar_primo, fibonacci, analisar_senha');
?>