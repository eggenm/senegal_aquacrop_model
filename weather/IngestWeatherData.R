library(zoo)
library(readxl)
library(readr)
library(dplyr)
library(tidyr)
library(apsimx)
require(nasapower)
library(chirps)
library(lubridate)
library(ggplot2)
library(patchwork)
require(XML)
require(Hmisc)
library(tidyverse)
library(ggrepel) 
library(DescTools)

######TEST CHIRPS IS UP###########################
lonlat <- data.frame(lon = c(-55.0281,-54.9857),
                     lat = c(-2.8094, -2.8756))

dates <- c("2017-12-15", "2017-12-31")

dt <- get_chirps(lonlat, dates)

dt

###############################################

#Define our sites
setwd('C:\\SenegalGIS\\VegIndicesAnalysis\\')
#lonlat<-read.csv('sites.csv')%>%filter(is_agriculture>0)%>%select(lon, lat, site)

lonlat <- data.frame(site = c("Bambey","Nioro du Rip", "Boudi", "Axum", "Hawzen"),
                     lon  = c(-16.4583, -15.7733,-15.5, 38.5, 39.5 ),
                     lat  = c(14.6965, 13.7437,15.5, 14, 13.5  ))
chirps_input = data.frame(lon=lonlat$lon, lat=lonlat$lat )
lonlat<-split(lonlat, lonlat$site)
chirpsdata1980<-lapply(lonlat, function(x) 
  get_chirps(data.frame(lon=x$lon, lat = x$lat),c("1981-01-02","1984-12-31") ) )
chirpsdata1985<-lapply(lonlat, function(x) 
  get_chirps(data.frame(lon=x$lon, lat = x$lat),c("1985-01-01","1989-12-31") ) )

chirpsdata1990<-lapply(lonlat, function(x) 
  get_chirps(data.frame(lon=x$lon, lat = x$lat),c("1990-01-01","1994-12-31") ) )
chirpsdata1995<-lapply(lonlat, function(x) 
  get_chirps(data.frame(lon=x$lon, lat = x$lat),c("1995-01-01","1999-12-31") ) )

chirpsdata2000<-lapply(lonlat, function(x) 
  get_chirps(data.frame(lon=x$lon, lat = x$lat),c("2000-01-01","2004-12-31") ) )
chirpsdata2005<-lapply(lonlat, function(x) 
  get_chirps(data.frame(lon=x$lon, lat = x$lat),c("2005-01-01","2009-12-31") ) )

chirpsdata2010<-lapply(lonlat, function(x) 
  get_chirps(data.frame(lon=x$lon, lat = x$lat),c("2010-01-01","2014-12-31") ) )
chirpsdata2015<-lapply(lonlat, function(x) 
  get_chirps(data.frame(lon=x$lon, lat = x$lat),c("2015-01-01","2020-12-31") ) )



#Use package apsimx to request the weather data from NASA
met1980<-lapply(lonlat, function(A)  get_power_apsim_met(lonlat =c(mean(A$lon),
                                                                   mean(A$lat ) ),
                                                         dates = c("1981-01-02","1989-12-31") ) )  
met1990<-lapply(lonlat, function(A)  get_power_apsim_met(lonlat =c(mean(A$lon),
                                                                   mean(A$lat ) ),
                                                         dates = c("1990-01-01","1999-12-31") ) ) 

met2000<-lapply(lonlat, function(A)  get_power_apsim_met(lonlat =c(mean(A$lon),
                                                                   mean(A$lat ) ),
                                                         dates = c("2000-01-01","2009-12-31") ) ) 

met2010<-lapply(lonlat, function(A)  get_power_apsim_met(lonlat =c(mean(A$lon),
                                                                   mean(A$lat ) ),
                                                         dates = c("2010-01-01","2020-12-31") ) ) 


NASA.Nioro <- dplyr::bind_rows(met1980$`Nioro`, met1990$`Nioro`,met2000$`Nioro`,met2010$`Nioro`, .id = 'site')
NASA.Nioro$site='Nioro'
NASA.Nioro$lon=lonlat$`Nioro`$lon
NASA.Nioro$lat=lonlat$`Nioro`$lat
NASA.Nioro$rain
CHIRPS.Nioro <- dplyr::bind_rows(chirpsdata1980$`Nioro`,chirpsdata1985$`Nioro`, chirpsdata1990$`Nioro`, chirpsdata1995$`Nioro`, chirpsdata2000$`Nioro`,chirpsdata2005$`Nioro`,chirpsdata2010$`Nioro`, chirpsdata2015$`Nioro`, .id = 'site')
CHIRPS.Nioro$site='Nioro'
CHIRPS.Nioro$day <- lubridate::yday(as.Date(CHIRPS.Nioro$date, format="%m/%d/%Y"))
CHIRPS.Nioro$year<-as.numeric(format(as.Date(CHIRPS.Nioro$date, format="%m/%d/%Y"),"%Y"))

metdata.Nioro<-merge(NASA.Nioro, CHIRPS.Nioro, by=c( "year","day", "site", 'lon', 'lat'), all.x=TRUE )
metdata.Nioro<- metdata.Nioro %>% mutate(year, day, chirps=round(chirps,2),mint=round(mint,2),maxt=round( maxt,2), radn=round(radn,2), lon, lat, site )
metdata.Nioro<- metdata.Nioro %>% select(year, day, maxt,radn, "rain"=chirps,mint, lon, lat, site )

write.csv(metdata.Nioro, file = 'C:/SenegalGIS/weather/Nioro/Nioro_Nasa_chirps.csv')


#NASA <- read_csv("C:/Users/carcedo/Desktop/APSIM workshop/mets/Nasa.csv")

#chirpsdata <- read_csv("C:/Users/carcedo/Desktop/APSIM workshop/mets/chirpsdata.csv")