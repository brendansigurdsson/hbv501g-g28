var xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
        var response = JSON.parse(xhttp.responseText);
        console.log(response.matches);
    }
};
xhttp.open("GET", "../data/matches/matches1.json", true);
xhttp.send();