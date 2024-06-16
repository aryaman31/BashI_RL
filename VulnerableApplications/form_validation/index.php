<!DOCTYPE html>
<html>
<head>
    <title>Form Validation</title>
</head>
<body>

    <h2>Validate User Input</h2>

    <form method="post" action="">
        <label for="username">Username:</label>
        <input type="text" name="username" id="username" required>
        <input type="submit" name="validate" value="Validate">
    </form>

    <?php
    if (isset($_POST["validate"])) {
        $username = $_POST["username"];

        // Vulnerable to command injection
        $validation_result = shell_exec("echo $username | grep '^[a-zA-Z0-9_]*$'");
        
        if ($validation_result) {
            echo "<h3>Validation Passed for $username</h3>";
        } else {
            echo "<h3>Validation Failed</h3>";
        }
    }
    ?>

</body>
</html>
