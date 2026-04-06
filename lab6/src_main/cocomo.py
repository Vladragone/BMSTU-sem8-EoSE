import math

def calculate_pm(cocomo_type, size, eaf):
    if cocomo_type == "organic":
        return 2.4 * eaf * (size ** 1.05)
    elif cocomo_type == "semi-detached":
        return 3.0 * eaf * (size ** 1.12)
    elif cocomo_type == "embedded":
        return 2.8 * eaf * (size ** 1.20)
    return 0

def calculate_tdev(cocomo_type, pm):
    if cocomo_type == "organic":
        return 2.5 * (pm ** 0.38)
    elif cocomo_type == "semi-detached":
        return 2.5 * (pm ** 0.35)
    elif cocomo_type == "embedded":
        return 2.5 * (pm ** 0.32)
    return 0

def get_eaf(factors):
    eaf = 1.0
    for factor in factors.values():
        eaf *= factor
    return eaf

def phase_distribution(pm):
    return {
        "Planning": pm * 0.08,
        "Design": pm * 0.18,
        "Detailed Design": pm * 0.25,
        "Coding": pm * 0.26,
        "Integration": pm * 0.31
    }