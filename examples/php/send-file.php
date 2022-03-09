<?php
session_start();

// a simple interval function to get status of file processing progress
function setInterval($f, $milliseconds, $addiotionalArgs)
{
    $seconds = (int)$milliseconds / 1000;
    while (true) {
        $f($addiotionalArgs);
        sleep($seconds);
    }
}

// selected file by user
$selectedFile = $_FILES['selected-file'];

// check if file exists
if ($selectedFile["name"] != "") {

    // ---------------------------------------------- Get auth token if not exist --------------------------------------------

    if (!isset($_SESSION['auth_token']) && empty($_SESSION['auth_token'])) {
        // Request Body
        $credentials = array(
            'username_or_phone_or_email' => "YOUR USERNAME HERE",
            'password' => "YOUR PASSWORD HERE",
        );

        // curl connection
        $ch = curl_init();
        // set curl url connection
        $curl_url = "https://accounting.persianspeech.com/account/login";
        // request config
        curl_setopt($ch, CURLOPT_URL, $curl_url);
        curl_setopt($ch, CURLOPT_POST, 1);
        curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false);
        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
        curl_setopt($ch, CURLOPT_POSTFIELDS, $credentials);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

        // server response
        $server_result = curl_exec($ch);
        curl_close($ch);

        // convert server response to json object like
        $jsonData = json_decode($server_result, true);

        $_SESSION['auth_token'] = $jsonData['user']['token'];
    }

    // ----------------------------------------------- UPLOAD FILE -----------------------------------------------------------

    // Request Body
    $audio_upload_val = array(
        'api_key' => "YOUR API KEY HERE",
        'auth_token' => $_SESSION['auth_token'],
        'save_transcription' => "false",
        'file' => new CurlFile($selectedFile['tmp_name'], $selectedFile['type'], $selectedFile['name'])
    );

    // Request Auth Header
    $header = array(
        'Authorization' => 'token ' . $_SESSION['auth_token']
    );

    // curl connection
    $ch = curl_init();
    // set curl url connection
    $curl_url = "https://api.persianspeech.com/recognize-file";
    // request config
    curl_setopt($ch, CURLOPT_URL, $curl_url);
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    curl_setopt($ch, CURLOPT_HTTPHEADER, $header);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $audio_upload_val);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

    // server response
    $server_result = curl_exec($ch);
    curl_close($ch);

    // convert server response to json object like
    $jsonData = json_decode($server_result, true);

    // ----------------------------------------------- CELERY -----------------------------------------------------------

    // interval with 5 sec period to check the status of file proccess
    setInterval(function ($jsonData) {

        // request header
        $header = array(
            'Authorization' => 'token ' . $_SESSION['auth_token']
        );
        // curl connection
        $ch = curl_init();
        // set curl url connection
        $curl_url = "https://api.persianspeech.com";
        // request config
        curl_setopt($ch, CURLOPT_URL, $curl_url . $jsonData['progress_url']);
        curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false);
        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
        curl_setopt($ch, CURLOPT_HTTPHEADER, $header);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        $server_result = curl_exec($ch);
        curl_close($ch);

        // convert server response to json object like
        $jsonData = json_decode($server_result, true);

        // check if file process is complete in each interval
        if ($jsonData['complete'] == true) {

            // return transcription and exit
            echo json_encode($jsonData['result']['transcription']);
            exit();
        }
    }, 5000, $jsonData);
} else {

    // file is empty
    $response = array(
        'status' => "error",
        'message' => "you must select a file"
    );

    echo json_encode($response);
}
