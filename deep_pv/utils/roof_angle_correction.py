import math

REFERENCE_ENERGY_DICT = {}

def get_correction_factors_pv(
    angles = [0.2, 0.3, 0.45, 0.55, 0.37, 0.6]) -> dict:

    """ Calculate correction factors of the most common PV angles.
    Returns dictionary: { 0.3 : 1.38, 0.4 : ......}"""

    def get_angle(angle):
        top_angle = 1.8 - angle - 0.9

        width_panel = 2
        length_panel = 1
        length_panel_angled = (length_panel * math.sin(0.9)) / math.sin(top_angle)

        observed_sqm = width_panel * length_panel
        true_sqm = width_panel * length_panel_angled
        correction_factor = true_sqm / observed_sqm
        return correction_factor

    return { angle : get_angle(angle) for angle in angles}

def get_production_solar(watt_sqm = 1000, day_hours = 5, efficiency = 0.15):
    energy = watt_sqm * efficiency * day_hours
    return energy

if __name__ == '__main__':
    print(get_correction_factors_pv())
