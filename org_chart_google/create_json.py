import pandas as pd
import json
import os

def pip_installer(package_name):
    """Install package if not installed"""
    try:
        import package_name
    except ImportError:
        os.system(f"pip install {package_name}")
    return True

if pip_installer("openpyxl"):
    import openpyxl


def json_write_with_indent(data, file_name):
    """Write json file with indent"""
    with open(file_name, "w") as f:
        json.dump(data, f, indent=4)

def clean_mod(model):
    """Clean model name"""
    model_clean = model.replace(" ", "").replace("-", "").replace("_", "").replace("+", "")
    return model_clean

def character_matcher_return_mostlikely(model):
    model = str(model).upper()
    needed_list = ['GEN2', 'S1_AIR', 'S1_X+', 'S1_PRO']
    for i in needed_list:
        if clean_mod(model) in clean_mod(i):
            return i
    return model

def main_cat_fixer(df):
    """Fix names to general names in main category"""
    needed_list = ['GEN2', 'S1_AIR', 'S1_X+', 'S1_PRO']
    df["Model"] = df["Model"].apply(lambda x: character_matcher_return_mostlikely(x))
    return df
# Read the "design.xlsx" file into a DataFrame
df = pd.read_excel("designs.xlsx")
df = main_cat_fixer(df)
main_dict = {
    'GEN2': [],
    'S1_AIR': [],
    'S1_X+': [],
    'S1_PRO': [],   
}
previous_design = {
    'GEN2': "",
    'S1_AIR': "",
    'S1_X+': "",
    'S1_PRO': "",   
}

seed_version_dict = {
    'GEN2': {},
    'S1_AIR': {},
    'S1_X+': {},
    'S1_PRO': {},   
}
# df_list = split df by model
# breakpoint()
for df_ in [df[df['Model'] == i] for i in df['Model'].unique().tolist() if i in main_dict.keys()]:
    previous_design[df_['Model'].iloc[0]] = df_['Model'].iloc[0]
    for i, row in df_.sort_values(by=['Design status']).iterrows():
        if str(row['Design status']) == 'nan':
            try:
                design_current = "SKIPPED"
            except:
                breakpoint()
        else:
            design_current = row['Design status']
            design_listed = design_current.split(".")
            if len(design_listed) == 1:
                previous_design[row['Model']] = row['Model']
            elif len(design_listed) > 1:
                previous_design[row['Model']] = design_listed[0]                
        main_dict[row['Model']].append([
            design_current, previous_design[row['Model']], row['Component']
        ])
        previous_design[row['Model']] = design_current


json_write_with_indent(main_dict, "designs.json")

