<?php
$server='localhost';
$username='root';
$password='';
$database='proyectos_cul';

try {
    $conn= new PDO("mysql:host=$server;dbname=$database;",$username,$password);

}catch (PDOException $e) {
    die('Conexion fallida: '.$e->getMessage());

}


?>
