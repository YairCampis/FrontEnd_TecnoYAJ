<?php
// Conexión a la base de datos MySQL
$servername = "localhost";
$username = "root";
$password = "";
$database = "proyectos_cul;

$conn = new mysqli($servername, $username, $password, $database);

// Verificar la conexión
if ($conn->connect_error) {
    die("Error de conexión: " . $conn->connect_error);
}

// Obtener los datos del formulario
$username = $_POST['inputEmail'];
$password = $_POST['inputPassword'];

// Consulta SQL para verificar las credenciales
$sql = "SELECT * FROM usuarios WHERE username='$username' AND password='$password'";
$result = $conn->query($sql);

// Verificar si se encontró un usuario con esas credenciales
if ($result->num_rows > 0) {
    // Usuario y contraseña válidos, redirigir a la página de inicio
    header("Location: index.html");
} else {
    // Usuario y/o contraseña incorrectos, mostrar mensaje de error
    echo "Usuario y/o contraseña incorrectos";
}

// Cerrar la conexión
$conn->close();
?>
