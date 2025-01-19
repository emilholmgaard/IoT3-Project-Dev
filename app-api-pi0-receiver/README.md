## Opsætning af app-api-pi0-receiver

### Krav

- **Python 3** skal være installeret.
- Du skal bruge et virtuelt miljø til at installere afhængighederne. (Brug `venv` for at oprette et virtuelt miljø)

### Trin 1: Klon repositoryet til din Raspberry Pi
1. Klon dette repository:
   ```bash
   git clone https://github.com/holmek/IoT3-Software-Development-Project.git
   cd IoT3-Software-Development-Project
   cd app-api-pi0-receiver
   cd src
   ```

2. Opret og aktiver et virtuelt miljø:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # På Windows: venv\\Scripts\\activate
   ```

3. Installer Python-afhængighederne:
   ```bash
   pip install -r requirements.txt
   ```

4. Kør applikationen:
   ```bash
   python app.py
   ```
