#################################################
######### PDFs####################
louga_data<-millet_factors%>%filter(site_id=='Drier/North')
louga<-ggplot(louga_data, aes(x=yield, color=Clay200, fill=Clay200)) +
  # geom_histogram(aes(y=..density..), position="identity", alpha=0.5)+
  geom_density(alpha=0.6)

nioro_data<-millet_factors%>%filter(site_id=='Middle' )
nioro<-ggplot(nioro_data, aes(x=yield, color=Clay200, fill=Clay200)) +
  # geom_histogram(aes(y=..density..), position="identity", alpha=0.5)+
  geom_density(alpha=0.6)

samyo<-ggplot(millet_factors%>%filter(site_id=='Humid/South' ), aes(x=yield, color=Clay200, fill=Clay200)) +
  # geom_histogram(aes(y=..density..), position="identity", alpha=0.5)+
  geom_density(alpha=0.6)


sample_means<-NULL
sample_means <- data.frame(matrix(ncol = 3, nrow = 2000))

#provide column names
colnames(sample_means) <- c('yield', 'condition', 'site')
j=1
n<-1000
for( y in list(nioro_data%>%filter(Clay200=='HIGH_CLAY'), nioro_data%>%filter(Clay200=='LOW_CLAY'))){
  for(i in 1:n){
    sample_means$yield[j] = mean(sample(y$biomass, 20, replace = FALSE, prob = NULL))
    sample_means$condition[j] = y$Clay200[1]
    sample_means$site  = y$site_id[1]
    j=j+1
  }
}

louga_means<-NULL
louga_means <- data.frame(matrix(ncol = 3, nrow = 2000))

#provide column names
colnames(louga_means) <- c('yield', 'condition', 'site')
j=1
n<-1000
for( x in list(louga_data%>%filter(Clay200=='HIGH_CLAY'), louga_data%>%filter(Clay200=='LOW_CLAY'))){
  for(i in 1:n){
    louga_means$yield[j] = mean(sample(x$biomass, 20, replace = FALSE, prob = NULL))
    louga_means$condition[j] = x$Clay200[1]
    louga_means$site  = x$site_id[1]
    j=j+1
  }
}

louga_clay_means_plot<-ggplot(louga_means, aes(x=yield, color=condition, fill=condition)) +
  # geom_histogram(aes(y=..density..), position="identity", alpha=0.5)+
  geom_density(alpha=0.6)+
  ggtitle("Drier/North") +
  theme(plot.title = element_text(hjust = 0.5))

nioro_clay_means_plot<-ggplot(sample_means, aes(x=yield, color=condition, fill=condition)) +
  # geom_histogram(aes(y=..density..), position="identity", alpha=0.5)+
  geom_density(alpha=0.6)+
  ggtitle("Middle") +
  theme(plot.title = element_text(hjust = 0.5))


aggregate_risk_louga = 100*length(louga_means$yield[which(louga_means$yield<600)])/length(louga_means$yield)
high_clay_risk_Louga = 100*length(louga_means$yield[which(louga_means$yield<600 & louga_means$condition=='HIGH_CLAY')])/length(louga_means$yield[which(louga_means$condition=='HIGH_CLAY')])
low_clay_risk_Louga = 100*length(louga_means$yield[which(louga_means$yield<600 & louga_means$condition=='LOW_CLAY')])/length(louga_means$yield[which(louga_means$condition=='LOW_CLAY')])

aggregate_risk_louga2 = 100*length(louga_data$biomass[which(louga_data$biomass<500 & louga_data$biomass>50)])/length(louga_data$biomass[which(louga_data$biomass>50)])
high_clay_risk_Louga2 = 100*length(louga_data$biomass[which(louga_data$biomass<500 & louga_data$biomass>50 & louga_data$Clay200=='HIGH_CLAY')])/length(louga_data$biomass[which(louga_data$Clay200=='HIGH_CLAY' & louga_data$biomass>50)])
low_clay_risk_Louga2 = 100*length(louga_data$biomass[which(louga_data$biomass<500 & louga_data$biomass>50 & louga_data$Clay200=='LOW_CLAY')])/length(louga_data$biomass[which(louga_data$Clay200=='LOW_CLAY' & louga_data$biomass>50)])


gridExtra::grid.arrange(louga_clay_means_plot,nioro_clay_means_plot, ncol = 1) 



aggregate_risk_nioro = 100*length(sample_means$yield[which(sample_means$yield<1400)])/length(sample_means$yield)
high_clay_risk_nioro = 100*length(sample_means$yield[which(sample_means$yield<1400 & sample_means$condition=='HIGH_CLAY')])/length(sample_means$yield[which(sample_means$condition=='HIGH_CLAY')])
low_clay_risk_nioro = 100*length(sample_means$yield[which(sample_means$yield<1400 & sample_means$condition=='LOW_CLAY')])/length(sample_means$yield[which(sample_means$condition=='LOW_CLAY')])

