# TD Prediction

import numpy as np
from tqdm import tqdm

from r01_env_agent import Environment, Agent
from r02_show import show_v_table

# TD(0) Prediction
np.random.seed(0)

# 초기화
env = Environment()
agent = Agent()
gamma = 0.9

# π← 평가할 정책
# 가능한 모든 행동이 무작위로 선택되도록 지정
# V <- 임의의 상태 가치 함수
V = np.zeros((env.reward.shape[0], env.reward.shape[1]))

# 최대 에피소드 수와 각 에피소드의 최대 길이 지정
max_episode = 10000
max_step = 100

alpha = 0.01
print("start TD(0) prediction")

# 각 에피소드에 대해 반복
for epi in tqdm(range(max_episode)):
    delta = 0
    i = 0
    j = 0
    agent.set_pos([i, j])

    # 에피소드의 각 스텝 반복
    for k in range(max_step):
        pos = agent.get_pos()
        # a <- 상태 s에서 정책 π에 의해 결정된 행동
        # 가능한 모든 행동이 무작위로 선택되게 함
        action = np.random.randint(0, 4)

        # 행동 a를 취한 후 보상 r과 다음 상태 s'을 관측
        # s <- s'
        observation, reward, done = env.move(agent, action)

        # V(𝑠)←V(𝑠)+ α[𝑟+𝛾𝑉(𝑠^)−𝑉(𝑠)]
        V[pos[0], pos[1]] += alpha * (
            reward + gamma * V[observation[0], observation[1]] - V[pos[0], pos[1]]
        )

        # s가 마지막 상태면 종료
        if done:
            break

print("V(s)")
show_v_table(np.round(V, 2), env)
