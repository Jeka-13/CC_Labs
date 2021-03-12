# Made by: Chetrari Eugeniu
# Group: FAF-193
# Variant: (32 + 1) - 6 = 27

import json
import os
import graphviz


def import_nfa_from_json(input_file):
    file = open(input_file)
    json_file = json.load(file)

    transitions = {}  # key [state in states, action in alphabet]
    #                   value [Set of arriving states in states]
    for p in json_file['transitions']:
        transitions.setdefault((p[0], p[1]), set()).add(p[2])

    nfa = {
        'alphabet': set(json_file['alphabet']),
        'states': set(json_file['states']),
        'initial_states': set(json_file['initial_states']),
        'accepting_states': set(json_file['accepting_states']),
        'transitions': transitions
    }

    return nfa


def nfa_to_dfa(nfa):
    dfa = {
        'alphabet': nfa['alphabet'].copy(),
        'initial_state': None,
        'states': set(),
        'accepting_states': set(),
        'transitions': dict()
    }

    if len(nfa['initial_states']) > 0:
        dfa['initial_state'] = str(nfa['initial_states'])
        dfa['states'].add(str(nfa['initial_states']))

    sets_states = list()
    sets_queue = list()
    sets_queue.append(nfa['initial_states'])
    sets_states.append(nfa['initial_states'])
    if len(sets_states[0].intersection(nfa['accepting_states'])) > 0:
        dfa['accepting_states'].add(str(sets_states[0]))

    while sets_queue:
        current_set = sets_queue.pop(0)
        for a in dfa['alphabet']:
            next_set = set()
            for state in current_set:
                if (state, a) in nfa['transitions']:
                    for next_state in nfa['transitions'][state, a]:
                        next_set.add(next_state)
            if len(next_set) == 0:
                continue
            if next_set not in sets_states:
                sets_states.append(next_set)
                sets_queue.append(next_set)
                dfa['states'].add(str(next_set))
                if next_set.intersection(nfa['accepting_states']):
                    dfa['accepting_states'].add(str(next_set))

            dfa['transitions'][str(current_set), a] = str(next_set)

    return dfa


def dfa_visualize(dfa, name, path='./'):
    g = graphviz.Digraph(format='svg')
    g.node('fake', style='invisible')
    for state in dfa['states']:
        if state == dfa['initial_state']:
            if state in dfa['accepting_states']:
                g.node(str(state), root='true',
                       shape='doublecircle')
            else:
                g.node(str(state), root='true')
        elif state in dfa['accepting_states']:
            g.node(str(state), shape='doublecircle')
        else:
            g.node(str(state))

    g.edge('fake', str(dfa['initial_state']), style='bold')
    for transition in dfa['transitions']:
        g.edge(str(transition[0]),
               str(dfa['transitions'][transition]),
               label=transition[1])

    if not os.path.exists(path):
        os.makedirs(path)

    g.render(filename=os.path.join(path, name + '.dot'))


# driver code
json_auto = import_nfa_from_json("input.json")
dfa = nfa_to_dfa(json_auto)
dfa_visualize(dfa, "dfa")
