# finding optimal value

import copy
import numpy as np
import time
from r01_env_agent import Environment, Agent
from r02_show import show_policy, show_v_table


# 최적 상태가치를 찾는 함수
def finding_optimal_value(env, agent, v_table):
    k = 0
    gamma = 0.9
    while True:
        delta = 0
        #  v ← 𝑉(𝑠)
        temp_v = copy.deepcopy(v_table)

        # 모든 𝑠 ∈ 𝑆 에 대해
        for i in range(env.reward.shape[0]):
            for j in range(env.reward.shape[1]):
                temp = -1e10

                # 가능한 행동 중 최댓값 찾기
                # # 𝑉(𝑠)← max(a) ∑𝑃(𝑠'|𝑠,𝑎)[𝑟(𝑠,𝑎,𝑠') +𝛾𝑉(𝑠')]
                for action in range(len(agent.action)):
                    agent.set_pos([i, j])
                    observation, reward, done = env.move(agent, action)

                    # 이동한 상태의 가치가 temp보다 크면
                    if temp < reward + gamma * v_table[observation[0], observation[1]]:
                        temp = reward + gamma * v_table[observation[0], observation[1]]

                # 이동 가능한 상태 중 가장 큰 가치 저장
                v_table[i, j] = temp

        # 이전 가치와 비교해 큰 값을 delta에 저장
        # 계산 전과 계산 후의 가치 차이 계산 ∆ ← max(∆,|v−𝑉(𝑠)|)
        delta = np.max([delta, np.max(np.abs(temp_v - v_table))])

        # delta가 작은 양수일 때까지 반복
        if delta < 0.0000001:
            break

        print("V{0}(S) : k = {1:3d}    delta = {2:0.6f}".format(k, k, delta))
        show_v_table(np.round(v_table, 2), env)
        k += 1

    return v_table


# 정책을 추출하는 함수
def policy_extraction(env, agent, v_table, optimal_policy):
    gamma = 0.9

    # 정책 𝜋를 다음과 같이 추출
    # 𝜋(𝑠)← argmax(a) ∑𝑃(𝑠'|𝑠,𝑎)[𝑟(𝑠,𝑎,𝑠') +𝛾𝑉(𝑠')]
    # 모든 𝑠∈𝑆에 대해
    for i in range(env.reward.shape[0]):
        for j in range(env.reward.shape[1]):
            temp = -1e10

            # 가능한 행동 중 가치가 가장 높은 값을 policy[i, j]에 저장
            for action in range(len(agent.action)):
                agent.set_pos([i, j])
                observation, reward, done = env.move(agent, action)
                if temp < reward + gamma * v_table[observation[0], observation[1]]:
                    optimal_policy[i, j] = action
                    temp = reward + gamma * v_table[observation[0], observation[1]]
    return optimal_policy


# 가치 반복
np.random.seed(0)
env = Environment()
agent = Agent()

# 초기화
# 모든 𝑠∈𝑆^+에 대해 𝑉(𝑠)∈𝑅을 임의로 설정
v_table = np.random.rand(env.reward.shape[0], env.reward.shape[1])

print("Initial random V0(S)")
show_v_table(np.round(v_table, 2), env)
print()

optimal_policy = np.zeros((env.reward.shape[0], env.reward.shape[1]))

print("start Value iteration")
print()

# 시작 시간 변수에 저장
start_time = time.time()

# 최적 상태가치 계산
v_table = finding_optimal_value(env, agent, v_table)

# 최적 정책 추출
optimal_policy = policy_extraction(env, agent, v_table, optimal_policy)

print("total_time = {}".format(np.round(time.time() - start_time), 2))
print()
print("Optimal policy")
show_policy(optimal_policy, env)
