<!DOCTYPE html>
<html>
<head>
    <title>Traceroute</title>
</head>
<body>

    <h2>Traceroute</h2>

    <form method="post" action="">
        <label for="host">Enter Hostname or IP Address:</label>
        <input type="text" name="host" id="host" required>
        <input type="submit" value="Traceroute">
    </form>

    <?php
    echo "<h3>Test</h3>";
    if (isset($_POST["host"])) {
        $host = $_POST["host"];
        // Vulnerable to command injection
        echo "<h3>Traceroute Results for $host:</h3>";
        echo "<pre>";
        system("traceroute " . $host);
        echo "</pre>";
    }
    ?>

</body>
</html>
