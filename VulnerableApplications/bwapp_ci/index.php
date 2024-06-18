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

    if( isset( $_GET[ 'ip_address' ]  ) ) {
        // Get input
        $target = $_GET[ 'ip_address' ];

        // Set blacklist
        $substitutions = array(
            '&' => '',
            ';'  => '',
            '|' => '',
        );

        // Remove any of the characters in the array (blacklist).
        $target = str_replace( array_keys( $substitutions ), $substitutions, $target );

        // Determine OS and execute the ping command.
        $cmd = shell_exec( 'timeout 5 ping -c 4 ' . $target );

        // Feedback for the end user
        echo "<h3>Ping Results for $target:</h3>";
        echo "<pre>$cmd</pre>";
    }

    ?>

</body>
</html>