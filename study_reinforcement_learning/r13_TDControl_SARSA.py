# TD(0) Control : SARSA

import numpy as np
from tqdm import tqdm
from r01_env_agent import Environment, Agent
from r02_show import show_q_table, show_policy


# πβππππππ¦ ν¨μ μμ±
def e_greedy(Q_table, agent, epsilon):
    pos = agent.get_pos()
    greedy_action = np.argmax(Q_table[pos[0], pos[1]])
    pr = np.zeros(4)
    for i in range(len(agent.action)):
        if i == greedy_action:
            pr[i] = 1 - epsilon + epsilon / len(agent.action)
        else:
            pr[i] = epsilon / len(agent.action)
    # μλ°μ΄νΈ λ pr νλ₯ μ λ°μν΄μ λ°©ν₯μ λλ€ μΆμΆνμ¬ λ°ν
    return np.random.choice(range(0, len(agent.action)), p=pr)


# ππππππ¦  ν¨μ μμ±
def greedy(Q_table, agent, epsilon):
    pos = agent.get_pos()
    # μ΅μ  λ°©ν₯ λ°ν
    return np.argmax(Q_table[pos[0], pos[1]])


np.random.seed(0)
env = Environment()
agent = Agent()
gamma = 0.9

# λͺ¨λ  π βπ,πβπ΄(π)μ λν΄ μ΄κΈ°ν:
# π(π ,π)βμμμ κ°. shape = (3,3,4)
Q_table = np.random.rand(env.reward.shape[0], env.reward.shape[1], len(agent.action))

# Q(π‘πππππππβπ π‘ππ‘π,π)=0 λͺ©μ μ§ μνλ 0
Q_table[-1, -1] = 0

max_episode = 10000
max_step = 100

print("Start TD(0) control : SARSA")
alpha = 0.1
epsilon = 0.8

# κ° μνΌμλ λ°λ³΅
for epi in tqdm(range(max_episode)):
    delta = 0
    i = 0
    j = 0
    agent.set_pos([i, j])
    temp = 0

    # s μμ νλ μ μ±(Behavior policy)μΌλ‘ νλ aλ₯Ό μ ν. => Ξ΅-greedy
    action = e_greedy(Q_table, agent, epsilon)

    # μνΌμλμ κ° μ€ν λ°λ³΅
    for k in range(max_step):
        pos = agent.get_pos()

        # νλ a λ₯Ό μ·¨ν ν λ³΄μ rκ³Ό λ€μ μν s'  κ΄μΈ‘
        observation, reward, done = env.move(agent, action)

        # s' μμ νκΉ μ μ±(Target policy)μΌλ‘ νλ a'λ₯Ό μ ν. => Ξ΅-greedy
        next_action = e_greedy(Q_table, agent, epsilon)

        # s <- s'
        # Q(π,π΄)βQ(π,π΄) + Ξ±[π+πΎπ(π',π΄')βπ(π,π΄)]
        Q_table[pos[0], pos[1], action] += alpha * (
            reward
            + gamma * Q_table[observation[0], observation[1], next_action]
            - Q_table[pos[0], pos[1], action]
        )

        # a <- a'
        action = next_action

        # sκ° λ§μ§λ§ μνλΌλ©΄ μ’λ£
        if done:
            break

# νμ΅λ μ μ± μ€ μ΅μ  νλμ optimal_policyμ μ μ₯
optimal_policy = np.zeros((env.reward.shape[0], env.reward.shape[1]))
for i in range(env.reward.shape[0]):
    for j in range(env.reward.shape[1]):
        optimal_policy[i, j] = np.argmax(Q_table[i, j])

print("SARSA : Q(s,a)")
show_q_table(np.round(Q_table, 2), env)
print("SARSA : optimal ploicy")
show_policy(optimal_policy, env)
