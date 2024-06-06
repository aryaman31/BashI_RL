<!-- This file doesn't sanitise the user input and runs a shell command,
     hence has a command injection vulnerability 
    Vuln is 
        ; ls     

    -->

<!DOCTYPE html>
<html>
<head>
    <title>Ping IP Address</title>
</head>
<body>

    <h2>Ping IP Address</h2>

    <form method="get" action="">
        <label for="ip_address">Enter IP Address:</label>
        <input type="text" name="ip_address" id="ip_address" required>
        <input type="submit" value="Ping">
    </form>

    <?php
    if (isset($_GET["ip_address"])) {
        $ip_address = $_GET["ip_address"];
        $ping_output = shell_exec("ping " . $ip_address . " -c 4");
        echo "<h3>Ping Results for $ip_address:</h3>";
        echo "<pre>$ping_output</pre>";
    }
    ?>

</body>
</html>
