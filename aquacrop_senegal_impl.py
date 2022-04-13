from aquacrop.core import *
from aquacrop.classes import *
from datetime import date, time, datetime
from pathlib import Path
import pandas as pd
import crop_config as crops
import soil_config as soils

filepath = 'C:\\SenegalGIS\\weather\\Tiel\\Tiel_Nasa_chirps.csv'
crops = crops.crops

result_dict = dict({'final':pd.DataFrame(), 'growth':pd.DataFrame(),'flux': pd.DataFrame(),'water':pd.DataFrame()})

climate_site_dict= {'sahel': 0,
                    'sudan_savanna': 6,#'Tiel_Nasa_chirps_aquacropOut.txt'  Tiel is 5,#,
                    'guinea_savanna': 3,
                    'Casamance': 3,
                    'Bassin arachidier':6,
                    'Zone sylvopastorale':0,
                    'Senegal oriental':4 }

def get_date():
    weather_df = pd.read_csv(filepath, header=0, delim_whitespace=False)
    output_df = pd.DataFrame(columns=['Day', 'Month', 'Year', 'Tmin(C)', 'Tmax(C)', 'Prcp(mm)', 'Et0(mm)'])
    # i=0
    for index, row in weather_df.iterrows():
        dtm = str(int(row['Year'])) + str(int(row['Day']))
        dtm = datetime.strptime(dtm, '%Y%j')
        row['Month'] = dtm.strftime("%m")
        row['Day'] = dtm.strftime("%d")
        output_df = output_df.append(row)
    output_df = output_df[['Day', 'Month', 'Year', 'Tmin(C)', 'Tmax(C)', 'Prcp(mm)', 'Et0(mm)']]
    output_df.to_csv('C:\\SenegalGIS\\weather\\Tiel\\Tiel_Nasa_chirps_aquacropOut.csv')


def get_climate_file(climate_zone):
    data_folder = Path("C:/SenegalGIS/weather/aquacrop_python/")
    clmate_files = {'sahel': 'Louga_Nasa_chirps_aquacropOut.TXT',
                    'sudan_savanna': 'Nioro_Nasa_chirps_aquacropOut.TXT',#'Tiel_Nasa_chirps_aquacropOut.txt' ,#,
                    'guinea_savanna': 'SamYoroGueye_Nasa_chirps_aquacropOut.txt',
                    'Casamance': 'Casamance_Nasa_chirpsAQ_OUT.txt',
                    'Bassin arachidier':'BassinArachidier_Nasa_chirpsAQ_OUT.TXT',
                    'Senegal oriental': 'SenegalOriental_Nasa_chirpsAQ_OUT.txt',
                    'Zone sylvopastorale':'ZoneSylvopastorale_Nasa_chirpsAQ_OUT.txt'}
    file = data_folder / clmate_files[climate_zone]
    return file


def prep_weather_data(climate_zone):
    file = get_climate_file(climate_zone)
    weather_data = prepare_weather(file)
    print(weather_data)
    data_folder = Path("C:/SenegalGIS/weather/aquacrop_python/")
    #file = data_folder / 'BassinArachidier_weather_from_python.csv'
    #weather_data.to_csv(file)
    return weather_data


def prep_soil(climate_zone, run_num):
    #soil = SoilClass(soilType='SandyLoam')
    #print(soil)
    id, soil = soils.get_soil(run_num, climate_zone)
    return id, soil


def prep_crop(crop_name):
    crop = crops[crop_name]
    # scrop = CropClass('Maize', PlantingDate='06/01')
    return crop


def prep_field_managment():
    print('TODO')
    # TODO

def save_result(results, soil_id, climate, planting_date):
    results.Final['soil_id'] = soil_id
    results.Final['site_id'] = climate_site_dict[climate]
    results.Final['zone'] = climate
    results.Final['planting_date'] = planting_date
    result_dict['final'] = result_dict['final'].append(results.Final)
    results.Flux['soil_id'] = soil_id
    results.Flux['site_id'] = climate_site_dict[climate]
    results.Flux['zone'] = climate
    results.Flux['planting_date'] = planting_date
    result_dict['flux'] = result_dict['flux'].append(results.Flux)
    results.Growth['soil_id'] = soil_id
    results.Growth['site_id'] = climate_site_dict[climate]
    results.Growth['zone'] = climate
    results.Growth['planting_date'] = planting_date
    result_dict['growth'] = result_dict['growth'].append(results.Growth)
    print('result appended.')

def write_result(crop):
    filename = 'C:\\SenegalGIS\\crop_model_result\\' + crop + '_FINAL_multiple_PlantingDatesNORTH.csv'
    result_dict['final'].to_csv(filename)
    filename = 'C:\\SenegalGIS\\crop_model_result\\' + crop + '_GROWTH_multiple_PlantingDates.csv'
   # result_dict['growth'].to_csv(filename)
    filename = 'C:\\SenegalGIS\\crop_model_result\\' + crop + '_FLUX_multiple_PlantingDates.csv'
  #  result_dict['flux'].to_csv(filename)




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


if __name__ == "__main__":
    #get_date()
    #for climate_zone in ['sudan_savanna'], 'guinea_savanna', 'sahel']:
    #weather = prep_weather_data('Bassin arachidier')
    my_crop = 'millet'
    if True:
        # file = get_filepath('tunis_climate.txt')
        crop = prep_crop(my_crop)
        for climate_zone in ['Senegal oriental']: # 'Casamance','Bassin arachidier','Zone sylvopastorale']:#['sudan_savanna', 'guinea_savanna', 'sahel']:
            weather = prep_weather_data(climate_zone)
            for planting_date in ['7/16', '7/21', '7/26', '8/1', '8/6', '8/11', '8/16', '8/21']:#, '8/26', '8/31', '9/5', '9/10']:
                crop.PlantingDate = planting_date
                for run_num in range(0, 849, 19):#1000):
                    soil_id, soil = prep_soil(climate_zone, run_num)
                    if soil :#soil returns false if missing data for a point
                        model_run = init_model(weather, soil, crop)
                        # initilize model
                        model_run.initialize()
                        # run model till termination
                        model_run.step(till_termination=True)
                        save_result(model_run.Outputs, soil_id, climate_zone, planting_date)

        write_result(my_crop)

