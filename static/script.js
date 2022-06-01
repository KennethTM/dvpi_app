
function parse_csv() {

    var file = document.getElementById('fileUpload').files[0];

    Papa.parse(file, { 
        header: true,
        complete: function(results) {
          var data = results.data;
          
          console.log(JSON.stringify(data))
        
          fetch("https://dvpi.herokuapp.com/dvpi", {
            method: "POST",
            headers: {'Content-Type': 'application/json', 'accept': 'application/json'}, 
            body: JSON.stringify(data)
          }).then(response => response.text())
          .then(data => document.getElementById('content').textContent = `Resultat = ` + data)
          .then(data => console.log(data));

          //document.getElementById('content').textContent = `Resultat = ${result}`
      }
    });

}
