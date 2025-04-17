import sys, os

# Pseudo-code for Gale-Shapley Algorithm:

# 1. Initialize all men and women to be free.
# 2. While there is a free man who hasn't proposed to every woman:
#    a. Choose such a man.
#    b. Choose the highest-ranked woman on his preference list to whom he has not yet proposed.
#    c. If the woman is free, engage her to the man.
#    d. If the woman is engaged, check if she prefers this new man over her current partner.
#       i. If she prefers the new man, engage her to the new man and make her old partner free.
#       ii. If she prefers her current partner, the new man remains free.
# 3. Repeat until there are no free men left who haven't proposed to every woman.


# Stable Matching Function:
# Initialize lists for unengaged men and proposals tracking.

# While there are unengaged men:
# Choose the first unengaged man and his preference list.
# For each preferred woman he hasn't proposed to:
# If she is free, engage them.
# If engaged, check if she prefers him over her current partner.
# If yes, re-engage her to him, make the former partner free.
# Continue until all men are engaged.
# Return the list of final matches and total proposals.

# Load Preferences Function:
# Read the number of participants.
# Read men and women's preferences into dictionaries.
# Return the preferences and count.
# Save Results Function:
# Write the matches and proposal count to an output file.

# Main Program:
# Read input file, extract preferences.
# Run stable matching, get matches and proposals.
# Save results to output file.

def stable_matching(mp, wp, count):
    m_uengd = list(mp.keys())
    pcount = {man: [] for man in mp}
    egnmts = {}

    while m_uengd:
        c_man = m_uengd[0]
        m_pref_list = mp[c_man]
        
        for w_pref in m_pref_list:

            if w_pref not in pcount[c_man]:
                pcount[c_man].append(w_pref)

                if w_pref not in egnmts:
                    egnmts[w_pref] = c_man
                    m_uengd.pop(0)

                else:
                    m_ctng = egnmts[w_pref]
                    wom_pref_list = wp[w_pref]
                
                    if wom_pref_list.index(c_man) < wom_pref_list.index(m_ctng):
                        egnmts[w_pref] = c_man
                        m_uengd.pop(0)
                        m_uengd.append(m_ctng)

                break

    stble_mtch = [(man, woman) for woman, man in egnmts.items()]
    all_prop = len(sum(pcount.values(), []))

    return stble_mtch, all_prop

def load_preferences(file_name):

    with open(file_name, 'r') as file:
        n_ptcp = int(file.readline().strip())

        mp = {}
        wp = {}

        for _ in range(n_ptcp):

            o_pref = file.readline().strip().split()
            mp[o_pref[0]] = o_pref[1:]

        for _ in range(n_ptcp):

            o_pref = file.readline().strip().split()
            wp[o_pref[0]] = o_pref[1:]

    return mp, wp, n_ptcp

def result(prev, m_res, p_all):
    o_fname = f'{prev}.txt'
    with open(o_fname, 'w') as file:
        for man, woman in m_res:
            file.write(f'{man} {woman}\n')
        file.write(f'{p_all}\n')
    
    print(f"Results saved to {o_fname}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)

    in_file = sys.argv[1]
    output_prev = in_file.split('.')[0].replace('input', 'output').replace('Input', 'Output')

    mp, wp, count = load_preferences(in_file)
    m_res, p_all = stable_matching(mp, wp, count)
    result(output_prev, m_res, p_all)
