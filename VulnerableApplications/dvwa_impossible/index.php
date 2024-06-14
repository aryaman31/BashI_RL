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
        $target = stripslashes( $target );

        // Split the IP into 4 octects
        $octet = explode( ".", $target );

        // Check IF each octet is an integer
        if( ( is_numeric( $octet[0] ) ) && ( is_numeric( $octet[1] ) ) && ( is_numeric( $octet[2] ) ) && ( is_numeric( $octet[3] ) ) && ( sizeof( $octet ) == 4 ) ) {
            // If all 4 octets are int's put the IP back together.
            $target = $octet[0] . '.' . $octet[1] . '.' . $octet[2] . '.' . $octet[3];
            $cmd = shell_exec( 'timeout 5 ping  -c 4 ' . $target );
            echo "<h3>Ping Results for $target:</h3>";
            echo "<pre>$cmd</pre>";
        }
        else {
            echo "<h3>Ping Results for $target:</h3>";
            echo "<pre>Invalid IP address</pre>";
        }
    }

    ?>

</body>
</html>