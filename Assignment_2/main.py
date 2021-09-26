from random import random
from random import choice
canser = [
    {'Menopause it40': False, 'Menopause ge40': True, 'Menopause premeno': False, 'Inv-nodes 0-2': False, 'Inv-nodes 3-5': True, 'Inv-nodes 6-8':  False, 'Deg-malign 1': False, 'Deg-malign 2': False, 'Deg-malign 3': True},
    {'Menopause it40': False, 'Menopause ge40': True, 'Menopause premeno': False, 'Inv-nodes 0-2': False, 'Inv-nodes 3-5': False, 'Inv-nodes 6-8': True,  'Deg-malign 1':  False, 'Deg-malign 2': False, 'Deg-malign 3': True},
    {'Menopause it40': False, 'Menopause ge40': False,'Menopause premeno': True, 'Inv-nodes 0-2':  True, 'Inv-nodes 3-5':  False, 'Inv-nodes 6-8': False, 'Deg-malign 1': False, 'Deg-malign 2': False,  'Deg-malign 3':  True},
]
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


example_condition = ['Menopause ge40', 'Inv-nodes 3-5', 'NOT Deg-malign 3']
example_condition2 = ['Menopause it40', 'Inv-nodes 0-2', 'Deg-malign 3']
example_condition3 = ['Menopause ge40', 'Inv-nodes 6-8', 'Deg-malign 3']

#print(evaluate_condition(canser[2], example_condition))


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


canser_rule = Memory(0.9, 0.1,{'Menopause it40': 1, 'NOT Menopause it40': 10,
                               'Menopause ge40': 1, 'NOT Menopause ge40': 1,
                               'Menopause premeno': 1, 'NOT Menopause premeno': 1,
                               'Inv-nodes 0-2': 1, 'NOT Inv-nodes 0-2': 1,
                               'Inv-nodes 3-5': 1, 'NOT Inv-nodes 3-5': 1,
                               'Inv-nodes 6-8':  1, 'NOT Inv-node 6-8':  1,
                               'Deg-malign 1': 1, 'NOT Deg-malign 1': 1,
                               'Deg-malign 2': 1, 'NOT Deg-malign 2': 1,
                               'Deg-malign 3': 10, 'NOT Deg-malign 3': 1})
print(f"R1: {canser_rule.get_condition()}")


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


for i in range(100):
    observation_id = choice([0,1,2])
    type_i_feedback(canser[observation_id], canser_rule)


print(canser_rule.get_memory())


print("IF " + " AND ".join(canser_rule.get_condition()) + " THEN Recurrence")


not_canser = [
    {'Menopause it40': True,  'Menopause ge40': False,'Menopause premeno': False, 'Inv-nodes 0-2': True, 'Inv-nodes 3-5':  False, 'Inv-nodes 6-8': False, 'Deg-malign 1': False, 'Deg-malign 2': False, 'Deg-malign 3': True},
    {'Menopause it40': False, 'Menopause ge40': True, 'Menopause premeno': False, 'Inv-nodes 0-2': True, 'Inv-nodes 3-5':  False, 'Inv-nodes 6-8': False, 'Deg-malign 1': False, 'Deg-malign 2': True, 'Deg-malign 3': False},
    {'Menopause it40': False, 'Menopause ge40': False,'Menopause premeno': True, 'Inv-nodes 0-2':  True, 'Inv-nodes 3-5':  False, 'Inv-nodes 6-8': False, 'Deg-malign 1': True,  'Deg-malign 2': False, 'Deg-malign 3': False},
]


def type_ii_feedback(observation, memory):
    if evaluate_condition(observation, memory.get_condition()) == True:
        for feature in observation:
            if observation[feature] == False:
                memory.memorize_always(feature)
            elif observation[feature] == True:
                memory.memorize_always('NOT ' + feature)


canser_rule = Memory(0.9, 0.1,{'Menopause it40': 1, 'NOT Menopause it40': 1,
                               'Menopause ge40': 1, 'NOT Menopause ge40': 1,
                               'Menopause premeno': 1, 'NOT Menopause premeno': 1,
                               'Inv-nodes 0-2': 1, 'NOT Inv-nodes 0-2': 1,
                               'Inv-nodes 3-5': 1, 'NOT Inv-nodes 3-5': 1,
                               'Inv-nodes 6-8':  1, 'NOT Inv-node 6-8':  1,
                               'Deg-malign 1': 1, 'NOT Deg-malign 1': 1,
                               'Deg-malign 2': 1, 'NOT Deg-malign 2': 1,
                               'Deg-malign 3': 10, 'NOT Deg-malign 3': 1})
print(f"R2: {canser_rule.get_condition()}")
for i in range(100):
    observation_id = choice([0,1,2])
    type_ii_feedback(not_canser[observation_id], canser_rule)
print(canser_rule.get_memory())


print("IF " + " AND ".join(canser_rule.get_condition()) + " THEN Recurrence")


print(canser_rule.get_memory())


def classify(observation, canser_rules, not_canser_rules):
    vote_sum = 0
    for canser_rule in canser_rules:
        if evaluate_condition(observation, canser_rule.get_condition()) == True:
            vote_sum += 1
    for not_canser_rule in not_canser_rules:
        if evaluate_condition(observation, not_canser_rule.get_condition()) == True:
            vote_sum -= 1
    if vote_sum >= 0:
        return "Recurrence"
    else:
        return "Non-Recurrence"


not_canser_rule = Memory(0.9, 0.1,{'Menopause it40': 1, 'NOT Menopause it40': 1,
                               'Menopause ge40': 1, 'NOT Menopause ge40': 1,
                               'Menopause premeno': 1, 'NOT Menopause premeno': 1,
                               'Inv-nodes 0-2': 10, 'NOT Inv-nodes 0-2': 1,
                               'Inv-nodes 3-5': 1, 'NOT Inv-nodes 3-5': 1,
                               'Inv-nodes 6-8':  1, 'NOT Inv-node 6-8':  1,
                               'Deg-malign 1': 1, 'NOT Deg-malign 1': 1,
                               'Deg-malign 2': 1, 'NOT Deg-malign 2': 1,
                               'Deg-malign 3': 1, 'NOT Deg-malign 3': 1})

print("Answer: Non-Recurrence, Predicated: " + classify(not_canser[1], [canser_rule], [not_canser_rule]))
print("Answer: Recurrence, Predicated: " + classify(canser[2], [canser_rule], [not_canser_rule]))