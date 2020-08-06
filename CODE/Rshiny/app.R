#install.packages("jsonlite")
#install.packages("curl")
#install.packages("shinydashboard")
#install.packages("rjson")
#install.packages("graphics")

library(shiny)
library(shinydashboard)
library(kernlab)
library(kknn)
library(rworldmap)
library(dplyr)
library(forcats)
library(ggmap)
library(data.table)
library(RColorBrewer)
library(plotly)
library(shinycssloaders)
library(shinyjs)
library(rjson)
library(r2d3)

# Text Recommendation required libraries
library(DT)
library(jsonlite)


################
# Init / Globals
################

# Keep this to yourselves! 
ggmap::register_google(key = "")

# use readLines to get the data
dat <- readLines("winemag-lngs-lats-precip-temp.csv")

# i had to do this to fix grep errors
Sys.setlocale('LC_ALL','C')

# filter out the repeating, and wonky headers
dat_2 <- grep("Node Name,RTC_date", dat, invert=TRUE, value=TRUE)

# turn that vector into a text connection for read.csv
dat_3 <- read.csv(textConnection(paste0(dat_2, collapse="\n")),
                  header=FALSE, stringsAsFactors=FALSE, encoding="UTF-8")

# limit it to the 32 columns you want (Which matches)
dat_4 <- dat_3[,1:18]

# grab the headers
headers <- strsplit(dat[1], ",")[[1]]

# and add the headers
colnames(dat_4) <- headers

df <- as.data.frame(dat_4[,1:18])
df <- df[-c(1),]
rownames(df) <- seq(length=nrow(df)) 

df[1:100,c("latitude", "longitude")]

# Eliminate rows where latitude is null
df <- df[-which(df$latitude == ""), ]

# get distict varieties
#varietyDf <- df %>% distinct(variety)
#varietyDf <- setorder(varietyDf)
#varietyTypes <- c('Any',varietyDf)

# get distict regions
regionDf <- df %>% distinct(region_2)
regionDf <- setorder(regionDf)
regionTypes <- c('Select a region',regionDf)

# get distict score
#pointsDf <- df %>% distinct(points)
#pointsDf <- setorder(pointsDf)
#pointsTypes <- c('Any',pointsDf)

# get distict winery
wineryDf <- df %>% distinct(winery)
wineryDf <- setorder(wineryDf)
wineryTypes <- c('Select a winery',wineryDf)

#########
# UI
#########

ui <- dashboardPage(
  skin = "purple",
  dashboardHeader(
    title  = "Your Cork"
    
  ),
  dashboardSidebar(
    sidebarUserPanel(
      tags$div(class = "header2", tags$p("Big Data Knights")),
      tags$head(tags$style("p{color: black; font-size: 16px;} .header2 p{font-size: 15px; color: white}"))
    ),
    sidebarMenu(
      menuItem("About", tabName = "About", icon = icon("info")),
      menuItem("Map", tabName = "Map", icon = icon("map")),
      menuItem("Stats", tabName = "Stats", icon = icon("chart-line")),
      menuItem("Recommender", tabName = "Recommend", icon = icon("wine-glass-alt")),
      menuItem("Attribute Recommender", tabName = "Traits", icon = icon("file-text-o"))
    )
  ),
  
  dashboardBody(
    includeScript("d3.v5.min.js"),
    includeScript("d3-tip.min.js"),
    
    includeScript(path = "http://d3js.org/d3-scale-chromatic.v1.min.js"),
    includeScript(path = "topojson.v2.min.js"),
    includeScript(path = "d3-legend.js"),
    tags$head(
      tags$link(rel = "stylesheet", type = "text/css", href = "wineries.css")
    ),

    tabItems(

    tabItem(tabName = "About",
      tags$img(src="yourCork.jpg", height='20%', width='60%')
    ),
    tabItem(tabName = "Map",
      fluidRow(
        tabBox(
          id = "tabset1", height = "250px", width = '100%',
          tabPanel(
            "Explore",
            fluidRow(
              #d3Output("wineMap1")
              tag("svg", list(width="1150", height="700")),
              includeScript(path = "wineries.js"),
              style = "background-color:lightblue"
            )
          )
        )
      )),
      tabItem(tabName = "Stats",
            fluidRow(
              tabBox(
                id = "tabset1", height = "250px", width = '100%',
                tabPanel(
                  "Origin Count",
                  fluidRow(
                    tag("img", list(src="CountryOfWineOriginCount.png"))
                  )
                ),
                tabPanel(
                  "Price By Origin",
                  fluidRow(
                    tag("img", list(src="PriceByCountryWineOrigin.png"))
                  )
                ),
                tabPanel(
                  "Province Origin",
                  fluidRow(
                    tag("img", list(src="ProvinceOfWineOrigin.png"))
                  )
                ),
                tabPanel(
                  "Top 20",
                  fluidRow(
                    tag("img", list(src="Top20.png"))
                  )
                ),
                tabPanel(
                  "Top 20 Variety",
                  fluidRow(
                    tag("img", list(src="Top20Variety.png"))
                  )
                )
              )
            )),
      tabItem(tabName = "Recommend",
        fluidRow(
          column(
            width = 3,
            tabPanel(
              shinyjs::useShinyjs(),
              title = 'Search',
              textInput("txtWinery", "Winery", placeholder="Enter a winery", width="100%"),
              actionButton("action_winery_search", label = "Search Recommendations", style="margin-bottom: 20px", width="100%"),
              #selectInput("varietySelected", "Variety", varietyTypes),
              selectInput("regionSelected", "Region", regionTypes, width="100%"),
              #selectInput("pointSelected", "Points", pointsTypes),
              selectInput("winerySelected", "Winery", wineryTypes, width="100%"),
              shinyjs::disabled(actionButton("action_winery_select", label = "Find Recommendations", width="100%")),
              textOutput("selected_var"),
              style="margin-left: 20px"
            )
          ),
          column(width = 6, plotOutput("wineMap2", hover = hoverOpts(id ="plot_hover"))  %>% withSpinner(color="#0dc5c1", size = 2))
        ),
        fluidRow(
         column(width = 3,  shinyjs::hidden(verbatimTextOutput("hover_info")), style="margin-left: 20px")
        )
      ),
      tabItem(tabName = "Traits",
        fluidRow(
          textAreaInput("txtAttribute", "Describe your favorite wine:",
            value = "Fruity, Acidic, Oaky, Tannic, Sweet, Body",
            width = '600px', height = '75px'),
          style="margin-left: 20px"
        ),
        fluidRow(
          column(width = 11, height = '50%', DT::dataTableOutput("tbl"))
        ),
        fluidRow(
          style="margin-top: 20px",
          column(
            width = 11, 
            #plotOutput("plot"),
            d3Output("wineMap1"),
            verbatimTextOutput("devel")
          )
        )
    )
  ) # tabItems
  ) # dashboardBody
) # dashboardPage

#########
# SERVER
#########

server <- function(input, output, session) {

  v <- reactiveValues(data = NULL)
  
  obsEvent1 <- observeEvent(input$action_winery_select, {
    #shinyjs::show("wineMap2")
    latLng <- df[df['winery'] == input$winerySelected, c("latitude", "longitude")][1,]
    v$data <- latLng
  })
  
  obsEvent2 <- observeEvent(input$action_winery_search, {
    #shinyjs::show("wineMap2")
    g <- geocode(input$txtWinery)
    v$data <- c(g[2], g[1])
  })
  
  
  output$wineMap2 = renderPlot({
    if (is.null(v$data)) return()
    
    shinyjs::show("hover_info")
    
    cluster_num = 8
    num_clusters = 50
    
    withProgress(message = 'Making plot', value = 0, {
      
      incProgress(0.25, detail = paste("Doing kmeans clustering"))
      
      kmodel <- kmeans(df[1:nrow(df),c("latitude", "longitude")], num_clusters)
      
      i_lon = as.numeric(v$data[2])
      i_lat = as.numeric(v$data[1])
      
      incProgress(0.25, detail = paste("Finding nearest cluster"))
      
      min_dist = 99999.9
      for (i in (1:nrow(df))) {
        dist = sqrt((i_lon-as.numeric(df$longitude[i]))^2 + (i_lat-as.numeric(df$latitude[i]))^2)
        if (dist < min_dist) {
          min_dist = dist
          cluster_num <- as.numeric(kmodel[[1]][i])
        }
      }
      
      length(unique(round(as.numeric(df$longitude[which(as.numeric(kmodel[[1]])==cluster_num)]), 1)))
      
      # Show model summary
      kmodel
      kmodel[1]
      
      incProgress(0.25, detail = paste("Generating map"))
      
      # creating a sample data.frame with your lat/lon points
      lon <- as.numeric(df$longitude)
      lat <- as.numeric(df$latitude)
      df2 <<- as.data.frame(cbind(lon,lat))
      
      df2$cluster = as.numeric(kmodel[[1]])
      
      n <- num_clusters
      qual_col_pals = brewer.pal.info[brewer.pal.info$category == 'qual',]
      col_vector = unlist(mapply(brewer.pal, qual_col_pals$maxcolors, rownames(qual_col_pals)))
      colors <- sample(col_vector, n)
      
      avg_lat = mean(as.numeric(df$latitude[which(as.numeric(kmodel[[1]])==cluster_num)]))
      avg_lon = mean(as.numeric(df$longitude[which(as.numeric(kmodel[[1]])==cluster_num)]))
      
      mapgilbert <- get_map(location = c(lon = avg_lon, lat = avg_lat), 
                            zoom = calc_zoom(extendrange(df2$lon[which(df2$cluster==cluster_num)]), extendrange(df2$lat[which(df2$cluster==cluster_num)]), f = 0.05),
                            maptype = "roadmap", scale = 1, bg="transparent")
      
      incProgress(1, detail = paste("Done", i))
      
    })
    
    
    # plotting the map with some points on it
    ggmap(mapgilbert) +
      theme(axis.line = element_blank(),
            axis.text = element_blank(),
            axis.ticks = element_blank(),
            plot.margin = unit(c(0, 0, -1, -1), 'lines')) +
      xlab("") + ylab("") +
      geom_point(data = df2,  aes(x = lon, y = lat, fill = colors[df2$cluster], color = colors[df2$cluster], alpha = 0.8), extent = 'device', size = 3.5, shape = 21, show.legend = FALSE)
  }, height = 600, width = 800, bg="transparent")
  
  output$hover_info <- renderPrint({
    if(!is.null(input$plot_hover)){
      hover=input$plot_hover
      dist=sqrt((hover$x-df2$lon)^2+(hover$y-df2$lat)^2)
      cat("Wine stats:\n")
      if(min(dist) < 0.1)
        cat(cbind('Winery: ', df$winery[which.min(dist)], '\n'))
        cat(cbind('Variety: ', df$variety[which.min(dist)], '\n'))
        cat(cbind('Country: ', df$country[which.min(dist)], '\n'))
        cat(cbind('Price: ', df$price[which.min(dist)], '\n'))
        cat(cbind('Points: ', df$points[which.min(dist)], '\n'))
      #cat(cbind('Cluster: ', df2$cluster[which.min(dist)], '\n'))
    }
  })

  obs <- observe({
      # update winery dropdown when region changes
      wineryDf <- df[df['region_2'] == input$regionSelected, ]
      wineryDf <- wineryDf %>% distinct(winery)
      wineryDf <- setorder(wineryDf)
      wineryTypes <- c('Select a winery',wineryDf)
      updateSelectInput(session, "winerySelected", choices = wineryTypes)
  })
  
  obs2 <- observe({
    input$winerySelected
    if(input$winerySelected != "Select a winery"){ 
      shinyjs::enable("action_winery_select")
    } else {
      shinyjs::disable("action_winery_select")
    }
  })
  
  # ---- Attribute Recommendation Section ----------------------------
  
  output$tbl = DT::renderDataTable(DT::datatable({
    data <- datasetInput()
    data
  },selection = 'single'))
  
  proxy <- DT::dataTableProxy("tbl")
  
  get_API <- function(url) {
    print(url)
    df <- fromJSON(url)
    json_data_frame <- fromJSON(df)
    print(json_data_frame)
    json_data_frame
  }
  
  datasetInput <- reactive({
    
    intext=input$txtAttribute
    
    shiny::validate(
      need((input$txtAttribute) !='' , "Please express yourself in at least 75 Characters.")
    )
    
    url=paste("http://localhost:5002/wine?inputtext=",intext)
    withProgress(message = 'Fetching your Wine', value = 0, { get_API(URLencode(url)) })
  })
  
  output$devel <- renderPrint({
    req(length(input$tbl_cell_clicked) > 0)
    input$tbl_cell_clicked$value
    print(input$tbl_cell_clicked$value)
  })
  
  output$wineMap1 <- renderD3({
    r <- datasetInput()
    r2d3(data=c(list(
      price=r[, 2],
      score=r[, 3], 
      name=r[, 1]
    )),
    script = "graph.js")
  })
  
  #output$plot <- renderPlot({
  #  #df = datasetInput()
  #  hist(datasetInput()[, 2], col = 'forestgreen', border = 'white',
  #       main = "Histogram of Average Price of top 10 Wines.",
  #       xlab = "Avg Price ",)
  #})
  
}

# Create Shiny app ----
shinyApp(ui = ui, server = server)
