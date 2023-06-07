######################################################
#
# This file runs the simulation calling other files to setup crop, weather and soil.
# This file calls major Aquacrop-OSPy classes
# Helpful notebooks here:  https://colab.research.google.com/github/thomasdkelly/aquacrop/
# Aquacrop python documentation here as well: https://www.sciencedirect.com/science/article/pii/S0378377421002419
#
# NOTE: filepaths are set up to run on Neff Shared lab computer and need to be changed for any other environment.
#
#############################################################
from aquacrop.core import *
from aquacrop.classes import *
from pathlib import Path
import pandas as pd
import crop_config as crops
import soil_config as soils

crops = crops.crops

result_dict = dict({'final':pd.DataFrame(), 'growth':pd.DataFrame(),'flux': pd.DataFrame(),'flux_summary': pd.DataFrame(),'water':pd.DataFrame()})

climate_site_dict= {'Casamance': 3,
                    'Bassin arachidier':6,
                    'Zone sylvopastorale':0,
                    'Senegal oriental':4 }

#This method looks up climate files per zone
def get_climate_file(climate_zone):
    data_folder = Path("C:/senegal_aquacrop_model/weather/aquacrop_python/")
    clmate_files = {'Casamance': 'Casamance_Nasa_chirpsAQ_OUT.txt',
                    'Bassin arachidier':'BassinArachidier_Nasa_chirpsAQ_OUT.TXT',
                    'Senegal oriental': 'SenegalOriental_Nasa_chirpsAQ_OUT.txt',
                    'Zone sylvopastorale':'ZoneSylvopastorale_Nasa_chirpsAQ_OUT.txt'}
    file = data_folder / clmate_files[climate_zone]
    return file

# This method gets the raw weather file
# and puts it into the format needed by
# the python version of aquacrop
def prep_weather_data(climate_zone):
    file = get_climate_file(climate_zone)
    weather_data = prepare_weather(file)
    data_folder = Path("C:/senegal_aquacrop_model/weather/aquacrop_python/")
    return weather_data

#Get the soil for the current model iteration and zone
def prep_soil(climate_zone, run_num):
    id, soil = soils.get_soil(run_num, climate_zone)
    return id, soil

#get the configured crop for the simulation
def prep_crop(crop_name):
    crop = crops[crop_name]
    # scrop = CropClass('Maize', PlantingDate='06/01')
    return crop


#Persists the 3 major outputs (flux, final and growth) from an aquacrop run to a dictionary for later use
def save_result(results, soil_id, climate, planting_date):
    results.Final['soil_id'] = soil_id
    results.Final['site_id'] = climate_site_dict[climate]
    results.Final['zone'] = climate
    results.Final['planting_date'] = planting_date
    result_dict['final'] = result_dict['final'].append(results.Final)
    results.Final = False

    results.Flux['soil_id'] = soil_id
    results.Flux['site_id'] = climate_site_dict[climate]
    results.Flux['zone'] = climate
    results.Flux['planting_date'] = planting_date
    results.Flux = results.Flux[["SeasonCounter", "DAP", 'soil_id', 'site_id', 'zone', 'planting_date', 'Wr', 'Tr', 'P', 'Es', 'EsPot']]
    result_dict['flux'] = result_dict['flux'].append(results.Flux)
    results.Flux = False

    results.Growth['soil_id'] = soil_id
    results.Growth['site_id'] = climate_site_dict[climate]
    results.Growth['zone'] = climate
    results.Growth['planting_date'] = planting_date
    results.Growth = results.Growth[["SeasonCounter", "DAP", 'soil_id', 'site_id', 'zone', 'planting_date', 'B', 'B_NS','Y' ]]
    results.Growth['year'] = results.Growth["SeasonCounter"] + 1981
    results.Growth = results.Growth[ results.Growth['B_NS']>0]
    #results.Growth = results.Growth.groupby(['year', 'site_id','soil_id', 'zone', 'planting_date']).agg(biomass=pd.NamedAgg(column='B', aggfunc='max'),biomass_nostress=pd.NamedAgg(column='B_NS', aggfunc='max'), season_yield=pd.NamedAgg(column='Y', aggfunc='max'))
    result_dict['growth'] = result_dict['growth'].append(results.Growth)
    results.Growth = False
    #print('result appended.')
    results = False

#Flux output is summarized before writing to disk
def summarize_flux(soil_id):
    flux = result_dict['flux']
    flux = flux.groupby(['soil_id', 'site_id', 'zone', "DAP"]).agg(
        water_content=pd.NamedAgg(column='Wr', aggfunc='mean'), DailyPrecip=pd.NamedAgg(column='P', aggfunc='mean'),
        DailyTrans=pd.NamedAgg(column='Tr', aggfunc='mean'),
        SoilEvap=pd.NamedAgg(column='Es', aggfunc='mean'), PotSoilEv= pd.NamedAgg(column='EsPot', aggfunc='mean'))
    result_dict['flux_summary'] = result_dict['flux_summary'].append(flux)
    result_dict['flux'] = pd.DataFrame()
    print(" Finished soil id:  ", soil_id)

#Write the final results to disk
def write_result(crop):
    filename = 'D:\\senegal_crop_model_result\\' + crop + '_FINAL_fullrunV2.csv'
    result_dict['final'].to_csv(filename)
    filename = 'D:\\senegal_crop_model_result\\' + crop + '_GROWTH_fullrunV2.csv'
    result_dict['growth'].to_csv(filename)
    filename = 'D:\\senegal_crop_model_result\\' + crop + '_FLUX_fullrunV2.csv'
    result_dict['flux_summary'].to_csv(filename)



#Set intial water content and major global simulation properties
def init_model(weather_data, soil, crop):
    InitWC = InitWCClass(value=['WP'])
    # combine into aquacrop model and specify start and end simulation date
    model = AquaCropModel(SimStartTime=f'{1981}/06/01',
                          SimEndTime=f'{2020}/12/31',
                          wdf=weather_data,
                          Soil=soil,
                          Crop=crop,
                          InitWC=InitWC,
                          )
    return model

#This main method runs when the program is called
if __name__ == "__main__":
    my_crop = 'millet'
    if True:
        crop = prep_crop(my_crop)
        for climate_zone in ['Senegal oriental', 'Casamance','Bassin arachidier']: #,'Zone sylvopastorale']:#['sudan_savanna', 'guinea_savanna', 'sahel']:
            weather = prep_weather_data(climate_zone)
            for run_num in range(0, 999, 1):
                soil_id, soil = prep_soil(climate_zone, run_num)
                for planting_date in ['7/16', '7/21', '7/26', '8/1', '8/6', '8/11', '8/16', '8/21']:
                    crop.PlantingDate = planting_date
                    if soil :#soil returns false if missing data for a point
                        model_run = init_model(weather, soil, crop)
                        # initialize model
                        model_run.initialize()
                        # run model till termination
                        #print('************  plant date: ', crop.PlantingDate)
                        try:
                            model_run.step(till_termination=True)
                            save_result(model_run.Outputs, soil_id, climate_zone, planting_date)
                            model_run.Outputs = False
                            model_run = False
                        except Exception as e:
                            print('Run failed: Plant date: ', crop.PlantingDate, 'soil_id: ', soil_id, 'Run: ', run_num)
                            print(e)
                if soil:#soil returns false if missing data for a point
                    summarize_flux(soil_id)

        write_result(my_crop)

