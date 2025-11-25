from constrains import *
from utils import *

problem = Problem()
t = schedule_teacher_uc(problem)
t = split_room(t)
t = attribute_room(t)
t = split_uc_day(t)
t = attribute_uc_day(t)
t = limit_uc_day(t)
t = split_teacher_slot(t)

final_solutions = []
feasible_solutions = 0
optimal_solutions = 0
number_of_tries = 10

four_days_week_soft = 0
uc_distinct_days_soft = 0
consecutive_ucs_soft = 0

#Get Solutions
hard_solutions = []
for i, solution in enumerate(t.getSolutionIter()):
    sol = break_solution_class(solution)
    feasible_solutions += 1
    if sol != None:
        hard_solutions.append(sol)
    if i >= number_of_tries:
        break

if(len(hard_solutions) > 0):
    #four days a week (soft)
    first_soft = []
    for i in range(len(hard_solutions)):
        sol = try_four_days_week(hard_solutions[i])
        if sol != None:
            first_soft.append(sol)
            four_days_week_soft += 1

    if(len(first_soft) > 0):
        #Distinct ucs in same day (soft)
        second_soft = []
        for i in range(len(first_soft)):
            sol = try_uc_distinct_days(first_soft[i])
            if (sol != None):
                second_soft.append(sol)
                uc_distinct_days_soft += 1

        if(len(second_soft) > 0):
            #Consecutive ucs in same day (soft)
            third_soft = []
            for i in range(len(second_soft)):
                 sol = try_consecutive_ucs(second_soft[i])
                 if(sol != None):
                     third_soft.append(sol)
                     consecutive_ucs_soft += 1

            if (len(third_soft) > 0):
                final_solutions = third_soft
            else:
                final_solutions = second_soft
        else:
            final_solutions = first_soft
    else:
        final_solutions = hard_solutions

    # Gets the best solution
    solutions_score = score_solutions(final_solutions, "solution", "score")
    best_solution = None
    for i in range(len(solutions_score)):
        if best_solution == None:
            best_solution = solutions_score[i]

        if (solutions_score[i]["score"] > best_solution["score"]):
            best_solution = solutions_score[i]

    print("--------------SOLUTIONS--------------")
    print("Possible Solutions: ", number_of_tries + 1)
    print("Feasible Solutions: ", feasible_solutions)
    print("Optimal Solutions: ", optimal_solutions)
    print("Best Solution Score: ", best_solution["score"])
    print("----------------DEBUG----------------")
    print("four_days_week_soft", four_days_week_soft)
    print("uc_distinct_days_soft", uc_distinct_days_soft)
    print("consecutive_ucs_soft", consecutive_ucs_soft)
    print_schedule_with_rooms_teachers(best_solution["solution"])


else:
    print("No solution found")
    
    


