document.addEventListener('DOMContentLoaded', function() {
    var socket = io.connect('http://' + document.domain + ':' + location.port);

    var modal = document.getElementById("matchModal");
    var span = document.getElementsByClassName("close")[0];
    var scoresDiv = document.getElementById('scores');
    var matches = [];

    function displayMatches() {
        scoresDiv.innerHTML = '';
        matches.forEach(data => {
            const matchDiv = document.createElement('div');
            matchDiv.classList.add('match');
            matchDiv.innerHTML = `
                <h2>${data.event_home_team} vs ${data.event_away_team}</h2>
                <p>Date: ${data.event_date}</p>
                <p>Time: ${data.event_time}</p>
                <p>Final Result: ${data.RawData.event_final_result}</p>
            `;
            matchDiv.onclick = function() {
                showMatchDetails(data);
            };
            scoresDiv.append(matchDiv);
        });
    }

    function showMatchDetails(data) {
        document.getElementById('modalTitle').innerText = `${data.event_home_team} vs ${data.event_away_team}`;
        document.getElementById('modalDate').innerText = `Date: ${data.event_date}`;
        document.getElementById('modalTime').innerText = `Time: ${data.event_time}`;
        document.getElementById('modalResult').innerText = `Final Result: ${data.RawData.event_final_result}`;

        // Display goalscorers
        const goalscorersDiv = document.getElementById('modalGoalscorers');
        goalscorersDiv.innerHTML = '';
        if (data.RawData.goalscorers && data.RawData.goalscorers.length > 0) {
            const goalscorersTitle = document.createElement('h3');
            goalscorersTitle.innerText = 'Goalscorers:';
            goalscorersDiv.appendChild(goalscorersTitle);
            data.RawData.goalscorers.forEach(scorer => {
                const scorerDetail = document.createElement('p');
                scorerDetail.innerText = `${scorer.away_scorer || scorer.home_scorer} (${scorer.away_assist || scorer.home_assist}) - ${scorer.time}`;
                goalscorersDiv.appendChild(scorerDetail);
            });
        } else {
            goalscorersDiv.innerHTML = '<p>No goalscorers available.</p>';
        }

        // Display statistics
        const statisticsDiv = document.getElementById('modalStatistics');
        statisticsDiv.innerHTML = '<h3>Statistics:</h3>';
        if (data.RawData.statistics && data.RawData.statistics.length > 0) {
            data.RawData.statistics.forEach(stat => {
                const statDetail = document.createElement('div');
                statDetail.classList.add('stat-item');
                statDetail.innerHTML = `<span>${stat.type}:</span> <span>Home - ${stat.home}, Away - ${stat.away}</span>`;
                statisticsDiv.appendChild(statDetail);
            });
        } else {
            statisticsDiv.innerHTML += '<p>No statistics available.</p>';
        }

        // Display lineups
        const lineupsDiv = document.getElementById('modalLineups');
        lineupsDiv.innerHTML = '<h3>Lineups:</h3>';
        if (data.RawData.lineups) {
            lineupsDiv.innerHTML += '<h4>Home Team:</h4>';
            data.RawData.lineups.home_team.starting_lineups.forEach(player => {
                const playerDetail = document.createElement('p');
                playerDetail.innerText = `${player.player} (#${player.player_number}) - ${player.player_position}`;
                lineupsDiv.appendChild(playerDetail);
            });
            lineupsDiv.innerHTML += '<h4>Away Team:</h4>';
            data.RawData.lineups.away_team.starting_lineups.forEach(player => {
                const playerDetail = document.createElement('p');
                playerDetail.innerText = `${player.player} (#${player.player_number}) - ${player.player_position}`;
                lineupsDiv.appendChild(playerDetail);
            });
        } else {
            lineupsDiv.innerHTML += '<p>No lineups available.</p>';
        }

        // Display substitutes
        const substitutesDiv = document.getElementById('modalSubstitutes');
        substitutesDiv.innerHTML = '<h3>Substitutes:</h3>';
        if (data.RawData.substitutes && data.RawData.substitutes.length > 0) {
            substitutesDiv.innerHTML += '<h4>Home Team:</h4>';
            data.RawData.lineups.home_team.substitutes.forEach(player => {
                const playerDetail = document.createElement('p');
                playerDetail.innerText = `${player.player} (#${player.player_number}) - ${player.player_position}`;
                substitutesDiv.appendChild(playerDetail);
            });
            substitutesDiv.innerHTML += '<h4>Away Team:</h4>';
            data.RawData.lineups.away_team.substitutes.forEach(player => {
                const playerDetail = document.createElement('p');
                playerDetail.innerText = `${player.player} (#${player.player_number}) - ${player.player_position}`;
                substitutesDiv.appendChild(playerDetail);
            });
        } else {
            substitutesDiv.innerHTML += '<p>No substitutes available.</p>';
        }

        modal.style.display = "block";
    }

    span.onclick = function() {
        modal.style.display = "none";
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }

    // Fetch initial data
    fetch('/initial_data')
        .then(response => response.json())
        .then(data => {
            matches = data;
            matches.sort((a, b) => new Date(`${a.event_date} ${a.event_time}`) - new Date(`${b.event_date} ${b.event_time}`));
            displayMatches();
        });

    socket.on('new_data', function(data) {
        matches.push(data);
        matches.sort((a, b) => new Date(`${a.event_date} ${a.event_time}`) - new Date(`${b.event_date} ${b.event_time}`));
        displayMatches();
    });
});
