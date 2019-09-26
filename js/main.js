var winRateContainer = document.getElementById("win-rate");

var ourRequest = new XMLHttpRequest();
ourRequest.open('GET', '../data/matches/matches1.json');
ourRequest.onload = function () {
    var ourData = JSON.parse(ourRequest.responseText);
    getWinRate(ourData);
};
ourRequest.send();

function getWinRate(data) {
    var champion = 67;
    var matches = 0;
    var wins = 0;

    var i;
    var j;
    for (i = 0; i < data.length; i++) {
        for (j = 0; j < 10; j++) {
            if (data[i].participants[j].championId == champion && data[i].participants[j].teamId == 100) {
                matches++;
                if (data[i].teams[0].win == "Win") {
                    wins++;
                }
            }
            if (data[i].participants[j].championId == champion && data[i].participants[j].teamId == 200) {
                matches++;
                if (data[i].teams[1].win == "Win") {
                    wins++;
                }
            }
        }
    }

    var winrate = (wins / matches) * 100;

    winRateContainer.insertAdjacentHTML('beforeend', 'Win Rate: ' + winrate + '%')
}