import json
from freactive import autoproperty
# import smokesignal

page = None

# def set_page(p):
#     global page
#     page = p
    
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
    print('BROADCASTING....')
    # smokesignal.emit('chose_dir', arg={'path': value,
    #                              'news': 'Sold for $1M'})
    page.pubsub.send_all_on_topic('chose_dir', {'path': value, })

def model_get_initial_directory():
    model = get_model()
    return model['initial_directory'] if 'initial_directory' in model else ''


# Possibly in future

if __name__ == '__main__':

    def update_counter_ui(arg1, arg2=None):
        print('update_counter_ui', arg2)

    # Define the model

    @autoproperty('counter', default_value=100, callback=update_counter_ui)
    @autoproperty('weather', default_value='sunny', callback=None)
    class Model:
        pass

    model = Model()
    model.boot()  # causes all observing callbacks to be called, which updates the UI with the initial state of the model

