<?php
function geturl($cURL, $url, $post = '', $token = '', $ref = 'https://www.easycancha.com/login')
{
    curl_setopt($cURL, CURLOPT_URL, $url);
    curl_setopt($cURL, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($cURL, CURLOPT_POST, 0);
    curl_setopt($cURL, CURLOPT_USERAGENT, 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36');

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

    $result = curl_exec($cURL);
    return ($result);
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
