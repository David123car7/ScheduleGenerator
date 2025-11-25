from constraint import *
from data import *
from collections import defaultdict

#duplica ucs mas com dias diferentes, e faz o seu dominio(soft)
#cria também a variável de SALA para cada sessão (R1/R2)
def schedule_teacher_uc(problem):
    for classe, ucs in classes.items():
        for uc in ucs:
            teacher = teacher_by_uc[uc]
            available = teacher_available_slots[teacher]
            problem.addVariable(f"{uc}_{classe}_D1", available)
            problem.addVariable(f"{uc}_{classe}_D2", available)
    return problem

#Dividir cada UC por dois dias por turma(soft)
def split_uc_day(problem):
    for classe, ucs in classes.items():
        for uc in ucs:
            d1 = f"{uc}_{classe}_D1"
            d2 = f"{uc}_{classe}_D2"
            problem.addConstraint(lambda a, b: split_days(a) !=split_days(b), (d1, d2))
    return problem


#coloca as mesma uc em dias diferentes(soft) 
def attribute_uc_day(problem):              
    for classe, ucs in classes.items():
        vars_classe = []
        for uc in ucs:
            vars_classe.append(f"{uc}_{classe}_D1")
            vars_classe.append(f"{uc}_{classe}_D2")
        problem.addConstraint(AllDifferentConstraint(), tuple(vars_classe))       
    return problem

def split_teacher_slot(problem):
    #Cria dicionario para guardar os slots dos professores
    teacher_slots = {}
    for classe, ucs in classes.items():
        for uc in ucs:
            #juntar as duas UC iguais, por professor
            teacher = teacher_by_uc[uc]
            teacher_slots.setdefault(teacher, []).extend([
                f"{uc}_{classe}_D1",
                f"{uc}_{classe}_D2",
            ])
    #adiciona a restricao a cada professor
    for teacher, slots in teacher_slots.items():
        problem.addConstraint(AllDifferentConstraint(), slots)
    return problem

def limit_uc_day(problem):
    for classe, ucs in classes.items():
        vars_classe = []
        for uc in ucs:
            vars_classe.append(f"{uc}_{classe}_D1")
            vars_classe.append(f"{uc}_{classe}_D2")

        problem.addConstraint(max_three_per_day, vars_classe)

    return problem

# HARD CONSTRAINT: Uma sala não pode ser utilizada por mais de uma aula no mesmo bloco horário.
def enforce_room_exclusivity(problem):
    # recolher todas as sessões (slot_var, room_var)
    sessions = []
    for classe, ucs in classes.items():
        for uc in ucs:
            slot1 = f"{uc}_{classe}_D1"
            slot2 = f"{uc}_{classe}_D2"
            room1 = f"{uc}_{classe}_R1"
            room2 = f"{uc}_{classe}_R2"
            sessions.append((slot1, room1))
            sessions.append((slot2, room2))

    # adiciona restrição par a par: não podem ter mesmo slot e mesma sala ao mesmo tempo
    def not_same_room_same_slot(sa, sb, ra, rb):
        # retorna True exceto quando sala e slot coincidem exatamente (que é proibido)
        return not (sa == sb and ra == rb)

    n = len(sessions)
    for i in range(n):
        for j in range(i+1, n):
            s1, r1 = sessions[i]
            s2, r2 = sessions[j]
            # se for exatamente a mesma variável, ignora
            if s1 == s2 and r1 == r2:
                continue
            problem.addConstraint(not_same_room_same_slot, (s1, s2, r1, r2))

    return problem


def attribute_room(problem):
    same_uc = []
    for classe, ucs in classes.items():
        for uc in ucs:
            same_uc.append((f"{uc}_{classe}_R1", f"{uc}_{classe}_D1"))
            same_uc.append((f"{uc}_{classe}_R2", f"{uc}_{classe}_D2"))

    for i in range(len(same_uc)):
        for j in range(i + 1, len(same_uc)):
            rA, dA = same_uc[i]
            rB, dB = same_uc[j]

            problem.addConstraint(
                lambda ra, sa, rb, sb: not (ra != "ONLINE" and rb != "ONLINE" and ra == rb and sa == sb),
                (rA, dA, rB, dB)
            )

    return problem


# HARD CONSTRAINT: Uma sala não pode ser utilizada por mais de uma aula no mesmo bloco horário.
def split_room(problem):
    for classe, ucs in classes.items():
        for uc in ucs:
            # cria variaveis de sala para cada sessao da UC
            r1 = f"{uc}_{classe}_R1"
            r2 = f"{uc}_{classe}_R2"

            if uc in room_schedule.get("lab01", []):
                # se a UC tem sala obrigatória, só pode usar essa sala
                obligatory_room1 = ["lab01"]
                obligatory_room2 = ["lab01"]
            else:
                # se a UC não tem sala obrigatória, pode usar qualquer sala disponível
                obligatory_room1 = available_rooms
                obligatory_room2 = available_rooms

            problem.addVariable(r1, obligatory_room1)
            problem.addVariable(r2, obligatory_room2)

            problem.addConstraint(lambda a, b: a == b, (r1, r2))
    return problem

def try_four_days_week(solution):
    for class_name, ucs_dict in solution.items():
        days = set()
        for uc, info in ucs_dict.items():
            slot = info.get("slot")
            days.add(slot // 4 + 1)
        if(len(days) != 4):
            return None

    return solution

def try_consecutive_ucs(solution):
    for class_name, ucs_dict in solution.items():
        slots_por_dia = defaultdict(list)

        for uc, info in ucs_dict.items():
            slot = info.get("slot")
            dia = slot // 4
            slots_por_dia[dia].append(slot)

        for slots in slots_por_dia.values():
            slots.sort()
            if len(slots) > 1:
                for i in range(len(slots) - 1):
                    if slots[i+1] - slots[i] != 1:
                        return None

    return solution

def try_uc_distinct_days(solution):
    for class_name, ucs_dict in solution.items():
        # group all UC sessions (D1, D2, ...) by UC base name
        grouped_by_uc = defaultdict(list)

        for uc_code, info in ucs_dict.items():
            slot = info.get("slot")
            dia = slot // 4
            uc_base = uc_code.split("_D")[0]  # e.g. UC12_D1 -> UC12
            grouped_by_uc[uc_base].append(dia)

        for uc, days in grouped_by_uc.items():
            if len(days) != len(set(days)):
                return None

    return solution

def score_solutions(solutions, solutionKey, scoreKey):
    solutions_scores = []
    for solution in solutions:
        for class_name, ucs_dict in solution.items():
            slots_por_dia = defaultdict(list)
            solution_scores_aux = {}
            score = 0

            for uc, info in ucs_dict.items():
                slot = info.get("slot")
                dia = slot // 4
                slots_por_dia[dia].append(slot)

            for slots in slots_por_dia.values():
                slots.sort()
                if len(slots) > 1:
                    for i in range(len(slots) - 1):
                        if slots[i+1] - slots[i] == 1:
                            score += 1

            solution_scores_aux[solutionKey] = solution
            solution_scores_aux[scoreKey] = score
            solutions_scores.append(solution_scores_aux)

    return solutions_scores




