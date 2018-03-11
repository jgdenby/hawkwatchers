
def check(new_text, thresh = .25):
    new_text = new_text.strip()
    outcome = []

    outcome.append(len(new_text) > 200)

    d = enchant.Dict('en_US')

    word_list = new_text.split(' ')
    non_en = 0

    for w in word_listL
        if not d.check(w):
            non_en += 1

    outcome.append(non_en/len(word_list) <= thresh)

    if "econ" not in new_text:
        outcome.append(False)
    else:
        True

    if False in outcome:
        return False
    else:
        return True

    
