function rollDice(numDice) {
    return Array(numDice).fill(0).map(() => Math.floor(Math.random() * 6) + 1);
}

// Neue Funktion zum Speichern der Würfelergebnisse
function saveRollResults(actionDice, dangerDice) {
    const results = {
        actionDice: actionDice,
        dangerDice: dangerDice,
        highestRemaining: Math.max(...actionDice.filter(d => !dangerDice.includes(d)))
    };
    return results;
}

function executeDiceRolls() {
    const actionDice = rollDice(3);
    const dangerDice = rollDice(1);

    console.log("Action Dice:", actionDice);
    console.log("Danger Dice:", dangerDice);

    const results = saveRollResults(actionDice, dangerDice);
    console.log("Ergebnisse:", results);
}

// Aufruf der Funktion, um die Würfelwürfe auszuführen
executeDiceRolls();