# PEESE-COVID19: New York State COVID-19 Health Crisis Mapping project
The project creates a dynamic map and trends dashboard webpage of NY state COVID-19 cases by county. 
![Preliminary Design]( https://github.com/PEESEgroup/PEESE-COVID19/blob/master/Capture.PNG
)

### Project URL

http://engineering.cornell.edu/covid-19map

http://www.coronavirus.peese.org/

## Files Description 

* [ny cases by county.csv](https://github.com/PEESEgroup/PEESE-COVID19/blob/master/ny%20cases%20by%20county.csv) – Dataset (will be updated daily)
* [ny cases by county-ls.csv](https://github.com/PEESEgroup/PEESE-COVID19/blob/master/ny%20cases%20by%20county%20-%20ls.csv) – Dataset with log scale

### Installing

A step by step examples that tell you how to get a development environment running

```
NYS Mapping Project Plotly App Setup (for Mac)
This article outlines how to set up the development environment of the PESSE NYS COVID 19 Mapping Project Plotly app. 

Pre-requisites
Command line interpreter
You will need to run all of these commands on a command line interpreter (ex. Terminal in Mac, Command Prompt in Windows)

Git
You will need Git installed on your computer. You can download Git here: https://git-scm.com/ 

Installation

1. Clone the Github repository in your Documents folder
    cd Documents
    git clone https://github.com/PEESEgroup/PEESE-COVID19.git


2. Now check that there is a folder named PEESE-COVID19 in your Documents folder. You can check it manually or run the following commands:
    cd Documents
    cd PEESE-COVID19/
    ls

 3. Install Python 3. 
 
 If you have Homebrew installed:

     homebrew python3

Alternatively, you can install Python 3 via https://www.python.org/downloads/

3. Install pip
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python get-pip.py

4. Install the modules used in the NYS Mapping Project Github. 

You can view what modules and packages they used by opening the app script in an IDE (such as VS Code). Go to your favorite IDE → Open a file and then select the PEESE - COVID19 folder → dash_app folder → app.py

Modules are individual objects of Python code and packages are a collection of modules (think of it as a library in other languages). The modules and packages are included into the file by writing:

    import module from package

Therefore, the modules included are:

- dash
- dash_core_components
- dash_html_components
- json
- pandas
- math
- datetime
- numpy

The packages included are: 

- requests
- urlopen
- dateutil

Run the following commands in the command line:

    pip3 install dash
    pip3 install dash_core_components
    pip3 install dash_html_components
    pip3 install pandas
    pip3 install requests
    pip3 install urlopen
    pip3 install python-dateutil --upgrade
    pip3 install numpy

5. Install plotly, by typing the following in the command line
    pip3 install plotly

6. Set up the development environment
     python3 -m venv venv

7. Run the app.

Make sure that your command line terminal is in the folder that the app.py is located in.

    cd Documents
    cd PEESE-COVID19/
    cd dash_app

    python3 app.py

8. Once you run the last command, the terminal will run the data analysis. It take upwards of 5 minutes.

9. At the end of the data analysis, the terminal will advise that the app is running on a specific URL. For example:
    
Copy the http link, open an Internet browser, paste it in your browser URL bar, and then navigate to it. 

```

## Deployment

Add additional notes about how to deploy this on a live website

## Data Sources

* [NY Department of Health]( https://coronavirus.health.ny.gov/county-county-breakdown-positive-cases) 
* [joeguinness]( https://github.com/joeguinness/covid19data/blob/master/ny_county_cases.csv)

## Contributing

## Versioning

## Authors

## License

## Acknowledgments

## Disclaimer

