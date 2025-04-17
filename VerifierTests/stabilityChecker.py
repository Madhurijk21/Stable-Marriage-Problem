import sys
import re

def pref(f_name):
    with open(f_name, 'r') as file:
        lines = file.readlines()
        p_count = int(lines[0].strip())
        mp = {}
        fp = {}

        for i in range(1, p_count + 1):
            pref = lines[i].strip().split()
            mp[pref[0]] = pref[1:]

        for i in range(p_count + 1, 2 * p_count + 1):
            pref = lines[i].strip().split()
            fp[pref[0]] = pref[1:]

    return mp, fp, p_count

def m_file(f_name):
    egmnts = {}

    with open(f_name, 'r') as file:
        lines = file.readlines()
        for line in lines:
            ptns = line.split()

            if len(ptns) != 2:
                print(f"Skipping invalid line: {line.strip()}")
                continue
            man, woman = ptns
            egmnts[man] = woman.strip()
    print("Loaded egmnts Dictionary:", egmnts)
    return egmnts

def stability_checker(mp1, fp1, egmnts):
    print("egmnts Dictionary:", egmnts)
    rgmnts = {woman: man for man, woman in egmnts.items()}
    print("Reversed egmnts Dictionary:", rgmnts)

    for cm1, cw1 in egmnts.items():

        print(f"Verifying engagement: {cm1} -> {cw1}")
        m_pref = mp1.get(cm1, [])
        w_pref = fp1.get(cw1, [])

        if not m_pref or not w_pref:
            print(f"Warning: Missing pref for {cm1} or {cw1}.")
            continue

        for w_pref2 in m_pref:
            if w_pref2 == cw1:
                break
            cmn1 = rgmnts.get(w_pref2, None)

            if cmn1 is None:
                print(f"Warning: {w_pref2} not in egmnts dictionary.")
                continue
            w_pref2_pref_list = fp1.get(w_pref2, [])

            if cmn1 not in w_pref2_pref_list:
                print(f"Warning: {cmn1} not in pref of {w_pref2}.")
                continue

            if w_pref2_pref_list.index(cm1) < w_pref2_pref_list.index(cmn1):
                print(f"Unstable pair found: {cm1} prefers {w_pref2}, and {w_pref2} prefers {cm1} over {cmn1}.")
                return "unstable"

    return "stable"

def result(f_name, rst):
    with open(f_name, 'w') as file:
        file.write(rst + '\n')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python stabilityChecker.py <pref__file_> <egmnts__file_>")
        sys.exit(1)

    pref__file_ = sys.argv[1]
    egmnts__file_ = sys.argv[2]

    match_index = re.search(r'input(\d+)', pref__file_, re.IGNORECASE)
    if match_index:
        prev = match_index.group(1)
        out_res = f"verified{prev}.txt"
    else:
        out_res = "verified.txt"


    mp, fp, _ = pref(pref__file_)
    egmnts = m_file(egmnts__file_)
    sts = stability_checker(mp, fp, egmnts)
    result(out_res, sts)

    print(f"Verification result saved to {out_res}")
