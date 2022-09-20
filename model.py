import json
from freactive import autoproperty

default_model = {
    'description': 'preferences for stable diffusion textfile cleaner',
    'version': 1,
    'strings_to_strip': [
        '_RealESRGAN_x4plus',
        '_GFPGANv1.3_RealESRGAN_x4plus',
    ],
    'favourite_directories': [],
    'initial_directory': '',
    'actually_delete': False,
    'other': 'other stuff'
}


def get_model():
    try:
        with open('prefs.json', 'r') as f:
            data = json.load(f)
    except:
        data = default_model.copy()
    return data

def save_model(model):
    with open('prefs.json', 'w') as f:
        json.dump(model, f, indent=2)


# Access

def model_set_initial_directory(value):
    model = get_model()
    model['initial_directory'] = value
    save_model(model)

def model_get_initial_directory():
    model = get_model()
    return model['initial_directory'] if 'initial_directory' in model else ''


# Possibly in future

"""
# Define the model

@autoproperty('counter', default_value=100, callback=update_counter_ui)
@autoproperty('weather', default_value='sunny', callback=update_weather_ui)
class Model:
    pass

model = Model()
model.boot()  # causes all observing callbacks to be called, which updates the UI with the initial state of the model

"""
