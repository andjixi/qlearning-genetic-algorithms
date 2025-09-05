from geneticAlgorithmCore import *
from collections import defaultdict

class QLearningAgent:
    def __init__(self, actions, alpha=0.2, gamma=0.9, epsilon_start=0.2, epsilon_end=0.02, total_steps=1):
        self.actions = list(actions)
        self.alpha = alpha # learning rate 
        self.gamma = gamma # discount factor
        self.epsilon_start = epsilon_start # initial exploration rate
        self.epsilon_end = epsilon_end # final exploration rate
        self.total_steps = max(1, total_steps) 
        self.step_count = 0
        self.Q = defaultdict(lambda: {a: 0.0 for a in self.actions}) # Q[state][action] = value

    # epsilon decay: gradually decreases exploration
    def epsilon(self):
        frac = min(1.0, self.step_count / self.total_steps)
        return self.epsilon_start + (self.epsilon_end - self.epsilon_start) * frac

    # choose an action using epsilon-greedy strategy
    def select_action(self, state):
        eps = self.epsilon()
        self.step_count += 1

        # with probability eps → explore 
        if random.random() < eps:
            return random.choice(self.actions)
        
        # # otherwise → exploit (choose action with max Q-value)
        qsa = self.Q[state]
        return max(qsa, key = qsa.get)
    

    def update(self, s, a, r, s_next):
        qsa = self.Q[s][a]
        max_next = max(self.Q[s_next].values()) if self.Q[s_next] else 0.0
        self.Q[s][a] = qsa + self.alpha*(r + self.gamma * max_next - qsa)


def genetic_algorithm_qlearning(problem, population_size=50, generations=50, tournament_size=3, mutation_rate=0.05,
                                elitism_size=2, alpha=0.2, gamma=0.9, epsilon_start=0.2, epsilon_end=0.02):

    # initialize population and agents  
    population = [Individual(problem) for _ in range(population_size)]

    crossover_actions = ['single_point','two_point','uniform','arithmetic']
    mutation_actions = ['bit_flip','swap','scramble']

    cx_agent = QLearningAgent(crossover_actions, alpha, gamma, epsilon_start, epsilon_end, generations)
    mut_agent = QLearningAgent(mutation_actions, alpha, gamma, epsilon_start, epsilon_end, generations)


    # operators
    mutation_ops = {
        'bit_flip': lambda ind: bit_flip_mutation(ind, mutation_rate),
        'swap': swap_mutation,
        'scramble': scramble_mutation
    }
    crossover_ops = {
        'single_point': single_point_crossover,
        'two_point': two_point_crossover,
        'uniform': uniform_crossover,
        'arithmetic': arithmetic_crossover
    }       

    # track the best fitness
    best_so_far = max(population,key=lambda ind: ind.fitness).fitness 
    improved_prev = 0 # indicator if last iteration improved

    # action_log = []

    for gen in range(generations):
        population.sort(key=lambda ind: ind.fitness, reverse=True)
        new_population = population[:elitism_size]

        # phase of evolution
        phase = 0 if gen < generations / 3 else 1 if gen < 2*generations / 3 else 2

        # print(f"[Gen {gen}] Phase = {phase}, Current best = {best_so_far}")

        while len(new_population) < population_size:
            parent1 = selection(population, tournament_size)
            parent2 = selection(population, tournament_size)
            parent_best = max(parent1.fitness,parent2.fitness)

            state = (phase, improved_prev)

            # crossover
            cx_choice = cx_agent.select_action(state)
            child1, child2 = crossover_ops[cx_choice](parent1, parent2)
            after_cx_best = max(child1.fitness,child2.fitness)
            reward_cx = (after_cx_best - parent_best) / max(abs(parent_best), 1) # normalize reward
            next_state_cx = (phase, 1 if reward_cx > 0 else 0)
            cx_agent.update(state, cx_choice, reward_cx, next_state_cx)

            # print(f"   CX: chose {cx_choice}, reward = {reward_cx:.3f}")

            # mutation
            mut_choice = mut_agent.select_action(next_state_cx)
            mutation_ops[mut_choice](child1)
            mutation_ops[mut_choice](child2)

            child1.fitness = child1.evaluate_fitness()
            child2.fitness = child2.evaluate_fitness()

            after_mut_best = max(child1.fitness, child2.fitness)
            reward_mut = (after_mut_best - after_cx_best) / max(abs(after_cx_best), 1)
            next_state_mut = (phase, 1 if reward_mut > 0 else 0)
            mut_agent.update(next_state_cx, mut_choice, reward_mut, next_state_mut)

            # print(f"   MUT: chose {mut_choice}, reward = {reward_mut:.3f}")

            improved_prev = 1 if after_mut_best > best_so_far else 0
            new_population.extend([child1, child2])
            # action_log.append((cx_choice, mut_choice))

        population = new_population[:population_size]
        best_so_far = max(best_so_far,population[0].fitness)
        # print("     best so far = ", best_so_far)


    # print(action_log)
    return max(population, key = lambda ind: ind.fitness)



# def main():
#     parser = argparse.ArgumentParser()
#     parser.add_argument('--instance', type=str, required=True)
#     parser.add_argument('--seed', type=int, required=True)
#     parser.add_argument('--population_size', type=int, default=50)
#     parser.add_argument('--generations', type=int, default=50)
#     parser.add_argument('--mutation_rate', type=float, default=0.05)
#     parser.add_argument('--elitism_size', type=int, default=2)
#     parser.add_argument('--tournament_size', type=int, default=3)
#     parser.add_argument('--alpha', type=float, default=0.2)
#     parser.add_argument('--gamma', type=float, default=0.9)
#     parser.add_argument('--epsilon_start', type=float, default=0.2)
#     parser.add_argument('--epsilon_end', type=float, default=0.02)
#     args = parser.parse_args()

#     random.seed(args.seed)
#     weights, values, capacity = load_kplib_instance(args.instance)
#     problem = KnapsackProblem(weights, values, capacity)

#     best = genetic_algorithm_qlearning(
#         problem,
#         population_size=args.population_size,
#         generations=args.generations,
#         tournament_size=args.tournament_size,
#         mutation_rate=args.mutation_rate,
#         elitism_size=args.elitism_size,
#         alpha=args.alpha,
#         gamma=args.gamma,
#         epsilon_start=args.epsilon_start,
#         epsilon_end=args.epsilon_end
#     )

#     print(best.fitness)


# if __name__ == "__main__":
#     main()  

