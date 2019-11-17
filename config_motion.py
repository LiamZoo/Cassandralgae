



def giveme(debug=False):
    """this contain the config for the motion
    """
    configuration = {}
    # This is the configuration of the motor =X= pin
    configuration['step_pin'] = 11  # This is the pins used to communicate with motor X for setps. Should be of Integrer type
    configuration['dir_pin'] = 12  # This is the pins used to communicate with motor X for direction. Should be of Integrer type
    configuration['led_pin'] = 13  # This is the pins used to communicate with motor X led. Should be of Integrer type

    # This is about time
    configuration['reaction_time'] = 0.001  # seconds
    return configuration
