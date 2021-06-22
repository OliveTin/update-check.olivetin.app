<?php
/**
 * Although PHP is not a pretty language (!), it's cheap to 
 * host an incredibly easy to scale. It also has the benefit of being
 * very readable, and auditable by inexperiend developers who want
 * to check what this update service is doing.
 *
 * For more information;
 * https://www.olivetin.app/_update_checks_and_tracking.html 
 */

error_reporting(E_ALL);
ini_set('display_errors', 'on');

function parseVersionRequest() {
	$req = file_get_contents('php://input', false, null, 0, 1000);
	$json = json_decode($req);

	if ($json == null) {
		exit('error-invalid-json');
	}

	// FIXME - could get any junk in the post body!

	return $req;
}

function storableVersionRequest($version) {
	return date(DATE_ATOM) . ' , ' . $version . "\n";
}

function isNewVersionAvailable($req) {
	echo 'none';
}

try {
	if (empty($_POST)) {
		echo '<a href = "hhttps://www.olivetin.app/_update_checks_and_tracking.html">OliveTin Update Check Documentation</a>';
		exit;
	}

	$version = parseVersionRequest();
		
	file_put_contents('checkins.log', storableVersionRequest($version), FILE_APPEND);

	echo isNewVersionAvailable($version);
} catch (Exception $e) {
	echo $e;
}

?>
