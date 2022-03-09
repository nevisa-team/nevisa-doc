<!DOCTYPE html>
<html lang="fa">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <link rel="stylesheet" href="index.css" />
</head>

<body dir="rtl">
    <div class="container">
        <div class="content">
            <div>
                <input type="file" id="file-test" title="Select File" />
            </div>
            <div>
                <p id="result"></p>
            </div>
        </div>
    </div>
</body>

<script>
    const fileInput = document.getElementById('file-test');
    const paragraph = document.getElementById('result');

    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        const formData = new FormData();

        paragraph.innerText = "در حال بارگذاری...";

        if (file) {
            formData.append('selected-file', file);

            fetch('send-file.php', {
                method: 'POST',
                body: formData
            }).then(response => {
                return response.text();
            }).then(result => {
                const transcription = JSON.parse(result)
                paragraph.innerText = transcription.text;
            }).catch(error => {
                console.log(error);
            })
        }
    })
</script>

</html>