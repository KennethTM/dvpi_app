
function upload_image() {

    var file = document.getElementById('imageUpload').files[0];
    let data = new FormData();
    data.append('file', file);

    fetch('https://dvpi.herokuapp.com/predict', {
        method: 'POST',
        body: data
    }).then(response => response.json())
    .then(data => document.getElementById('dvpi_art').textContent = `Resultat = ` + data.response)
    .then(data => console.log(data))
}