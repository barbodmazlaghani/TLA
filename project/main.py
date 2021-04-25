import os

os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.27/bin'

from dfa import DFA

special_regex_characters = ["*", "(", ")", "+", "Σ"]


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

    def extract_states_from_input(self, input_string):
        input_string = input_string.replace("{", "")
        input_string = input_string.replace("}", "")
        input_string = input_string.replace(",", " ")

        return input_string.split()

    def extract_rule(self, input_string):
        input_string = input_string.replace(",", " ")
        rule_set = input_string.split()
        if rule_set[0] not in self.state_list:
            raise Exception("Rule wrong. not in state list")

        return rule_set

    def extract_input_string(self, input_string):
        input_string_list = []
        for i in input_string:
            input_string_list.append(i)
        return input_string_list

    def check_final_state_list(self):
        for i in self.final_state_list:
            if i not in self.state_list:
                raise Exception("Final state wrong. not in state list")

    def begin_program(self):
        # state_input = input("1- input states: ")  # {q0,q1,q2,q3,q4,q5}
        state_input = "{q0,q1,q2,q3,q4,q5,q6}"
        # alphabet_input = input("1- input alphabet: ")  # {a,b}
        alphabet_input = "{a,b}"
        # final_state_input = input("1- input final states: ")  # {q1,q3}
        final_state_input = "{q1,q3,q6}"
        # rule_count = input("1- input rule count: ")  # 6,
        rule_count = "9"

        self.state_list = self.extract_states_from_input(state_input)
        self.inital_state = self.state_list[0]
        self.alphabet_list = self.extract_states_from_input(alphabet_input)

        self.final_state_list = self.extract_states_from_input(
            final_state_input)
        self.check_final_state_list()

        rule_set = []
        # for i in range(0, int(rule_count)):
        #     rule = input("input {0}st rule: ".format(i+1))
        #    rule_set.append(self.extract_rule(rule))
        temp_rule_set = ["q0,q1,a",
                         "q1,q1,b",
                         "q1,q2,",
                         "q2,q3,a",
                         "q3,q2,a",
                         "q3,q4,b",
                         "q2,q5,b",
                         "q5,q6,a",
                         "q6,q1,b"]
        for elem in temp_rule_set:
            rule_set.append(self.extract_rule(elem))
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

        # print("state: " + str(initial_state) + " alphabet_word: " + str(alphabet_word) + " next_state: " + str(next_direct_state_list))
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
        input_string_list = self.extract_input_string(input_string)

        final_path_state_list = self.travers_nfa(
            input_string_list, len(input_string_list))
        for state in final_path_state_list:
            if state in self.final_state_list:
                return True

        return False

    def draw_nfa(self):
        from graphviz import Digraph

        diagram = Digraph('nfa', format='png')
        diagram.attr(rankdir='q', size='8,5')

        diagram.attr('node', shape='doublecircle')
        for final_state in self.final_state_list:
            diagram.node(final_state)

        diagram.attr('node', shape='circle')
        for rule in self.rule_set:
            if len(rule) == 2:
                diagram.edge(rule[0], rule[1], label='')
            else:
                diagram.edge(rule[0], rule[1], label=rule[2])

        diagram.render()

        return

    def Union(self,lst1, lst2):
        final_list = list(set(lst1) | set(lst2))
        return final_list

    def convert_to_dfa(self):
        import collections
        compare = lambda x, y: collections.Counter(x) == collections.Counter(y)
        table = []
        for i in range(len(self.alphabet_list)):
            x=[]
            table.append(x)
        running = True;
        table_states=[]
        table_states.append([self.inital_state])
        trap_state=False;
        #print(self.get_next_state(self.state_list[4],"a"))
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





if __name__ == "__main__":
    nfa = NFA()
    nfa.begin_program()

    while True:
        input_command = input(
            "1 - for checking string, enter 1: \n2 - for generating dfa, enter 2: \n3 - for drawing nfa, enter 3: \n4 - to create regex, enter 4: \n5 - to exit, enter 5: \n")

        if int(input_command) == 1:
            is_accepted = nfa.is_accepted_by_nfa()
            if is_accepted:
                print("string is accepted")
            else:
                print("string is NOT accepted")

        elif int(input_command) == 2:
            generated_dfa = nfa.convert_to_dfa()
            print("DFA generated successfuly!")

        elif int(input_command) == 3:
            nfa.draw_nfa()
            print("NFA generated successfuly!")

        elif int(input_command) == 4:
            regex = nfa.find_regex()
            print("the generated regex is: " + regex)

        elif int(input_command) == 5:
            break
