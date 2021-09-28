from random import random
from random import choice
reccuring = [
    {'Menopause it40': False, 'Menopause ge40': True, 'Menopause premeno': False, 'Inv-nodes 0-2': False, 'Inv-nodes 3-5': True, 'Inv-nodes 6-8':  False, 'Deg-malign 1': False, 'Deg-malign 2': False, 'Deg-malign 3': True},
    {'Menopause it40': False, 'Menopause ge40': True, 'Menopause premeno': False, 'Inv-nodes 0-2': False, 'Inv-nodes 3-5': False, 'Inv-nodes 6-8': True,  'Deg-malign 1':  False, 'Deg-malign 2': False, 'Deg-malign 3': True},
    {'Menopause it40': False, 'Menopause ge40': False,'Menopause premeno': True, 'Inv-nodes 0-2':  True, 'Inv-nodes 3-5':  False, 'Inv-nodes 6-8': False, 'Deg-malign 1': False, 'Deg-malign 2': False,  'Deg-malign 3':  True},
]

not_reccuring = [
    {'Menopause it40': True,  'Menopause ge40': False,'Menopause premeno': False, 'Inv-nodes 0-2': True, 'Inv-nodes 3-5':  False, 'Inv-nodes 6-8': False, 'Deg-malign 1': False, 'Deg-malign 2': False, 'Deg-malign 3': True},
    {'Menopause it40': False, 'Menopause ge40': True, 'Menopause premeno': False, 'Inv-nodes 0-2': True, 'Inv-nodes 3-5':  False, 'Inv-nodes 6-8': False, 'Deg-malign 1': False, 'Deg-malign 2': True, 'Deg-malign 3': False},
    {'Menopause it40': False, 'Menopause ge40': False,'Menopause premeno': True, 'Inv-nodes 0-2':  True, 'Inv-nodes 3-5':  False, 'Inv-nodes 6-8': False, 'Deg-malign 1': True,  'Deg-malign 2': False, 'Deg-malign 3': False},
]


#To evaluate the condition of a rule
def evaluate_condition(observation, condition):
    truth_value_of_condition = True
    for feature in observation:
        if feature in condition and observation[feature] == False:
            truth_value_of_condition = False
            break
        if 'NOT ' + feature in condition and observation[feature] == True:
            truth_value_of_condition = False
            break
    return truth_value_of_condition


class Memory:
    def __init__(self, forget_value, memorize_value, memory):
        self.memory = memory
        self.forget_value = forget_value
        self.memorize_value = memorize_value

    def get_memory(self):
        return self.memory

    def get_literals(self):
        return list(self.memory.keys())

    def get_condition(self):
        condition = []
        for literal in self.memory:
            if self.memory[literal] >= 6:
                condition.append(literal)
        return condition

    def memorize(self, literal):
        if random() <= self.memorize_value and self.memory[literal] < 10:
            self.memory[literal] += 1

    def forget(self, literal):
        if random() <= self.forget_value and self.memory[literal] > 1:
            self.memory[literal] -= 1

    def memorize_always(self, literal):
        if self.memory[literal] < 10:
            self.memory[literal] += 1




#To produce frequent patteren with two learning steps:
#Check if the condition part of the rule is True by assessing the object's literals.
#If the condition part is True, then memorize all the literals that are True for the object.
#Forget all remaining literals.
def type_i_feedback(observation, memory):
    remaining_literals = memory.get_literals()
    if evaluate_condition(observation, memory.get_condition()) == True:
        for feature in observation:
            if observation[feature] == True:
                memory.memorize(feature)
                remaining_literals.remove(feature)
            elif observation[feature] == False:
                memory.memorize('NOT ' + feature)
                remaining_literals.remove('NOT ' + feature)
    for literal in remaining_literals:
        memory.forget(literal)

#The type_ii_feedback() method implements the third and final learning step:
#Check if the condition part of the rule is True by assessing the object’s literals.
#If the condition part is True, then memorize all Forgotten literals that are False for the object.
#This time there is no randomization – the increment is always performed.
def type_ii_feedback(observation, memory):
    if evaluate_condition(observation, memory.get_condition()) == True:
        for feature in observation:
            if observation[feature] == False:
                memory.memorize_always(feature)
            elif observation[feature] == True:
                memory.memorize_always('NOT ' + feature)

# To create recurrace rule
def create_reccurance_rule(recurrace_rule):
    for i in range(1000):
        observation_id = choice([0,1,2])
        num = choice([0,1])
        if num == 1:
            type_i_feedback(reccuring[observation_id], recurrace_rule)
        else:
            type_ii_feedback(not_reccuring[observation_id], recurrace_rule)

    # print(f"R2: {reccuring_rule.get_condition()}")
    print("IF " + " AND ".join(recurrace_rule.get_condition()) + " THEN Recurrence")

# To create non recurrace rule
def create_non_reccurance_rule(non_recurrace_rule):
    for i in range(1000):
        observation_id = choice([0,1,2])
        num = choice([0,1])
        if num == 1:
            type_i_feedback(not_reccuring[observation_id], non_recurrace_rule)
        else:
            type_ii_feedback(reccuring[observation_id], non_recurrace_rule)

    # print(f"R2: {reccuring_rule.get_condition()}")
    print("IF " + " AND ".join(non_recurrace_rule.get_condition()) + " THEN Non Recurrence")


def classify(observation, reccuring_rules, not_reccuring_rules):
    vote_sum = 0
    for reccuring_rule in reccuring_rules:
        if evaluate_condition(observation, reccuring_rule.get_condition()) == True:
            vote_sum += 1
    for not_reccuring_rule in not_reccuring_rules:
        if evaluate_condition(observation, not_reccuring_rule.get_condition()) == True:
            vote_sum -= 1
    if vote_sum >= 0:
        return "Recurrence"
    else:
        return "Non-Recurrence"

def classify_2(observation, reccuring_rules, not_reccuring_rules):
    vote_sum = 0
    for reccuring_rule in reccuring_rules:
        if evaluate_condition(observation, reccuring_rule.get_condition()) == True:
            vote_sum -= 1
    for not_reccuring_rule in not_reccuring_rules:
        if evaluate_condition(observation, not_reccuring_rule.get_condition()) == True:
            vote_sum += 1
    if vote_sum >= 0:
        return "Non-Recurrence"
    else:
        return "Recurrence"

reccuring_rule = Memory(0.8, 0.2, {'Menopause it40': 5, 'NOT Menopause it40': 5,
                               'Menopause ge40': 5, 'NOT Menopause ge40': 5,
                               'Menopause premeno': 5, 'NOT Menopause premeno': 5,
                               'Inv-nodes 0-2': 5, 'NOT Inv-nodes 0-2': 5,
                               'Inv-nodes 3-5': 5, 'NOT Inv-nodes 3-5': 5,
                               'Inv-nodes 6-8': 5, 'NOT Inv-nodes 6-8': 5,
                               'Deg-malign 1': 5, 'NOT Deg-malign 1': 5,
                               'Deg-malign 2': 5, 'NOT Deg-malign 2': 5,
                               'Deg-malign 3': 5, 'NOT Deg-malign 3': 5})


not_reccuring_rule = Memory(0.9, 0.1, {'Menopause it40': 5, 'NOT Menopause it40': 5,
                               'Menopause ge40': 5, 'NOT Menopause ge40': 5,
                               'Menopause premeno': 5, 'NOT Menopause premeno': 5,
                               'Inv-nodes 0-2': 5, 'NOT Inv-nodes 0-2': 5,
                               'Inv-nodes 3-5': 5, 'NOT Inv-nodes 3-5': 5,
                               'Inv-nodes 6-8': 5, 'NOT Inv-nodes 6-8': 5,
                               'Deg-malign 1': 5, 'NOT Deg-malign 1': 5,
                               'Deg-malign 2': 5, 'NOT Deg-malign 2': 5,
                               'Deg-malign 3': 5, 'NOT Deg-malign 3': 5})
# print(f"R3: {not_reccuring_rule.get_condition()}")
def predict_for_reccurance(reccuring_rule):
    create_reccurance_rule(reccuring_rule)
    for i in range(len(not_reccuring)):
        print(f"Answer{i}: Non-Recurrence, Predicated: " + classify(not_reccuring[i], [reccuring_rule], [not_reccuring_rule]))

    for i in range(len(reccuring)):
        print(f"Answer{i}: Recurrence, Predicated: " + classify(reccuring[i], [reccuring_rule], [not_reccuring_rule]))


def predict_for_non_reccurance(not_reccuring_rule):
    create_non_reccurance_rule(not_reccuring_rule)
    create_reccurance_rule(reccuring_rule)
    for i in range(len(not_reccuring)):
        print(f"Answer {i}: Non-Recurrence, Predicated: " + classify_2(not_reccuring[i], [reccuring_rule], [not_reccuring_rule]))

    for i in range(len(reccuring)):
        print(f"Answer {i}: Recurrence, Predicated: " + classify_2(reccuring[i], [reccuring_rule], [not_reccuring_rule]))

predict_for_reccurance(reccuring_rule)
# predict_for_non_reccurance(not_reccuring_rule)