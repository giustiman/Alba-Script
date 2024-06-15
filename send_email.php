<?php

use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;

require 'phpmailer/src/Exception.php';
require 'phpmailer/src/PHPMailer.php';
require 'phpmailer/src/SMTP.php';

if ($_SERVER["REQUEST_METHOD"] == "POST")
{
    $to = $_POST['to'];
    if ($to == 'cristobal.giusti@gmail.com')
    {
        $userName = 'cristobal.giusti@gmail.com';
        $pass = 'danshgpxljsaaauy';
    }
    else
    {
        $userName = 'tomas.valverde@gmail.com';
        $pass = '';
    }
    $subject = $_POST['subject'];
    $message = $_POST['message'];

    $mail = new PHPMailer(true);
    try
    {
        //Server settings
        $mail->isSMTP();                              //Send using SMTP
        $mail->Host       = 'smtp.gmail.com';       //Set the SMTP server to send through
        $mail->SMTPAuth   = true;             //Enable SMTP authentication
        $mail->Username   = $userName;   //SMTP write your email
        $mail->Password   = $pass;      //SMTP password
        $mail->SMTPSecure = 'ssl';            //Enable implicit SSL encryption
        $mail->Port       = 465;

        //Recipients
        $mail->setFrom('cristobal.giusti@gmail.com', 'giusti'); // Sender Email and name
        $mail->addAddress($to);     //Add a recipient email  

        //Content
        $mail->isHTML(true);               //Set email format to HTML
        $mail->Subject = $subject;   // email subject headings
        $mail->Body    = $message; //email message

        // Success sent message alert
        $mail->send();
        echo 'El mensaje ha sido enviado';
    }
    catch (Exception $e)
    {
        echo "El mensaje no pudo ser enviado. Error de PHPMailer: {$mail->ErrorInfo}";
    }
}
else
{
    echo 'Solicitud no válida';
}
