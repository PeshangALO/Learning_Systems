import random
import matplotlib.pyplot as pl


class Environment:
    def __init__(self, p_yes, r_yes):
        self.p_yes = p_yes
        self.r_yes = r_yes

    def penalty(self, action):
        if action == 0:
            if random.random() <= self.p_yes:
                return True
            else:
                return False
        elif action == 1:
            if random.random() <= self.p_yes:
                return True
            else:
                return False



class Tsetlin:
    def __init__(self, n):
        # n is the number of states per action
        self.n = n

        # Initial state selected randomly
        self.state = random.choice([self.n, self.n + 1])

    def reward(self):
        if self.state <= self.n and self.state > 1:
            self.state -= 1
        elif self.state > self.n and self.state < 2 * self.n:
            self.state += 1

    def penalize(self):
        if self.state <= self.n and self.state < 2 * self.n:
            self.state += 1
        elif self.state > self.n and self.state > 1:
            self.state -= 1

    def makeDecision(self):
        if self.state <= self.n:
            return 0
        else:
            return 1


Number_OF_States = 5
Number_Of_Round = 200
Number_Of_Auto = 5
Number_Of_Game = 10


def calculate_penalty(Number_Of_Yes):
    if Number_Of_Yes < 4:
        r_yes = Number_Of_Yes * 0.2
        p_yes = 1 - r_yes
        return p_yes, r_yes

    if Number_Of_Yes > 3:
        r_yes = 0.6 - (Number_Of_Yes - 3) * 0.2
        p_yes = 1 - r_yes
        return p_yes, r_yes


def create_automata(n_automata):
    Automata_array = []
    for i in range(n_automata):
        Automata_array.append(Tsetlin(Number_OF_States))
    return Automata_array


def calculate_action(a_array):
    action_array = []
    Number_Of_Yes = 0
    for i in range(len(a_array)):
        action_array.append(a_array[i].makeDecision())
        Number_Of_Yes += action_array[i]
    return action_array, Number_Of_Yes

def Average(lst):
    return sum(lst) / len(lst)


Preformance = []
for h in range(Number_Of_Game):
    plot_result = ([], [])
    Match = 0
    Accurcy = 0
    la_array = create_automata(Number_Of_Auto)
    for i in range(Number_Of_Round):
        action_array, Number_Of_Yes = calculate_action(la_array)

        if(Number_Of_Yes == 3):
            Match += 1

        plot_result[0].append(i)
        p_yes, r_yes = calculate_penalty(Number_Of_Yes)
        plot_result[1].append(Number_Of_Yes)
        env = Environment(p_yes, r_yes)

        for j in range(len(action_array)):
            penalty = env.penalty(action_array[j])
            if penalty:
                la_array[j].penalize()
            else:
                la_array[j].reward()

    Probability = Match / Number_Of_Round;
    Preformance.append(Probability)
    average = Average(Preformance)
    print(f"Number of round: {h}")
    print(f"Number of times the team get rewards: {Match} of {Number_Of_Round}" )
    print("Probability:", Probability)
    pl.plot(plot_result[0], plot_result[1])
    pl.show()

print(f"Average of rewarding probabilities of {Number_Of_Game} games:  ", average)
#print("#Action 1: ", action_count[0], "#Action 2:", action_count[1])
