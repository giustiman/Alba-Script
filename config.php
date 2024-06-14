<?php
function geturl($cURL, $url, $post = '', $token = '', $ref = 'https://www.easycancha.com/login', $proxy = '')
{
    curl_setopt($cURL, CURLOPT_URL, $url);
    curl_setopt($cURL, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($cURL, CURLOPT_POST, 0);
    curl_setopt($cURL, CURLOPT_VERBOSE, true);
    curl_setopt($cURL, CURLOPT_USERAGENT, 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36');


    // Configurar proxy si se proporciona
    if ($proxy)
    {
        curl_setopt($cURL, CURLOPT_PROXY, $proxy);
    }

    if ($post)
    {
        curl_setopt($cURL, CURLOPT_POST, 1);
        curl_setopt($cURL, CURLOPT_POSTFIELDS, $post);
    }

    $headers = [];
    $headers[] = 'Content-Type: application/json;charset=UTF-8';
    $headers[] = 'Referer: ' . $ref;
    if ($token)
    {
        $headers[] = 'Authorization: ' . $token;
    }
    curl_setopt($cURL, CURLOPT_HTTPHEADER, $headers);

    $verbose = fopen('php://temp', 'w+');
    curl_setopt($cURL, CURLOPT_STDERR, $verbose);
    $response = curl_exec($cURL);
    rewind($verbose);
    $verbose = stream_get_contents($verbose);

    $result = curl_exec($cURL);

    // Manejo de errores
    if ($result === false)
    {
        echo 'Curl error: ' . curl_error($cURL);
    }

    return $result;
}

function getNextSevenDays()
{
    // Array para almacenar las fechas
    $dates = [];

    // Obtener la fecha actual
    $currentDate = new DateTime();

    // Iterar 7 veces para obtener las fechas consecutivas
    for ($i = 0; $i < 8; $i++)
    {
        // Clonar la fecha actual para no modificar el objeto original
        $date = clone $currentDate;

        // Añadir días consecutivos
        $date->modify("+$i day");

        // Añadir la fecha al array en formato 'YYYY-MM-DD'
        $dates[] = $date->format('Y-m-d');
    }

    return $dates;
}

// Función para guardar el token en un archivo
function saveToken($token)
{
    file_put_contents('token.txt', $token);
}

// Función para leer el token del archivo
function readToken()
{
    if (file_exists('token.txt'))
    {
        return file_get_contents('token.txt');
    }
    return null;
}

// Función para verificar si el token es válido
function isTokenValid($c, $token)
{
    $q = geturl($c, 'https://www.easycancha.com/api/sports/1/clubs/59/timeslots?date=' . date('Y-m-d') . '&timespan=60', '', $token);

    $http_code = curl_getinfo($c, CURLINFO_HTTP_CODE);

    return $http_code === 200;
}


function isProxyActive($proxy)
{
    $c = curl_init();
    curl_setopt($c, CURLOPT_URL, 'https://www.google.com');
    curl_setopt($c, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($c, CURLOPT_TIMEOUT, 10);
    curl_setopt($c, CURLOPT_PROXY, $proxy);
    curl_setopt($c, CURLOPT_USERAGENT, 'Mozilla/5.0');
    $result = curl_exec($c);
    $http_code = curl_getinfo($c, CURLINFO_HTTP_CODE);
    curl_close($c);

    return $http_code === 200;
}
