<!-- This file doesn't sanitise the user input and runs a shell command,
     hence has a command injection vulnerability 
     
    Vuln is 
    " . shell_exec("ls") ; #  
-->

<!DOCTYPE html>
<html>
<head>
    <title>Your Age</title>
</head>
<body>

    <h2>Enter your age</h2>

    <form method="get" action="">
        <label for="age">Enter your age:</label>
        <input type="text" name="age" id="age" required>
        <input type="submit" value="echoAge">
    </form>

    <?php
    // Test
    if (isset($_GET["age"])) {
        $age = $_GET["age"];
        eval("echo \"Your age is " . $_GET["age"] . ".\";");
        // echo "Your age is "" .";
    }
    ?>

</body>
</html>
