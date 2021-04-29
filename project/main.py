import os

os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.27/bin'

from dfa import DFA

special_regex_characters = ["*", "(", ")", "+", "Σ"]

def extract_states_from_input(input_string):
    input_string = input_string.replace("{", "")
    input_string = input_string.replace("}", "")
    input_string = input_string.replace(",", " ")

    return input_string.split()

def extract_rule(input_string):
    input_string = input_string.replace(",", " ")
    rule_set = input_string.split()

    return rule_set

def extract_input_string(input_string):
    input_string_list = []
    for i in input_string:
        input_string_list.append(i)
    return input_string_list

class ProcessLayer:
    state = ""
    result = ""
    is_completely_processed = False

    def __init__(self, state, result, is_completely_processed):
        self.state = state
        self.result = result
        self.is_completely_processed = is_completely_processed


class NFA:
    inital_state = ""
    state_list = []
    alphabet_list = []
    final_state_list = []
    rule_set = []
    dfa = None

    def check_final_state_list(self):
        for i in self.final_state_list:
            if i not in self.state_list:
                raise Exception("Final state wrong. not in state list")

    def begin_program(self):
        state_input = input("1- input states: ")  # {q0,q1,q2,q3,q4,q5}
        alphabet_input = input("1- input alphabet: ")  # {a,b}
        final_state_input = input("1- input final states: ")  # {q1,q3}
        rule_count = input("1- input rule count: ")  # 6,

        self.state_list = extract_states_from_input(state_input)
        self.inital_state = self.state_list[0]
        self.alphabet_list = extract_states_from_input(alphabet_input)

        self.final_state_list = extract_states_from_input(final_state_input)
        self.check_final_state_list()

        rule_set = []
        for i in range(0, int(rule_count)):
            rule = input("input {0}st rule: ".format(i+1))
            rule_set.append(self.extract_rule(rule))
        self.rule_set = rule_set

    def check_input_string_list(self, input_string_list):
        for i in input_string_list:
            if (i not in self.alphabet_list):
                return False

        return True

    def get_next_state(self, initial_state, alphabet_word):
        next_direct_state_list = []
        for elem in self.rule_set:
            if elem[0] == initial_state and len(elem) == 3 and elem[2] == alphabet_word:
                next_direct_state_list.append(elem[1])

        next_indirect_state_list = []
        next_state_list_with_lambda = []
        for elem in self.rule_set:
            if elem[0] == initial_state and len(elem) == 2:
                next_state_list_with_lambda.append(elem[1])

        for elem in self.rule_set:
            for state in next_state_list_with_lambda:
                if elem[0] == state and len(elem) == 3 and elem[2] == alphabet_word:
                    next_indirect_state_list.append(elem[1])

        next_direct_state_list.extend(next_indirect_state_list)

        for elem in next_direct_state_list:
            for rule in self.rule_set:
                if len(rule) == 2 and rule[0] == elem:
                    next_direct_state_list.append(rule[1])

        return list(set(next_direct_state_list))

    def travers_nfa(self, input_string_list, input_string_length):
        self.check_input_string_list(input_string_list)
        current_state_list = []
        first_word = True
        for i in range(0, input_string_length):
            alphabet_word = input_string_list.pop(0)
            if first_word:
                next_states = self.get_next_state(
                    self.inital_state, alphabet_word)
                current_state_list = next_states
                first_word = False

            else:
                next_state_list = []
                current_state_list_length = len(current_state_list)
                for j in range(0, current_state_list_length):
                    current_state = current_state_list.pop(0)
                    result = self.get_next_state(current_state, alphabet_word)
                    next_state_list.extend(result)

                current_state_list.extend(next_state_list)
            current_state_list = list(set(current_state_list))

        return current_state_list

    def is_accepted_by_nfa(self):
        input_string = input('1- input string,e.g aabba: ')
        input_string_list = extract_input_string(input_string)

        final_path_state_list = self.travers_nfa(
            input_string_list, len(input_string_list))
        for state in final_path_state_list:
            if state in self.final_state_list:
                return True

        return False

    def draw_nfa(self):
        from graphviz import Digraph

        diagram = Digraph('nfa', format='png')
        diagram.attr(rankdir='q', size='15')

        diagram.attr('node', shape='doublecircle')
        for final_state in self.final_state_list:
            diagram.node(final_state)

        diagram.attr('node', shape='circle')
        for rule in self.rule_set:
            if len(rule) == 2:
                diagram.edge(rule[0], rule[1], label='')
            else:
                diagram.edge(rule[0], rule[1], label=rule[2])

        diagram.view(quiet_view=True)

        return

    def Union(self,lst1, lst2):
        final_list = list(set(lst1) | set(lst2))
        return final_list
    
    def get_all_states_from(self, state):
        next_states = []
        for rule in self.rule_set:
            if rule[0] == state:
                if len(rule) == 2:
                    next_states.append([rule[1], ''])
                else:
                    next_states.append(rule[1:])
        return next_states
    
    def get_all_states_to(self, state):
        next_states = []
        for rule in self.rule_set:
            if rule[1] == state:
                if len(rule) == 2:
                    next_states.append([rule[0], ''])
                else:
                    next_states.append([rule[0], rule[2]])
        return next_states
    
    def find_regex(self):
        from copy import deepcopy
        tmpNFA = deepcopy(self)
        tmpNFA.rule_set.append(['start', self.inital_state])
        tmpNFA.state_list.append('start')
        tmpNFA.inital_state = 'start'
        for final_state in self.final_state_list:
            tmpNFA.rule_set.append([final_state, 'final'])
        tmpNFA.state_list.append('final')
        tmpNFA.final_state_list = ['final']
        while True:
            transitions_from_start = tmpNFA.get_all_states_from('start')
            next_state, next_exp = '', ''
            for state, exp in transitions_from_start:
                if state != 'final':
                    next_state = state
                    next_exp = exp
                    break
            if next_state == '':
                reg_exp = transitions_from_start[0][1]
                for i in range(1, len(transitions_from_start)):
                    reg_exp += ' + ' + transitions_from_start[i][1]
                return reg_exp
            states_from_next = tmpNFA.get_all_states_from(next_state)
            states_to_next = tmpNFA.get_all_states_to(next_state)
            if len(states_to_next) == 0:
                return 'null'
            from_dict = {}
            to_dict = {}
            for state_a, exp_a in states_to_next:
                if exp_a == '':
                    exp = 'λ'
                else:
                    exp = exp_a
                if state_a in from_dict:
                    from_dict[state_a] += ' + ' + exp
                else:
                    from_dict[state_a] = exp
            for state_b, exp_b in states_from_next:
                if exp_b == '':
                    exp = 'λ'
                else:
                    exp = exp_b
                if state_b in to_dict:
                    to_dict[state_b] += ' + ' + exp
                else:
                    to_dict[state_b] = exp
            for state in from_dict:
                from_dict[state] = '(' + from_dict[state] + ')'
            for state in to_dict:
                to_dict[state] = '(' + to_dict[state] + ')'
            loop = ''
            if next_state in from_dict:
                loop_base = from_dict[next_state]
                if len(loop_base) == 3:
                    loop = loop_base[1] + '*'
                else:
                    loop = loop_base + '*'
            for state_a in from_dict:
                if state_a == next_state:
                    continue
                exp_a = from_dict[state_a]
                if exp_a == '(λ)':
                    exp_from = ''
                elif '+' in exp_a:
                    exp_from = exp_a
                else:
                    exp_from = exp_a[1:-1]
                for state_b in to_dict:
                    if state_b == next_state:
                        continue
                    exp_b = to_dict[state_b]
                    if exp_b == '(λ)':
                        exp_to = ''
                    elif '+' in exp_b:
                        exp_to = exp_b
                    else:
                        exp_to = exp_b[1:-1]
                    transition = [state_a, state_b, exp_from + loop + exp_to]
                    tmpNFA.rule_set.append(transition)
            tmpNFA.rule_set = [t for t in tmpNFA.rule_set if not (t[0] == next_state or t[1] == next_state)]
            tmpNFA.state_list.remove(next_state)
    
    def convert_to_dfa(self):
        import collections
        compare = lambda x, y: collections.Counter(x) == collections.Counter(y)
        table = []
        for i in range(len(self.alphabet_list)):
            x=[]
            table.append(x)
        running = True
        table_states=[]
        table_states.append([self.inital_state])
        trap_state=False
        while(running):
            generated_state=[]
            for i in range(len(table_states)):
                for j in range(len(self.alphabet_list)):
                    add_list=[]
                    for k in range(len(table_states[i])):
                        if (len(self.get_next_state(table_states[i][k], self.alphabet_list[j])) != 0):
                            add_list=self.Union(add_list,self.get_next_state(table_states[i][k],self.alphabet_list[j]))
                    if(i >= len(table[j])):
                        if(len(add_list) == 0 and i >= len(table[j])):
                            table[j].append([""])
                            trap_state=True
                        else:
                            table[j].append(add_list)
                            generated_state.append(add_list)

            new_state=0
            for i in range(len(generated_state)):
                exist = False
                for j in range(len(table_states)):
                    if(compare(generated_state[i],table_states[j])):
                        exist=True
                if(not(exist)):
                    table_states.append(generated_state[i])
                    new_state+=1
            if(new_state==0):
                running=False

        if(trap_state):
            table_states.append([""])
            for i in range(len(self.alphabet_list)):
                table[i].append([""])
        table_final_states=[]
        table_states_dfa=[]
        final_states_dfa=[]
        transition_dfa=[]
        for i in range(len(table_states)):
            table_states_dfa.append('[%s]' % ', '.join(map(str, table_states[i])))
            for p in range(len(self.alphabet_list)):
                    table[p][i]='[%s]' % ', '.join(map(str, table[p][i]))
                    transition_dfa.append([table_states_dfa[i],table[p][i],self.alphabet_list[p]])
            for j in range(len(self.final_state_list)):
                if(self.final_state_list[j] in table_states[i]):
                    table_final_states.append(table_states[i])
                    break
        for i in range(len(table_final_states)):
            final_states_dfa.append('[%s]' % ', '.join(map(str, table_final_states[i])))

        DFAO = DFA(table_states_dfa,self.alphabet_list,final_states_dfa,transition_dfa)
        return DFAO


def input_dfa(dfa):
    state_input = input("1- input states: ")  # {q0,q1,q2,q3,q4,q5}
    alphabet_input = input("1- input alphabet: ")  # {a,b}
    final_state_input = input("1- input final states: ")  # {q1,q3}
    rule_count = input("1- input rule count: ")  # 6,

    state_list = extract_states_from_input(state_input)
    inital_state = self.state_list[0]
    alphabet_list = extract_states_from_input(alphabet_input)
    final_state_list = extract_states_from_input(final_state_input)

    rule_set = []
    for i in range(0, int(rule_count)):
        rule = input("input {0}st rule: ".format(i+1))
        rule_set.append(extract_rule(rule))
    
    dfa = DFA(state_list, alphabet_list, final_state_list, rule_set)

if __name__ == "__main__":
    nfa = NFA()
    dfa = None

    while True:
        print('#' * 80)
        print('NFA-isaccept: read string from input and check if it is accepted by NFA')
        print('NFA-regex: find the regular expression corresponding to NFA')
        print('NFA-show: show the diagram corresponding to NFA')
        print('NFA-convert: convert NFA to DFA')
        print('#' * 80)
        print('DFA-isaccept: read string from input and check if it is accepted by DFA')
        print('DFA-simple: create the simplified equivalent to existing DFA')
        print('DFA-show: show the diagram corresponding to DFA')
        print('#' * 80)
        print('nfa-input: read arguments from input and create a NFA')
        print('dfa-input: read arguments from input and create a DFA')
        print('exit: quit the program')
        print('#' * 80)
        input_command = input().lower()
        if input_command == 'nfa-input':
            nfa.begin_program()
        elif input_command == 'dfa-input':
            input_dfa(dfa)
        elif input_command == 'exit':
            break
        elif input_command == 'nfa-isaccept':
            is_accepted = nfa.is_accepted_by_nfa()
            if is_accepted:
                print("string is accepted")
            else:
                print("string is NOT accepted")
        elif input_command == 'nfa-show':
            nfa.draw_nfa()
            print("NFA diagram generated successfuly!")
        elif input_command == 'nfa-regex':
            regex = nfa.find_regex()
            print("the generated regex is: " + regex)
        elif input_command == 'nfa-convert':
            dfa = nfa.convert_to_dfa()
            print("DFA generated successfuly!")
        elif input_command == 'dfa-isaccept':
            string = input('Please enter your desired string:')
            if dfa.isAcceptByDFA(string):
                print("string is accepted")
            else:
                print("string is NOT accepted")
        elif input_command == 'dfa-simple':
            simplified_dfa = dfa.makeSimpleDFA()
            simplified_dfa.draw_dfa()
            print("DFA successfully simplified!")
        elif input_command == 'dfa-show':
            dfa.draw_dfa()
        else:
            print('Invalid command! Please try again.')
