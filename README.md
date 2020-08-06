# Your Cork (Big Data Knights)

### DESCRIPTION
This application consists of two parts. A lightweight python api (/Code/SentimentAnalysis) linked to a sentiment analysis model
and an RShiny application (/Code/Rshiny). The api will be used by the RShiny application and will not need to interacted with directly.
The RShiny application consists of a web GUI in which to interact with the various visualizations.

The /Code/Scripts directory contains several scripts that were used for cleaning and modifying the dataset as described in the report. Each takes in a source csv and outputs a csv with appended columns. These scripts are included for reference but do not need to executed in order to run the application.

The /Doc directory contains final report and presentation poster

### INSTALLATION

##### Download data
There are three larger data files that must be downloaded in order to run the application.

1. sa.mdl (download to /Code/SentimentAnalysis)
https://drive.google.com/open?id=1R3xpXtmFgy3Q_wbzwFXUFXII_JAFsG6Z

2. winemag-data-139k-v2.csv (download to /Code/SentimentAnalysis/input) 
https://drive.google.com/open?id=1BZgE7d_b-tUx-7hNwiOGs6D_WmyD3V8M
[Code](https://github.com/mjshrestha/web_scraper)]

3. winemag-lngs-lats-precip-temp.csv (download to /Code/Rshiny) 
https://drive.google.com/open?id=13P5aSj_MIjjl4IXB0ll2S3wXTMQlk7mu
[Ref Code](https://github.com/mjshrestha/topojson)] and [[Csv code](https://github.com/mjshrestha/data/tree/master/Scripts)]

##### Setup R Environment
1. Install R and RStudio - https://www.rstudio.com/products/RStudio/
2. From R session console, run the following command to install dependencies:
    `install.packages(c("shiny", "shinydashboard", "ggmap", "kernlab", "kknn", "rworldmap", "dplyr", "forcats", "data.table", "RColorBrewer", "plotly", "shinycssloaders", "shinyjs", "rjson", "jsonlite", "curl", "graphics", "DT", "r2d3"))`

##### Setup Python Environment
1. Install latest version of python 3
2. cd /SentimentAnalysis
3. Run `pip install -r requirements.txt`

### EXECUTION
##### Start Wine API
1. cd /SentimentAnalysis
2. Run `python wineAPI.py`

##### Start RShiny App
1. Launch R Studio
2. Open app.R
3. Click "Run App"
4. Click "Open in Browser" and test there for best results
