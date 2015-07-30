COLOUR_ID_CHOICES = (('any', 'Any'),
                     ('1', '1 - Gold'),
                     ('2', '2 - Green'),
                     ('3', '3 - Red'),
                     ('4', '4 - Blue'))


EDUCATION_LEVELS = (('any', 'Any'),
      ('primary to junior high', 'Primary School to Junior High School'),
      ('school certificate', 'Junior Secondary (up to School Certificate level)'),
      ('higher school certificate', 'Senior Secondary (Higher School Certificate)'),
      ('TAFE Certificate', 'TAFE Certificate'),
      ('Diploma', 'Diploma'),
      ('Advanced Diploma', 'Advanced Diploma'),
      ('Associate Degree', 'Associate Degree'),
      ('Bachelor Degree', 'Bachelor Degree'),
      ('Vocational Graduate Certificate', 'Vocational Graduate Certificate'),
      ('Vocational Graduate Diploma', 'Vocational Graduate Diploma'),
      ('Graduate Certificate', 'Graduate Certificate'),
      ('Graduate Diploma', 'Graduate Diploma'),
      ('Masters Degree', 'Masters Degree'),
      ('Doctoral Degree', 'Doctoral Degree'),
)

ENROLLMENT_TYPES = (('any', 'Any'),
    ('fulltime', 'Full Time'),
    ('parttime', 'Part Time'),
)

PROFESSIONAL_CATEGORIES = (('any', 'Any'),
    ("manager and admin", "Managers and Administrators (e.g. school principal, judge, farm manager)"),
    ("professional", "Professionals (e.g. doctors, engineer, architect, scientist, teacher)"),
    ("assoc professional", "Associate professionals (e.g. police officer, nurse, ambulance driver)"),
    ("tradesperson", "Tradespersons and related workers (e.g. mechanic, plumber, baker)"),
    ("clerical and service", "Advanced clerical and service workers (e.g. secretary, insurance agent)"),
    ("intermediate clerical and service", "Intermediate clerical, sales and service workers (e.g. receptionist, teacher's aide)"),
    ("intermediate production", "Intermediate production and transport workers (e.g. miner, truck driver)"),
    ("elementary clerical", "Elementary clerical, sales and service workers (e.g. filing clerk, sales assistant)"),
    ("labourer", "Labourers and related workers (e.g. farm hand, fast food cook, handyperson)"),
    ("home duties", "Home duties"),
    ("unemployed", "Unemployed"),
)

CULTURAL_HERITAGES = (('any', 'Any'),
    ("Australian", "Australian"),
    ("Aboriginal Australian", "Aboriginal Australian"),
    ("Other", "Other"),
)

GENDER_CHOICES = (
    ('any', 'Any'), 
    ('male', 'Male'), 
    ('female', 'Female')
)

SES_CHOICES = (
    ('any', 'Any'), 
    ('Professional', 'Professional'), 
    ('Non-Professional', 'Non-Professional')
)

AGEGROUP_CHOICES = (
    ('any', 'Any'),
    ('<30', 'less than 30'),
    ('30-49', '30 to 49'),
    ('>50', 'over 50'),                
    )

RECORDING_SITES = (
    ('any', 'Any'),
    ('<http://id.austalk.edu.au/protocol/site/FLIN>', 'Adelaide, Flinders University'),
    ('<http://id.austalk.edu.au/protocol/site/UNE>', 'Armidale, University of New England'),
    ('<http://id.austalk.edu.au/protocol/site/CSUB>', 'Bathurst, Charles Sturt University'),
    ('<http://id.austalk.edu.au/protocol/site/UQB>', 'Brisbane, University of Queensland'),
    ('<http://id.austalk.edu.au/protocol/site/UC>', 'Canberra, University of Canberra'),
    ('<http://id.austalk.edu.au/protocol/site/ANU>', 'Canberra, Australian National University'),
    ('<http://id.austalk.edu.au/protocol/site/UMELBC>', 'Castlemaine, University of Melbourne'),
    ('<http://id.austalk.edu.au/protocol/site/CDUD>', 'Darwin, Charles Darwin University'),
    ('<http://id.austalk.edu.au/protocol/site/UTAS>', 'Hobart, University of Tasmania'),
    ('<http://id.austalk.edu.au/protocol/site/USCM>', 'Maroochydore, University of the Sunshine Coast'),
    ('<http://id.austalk.edu.au/protocol/site/UMELBM>', 'Melbourne, University of Melbourne'),
    ('<http://id.austalk.edu.au/protocol/site/UWA>', 'Perth, University of Western Australia'),
    ('<http://id.austalk.edu.au/protocol/site/USYD>', 'Sydney, University of Sydney'),
    ('<http://id.austalk.edu.au/protocol/site/UNSW>', 'Sydney, University of New South Wales'),
    ('<http://id.austalk.edu.au/protocol/site/UQT>', 'Townsville, University of Queensland'),
    )

LANGUAGE_CHOICES = (
    ('any', 'Any'),
    )

EXTRA_CHOICES = [('all', 'All')]

DEFAULT_SPEAKER_QUANTITY = 1