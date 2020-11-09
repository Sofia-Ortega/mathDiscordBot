setting = {
    'questNum': 0,
    'time_mode': False,
    'timer': 0,
    'startTime': 0,
    'endTime': 0,
    'default_setting': False
}

def_setting = {
    'questNum': 0,
    'time_mode': False,
    'timer': 0,
    'startTime': 0,
    'endTime': 0,
    'default_setting': False
}




def display_setting(key=""):
    """Takes optional input of key. If key in setting, outputs its values. If no key given, outputs all setting keys """
    setting_str = "Take a look at the default settings!\n If you would like to change them, " \
                  "enter --setting key new_value\n\n"

    if key in setting:
        setting_str = key + ": " + str(def_setting[key])
    elif key:
        setting_str = key + "is not found in the settings. Check for any misspellings, or type --setting to see all " \
                            "of acceptable key values "
    else:
        for key in setting:
            setting_str += key + ": " + str(def_setting[key]) + "\n"

    return setting_str


def set_default(key, value):
    if key in def_setting:
        def_setting[key] = value
        return True

    return False

