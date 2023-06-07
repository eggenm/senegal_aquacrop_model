from aquacrop.core import *
from aquacrop.classes import *
import pandas as pd

soils_csv = pd.read_csv('data/AEZ_samples_with_soil2.txt')
#print(soils_csv.columns)

columns_by_layer = dict(  { 1:('sand_0_5cm', 'clay_0_5cm', 'soc_0_5cm'),
                        2:('sand_5_15c', 'clay_5_15c', 'soc_5_15cm'),
                        3:('sand_15_30', 'clay_15_30', 'soc_15_30c'),
                        4:('sand_30_60', 'clay_30_60', 'soc_30_60c'),
                        5:('sand_60_10', 'clay_60_10', 'soc_60_100'),
                        6:('sand_100_2', 'clay_100_2', 'soc_100_20') }  )

layer_thickness = [0.05, 0.1, 0.15, 0.3, 0.4, 1]

def build_soil_db():
    soils_csv = pd.read_csv('data/AEZ_samples_with_soil2.txt')
    print(soils_csv.loc[soils_csv['region']=='Zone des Niayes'])
    #print(soils_csv.index)

def get_soil(key, climate):
    #print(" KEY:  ", key, "ZONE:  ", climate)

    #sand = soils_dict[climate][key]['prop1']
    #clay = soils_dict[climate][key]['prop2']
    #org_matter = soils_dict[climate][key]['prop3']
    custom = SoilClass('custom', dz=layer_thickness)#, CN= ?, REW = ?)
    #custom.add_layer_from_texture(thickness=custom.zSoil, Sand=sand, Clay=clay, OrgMat=org_matter, penetrability=100)
    #soil = SoilClass('custom', prop1=soil-prop1, prop2=soil-prop2, ...)
    zone_soil = soils_csv.loc[soils_csv['region'] == climate]
    adjustment = min(zone_soil['CID'])*1000
    key = adjustment + key
    soil_id =  key
    #print('SOIL ID:', soil_id)
    for layer in range(1,7):
    #     layer_dict = getlayer(layer)
    #     thickness = thickness_by_layer[layer]
    #     sand = layer_dict[key][sand]
    #     clay = layer_dict[key][clay]
        #print('LAYER: ' , layer)

        sand = zone_soil[columns_by_layer[layer][0]][key]/10
        if(layer==1 and sand <=0):
            return False, False
       # print('Sand:  ', sand)
        clay = soils_csv.loc[soils_csv['region'] == climate][columns_by_layer[layer][1]][key]/10
      ##  print('Clay:  ', clay)
        org_matter = soils_csv.loc[soils_csv['region'] == climate][columns_by_layer[layer][2]][key]/100
        org_matter_previous = 0
        if org_matter>0 :
            org_matter_previous = org_matter
        else:#TODO, how to deal with missing org matter in deeper layers
            org_matter = org_matter_previous
        org_matter_previous = org_matter
        #print('OrgMatter:  ', org_matter)
        thickness = layer_thickness[layer-1]
       #int('Thick', thickness)
        custom.add_layer_from_texture(thickness=thickness, Sand=sand, Clay=clay, OrgMat=org_matter, penetrability=100 )
    return soil_id, custom

if __name__ == "__main__":
    soil_id, soil = get_soil(5, 'Casamance')
    print(soil.profile);