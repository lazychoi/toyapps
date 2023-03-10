# Actor-Critic Algorithm

import numpy as np
from tqdm import tqdm
from r01_env_agent import Environment, Agent
from r02_show import show_v_table, show_q_table, show_policy

np.random.seed(0)
env = Environment()
agent = Agent()
gamma = 0.9

# p(π ,π), π(π )βμμμ κ°
V = np.random.rand(env.reward.shape[0], env.reward.shape[1])
policy = np.random.rand(env.reward.shape[0], env.reward.shape[1], len(agent.action))

# νλ₯ μ ν©μ΄ 1μ΄ λλλ‘ λ³ν -> μ κ·ν(κ°λ³κ°/ν©κ³)
for i in range(env.reward.shape[0]):
    for j in range(env.reward.shape[1]):
        policy[i, j, :] = policy[i, j, :] / np.sum(policy[i, j, :])

max_episode = 10000
max_step = 100

print("start Actor-Critic")
alpha = 0.1

# κ° μνΌμλμ λν΄ λ°λ³΅ :
for epi in tqdm(range(max_episode)):
    # S μ΄κΈ°ν
    i = 0
    j = 0
    agent.set_pos([i, j])

    # μνΌμλμ κ° μ€ν λ°λ³΅ :
    for k in range(max_step):
        # Actor : p(π , π)λ‘λΆν° aλ₯Ό μ ν ( μ: Gibbs softmax method)
        # Gibbs softmax method λ‘ μ νλ  νλ₯ μ μ‘°μ 
        # np.exp() -> κ° μμμ μμ°μμλ₯Ό λ°μΌλ‘ νλ μ§μν¨μλ₯Ό μ μ©νμ¬ λ°ν. np.exp(2) -> e^2
        # νλ₯ μ ν©μ 1λ‘ λ§λ€κΈ° μν΄ μ κ·ν(ν©κ³λ‘ κ°λ³κ°μ λλ)
        pos = agent.get_pos()  # μμ΄μ νΈμ νμ¬ μμΉ κ°μ Έμ΄
        pr = np.zeros(4)
        for i in range(len(agent.action)):  # κΉμ€μ μννΈλ©μ€ ν¨μλ₯Ό μ μ©ν΄ λ€ λ°©ν₯μ νλ₯  μμ±
            pr[i] = np.exp(policy[pos[0], pos[1], i]) / np.sum(
                np.exp(policy[pos[0], pos[1], :])
            )
        action = np.random.choice(range(0, len(agent.action)), p=pr)  # νλ μ ν

        # νλ a μ·¨ν ν λ³΄μ r, λ€μ μν s' κ΄μΈ‘
        observation, reward, done = env.move(agent, action)

        # ν¬λ¦¬ν± νμ΅
        # Ξ΄t = r(t+1) + Ξ³V(S(t+1)) - V(St)
        td_error = (
            reward + gamma * V[observation[0], observation[1]] - V[pos[0], pos[1]]
        )

        # μνκ°μΉ νμ΅(μλ°μ΄νΈ)
        V[pos[0], pos[1]] += alpha * td_error  # μνμ°©μ€ * νμ΅λ₯ 

        # μ‘ν° νμ΅ (νλμ μ± μλ°μ΄νΈ)
        # p(st,at) = p(st,at) - Ξ²Ξ΄_t
        policy[pos[0], pos[1], action] += td_error * 0.01  # μνμ°©μ€μ 1% λ°μ

        # νλ₯ μ μμκ° μμ κ²½μ° μμκ° λλλ‘ λ³΄μ (ν¬λ¦¬ν± νμ΅ μμμ λΊμμ΄ μμ΄ μμκ° λμ¬ μ μμ)
        # a = [0.2, 0.4, 0.7, -0.5]
        # a = a - np.min(a)         => [0.7 0.9 1.2 0. ]
        # κ° μμμ μμ μμλ₯Ό λΉΌλ©΄ => μμ μμμ μ λκ°μ λνλ ν¨κ³Ό => μμ μμλ 0μ΄ λ¨
        if np.min(policy[pos[0], pos[1], :]) < 0:
            policy[pos[0], pos[1], :] -= np.min(policy[pos[0], pos[1], :])
        # νλ₯ μ ν©μ΄ 1μ΄ λλλ‘ μ κ·ν
        for i in range(env.reward.shape[0]):
            for j in range(env.reward.shape[1]):
                policy[i, j, :] = policy[i, j, :] / np.sum(policy[i, j, :])

        # sκ° λ§μ§λ§ μνλΌλ©΄ μ’λ£
        if done:
            break

# νμ΅λ μ μ± μ€ μ΅μ  νλμ optimal_policyμ μ μ₯
optimal_policy = np.zeros((env.reward.shape[0], env.reward.shape[1]))
for i in range(env.reward.shape[0]):
    for j in range(env.reward.shape[1]):
        optimal_policy[i, j] = np.argmax(policy[i, j, :])

print("Actor-Critic : V(s)")
show_v_table(np.round(V, 2), env)
print("Actor-Critic : policy(s,a)")
show_q_table(np.round(policy, 2), env)
print("Actor-Critic : optimal policy")
show_policy(np.round(optimal_policy, 2), env)
