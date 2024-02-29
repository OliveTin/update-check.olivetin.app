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


function parseVersionRequest()
{
    $req = file_get_contents('php://input', false, null, 0, 1000);
    $json = json_decode($req);

    if ($json == null) {
        exit('error-invalid-json');
    }

    // FIXME - could get any junk in the post body!

    return $json;
}

function storableVersionRequest($version)
{
    return date(DATE_ATOM) . ' , ' . json_encode($version) . "\n";
}

function getUpdatedVersion($req)
{
    $latest = '2024.02-28';

    $versionMap = array();
    $versionMap['dev'] = 'you-are-using-a-dev-build';
    $versionMap['2021-07-19'] = $latest;
    $versionMap['2021-11-19'] = $latest;
    $versionMap['2022-01-06'] = $latest;
    $versionMap['2023.12.01'] = $latest;
    $versionMap['2024.02.01'] = $latest;
    $versionMap['2024.02.27'] = $latest;
    $versionMap[$latest] = 'none'; // You are using the latest version.

    if (isset($versionMap[$req])) {
        return $versionMap[$req];
    }

    return 'none'; // You are using an unknown version.
}

function isJson()
{
    $headers = getallheaders();

    if (isset($headers['Content-Type'])) {
        if ($headers['Content-Type'] == 'application/json') {
            return true;
        }
    }

    return false;
}

try {
    if (!isJson()) {
        exit('<a href = "https://docs.olivetin.app/update-tracking.html">OliveTin Update Check Documentation</a>');
    }

    $req = parseVersionRequest();
        
    file_put_contents('checkins.log', storableVersionRequest($req), FILE_APPEND);

    echo getUpdatedVersion($req->CurrentVersion);
} catch (Exception $e) {
    echo $e;
}
