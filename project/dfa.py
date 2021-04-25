import itertools

class DFA:
    def __init__(self, states, alphabet, final_states, transition_list):
        self.alphabet = alphabet
        self.transition_list=transition_list
        self.states = states
        self.initial_state = states[0]
        self.final_states = final_states
        self.transition_table = {q : {} for q in states}
        for t in transition_list:
            self.transition_table[t[0]][t[2]] = t[1]
    
    def isAcceptByDFA(self, input):
        state = self.initial_state
        for c in input:
            state = self.transition_table[state][c]
        return state in self.final_states
    
    def states_are_equal(self, q1, q2, t1, t2):
        if (q1 in self.final_states) != (q2 in self.final_states):
            return False
        for c in self.alphabet:
            if not (t1[c] == t2[c] or t1[c] == q2 or t2[c] == q1):
                return False
        return True

    def makeSimpleDFA(self):
        found_new_state = True
        reachable_states = set([self.initial_state])
        while found_new_state:
            new_reachable_states = set(itertools.chain.from_iterable \
                                 (self.transition_table[q].values() \
                                 for q in reachable_states)).union(reachable_states)
            found_new_state = reachable_states != new_reachable_states
            reachable_states = new_reachable_states
        new_transition_table = {q : self.transition_table[q] \
             for q in reachable_states}
        state_group = {q : q for q in reachable_states}
        found_extra_state = True
        while found_extra_state:
            found_extra_state = False
            temp_transition_table = new_transition_table
            new_transition_table = {self.initial_state \
                : temp_transition_table[self.initial_state]}
            for state in temp_transition_table:
                if state == self.initial_state:
                    continue
                transition = temp_transition_table[state]
                state_is_new = True
                for new_state in new_transition_table:
                    new_transition = new_transition_table[new_state]
                    if self.states_are_equal(state, new_state\
                        , transition, new_transition):
                        state_is_new = False
                        found_extra_state = True
                        for q in reachable_states:
                            if state_group[q] == state:
                                state_group[q] = new_state
                        
                if state_is_new:
                    new_transition_table[state] = transition
        new_final_states = [q for q in self.final_states \
                             if q in new_transition_table]
        new_transition_list = [[q, state_group[new_transition_table[q][c]], c] \
             for c in self.alphabet for q in new_transition_table]
        return DFA(list(new_transition_table.keys()), self.alphabet, \
                     new_final_states, new_transition_list)
    def draw_dfa(self):
        from graphviz import Digraph

        diagram = Digraph('dfa', format='png')
        diagram.attr(rankdir='q', size='15')
        diagram.attr('node', shape='doublecircle')
        for final_state in self.final_states:
            diagram.node(final_state)
        diagram.attr('node', shape='circle')
        for rule in self.transition_list:
                diagram.edge(rule[0], rule[1], label=rule[2])

        diagram.render()

        return

dfa = DFA(['q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6']\
        , ['a', 'b']\
        , ['q1', 'q5']\
        , [['q0', 'q1', 'a'],\
            ['q0', 'q2', 'b'],\
            ['q1', 'q0', 'a'],\
            ['q1', 'q0', 'b'],\
            ['q2', 'q3', 'a'],\
            ['q2', 'q4', 'b'],\
            ['q3', 'q1', 'a'],\
            ['q3', 'q2', 'b'],\
            ['q4', 'q1', 'a'],\
            ['q4', 'q2', 'b'],\
            ['q5', 'q5', 'a'],\
            ['q5', 'q6', 'b'],\
            ['q6', 'q6', 'a'],\
            ['q6', 'q5', 'b']])
# print(dfa.transition_table)

# print(dfa.isAcceptByDFA('ababa'))
# print(dfa.isAcceptByDFA('ababab'))
# print(dfa.isAcceptByDFA('abaab'))

# opt = dfa.makeSimpleDFA()
# print(opt.transition_table)