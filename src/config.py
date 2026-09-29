FEATURES = [
    "RBC", "Hb", "Hct", "MCV", "MCH", "MCHC", "RDW-CV", "RDW-SD",
    "WBC", "Eo", "Baso (0.01-0.08)", "Mono (0.24-0.8)", "Lymph",
    "Neut (1.9-6.7)", "IG", "Plt", "Eo%", "Baso%", "Mono%",
    "Lymph%", "Neut% (42-71)", "IG%", "NRBC%",
    "Kaalium (3.4-4.8)", "Naatrium", "Kaltsium (ioniseeritud)",
    "CRP", "ALAT", "ASAT", "ALP", "GGT", "Bilirubiin",
    "Kreatiniin", "eGFR (Crea, CKD-EPI)", "Uurea",
    "Albumiin (35-52)", "Lipaas",
]

REFERENCE_RANGES = {
    "MCV": (82, 95),
    "MCH": (28, 33),
    "MCHC": (322, 356),
    "RDW-CV": (12, 15),
    "RDW-SD": (38, 48),
    "WBC": (4.1, 9.7),
    "Eo": (0.02, 0.40),
    "Baso (0.01-0.08)": (0.01, 0.08),
    "Mono (0.24-0.8)": (0.24, 0.80),
    "Lymph": (1.3, 3.1),
    "Neut (1.9-6.7)": (1.9, 6.7),
    "IG": (0, 0.03),
    "Plt": (157, 372),
    "Eo%": (0.4, 6.0),
    "Baso%": (0.1, 1.3),
    "Mono%": (4, 11),
    "Lymph%": (21, 45),
    "Neut% (42-71)": (42, 71),
    "IG%": (0, 0.5),
    "NRBC%": (0, 0.5),
    "Kaalium (3.4-4.8)": (3.4, 4.8),
    "Naatrium": (136, 145),
    "Kaltsium (ioniseeritud)": (1.16, 1.32),
    "CRP": (0, 5),
    "ALAT": (0, 50),
    "ASAT": (0, 50),
    "ALP": (40, 129),
    "GGT": (0, 60),
    "Bilirubiin": (0, 21),
    "Uurea": (0, 8.1),
    "Albumiin (35-52)": (35, 52),
    "Lipaas": (13, 60),
    "eGFR (Crea, CKD-EPI)": (90, 120),
}

MALE_RANGES = {
    "RBC": (4.5, 5.7),
    "Hb": (134, 170),
    "Hct": (40, 49),
    "Kreatiniin": (59, 104),
}

FEMALE_RANGES = {
    "RBC": (4.1, 5.2),
    "Hb": (121, 150),
    "Hct": (37, 45),
    "Kreatiniin": (45, 84),
}

N_LOW_VARIANCE_AXES = 5
N_PERMUTATIONS = 1000
RANDOM_SEED = 12345
REGULARIZATION = 1e-5


def clinical_midpoints(features=FEATURES):
    """Return a midpoint vector aligned with FEATURES.

    Sex-specific variables use the average of male and female midpoints,
    matching the sensitivity analysis in the original analysis script.
    """
    midpoints = []
    for feature in features:
        if feature in MALE_RANGES:
            male_low, male_high = MALE_RANGES[feature]
            female_low, female_high = FEMALE_RANGES[feature]
            midpoint = (
                (male_low + male_high) / 2
                + (female_low + female_high) / 2
            ) / 2
        else:
            low, high = REFERENCE_RANGES[feature]
            midpoint = (low + high) / 2
        midpoints.append(midpoint)
    return midpoints
