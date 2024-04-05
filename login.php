<?php
session_start();

// Conexión a la base de datos MySQL
$servername = "localhost";
$username = "root";
$password = "";
$database = "proyectos_cul";

$conn = new mysqli($servername, $username, $password, $database);

// Verificar la conexión
if ($conn->connect_error) {
    die("Error de conexión: " . $conn->connect_error);
}

// Obtener los datos del formulario y limpiarlos
$username = mysqli_real_escape_string($conn, $_POST['email']);
$password = mysqli_real_escape_string($conn, $_POST['password']);

// Consulta SQL preparada para verificar las credenciales
$sql = "SELECT * FROM usuarios WHERE username=? LIMIT 1";
$stmt = $conn->prepare($sql);
$stmt->bind_param("s", $username);
$stmt->execute();
$result = $stmt->get_result();

// Verificar si se encontró un usuario con ese nombre de usuario
if ($result->num_rows == 1) {
    $row = $result->fetch_assoc();
    if (password_verify($password, $row['password'])) {
        // Inicio de sesión exitoso, redirigir al usuario a la página de inicio
        $_SESSION['username'] = $username;
        header("Location: index.html");
        exit();
    } else {
        // Contraseña incorrecta, mostrar mensaje de error
        echo "Usuario y/o contraseña incorrectos";
    }
} else {
    // Usuario no encontrado, mostrar mensaje de error
    echo "Usuario y/o contraseña incorrectos";
}

// Cerrar la conexión
$stmt->close();
$conn->close();
?>
