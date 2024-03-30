<?php
require_once('config.php');
$email=$_POST['email'];
$password=$_POST['password'];

$query="SELECT * FROM usuarios where correo='$email' AND password='$password'";
$result=$conexion->query($query);
if(result->num_rows>0){
    header("Location: ../index.html");
}else{
    header("Location:  ../login.html");
}
?>