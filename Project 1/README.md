# CPSC 449 Project-1
## Spencer DeMera & Ricardo Segarra

## Project Description:
* This project takes user input from the python command line, requested data from the FOAAS API, censors it with the PurgoMalum API, and returns the data as dynamically generated HTML. 
* This project makes use of FOAAS
    * All FOAAS paths and documentation : https://foaas.com/

## Contents:
* File README.md. README file for the project.<br>
* File redact.py. Main program file for the project.

## Installation & Running
* Unpack the .tar.gz file into a new folder.
* Open a terminal or command prompt.
* Enter the redact.py file & add a FOAAS API path via `python3 redact.py /path/from`
    * Example `python3 redact.py /because/Joe`
* Output should display localhost port.
* Open a broswer window and go to `localhost:<given PORT number>`
* Complete the browser query with desired FOAAS path.
    * Example `localhost:8080/because/name`

## Errors & Bugs
* Server displays Python `UnicodeDecodeError: 'utf-8' codec can't decode byte 0x8b in position 62: invalid start byte`
    * This is due to included html/bootstrap from FOAAS output server
    * (Not sure hot to resolve issue: insufficient time)
