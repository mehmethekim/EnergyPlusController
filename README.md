# EnergyPlus Controller

EnergyPlus is a powerful building energy simulation tool used to model the energy consumption of buildings and HVAC systems. This repository contains an EnergyPlus Controller that provides an API for interacting with EnergyPlus simulations and a Reinforcement Learning Controller for optimizing building energy performance.

## Table of Contents

- [EnergyPlus Controller](#energyplus-controller)
  - [Table of Contents](#table-of-contents)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
  - [EnergyPlus Controller API](#energyplus-controller-api)
  - [Reinforcement Learning Controller](#reinforcement-learning-controller)

## Getting Started

### Prerequisites

Before using the EnergyPlus Controller, ensure you have the following installed on your system:

- [EnergyPlus](https://energyplus.net/downloads)
- Python 3.x
- Virtual Environment (optional but recommended)

### Installation

1. Clone this repository:

   ```shell
   git clone https://github.com/yourusername/energyplus-controller.git
   ```
2. Navigate to the project directory:
     ```shell
   cd energyplus-controller
   ```
3. Create a Python virtual environment (optional but recommended):
    ```shell
   python -m venv venv
   ```
   or
    ```shell
   python3 -m venv venv
   ```
4. Activate the virtual environment:
- On macOS/Linux:

    ```shell
   source venv/bin/activate
   ```
- On Windows (PowerShell):
   ```shell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   env\Scripts\activate
   ```
5. Install the required Python packages:
```shell
   pip install -r requirements.txt
   ```
## EnergyPlus Controller API

The EnergyPlus Controller API allows you to interact with EnergyPlus simulations programmatically. It provides functions to run simulations, retrieve results, and control HVAC systems within a building model.

## Reinforcement Learning Controller
The Reinforcement Learning Controller demonstrates how to use reinforcement learning techniques to optimize building energy performance using EnergyPlus simulations. It includes example RL agents and environments for training and evaluating RL controllers.