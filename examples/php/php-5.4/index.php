<!DOCTYPE html>

<head>
  <meta charset='UTF-8'>
</head>
<html>
<style>
  #myProgress {
    width: 100%;
    background-color: #ddd;
  }

  #myBar {
    width: 1%;
    height: 30px;
    background-color: #04AA6D;
  }
</style>

<body>

  <form action="index.php" method="post" enctype="multipart/form-data">
    Select file to upload:
    <input type="file" name="selected-file" id="selected-file">
    <input type="submit" value="Upload" name="submit">
  </form>

  <?php
  session_start();
  if (!isset($_FILES['selected-file'])) {
    return;
  }
  // selected file by user
  $selectedFile = $_FILES['selected-file'];
  // check if file exists
  if ($selectedFile["name"] != "") {

    if (isset($_SESSION['auth_token'])) {

      // ---------------------------------------------- Get retrieve user info --------------------------------------------
      $ch = curl_init();
      $curl_url = "https://accounting.persianspeech.com/account/retrieve";
      // request config
      curl_setopt($ch, CURLOPT_URL, $curl_url);
      curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false);
      curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
      curl_setopt($ch, CURLOPT_HTTP_VERSION, CURL_HTTP_VERSION_1_1);
      curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "GET");
      curl_setopt($ch, CURLOPT_HTTPHEADER, array('Authorization: token ' . $_SESSION['auth_token'], 'accept: application/json', 'Content-Type: application/json'));
      curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
      // server response
      $server_result = curl_exec($ch);
      $jsonData = json_decode($server_result, true);
      if ($jsonData['username']) {
      } else {
        unset($_SESSION['auth_token']);
      }
      curl_close($ch);
    }
    if (!isset($_SESSION['auth_token'])) {
      // Request Body
      $credentials = array(
        'username_or_phone_or_email' => "Your username", // Enter Your username
        'password' => "Your password", // Enter Your password
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
      $_SESSION['api_key'] = $jsonData['user']['nevisa_service_account']['current_service_record']['key'];
    }
    // ----------------------------------------------- UPLOAD FILE -----------------------------------------------------------
    // Request Body
    $audio_upload_val = array(
      'api_key' => $_SESSION['api_key'],
      'auth_token' => $_SESSION['auth_token'],
      'save_transcription' => "false",
      //'file' => new CurlFile($selectedFile['tmp_name'], $selectedFile['type'], $selectedFile['name'])      
      'file' => "@" . $selectedFile['tmp_name']
        . ";type=" . $selectedFile['type']
        . ";filename=" . $selectedFile['name']
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

    $_SESSION['progress_url'] = "https://api.persianspeech.com" . $jsonData['progress_url'];
  }
  ?>
  <div id="myProgress">
    <div id="myBar"></div>
  </div>
  <div dir='rtl' id="result">
  </div>
  <br>
  <script type='text/javascript'>
    async function get_progress(url) {
      return await fetch(url)
        .then((response) => {
          return response.json()
        })
        .catch(error => {
          console.error(error);
        });
    }
    var progress_url = "<?php echo $_SESSION['progress_url'] ?>";
    move(progress_url);

    function move(url) {
      var elem = document.getElementById("myBar");
      let width;
      let txt;
      get_progress(url).then((data) => {
        width = data['progress']['percent'];
      });
      var id = setInterval(frame, 100);

      function frame() {
        elem.style.width = width + "%";
        if (width >= 100) {
          clearInterval(id);
          get_progress(url).then((data) => {
            if (data['state'] == 'SUCCESS') {
              document.getElementById("result").innerHTML = data['result']['transcription']['text'];
            }
          });
        } else {
          get_progress(url).then((data) => {
            width = data['progress']['percent'];
          });
        }
      }
    }
  </script>

</body>

</html>