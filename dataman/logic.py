
MAX_ATTEMPTS = 2


def check_answer(correct_answer, submitted_answer, attempts_used):
    if attempts_used >= MAX_ATTEMPTS:
        return {
            "status": "revealed",
            "attempts_used": attempts_used,
            "message": "The correct answer is: " + correct_answer
        }

    attempts_used += 1

    if submitted_answer.strip().lower() == correct_answer.strip().lower():
        return {
            "status": "correct",
            "attempts_used": attempts_used,
            "message": "Correct! Great job."
        }

    if attempts_used >= MAX_ATTEMPTS:
        return {
            "status": "revealed",
            "attempts_used": attempts_used,
            "message": "The correct answer is: " + correct_answer
        }

    return {
        "status": "retry",
        "attempts_used": attempts_used,
        "message": "Incorrect. You have one attempt remaining."
    }
