# TD(0) 함수 근사

import numpy as np
from tqdm import tqdm
from r01_env_agent import Environment, Agent
from r02_show import show_v_table

np.random.seed(1)
env = Environment()
agent = Agent()
gamma = 0.9

# 초기화
# 𝑣(𝑠│𝒘) ← 미분 가능한 함수
# w ← 함수의 가중치를 임의의 값으로 초기화
# w[0]+ w[1] * x1  + w[1] * x2
w = np.random.rand(env.reward.shape[0])
w -= 0.5  # 왜 빼지???

v_table = np.zeros((env.reward.shape[0], env.reward.shape[1]))
for i in range(env.reward.shape[0]):
    for j in range(env.reward.shape[1]):
        v_table[i, j] = w[0] + w[1] * i + w[2] * j

print("Before : TD(0) Function Approximation : v(s|w)")
print()
print("Initial w")
print("w = {}".format(np.round(w, 2)))
show_v_table(np.round(v_table, 2), env)

max_episode = 10000
max_step = 100
alpha = 0.01
epsilon = 0.3
print("start Function Approximation TD(0) prediction")

# 각 에피소드 반복
for epi in tqdm(range(max_episode)):
    delta = 0

    # s 초기화
    i = 0
    j = 0
    agent.set_pos([i, j])

    # 에피소드의 각 스텝 반복
    for k in range(max_step):
        pos = agent.get_pos()

        # 무작위로 행동 선택
        action = np.random.randint(0, len(agent.action))

        # 행동 a를 취한 후 보상 r과 다음 상태 s' 관측
        observation, reward, done = env.move(agent, action)
        now_v = 0
        next_v = 0

        # 현재 상태가치함수와 다음 상태가치함수를 v(s|w)로부터 계산
        now_v = w[0] + np.dot(w[1:], pos)  # <- w0 + w1x1 + w2x2
        next_v = w[0] + np.dot(w[1:], observation)

        # w ← 𝑤 + 𝛼[𝑟 − 𝑣(𝑠│𝒘)](𝜕𝑣(s│𝒘))/𝜕𝑤
        w[0] += alpha * (reward + gamma * next_v - now_v)
        w[1] += alpha * (reward + gamma * next_v - now_v) * pos[0]
        w[2] += alpha * (reward + gamma * next_v - now_v) * pos[1]

        # s가 마지막 상태라면 종료
        if done:
            break

for i in range(env.reward.shape[0]):
    for j in range(env.reward.shape[1]):
        v_table[i, j] = w[0] + w[1] * i + w[2] * j

print()
print("After : TD(0) Function Approximation : v(s|w)")
print()
print("Final w")
print("w = {}".format(np.round(w, 2)))

print("TD(0) Function Approximation : V(s)")
show_v_table(np.round(v_table, 2), env)
