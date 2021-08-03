<?php
  error_reporting(E_ALL);
  ini_set("display_errors", "On");

  function randnumb($length = 3) {
    return substr(str_shuffle(str_repeat($x='0123456789', ceil($length/strlen($x)) )),1,$length);
  }

  $max_text = 300;
  $num_images = 6;
  $top_text = "{empty}";
  $middle_text = "{empty}";
  $bottom_text = "{empty}";
  $color_1 = "#ffffff>";
  $color_2 = "#ffffff>";
  $color_3 = "#ffffff>";

  if($_FILES["file"]["name"] == "") {
    echo "No image was provided.";
    exit(0);
  }

  if($_FILES["file"]["size"] > 9999999) {
    echo "File is too large.";
    exit(0);
  }

  if(isset($_POST["top_text"])) {
    $top_text = addslashes(trim($_POST["top_text"]));
  }

  if(isset($_POST["middle_text"])) {
    $middle_text = addslashes(trim($_POST["middle_text"]));
  }

  if(isset($_POST["bottom_text"])) {
    $bottom_text = addslashes(trim($_POST["bottom_text"]));
  }

  if($top_text == "") {
    $top_text = "{empty}";
  }

  if($middle_text == "") {
    $middle_text = "{empty}";
  }

  if($bottom_text == "") {
    $bottom_text = "{empty}";
  }

  if($top_text == "{empty}" and $middle_text == "{empty}" and $bottom_text == "{empty}") {
    echo "No text provided.";
    exit(0);
  }

  if(strlen($top_text) > $max_text) {
    echo "Text is too long.";
    exit(0);
  }

  if(strlen($middle_text) > $max_text) {
    echo "Text is too long.";
    exit(0);
  }

  if(strlen($bottom_text) > $max_text) {
    echo "Text is too long.";
    exit(0);
  }

  if(isset($_POST["color_1"])) {
    $color_1 = trim($_POST["color_1"]);
  }

  if(isset($_POST["color_2"])) {
    $color_2 = trim($_POST["color_2"]);
  }

  if(isset($_POST["color_3"])) {
    $color_3 = trim($_POST["color_3"]);
  }

  $fname = basename($_FILES["file"]["name"]);
  $ext = pathinfo($fname)["extension"];
  $fname2 = time() . "_" . randnumb() . "." . $ext;
  $target = "uploads/" . $fname2;

  if (move_uploaded_file($_FILES["file"]["tmp_name"], $target)) {
    $date1 = microtime(true);

    try {
      $cmd = 'python3 rigga.py "' . $target . '" "' . $top_text
        . '" "' . $middle_text . '" "' . $bottom_text 
        . '" "' . $color_1 . '" "' . $color_2 . '" "' . $color_3 . '" '. $num_images;
    } catch (Exception $e) {
      unlink($target);
      exit(0);
    }

    $paths = explode(" ", exec($cmd));
    $date2 = microtime(true);

    $style = "body, html {
      font-family: sans-serif;
      background-color: rgb(101, 59, 199);
      color: #FF2D40;
    } 
    
    .item {
      display: inline-block;
      padding: 20px;
    } 
    
    .title {
      padding-bottom: 5px;
      display: block;
    }

    .image {
      max-height: 800px;
      max-width: 800px;
    }
    
    .info {
      margin-left: 20px;
      margin-right: 20px;
      margin-top: 20px;
      margin-bottom: 15px;
      padding: 5px;
      background-color: #dfe4fb;
    }";

    $topheader = "<title>Rigga Result</title>
    <meta http-equiv='Content-Type' content='text/html; charset=utf-8'>
    <link rel='shortcut icon' href='beebs.jpg?v=1' type='image/x-icon'>";

    $diff = round(($date2 - $date1), 2);
    $seconds = "seconds";

    if($diff == 1) {
      $seconds = "second";
    }

    echo "<head>" . $topheader . "<style>" . $style . "</style></head>";
    echo "<div class='info'>Rig done in " . $diff . " " . $seconds . "</div>";

    try {
      for ($i = 0; $i < count($paths); $i++) {
        echo "<div class='item'><div class='title'>Size: " . round(filesize($paths[$i]) / 1024 / 1024, 2) . " MiB</div>";
        $data = file_get_contents($paths[$i]);
        echo "<img class='image' src='data:" . mime_content_type($paths[$i]) . ";base64," . base64_encode($data) . "'></div>";
      }
    } catch (Exception $e) {
      cleanup();
      exit(0);
    }

    cleanup();
  } else {
    echo "There was an error uploading the image.";
  }
  
  function cleanup() {
    global $target;
    global $paths;

    unlink($target);

    for ($i = 0; $i < count($paths); $i++) {
      unlink($paths[$i]);
    }
  }
?>