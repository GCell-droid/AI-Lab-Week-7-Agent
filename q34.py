import numpy as np

class NonStationaryBandit:
    def __init__(self, n_arms=10):
        self.n_arms = n_arms
        self.q_true = np.zeros(n_arms)
        
    def pull(self, arm):
        self.q_true += np.random.normal(0, 0.01, self.n_arms)
        return np.random.normal(self.q_true[arm], 1)
    
    def get_optimal_arm(self):
        return np.argmax(self.q_true)

class ModifiedEpsilonGreedyAgent:
    def __init__(self, n_arms=10, epsilon=0.1, alpha=0.1):
        self.n_arms = n_arms
        self.epsilon = epsilon
        self.alpha = alpha
        self.Q = np.zeros(n_arms)
        
    def choose_action(self):
        if np.random.random() < self.epsilon:
            return np.random.randint(self.n_arms)
        return np.argmax(self.Q)
    
    def update(self, action, reward):
        self.Q[action] += self.alpha * (reward - self.Q[action])

def run_experiment(n_steps=10000):
    bandit = NonStationaryBandit()
    agent = ModifiedEpsilonGreedyAgent()
    
    rewards = np.zeros(n_steps)
    optimal_actions = np.zeros(n_steps)
    chosen_actions = np.zeros(n_steps)
    
    for t in range(n_steps):
        action = agent.choose_action()
        reward = bandit.pull(action)
        agent.update(action, reward)
        
        rewards[t] = reward
        optimal_actions[t] = bandit.get_optimal_arm()
        chosen_actions[t] = action
    
    return rewards, optimal_actions, chosen_actions

def analyze_results(rewards, optimal_actions, chosen_actions):
    avg_reward = np.mean(rewards)
    final_avg_reward = np.mean(rewards[-1000:])
    optimal_action_rate = np.mean(chosen_actions == optimal_actions)
    final_optimal_rate = np.mean(chosen_actions[-1000:] == optimal_actions[-1000:])
    
    print(f"Average reward: {avg_reward:.2f}")
    print(f"Final 1000 steps average reward: {final_avg_reward:.2f}")
    print(f"Optimal action selection rate: {optimal_action_rate:.2%}")
    print(f"Final 1000 steps optimal action rate: {final_optimal_rate:.2%}")

if __name__ == "__main__":
    np.random.seed(42)
    rewards, optimal_actions, chosen_actions = run_experiment()
    analyze_results(rewards, optimal_actions, chosen_actions)