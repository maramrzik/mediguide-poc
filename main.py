import pygame
import sys
from mediguide_respiratory_safety_checker import (
    evaluate_patient, check_ddi, check_respiratory_side_effects, check_lab_thresholds
)

# Sample patient database
patients = [
    {
        'name': 'Anna Benk', 'gfr': 50, 'conditions': ['asthma', 'hypertension'], 'age': 65, 'weight': 80,
        'gender': 'female', 'ethnicity': 'Caucasian', 'ALT': 22, 'AST': 30, 'bilirubin': 0.9,
        'genetic_variants': {}, 'lifestyle': {'smoking': False, 'alcohol': 'moderate'},
        'current_medications': ['salmeterol', 'prednisolone'], 'allergies': ['penicillin']
    },
    {
        'name': 'Jin Tanaka', 'gfr': 25, 'conditions': ['COPD', 'heart failure'], 'age': 70, 'weight': 72,
        'gender': 'male', 'ethnicity': 'Asian', 'ALT': 35, 'AST': 40, 'bilirubin': 1.2,
        'genetic_variants': {}, 'lifestyle': {'smoking': True, 'alcohol': 'low'},
        'current_medications': ['theophylline', 'metformin'], 'allergies': []
    },
     {
        'name': 'Markus Schneider',
        'gfr': 58,
        'conditions': ['asthma', 'diabetes'],
        'age': 45,
        'weight': 90,
        'gender': 'male',
        'ethnicity': 'Caucasian',
        'ALT': 28,
        'AST': 25,
        'bilirubin': 1.0,
        'genetic_variants': {},
        'lifestyle': {'smoking': False, 'alcohol': 'low'},
        'current_medications': ['prednisolone', 'theophylline'],
        'allergies': ['aspirin']
    },
    {
        'name': 'Leila Al-Mansouri',
        'gfr': 65,
        'conditions': ['chronic bronchitis', 'hypertension'],
        'age': 55,
        'weight': 68,
        'gender': 'female',
        'ethnicity': 'Middle Eastern',
        'ALT': 20,
        'AST': 22,
        'bilirubin': 0.7,
        'genetic_variants': {},
        'lifestyle': {'smoking': True, 'alcohol': 'none'},
        'current_medications': ['salmeterol', 'ibuprofen'],
        'allergies': []
    },
    {
        'name': 'Thomas Okafor',
        'gfr': 28,
        'conditions': ['copd', 'renal impairment'],
        'age': 72,
        'weight': 74,
        'gender': 'male',
        'ethnicity': 'African',
        'ALT': 40,
        'AST': 45,
        'bilirubin': 1.3,
        'genetic_variants': {},
        'lifestyle': {'smoking': True, 'alcohol': 'moderate'},
        'current_medications': ['metformin', 'salmeterol'],
        'allergies': ['nsaids']
    },
    {
        'name': 'Raj Patel',
        'gfr': 38,  # triggers metformin warning
        'conditions': ['asthma'],
        'age': 60,
        'weight': 74,
        'gender': 'male',
        'ethnicity': 'Indian',
        'ALT': 55,  # triggers isoniazid warning
        'AST': 50,
        'bilirubin': 1.4,
        'genetic_variants': {},
        'lifestyle': {'smoking': False, 'alcohol': 'low'},
        'current_medications': ['metformin', 'isoniazid'],
        'allergies': [],
    },
    {
        'name': 'Maria Ramírez',
        'gfr': 70,
        'conditions': ['copd', 'heart failure'],
        'age': 68,
        'weight': 62,
        'gender': 'female',
        'ethnicity': 'Hispanic',
        'ALT': 30,
        'AST': 25,
        'bilirubin': 0.9,
        'genetic_variants': {},
        'lifestyle': {'smoking': True, 'alcohol': 'moderate'},
        'current_medications': ['theophylline', 'ciprofloxacin'],  # triggers DDI
        'allergies': []
    },
    {
        'name': 'Omar Haddad',
        'gfr': 80,
        'conditions': ['asthma'],
        'age': 45,
        'weight': 78,
        'gender': 'male',
        'ethnicity': 'Arab',
        'ALT': 22,
        'AST': 25,
        'bilirubin': 1.0,
        'genetic_variants': {},
        'lifestyle': {'smoking': False, 'alcohol': 'none'},
        'current_medications': ['montelukast', 'ibuprofen'],  # side effects + contraindications
        'allergies': ['nsaids']
    },
    {
        'name': 'Elena Fischer',
        'gfr': 65,
        'conditions': ['asthma', 'hypertension'],
        'age': 59,
        'weight': 68,
        'gender': 'female',
        'ethnicity': 'Caucasian',
        'ALT': 30,
        'AST': 28,
        'bilirubin': 1.0,
        'genetic_variants': {},
        'lifestyle': {'smoking': False, 'alcohol': 'low'},
        'current_medications': ['ibuprofen', 'prednisolone'],  # should trigger interaction from ddinter.csv
        'allergies': []
    },
    {
        'name': 'Thomas Becker',
        'gfr': 50,
        'conditions': ['copd'],
        'age': 73,
        'weight': 85,
        'gender': 'male',
        'ethnicity': 'German',
        'ALT': 42,
        'AST': 38,
        'bilirubin': 1.1,
        'genetic_variants': {},
        'lifestyle': {'smoking': True, 'alcohol': 'moderate'},
        'current_medications': ['salmeterol', 'theophylline'],  # another DDI
        'allergies': []
    },
    {
        'name': 'Fatima Darwish',
        'gfr': 72,
        'conditions': ['asthma'],
        'age': 33,
        'weight': 56,
        'gender': 'female',
        'ethnicity': 'Middle Eastern',
        'ALT': 25,
        'AST': 22,
        'bilirubin': 0.8,
        'genetic_variants': {},
        'lifestyle': {'smoking': False, 'alcohol': 'none'},
        'current_medications': ['montelukast', 'paracetamol'],
        'allergies': ['aspirin']
    }
]

pygame.init()

width, height = 1000, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("MediGuide Respiratory Safety Checker")
font = pygame.font.SysFont("arial", 18)

fields = [
    'name', 'gfr', 'conditions', 'age', 'weight', 'gender', 'ethnicity',
    'ALT', 'AST', 'bilirubin', 'smoking', 'alcohol', 'current_medications', 'allergies'
]

inputs = {field: '' for field in fields}
input_rects = {}
active_field = None

start_y = 60
for i, field in enumerate(fields):
    y = start_y + i * 35
    input_rects[field] = pygame.Rect(200, y, 300, 28)

check_button = pygame.Rect(400, start_y + len(fields) * 35 + 20, 180, 40)
dropdown_button = pygame.Rect(600, start_y, 300, 28)
dropdown_open = False
visible_limit = 10
scroll_offset = 0

results_rect = pygame.Rect(50, check_button.y + 60, 900, 250)
warnings = []

logo = pygame.image.load("logo.png")
logo = pygame.transform.scale(logo, (150, 150))

# Text wrapping function
def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = ''
    for word in words:
        test_line = f'{current_line} {word}'.strip()
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines

running = True

while running:
    screen.fill("#F0F8FF")
    pygame.draw.rect(screen, pygame.Color("#F5F5F5"), (40, start_y - 10, width - 80, len(fields)*35 + 20))
    pygame.draw.line(screen, pygame.Color("gray"), (40, start_y - 10), (width - 40, start_y - 10), 2)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            active_field = None
            if dropdown_button.collidepoint(event.pos):
                dropdown_open = not dropdown_open
            elif dropdown_open:
                for i, patient in enumerate(patients[scroll_offset:scroll_offset + visible_limit]):
                    rect = pygame.Rect(600, 100 + i * 30, 300, 25)
                    if rect.collidepoint(event.pos):
                        dropdown_open = False
                        selected = patient
                        inputs = {
                            'name': selected['name'],
                            'gfr': str(selected['gfr']),
                            'conditions': ", ".join(selected['conditions']),
                            'age': str(selected['age']),
                            'weight': str(selected['weight']),
                            'gender': selected['gender'],
                            'ethnicity': selected['ethnicity'],
                            'ALT': str(selected['ALT']),
                            'AST': str(selected['AST']),
                            'bilirubin': str(selected['bilirubin']),
                            'smoking': str(selected['lifestyle']['smoking']),
                            'alcohol': selected['lifestyle']['alcohol'],
                            'current_medications': ", ".join(selected['current_medications']),
                            'allergies': ", ".join(selected['allergies'])
                        }
                        break
            else:
                for field, rect in input_rects.items():
                    if rect.collidepoint(event.pos):
                        active_field = field
                        break
                if check_button.collidepoint(event.pos):
                    try:
                        patient = {
                            'name': inputs['name'],
                            'gfr': int(inputs['gfr']) if inputs['gfr'] else None,
                            'conditions': [s.strip().lower() for s in inputs['conditions'].split(',') if s.strip()],
                            'age': int(inputs['age']) if inputs['age'] else None,
                            'weight': int(inputs['weight']) if inputs['weight'] else None,
                            'gender': inputs['gender'].strip().lower(),
                            'ethnicity': inputs['ethnicity'].strip(),
                            'ALT': float(inputs['ALT']) if inputs['ALT'] else None,
                            'AST': float(inputs['AST']) if inputs['AST'] else None,
                            'bilirubin': float(inputs['bilirubin']) if inputs['bilirubin'] else None,
                            'genetic_variants': {},
                            'lifestyle': {
                                'smoking': inputs['smoking'].strip().lower() == 'true',
                                'alcohol': inputs['alcohol'].strip().lower()
                            },
                            'current_medications': [s.strip().lower() for s in inputs['current_medications'].split(',') if s.strip()],
                            'allergies': [s.strip().lower() for s in inputs['allergies'].split(',') if s.strip()]
                        }

                        eval_results = evaluate_patient(patient)
                        ddi_results = check_ddi(patient['current_medications'])
                        resp_results = check_respiratory_side_effects(patient['current_medications'])
                        lab_results = check_lab_thresholds(patient)

                        warnings = eval_results + ddi_results + resp_results + lab_results

                        if not warnings:
                            warnings = [{"Drug": patient['name'], "Reason": "✅ No major warnings found."}]

                    except Exception as e:
                        warnings = [{"Drug": "Input Error", "Reason": str(e)}]

        elif event.type == pygame.KEYDOWN and active_field:
            if event.key == pygame.K_BACKSPACE:
                inputs[active_field] = inputs[active_field][:-1]
            elif event.key == pygame.K_RETURN:
                active_field = None
            else:
                inputs[active_field] += event.unicode

        elif event.type == pygame.MOUSEWHEEL:
            if dropdown_open:
                scroll_offset = max(0, min(scroll_offset - event.y, len(patients) - visible_limit))

    # Draw dropdown
    pygame.draw.rect(screen, pygame.Color("lightblue"), dropdown_button)
    screen.blit(font.render("Import Patient", True, pygame.Color("black")), (dropdown_button.x + 10, dropdown_button.y + 5))

    if dropdown_open:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for i, patient in enumerate(patients[scroll_offset:scroll_offset + visible_limit]):
            entry_rect = pygame.Rect(600, 100 + i * 30, 300, 25)
            is_hovered = entry_rect.collidepoint(mouse_x, mouse_y)
            pygame.draw.rect(screen, pygame.Color("#e0f0ff") if is_hovered else pygame.Color("white"), entry_rect)
            pygame.draw.rect(screen, pygame.Color("black"), entry_rect, 1)
            screen.blit(font.render(patient['name'], True, pygame.Color("black")), (entry_rect.x + 5, entry_rect.y + 5))

    pygame.draw.line(screen, pygame.Color("gray"), (550, start_y - 10), (550, start_y + len(fields)*35 + 20), 2)

    for i, (field, rect) in enumerate(input_rects.items()):
        label = font.render(f"{field}:", True, pygame.Color("black"))
        screen.blit(label, (50, rect.y + 5))
        pygame.draw.rect(screen, pygame.Color("white"), rect)
        pygame.draw.rect(screen, pygame.Color("black"), rect, 2)
        value = inputs[field]
        rendered_text = font.render(value, True, pygame.Color("black"))
        screen.blit(rendered_text, (rect.x + 5, rect.y + 5))

    screen.blit(logo, (750, check_button.y - 160))
    pygame.draw.rect(screen, pygame.Color("darkslateblue"), check_button)
    screen.blit(font.render("Check Safety", True, pygame.Color("white")), (check_button.x + 30, check_button.y + 10))

    # Draw warnings table with headers
    pygame.draw.rect(screen, pygame.Color("lightgray"), results_rect)
    header = ["Type", "Drug", "Detail", "Level", "Reason"]
    col_widths = [140, 160, 180, 100, 300]
    col_x = results_rect.x + 10
    col_y = results_rect.y + 10

    for i, title in enumerate(header):
        text_surface = font.render(title, True, pygame.Color("black"))
        screen.blit(text_surface, (col_x, col_y))
        col_x += col_widths[i]

    col_y += 30
    for warning in warnings:
        col_x = results_rect.x + 10
        values = [
            warning.get("Type", "").replace("Drug–Drug Interaction", "Drug–Drug").replace("Drug–Disease Interaction", "Drug–Disease"),
            warning.get("Drug", ""),
            warning.get("Detail", ""),
            warning.get("Level", ""),
            warning.get("Reason", "")
        ]
        for i, value in enumerate(values):
            wrapped_lines = wrap_text(str(value), font, col_widths[i] - 10)
            for j, line in enumerate(wrapped_lines):
                color = pygame.Color("black")
                if i == 3:  # Level column coloring
                    if "minor" in value.lower():
                        color = pygame.Color("darkgreen")
                    elif "moderate" in value.lower():
                        color = pygame.Color("orange")
                    elif "major" in value.lower() or "high" in value.lower() or "caution" in value.lower():
                        color = pygame.Color("red")
                screen.blit(font.render(line, True, color), (col_x, col_y + j * (font.get_height() + 2)))
            col_x += col_widths[i]
        col_y += max(len(wrap_text(values[-1], font, col_widths[-1] - 10)), 1) * (font.get_height() + 4)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
