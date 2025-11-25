import csv
from constraint import *
from data import *
import os


def break_solution_class(solution):
    """
    Transforma a solução plana (variáveis -> valores) numa estrutura:
    { "t01": { "UC11_D1": {"slot": int, "room": "lab01"}, "UC11_D2": {...}, ... }, ... }
    """
    final = {}

    for varname, value in solution.items():
        # parse robusto: pode assegurar que UC ou nomes com '_' não quebram
        parts = varname.rsplit('_')
        if len(parts) != 3:
            # variáveis que não sigam o padrão são ignoradas
            continue
        uc, classe, suffix = parts  # e.g. "UC11", "t01", "D1" or "R2"

        final.setdefault(classe, {})

        if suffix.startswith("D"):  # é um slot
            label = f"{uc}_{suffix}"
            # garante que a entrada existe e coloca o slot
            final[classe].setdefault(label, {"slot": None, "room": None})
            final[classe][label]["slot"] = int(value)
        elif suffix.startswith("R"):  # é uma sala
            # mapear para a correspondente D# (R1 -> D1)
            d_suffix = "D" + suffix[1:]
            label = f"{uc}_{d_suffix}"
            final[classe].setdefault(label, {"slot": None, "room": None})
            final[classe][label]["room"] = value

    # Filtra sessões incompletas (sem slot)
    for turma in list(final.keys()):
        final[turma] = {k: v for k, v in final[turma].items() if v["slot"] is not None}

    return final

#
def print_schedule_with_rooms_teachers(solution):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    for class_name, courses in solution.items():
        print(f"\n🧩 Class {class_name}")
        print("-" * (len(class_name) + 10))
        
        entries = []
        for course, info in courses.items():
            slot = info.get("slot")
            if slot is None or not isinstance(slot, int):
                continue
            day_index = slot // 4
            block = slot % 4 + 1
            room = info.get("room", "?")
            teacher = teacher_by_uc.get(course.split("_")[0], "?")
            entries.append((day_index, block, course, room, teacher))

        # Sort by day then by block
        entries.sort()

        # Print grouped by day
        current_day = None
        for day_index, block, course, room, teacher in entries:
            if day_index != current_day:
                print(f"  {days[day_index]}:")
                current_day = day_index
            print(f"    - {course}  (Block {block}, Room {room}, Teacher {teacher})")

    print("\n✅ End of schedule")



