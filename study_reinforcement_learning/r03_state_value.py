import numpy as np
import matplotlib.pyplot as plt
import time
from r01_env_agent import Environment, Agent
from r02_show import show_v_table


# 상태 가치 계산
def state_value_function(env, agent, G, max_step, now_step):
    """
    미로의 모든 셀을 순회하며 각 셀에서의 에이전트의 모든 움직임에 따른 수익을 계산해 반환한다.
    에이전트의 각 움직임의 확률 * 감가율 * 보상
    :param env: Environment class
    :param agent: Agent class
    :param G: 수익(reward의 총합)
    :param max_step: 연결된 상태 중 참고할 최대 단계
    :param now_step:
    :return: G(수익, reward의 총합)
    """

    # 1. 감가율 설정
    gamma = 0.9

    # 2. 현재 위치가 도착지점인지 확인
    if env.reward_list1[agent.pos[0]][agent.pos[1]] == "goal":
        return env.goal

    # 3. 마지막 상태는 보상만 계산
    if max_step == now_step:
        pos1 = agent.get_pos()

        # 3.1 가능한 모든 행동의 보상을 계산
        for i in range(len(agent.action)):
            agent.set_pos(pos1)
            observation, reward, done = env.move(agent, i)
            G += agent.select_action_pr[i] * reward

        return G

    # 4. 현재 상태의 보상을 계산한 후 다음 step으로 이동
    else:
        # 4.1현재 위치 저장
        pos1 = agent.get_pos()

        # 4.2 현재 위치에서 가능한 모든 행동을 조사한 후 이동
        for i in range(len(agent.action)):
            observation, reward, done = env.move(agent, i)

            # 4.2.1 현재 상태에서의 보상을 계산
            G += agent.select_action_pr[i] * reward

            # 4.2.2 이동 후 위치 확인 : 미로밖, 벽, 구멍인 경우 이동전 좌표로 다시 이동
            if done:
                if (
                    observation[0] < 0
                    or observation[0] >= env.reward.shape[0]
                    or observation[1] < 0
                    or observation[1] >= env.reward.shape[1]
                ):
                    agent.set_pos(pos1)

            # 4.2.3 다음 step을 계산 -> 재귀함수(until max_step == now_step)
            next_v = state_value_function(env, agent, 0, max_step, now_step + 1)
            G += agent.select_action_pr[i] * gamma * next_v

            # 4.2.4 현재 위치를 복구
            agent.set_pos(pos1)

        return G


# 상태 가치 계산
# 1. 환경 초기화
env = Environment()

# 2. 에이전트 초기화
agent = Agent()
np.random.seed(0)

# 3. 최대 max_step_number 제한 : 연결된 다음 상태 중 몇 번째까지 참고할 것인가
# r0 - r12 까지 계산
max_step_number = 13

# 4. 계산 시간 저장을 위한 list
time_len = []

# 5. 재귀함수 state_value_function을를 이용해 각 상태 가치를 계산
for max_step in range(max_step_number):
    # 5.1 미로 각 상태의 가치를 테이블 형식으로 저장
    # 매 max_step 마다 v_table을 초기화하여 reward를 동일하게 반환
    v_table = np.zeros((env.reward.shape[0], env.reward.shape[1]))
    start_time = time.time()

    # 5.2 미로의 각 상태에 대해 state_value_function() 을 이용해 가치를 계산한 후 테이블 형식으로 저장
    for i in range(env.reward.shape[0]):
        for j in range(env.reward.shape[1]):
            agent.set_pos([i, j])
            v_table[i, j] = state_value_function(env, agent, 0, max_step, 0)

    # 5.3 max_down에 따른 계산시간 저장
    time_len.append(time.time() - start_time)
    print(
        "max_step_number = {} total_time = {}(s)".format(
            max_step, np.round(time.time() - start_time, 2)
        )
    )

    # max_step 단계마다 상태 가치를 소숫점 2자리까지 표시
    show_v_table(np.round(v_table, 2), env)

# 6. step 별 계산 시간 그래프 그리기
plt.plot(time_len, "o-k")
plt.xlabel("max_down")
plt.ylabel("time(s)")
plt.legend()
plt.show()
