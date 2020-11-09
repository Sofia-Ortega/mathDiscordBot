"""Keeps track of the score"""

score = {
    # channel1_id : { "Sofia": 10, "Amy": 3, "Raul": 20 }
    # channel2_id : { "Jake": 5, "Bob": 2, "Paul": 10 }
}

def update_score(channel_id, name):
    try:
        if name in score[channel_id]:
            score[channel_id][name] += 1
        else:
            score[channel_id][name] = 1
    except:
        score[channel_id] = {}
        if name in score[channel_id]:
            score[channel_id][name] += 1
        else:
            score[channel_id][name] = 1

def get_final_score(channel_id):
    final_score = ''
    for key in score[channel_id]:
        final_score += key + ": " + str(score[channel_id][key]) + "\n"

    return final_score

def reset_score(channel_id):
    score[channel_id].clear()
