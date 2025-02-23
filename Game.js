const fs = require('fs');
const path = require('path');

const charactersFilePath = path.join(__dirname, 'data', 'characters.json');
const questsFilePath = path.join(__dirname, 'data', 'quests.json');

function loadCharacters() {
    const data = fs.readFileSync(charactersFilePath);
    return JSON.parse(data).characters;
}

function saveCharacter(character) {
    const characters = loadCharacters();
    characters.push(character);
    fs.writeFileSync(charactersFilePath, JSON.stringify({ characters }, null, 2));
}

function loadQuests() {
    const data = fs.readFileSync(questsFilePath);
    return JSON.parse(data).quests;
}

function saveQuest(quest) {
    const quests = loadQuests();
    quests.push(quest);
    fs.writeFileSync(questsFilePath, JSON.stringify({ quests }, null, 2));
}

// Beispiel für die Initialisierung eines Charakters
function createCharacter(name, faction) {
    const character = {
        name: name,
        faction: faction,
        attributes: { STR: 0, INT: 0, CHA: 0, DEX: 0 },
        inventory: [],
        xp: 0,
        currentQuest: null
    };
    saveCharacter(character);
}

// Beispiel für die Initialisierung eines Quests
function createQuest(title, description) {
    const quest = {
        title: title,
        description: description,
        completed: false
    };
    saveQuest(quest);
}

// Terminal-UI-Interaktion (z.B. mit readline)
const readline = require('readline').createInterface({
    input: process.stdin,
    output: process.stdout
});

// Beispiel für die Benutzerinteraktion
readline.question('Gib den Namen deines Charakters ein: ', (name) => {
    readline.question('Gib die Fraktion deines Charakters ein: ', (faction) => {
        createCharacter(name, faction);
        console.log(`Charakter ${name} erstellt!`);
        readline.close();
    });
}); 