# policy evalution, policy improvement

import copy
import time
import numpy as np
from r01_env_agent import Environment, Agent
from r02_show import show_policy, show_v_table


# 정책 평가 함수
def policy_evaluation(env, agent, v_table, policy):
    while True:
        delta = 0
        temp_v = copy.deepcopy(v_table)

        for i in range(env.reward.shape[0]):
            for j in range(env.reward.shape[1]):
                # 에이전트를 지정된 좌표에 위치시킨 후 가치함수 계산
                agent.set_pos([i, j])

                # 현재 정책의 행동 선택
                action = policy[i, j]
                observation, reward, done = env.move(agent, action)
                v_table[i, j] = (
                    reward
                    + gamma
                    * v_table[
                        observation[0],
                        observation[1],
                    ]
                )

        # 계산 전후의 차이 계산
        delta = np.max([delta, np.max(np.abs(temp_v - v_table))])

        # delta < theta일 때까지 반복
        if delta < 0.000001:
            break

    return v_table, delta


# 정책 개선 함수
def policy_improvement(env, agent, v_table, policy):
    policy_stable = True

    for i in range(env.reward.shape[0]):
        for j in range(env.reward.shape[1]):
            old_action = policy[i, j]

            # 가능한 행동 중 최댓값을 가지는 행동 선택
            temp_action = 0
            temp_value = -1e10
            for action in range(len(agent.action)):
                agent.set_pos([i, j])
                observation, reward, done = env.move(agent, action)
                # '기존 상태 가치 * 감가율'에 보상을 더한 값 중 최댓값을 가져오는 방향(action) 반환
                if (
                    temp_value
                    < reward + gamma * v_table[observation[0], observation[1]]
                ):
                    temp_action = action
                    temp_value = (
                        reward + gamma * v_table[observation[0], observation[1]]
                    )

            # 만약 old_action이 현재 정책과 다르다면 policy_stabel <- False
            # old_action과 새로운 action이 다른지 체크
            if old_action != temp_action:
                policy_stable = False
            policy[i, j] = temp_action

    return policy, policy_stable


# 정책 반복
# 환경과 에이전트 초기 설정
np.random.seed(0)
env = Environment()
agent = Agent()
gamma = 0.9
k = 1

# 1. 초기화
# 모든 𝑠∈𝑆에 대해 𝑉(𝑠)∈𝑅과 π(𝑠)∈𝐴(𝑠)를 임의로 설정
# v_table(3x3) <- 0-1 사이 난수
# policy(3x3) <- 0-3 사이 정수 : 처음에는 방향을 무작위로 선택
v_table = np.random.rand(env.reward.shape[0], env.reward.shape[1])
policy = np.random.randint(
    0, 4, (env.reward.shape[0], env.reward.shape[1])
)  # low, high, size(output shape)

print("Initial random V(S)")
show_v_table(np.round(v_table, 2), env)
print()
print("Initial random Policy π0(S)")
show_policy(policy, env)
print("start policy iteration")

# 시작 시간을 변수에 저장
start_time = time.time()

max_iter_number = 20000
for iter_number in range(max_iter_number):
    # 2. 정책 평가
    v_table, delta = policy_evaluation(env, agent, v_table, policy)

    # 정책 평가 후 결과 표시(상태 가치)
    print("")
    print("Vπ{0:}(S) delta = {1:.10f}".format(iter_number, delta))
    show_v_table(np.round(v_table, 2), env)
    print()

    # 3. 정책 개선
    policy, policy_stable = policy_improvement(env, agent, v_table, policy)

    # 정책 개선 후 움직일 방향 표시
    print("policy π{}(S)".format(iter_number + 1))
    show_policy(policy, env)

    # 하나라도 old_action과 new_action이 다르면 '2.정책 평가' 반복
    if policy_stable:
        break

    k += 1

print("total_time = {}".format(time.time() - start_time))
