# Dicionário com as variaveis
classes = {
    "t01": ["UC11", "UC12", "UC13", "UC14", "UC15"],
    "t02": ["UC21", "UC22", "UC23", "UC24", "UC25"],
    "t03": ["UC31", "UC32", "UC33", "UC34", "UC35"]
}

# Dicionario com as aulas que cada professor da
# nome do professor e o index
teacher_uc = {
    "jo": ["UC11", "UC21", "UC22", "UC31"],
    "mike": ["UC12", "UC23", "UC32"],
    "rob": ["UC13", "UC14", "UC24", "UC33"],
    "sue": ["UC15", "UC25", "UC34", "UC35"],
}

# Cria 20 slots vazios para cada professor
teacher_schedule = {
    "jo": [0] * 20,
    "mike": [0] * 20,
    "rob": [0] * 20,
    "sue": [0] * 20,
}

# Aulas com sala obrigatoria
room_schedule = {
    "lab01": ["UC14", "UC22"],
}

available_rooms = ["r01", "r02", "r03", "r04", "r05"] + list(room_schedule.keys())
# Aulas online
online_schedule = {
    "UC21": [2],
    "UC31": [2],
}

# Slots em que cada professor esta indisponivel
teacher_restrictions = {
    "mike": [12, 13, 14, 15, 16, 17, 18, 19],
    "rob": [0, 1, 2, 3],
    "sue": [8, 9, 10, 11, 16, 17, 18, 19],
    "jo": []
}

# cria vinte espacos numerados de 0 a 19(espacos do horario)
slots = list(range(20))

# cria dicionario em que a key é a turma e cada turma tem 5 arryas(cada dia da semana)
classes_por_dia = {turma: {d: [] for d in range(5)} for turma in classes.keys()}

# cria dicionario para guardar os slots disponiveis de cada professor(key=professor, value=lista de slots disponiveis)
teacher_available_slots = {}
# Preenche teacher_available_slots com os slots (0..19) que não estão nas restrições de cada professor
for teacher in teacher_schedule.keys():
    unavailable = set(teacher_restrictions.get(teacher, []))  # coloca os slots indisponiveis em um set
    available = [s for s in slots if
                 s not in unavailable]  # cria uma lista somente com os slots disponiveis por cada professor
    teacher_available_slots[teacher] = available  # adiciona ao dicionario o professor e os seus slots disponiveis

# cria dicionario para mapear cada UC ao seu professor
teacher_by_uc = {uc: teacher for teacher, ucs in teacher_uc.items() for uc in ucs}


def split_days(slots):
    return slots // 4


def max_three_per_day(*slots):
    # convert slot numbers to day indexes (0–4)
    days = [s // 4 for s in slots]
    # count how many per day, and ensure none exceed 3
    return all(days.count(day) <= 3 for day in range(5))






