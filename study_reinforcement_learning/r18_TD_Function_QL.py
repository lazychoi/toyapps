# 함수 근사 : Q-learning

import numpy as np
from tqdm import tqdm
from r01_env_agent import Environment, Agent
from r02_show import show_q_table, show_policy

np.random.seed(0)
env = Environment()
agent = Agent()
gamma = 0.9

# 초기화
# 𝑣(𝑠│𝒘) ← 미분 가능한 함수
# w ← 함수의 가중치를 임의의 값으로 초기화
# w[0]+ w[1] * x1  + w[1] * x2
w = np.random.rand(len(agent.action), env.reward.shape[0])
# w -= 0.5    # 왜 빼지???

FA_Q_table = np.zeros((env.reward.shape[0], env.reward.shape[1], len(agent.action)))

# 함수를 테이블에 저장
for i in range(env.reward.shape[0]):
    for j in range(env.reward.shape[1]):
        for k in range(len(agent.action)):
            FA_Q_table[i, j, k] = w[k, 0] + w[k, 1] * i + w[k, 2] * j

# 학습된 정책에서 최적 행동 추출
optimal_policy = np.zeros((env.reward.shape[0], env.reward.shape[1]))
for i in range(env.reward.shape[0]):
    for j in range(env.reward.shape[1]):
        optimal_policy[i, j] = np.argmax(FA_Q_table[i, j, :])

print("Before : Function Approximation Q-learning : Q(s,a|w)")
show_q_table(np.round(FA_Q_table, 2), env)
print()
print("Before : Function Approximation Q-learning :optimal policy")
show_policy(optimal_policy, env)
print()
print("Initial w")
print("w = {}".format(np.round(w, 2)))
print()

max_episode = 100000
max_step = 100
alpha = 0.01

print("start Function Approximation : Q-learning")

# 각 에피소드 반복
for epi in tqdm(range(max_episode)):
    # s 초기화
    i = 0
    j = 0
    agent.set_pos([i, j])

    # 에피소드의 각 스텝 반복
    for k in range(max_step):
        pos = agent.get_pos()

        # s에서 Behavior policy로 행동 a를 선택 (Gibbs 소프트맥스 함수사용)
        action = np.zeros(4)
        for act in range(len(agent.action)):
            action[act] = w[act, 0] + w[act, 1] * pos[0] + w[act, 2] * pos[1]
        pr = np.zeros(4)
        for i in range(len(agent.action)):
            pr[i] = np.exp(action[i]) / np.sum(np.exp(action[:]))
        action = np.random.choice(range(0, len(agent.action)), p=pr)

        # 행동 a를 취한 후 보상 r과 다음 상태 s' 관측
        observation, reward, done = env.move(agent, action)

        # s'에서 Target policy 행동 a'를 선택 (𝑔𝑟𝑒𝑒𝑑𝑦)
        next_act = np.zeros(4)
        for act in range(len(agent.action)):
            next_act[act] = np.dot(w[act, 1:], observation) + w[act, 0]
        best_action = np.argmax(next_act)
        now_q = np.dot(w[action, 1:], pos) + w[action, 0]
        next_q = np.dot(w[best_action, 1:], observation) + w[best_action, 0]

        # w ← 𝑤 + 𝛼[𝑟 + 𝛾maxQ'(𝑠',a'|𝒘) - Q(𝑠,a|𝒘)](𝜕Q(s,a|𝒘))/𝜕𝑤
        w[action, 0] += alpha * (reward + gamma * next_q - now_q)
        w[action, 1] += alpha * (reward + gamma * next_q - now_q) * pos[0]
        w[action, 2] += alpha * (reward + gamma * next_q - now_q) * pos[1]

        # s가 마지막 상태라면 종료
        if done:
            break

# 함수를 테이블에 저장
for i in range(env.reward.shape[0]):
    for j in range(env.reward.shape[1]):
        for k in range(len(agent.action)):
            FA_Q_table[i, j, k] = w[k, 0] + w[k, 1] * i + w[k, 2] * j

# 학습된 정책에서 최적 행동 추출
for i in range(env.reward.shape[0]):
    for j in range(env.reward.shape[1]):
        optimal_policy[i, j] = np.argmax(FA_Q_table[i, j, :])


print("After : Function Approximation Q-learning : Q(s,a|w)")
show_q_table(np.round(FA_Q_table, 2), env)
print()
print("After : Function Approximation Q-learning :optimal policy")
show_policy(optimal_policy, env)
print()
print("Final w")
print("w = {}".format(np.round(w, 2)))
print()
