setting = {
    'questNum': 0,
    'time_mode': False,
    'timer': 0,
    'startTime': 0,
    'endTime': 0,
    'default_setting': False
}


def display_setting(key=""):
    """Takes optional input of key. If key in setting, outputs its values. If no key given, outputs all setting keys """
    setting_str = ""
    if key in setting:
        setting_str = key + ": " + str(setting[key])
    elif key:
        setting_str = key + "is not found in the settings. Check for any misspellings, or type --setting to see all " \
                            "of acceptable key values "
    else:
        for key in setting:
            setting_str += key + ": " + str(setting[key]) + "\n"

    return setting_str

# for item in setting:
#     print(display_setting(item))
#
# print()
# print(display_setting())