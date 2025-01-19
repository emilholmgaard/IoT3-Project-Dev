
## Opsætning af webapp-pi0

### Krav

- **Node.js** og **npm** (Node Package Manager) skal være installeret. Du kan installere dem via [Node.js' officielle hjemmeside](https://nodejs.org/) eller ved at bruge [Homebrew](https://brew.sh/) på macOS.

### Trin 1: Klon repositoryet til din Raspberry Pi
1. Klon dette repository:
   ```bash
   git clone https://github.com/holmek/IoT3-Software-Development-Project.git
   cd IoT3-Software-Development-Project
   cd webapp-pi0
   cd src
   ```

2. Installer Node.js afhængighederne:
   ```bash
   npm install
   ```

3. Start udviklingsserveren:
   ```bash
   npm run dev
   ```

   Hvis applikationen skal bruges med Nginx eller en anden webserver, kan du bygge applikationen for produktion:
   ```bash
   npm run build
   ```

### Trin 2: Gentag processen
Hvis du ønsker at klone projektet igen eller arbejde på en ny kopi, skal du følge disse trin:

1. Klon projektet:
   ```bash
   git clone https://github.com/holmek/IoT3-Software-Development-Project.git
   cd IoT3-Software-Development-Project
   cd webapp-pi0
   cd src
   ```

2. Installer afhængighederne:
   ```bash
   npm install
   ```

3. Byg applikationen for produktion:
   ```bash
   npm run build
   ```
