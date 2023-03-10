# Double Q-learning

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
# π1(π ,π), π2(π ,π) β μμμ κ°
Q1_table = np.random.rand(env.reward.shape[0], env.reward.shape[1], len(agent.action))
Q2_table = np.random.rand(env.reward.shape[0], env.reward.shape[1], len(agent.action))

# Q(π‘πππππππβπ π‘ππ‘π,π)=0
Q1_table[-1, -1, :] = 0
Q2_table[-1, -1, :] = 0

max_episode = 10000
max_step = 10

print("start Double Q-learning")
alpha = 0.1
epsilon = 0.3

# κ° μνΌμλμ λν΄ λ°λ³΅ :
for epi in tqdm(range(max_episode)):
    dleta = 0
    # S λ₯Ό μ΄κΈ°ν
    i = 0
    j = 0
    agent.set_pos([i, j])

    # μνΌμλμ κ° μ€νμ λν΄ λ°λ³΅ :
    for k in range(max_step):
        pos = agent.get_pos()

        # π1κ³Ό π2λ‘ λΆν° aλ₯Ό μ ν (μ : πβππππππ¦ in π1+π2)
        Q = Q1_table + Q2_table
        action = e_greedy(Q, agent, epsilon)

        # νλ a λ₯Ό μ·¨ν ν λ³΄μ rκ³Ό λ€μ μν s'λ₯Ό κ΄μΈ‘
        observation, reward, done = env.move(agent, action)

        # s' μμ νκΉ μ μ±(Target policy)μΌλ‘ νλ a'λ₯Ό μ ν(greedy)
        p = np.random.random()

        # νλ₯ μ΄ 0.5λ³΄λ€ μλ€λ©΄
        if p < 0.5:
            next_action = greedy(Q1_table, agent, epsilon)

            # π1(π ,π) β π1(π ,π) + Ξ±[π + πΎπ2(π', argmaxQ1(s', a')) β π1 (π ,π)]
            Q1_table[pos[0], pos[1], action] += alpha * (
                reward
                + gamma * Q2_table[observation[0], observation[1], next_action]
                - Q1_table[pos[0], pos[1], action]
            )
        else:
            next_action = greedy(Q2_table, agent, epsilon)

            # π2(π ,π) β π2(π ,π) + Ξ±[π + πΎπ1(π', argmaxQ2(s', a')) β π2(π ,π)]
            Q2_table[pos[0], pos[1], action] += alpha * (
                reward
                + gamma * Q1_table[observation[0], observation[1], next_action]
                - Q2_table[pos[0], pos[1], action]
            )

        # sκ° λ§μ§λ§ μνλΌλ©΄ μ’λ£
        if done:
            break

# νμ΅λ μ μ± μ€ μ΅μ  νλμ optimal_policyμ μ μ₯
optimal_policy = np.zeros((env.reward.shape[0], env.reward.shape[1]))
for i in range(env.reward.shape[0]):
    for j in range(env.reward.shape[1]):
        optimal_policy[i, j] = np.argmax(Q1_table[i, j, :] + Q1_table[i, j, :])

print("Double Q-learning : Q1(s,a)")
show_q_table(np.round(Q1_table, 2), env)
print("Double Q-learning : Q2(s,a)")
show_q_table(np.round(Q2_table, 2), env)
print("Double Q-learning : Q(s,a)")
show_q_table(np.round(Q1_table + Q2_table, 2), env)
print("Double Q-learning : optimal policy")
show_policy(optimal_policy, env)
