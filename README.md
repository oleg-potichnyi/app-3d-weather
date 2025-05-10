# 3D Weather Desktop App

This project is a desktop application built using PyQt5 and OpenGL. It combines interactive 3D graphics (a rotatable cube) with real-time weather data fetched from the wttr.in API.

## Features

* Displays an interactive 3D cube inside a window.
* Allows users to rotate the cube with the mouse and zoom with the mouse wheel.
* Includes a reset button to return the cube to its original position.
* Adds basic lighting to the scene.
* Allows the user to choose a color for each of the cube's faces.
* Fetches and displays current weather using an HTTP request.
* Periodically updates the weather data using a timer.

## Technology stack

* Language: Python 3
* GUI Framework: PyQt5
* 3D Graphics: OpenGL (via PyOpenGL)
* HTTP Requests: requests
* Weather API: wttr.in

## Installation

### Prerequisites

* Python 3.7+
* pip (Python package installer)

### Setup

#### Clone this repository:
* git clone https://github.com/oleg-potichnyi/app-3d-weather
* cd app-3d-weather

#### Install required dependencies: 
* pip install -r requirements.txt

## Usage

### Run the application by executing:

* python main.py

### This will:

* Open a window displaying a 3D cube.
* Allow you to interact with the cube.
* Automatically fetch and display current weather data.
* Update the weather periodically.
