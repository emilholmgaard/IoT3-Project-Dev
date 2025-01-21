
# IoT3-Project-Dev

This project is part of the IoT3 ecosystem, comprising multiple components that work together to deliver a complete IoT solution.

## Table of Contents
- [app-api-pi0-receiver](#app-api-pi0-receiver)
- [app-pi4-transmitter](#app-pi4-transmitter)
- [webapp-pi0](#webapp-pi0)
- [nginx](#nginx)
- [3A7_SmartHealth.pdf](#3a7_smarthealthpdf)
- [3A7_SmartHealth_Stykliste.xlsx](#3a7_smarthealth_styklistexlsx)

## app-api-pi0-receiver

This component is responsible for receiving data from various sources and processing it accordingly.

### Requirements
- **Python 3** must be installed.
- A virtual environment is recommended for managing dependencies.

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/emilholmgaard/IoT3-Project-Dev.git
   cd IoT3-Project-Dev/app-api-pi0-receiver/src
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python app.py
   ```

## app-pi4-transmitter

This component is responsible for transmitting data to other devices or systems.

### Requirements
- **Python 3** must be installed.
- A virtual environment is recommended for managing dependencies.

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/emilholmgaard/IoT3-Project-Dev.git
   cd IoT3-Project-Dev/app-pi4-transmitter/src
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python main.py
   ```

## webapp-pi0

This component is a web application that provides a user interface for the system.

### Requirements
- **Node.js** and **npm** must be installed.

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/emilholmgaard/IoT3-Project-Dev.git
   cd IoT3-Project-Dev/webapp-pi0/src
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

4. For production, build the application:
   ```bash
   npm run build
   ```

## nginx

This directory contains configuration files for the Nginx web server.

## 3A7_SmartHealth.pdf

This PDF file includes documentation or specifications related to the SmartHealth project.

## 3A7_SmartHealth_Stykliste.xlsx

This Excel file contains a bill of materials for the SmartHealth project, specifying the required components and materials.

For additional information, please refer to the respective directories and files in the repository.
