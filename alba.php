<?php
include 'config.php';

$c = curl_init();
$token = readToken();

// Verificar si el token es válido, si no, hacer login
if (!$token || !isTokenValid($c, $token))
{
    $payload = [
        "email" => "easycancha.v2@gmail.com",
        "password" => "chupaman",
    ];

    $q = geturl($c, 'https://www.easycancha.com/api/login', json_encode($payload));
    $token = json_decode($q, true)["token"];
    saveToken($token);
}

$dates = getNextSevenDays();
$result = [];

foreach ($dates as $date)
{
    $q = geturl($c, "https://www.easycancha.com/api/sports/1/clubs/59/timeslots?date=$date&timespan=60", '', $token);
    $q = json_decode($q, true)["alternative_timeslots"];
    if (empty($q))
    {
        $result[$date] = [];
        continue;
    }
    else
    {
        foreach ($q as $hrs_disp)
        {
            $hora = $hrs_disp["hour"];
            $result[$date][] = $hora;
        }
    }
}

echo '{
    "code":200,
    "msg":"OK",
    "horas disponibles":' . json_encode($result) . '
    }';
