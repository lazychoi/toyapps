# Actor-Critic Algorithm

import numpy as np
from tqdm import tqdm
from r01_env_agent import Environment, Agent
from r02_show import show_v_table, show_q_table, show_policy

np.random.seed(0)
env = Environment()
agent = Agent()
gamma = 0.9

# p(𝑠,𝑎), 𝑉(𝑠)←임의의 값
V = np.random.rand(env.reward.shape[0], env.reward.shape[1])
policy = np.random.rand(env.reward.shape[0], env.reward.shape[1], len(agent.action))

# 확률의 합이 1이 되도록 변환 -> 정규화(개별값/합계)
for i in range(env.reward.shape[0]):
    for j in range(env.reward.shape[1]):
        policy[i, j, :] = policy[i, j, :] / np.sum(policy[i, j, :])

max_episode = 10000
max_step = 100

print("start Actor-Critic")
alpha = 0.1

# 각 에피소드에 대해 반복 :
for epi in tqdm(range(max_episode)):
    # S 초기화
    i = 0
    j = 0
    agent.set_pos([i, j])

    # 에피소드의 각 스텝 반복 :
    for k in range(max_step):
        # Actor : p(𝑠, 𝑎)로부터 a를 선택 ( 예: Gibbs softmax method)
        # Gibbs softmax method 로 선택될 확률을 조정
        # np.exp() -> 각 요소에 자연상수를 밑으로 하는 지수함수를 적용하여 반환. np.exp(2) -> e^2
        # 확률의 합을 1로 만들기 위해 정규화(합계로 개별값을 나눔)
        pos = agent.get_pos()  # 에이전트의 현재 위치 가져옴
        pr = np.zeros(4)
        for i in range(len(agent.action)):  # 깁스의 소프트멕스 함수를 적용해 네 방향의 확률 생성
            pr[i] = np.exp(policy[pos[0], pos[1], i]) / np.sum(
                np.exp(policy[pos[0], pos[1], :])
            )
        action = np.random.choice(range(0, len(agent.action)), p=pr)  # 행동 선택

        # 행동 a 취한 후 보상 r, 다음 상태 s' 관측
        observation, reward, done = env.move(agent, action)

        # 크리틱 학습
        # δt = r(t+1) + γV(S(t+1)) - V(St)
        td_error = (
            reward + gamma * V[observation[0], observation[1]] - V[pos[0], pos[1]]
        )

        # 상태가치 학습(업데이트)
        V[pos[0], pos[1]] += alpha * td_error  # 시행착오 * 학습률

        # 액터 학습 (행동정책 업데이트)
        # p(st,at) = p(st,at) - βδ_t
        policy[pos[0], pos[1], action] += td_error * 0.01  # 시행착오의 1% 반영

        # 확률에 음수가 있을 경우 양수가 되도록 보정(크리틱 학습 수식에 뺄셈이 있어 음수가 나올 수 있음)
        # a = [0.2, 0.4, 0.7, -0.5]
        # a = a - np.min(a)         => [0.7 0.9 1.2 0. ]
        # 각 요소에 음수 요소를 빼면 => 음수 요소의 절대값을 더하는 효과 => 음수 요소는 0이 됨
        if np.min(policy[pos[0], pos[1], :]) < 0:
            policy[pos[0], pos[1], :] -= np.min(policy[pos[0], pos[1], :])
        # 확률의 합이 1이 되도록 정규화
        for i in range(env.reward.shape[0]):
            for j in range(env.reward.shape[1]):
                policy[i, j, :] = policy[i, j, :] / np.sum(policy[i, j, :])

        # s가 마지막 상태라면 종료
        if done:
            break

# 학습된 정책 중 최적 행동을 optimal_policy에 저장
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
