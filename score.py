"""Keeps track of the score"""

score = {
    # "Sofia": 10,
    # "Amy": 3,
    # "Raul": 20
}

def update_score(name):
    if name in score:
        score[name] += 1
    else:
        score[name] = 1

def get_final_score():
    final_score = "AND THE SCORES ARE:\n"
    for key in score:
        final_score += key + ": " + str(score[key]) + "\n"

    return final_score

print(get_final_score())