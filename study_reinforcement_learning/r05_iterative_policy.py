import numpy as np
import copy
import time
from r01_env_agent import Environment, Agent
from r02_show import show_v_table


# 반복 정책 평가
np.random.seed(0)
env = Environment()
agent = Agent()
gamma = 0.9

# 1. 모든 𝑠 ∈ 𝑆^에 대해서 배열 𝑉(𝑠)=0으로 초기화
v_table = np.zeros(
    (
        env.reward.shape[0],
        env.reward.shape[1],
    )
)

print("start Iterative Policy Evaluation")

k = 1
print()
print("V0(S)   k = 0")

# 초기화 된 V 테이블 출력
show_v_table(np.round(v_table, 2), env)

# 시작 시간 변수에 저장
start_time = time.time()

# 반복
while True:
    # 2. 𝛥 <- 0
    delta = 0

    # 3. v <- V(s)
    # 계산 전 가치 저장
    temp_v = copy.deepcopy(v_table)

    # 4. 모든 s에 대해
    for i in range(env.reward.shape[0]):
        for j in range(env.reward.shape[1]):
            G = 0

            # 5. 가능한 모든 행동으로 다음 상태만 이용해 V(s) 계산 -> 연결된 모든 상태의 가치를 더함
            for action in range(len(agent.action)):
                agent.set_pos([i, j])
                observation, reward, done = env.move(agent, action)

                G += agent.select_action_pr[action] * (
                    reward + gamma * v_table[observation[0], observation[1]]
                )

            v_table[i, j] = G

    # 6. 𝛥 <- max(𝛥, | v - V(s) |
    # 계산 전과 계산 후의 가치 차이 계산
    delta = np.max([delta, np.max(np.abs(temp_v - v_table))])

    end_time = time.time()
    print(
        "V{0}(S) : k = {1:3d}    delta = {2:0.6f} total_time = {3}".format(
            k, k, delta, np.round(end_time - start_time), 2
        )
    )

    show_v_table(np.round(v_table, 2), env)

    k += 1

    # 7. 𝛥 < theta가 작은 양수일 때까지 반복
    if delta < 0.000001:
        break

end_time = time.time()
print("total_time = {}".format(np.round(end_time - start_time), 2))
