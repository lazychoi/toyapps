import numpy as np
from r01_env_agent import Environment, Agent
from r02_show import show_q_table, show_q_table_arrow


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
            if done == True:
                if (
                    observation[0] < 0
                    or observation[0] >= env.reward.shape[0]
                    or observation[1] < 0
                    or observation[1] >= env.reward.shape[1]
                ):
                    agent.set_pos(pos1)

            # 4.2.3 다음 step을 계산
            next_v = state_value_function(env, agent, 0, max_step, now_step + 1)
            G += agent.select_action_pr[i] * gamma * next_v

            # 4.2.4 현재 위치를 복구
            agent.set_pos(pos1)

        return G


# 행동 가치 함수
def action_value_function(env, agent, act, G, max_step, now_step):
    # 1. 감가율 결정
    gamma = 0.9

    # 2. 현재 위치가 목적지인지 확인
    if env.reward_list1[agent.pos[0]][agent.pos[1]] == "goal":
        return env.goal

    # 3. 마지막 상태는 보상만 계산
    if max_step == now_step:
        observation, reward, done = env.move(agent, act)
        G += agent.select_action_pr[act] * reward
        return G

    # 4. 현재 상태의 보상을 계산한 후 다음 행동과 함께 다음 step으로 이동
    else:
        # 4.1 현재 위치 저장
        pos1 = agent.get_pos()
        observation, reward, done = env.move(agent, act)
        G += agent.select_action_pr[act] * reward

        # 4.2 이동 후 위치 확인: 미로 밖인 경우 이동 전 좌표로 다시 이동
        if done:
            if (
                observation[0] < 0
                or observation[0] >= env.reward.shape[0]
                or observation[1] < 0
                or observation[1] >= env.reward.shape[1]
            ):
                agent.set_pos(pos1)

        # 4.3 현재 위치를 다시 저장
        pos1 = agent.get_pos()

        # 4.4 현재 위치에서 가능한 모든 행동을 선택한 후 이동
        for i in range(len(agent.action)):
            agent.set_pos(pos1)
            next_v = action_value_function(env, agent, i, 0, max_step, now_step + 1)
            G += agent.select_action_pr[i] * gamma * next_v
        return G


# 행동 가치 계산
# 1. 환경 초기화
env = Environment()

# 2. 에이전트 초기화
agent = Agent()
np.random.seed(0)

# 3. 최대 max_step_number 제한 : 연결된 다음 상태 중 몇 번째까지 참고할 것인가
max_step_number = 8

# 4. 모든 상태에 대해
for max_step in range(max_step_number):
    # 4.1 미로 상의 모든 상태에서 가능한 행동의 가치를 저장할 테이블 정의
    print("max_step = {}".format(max_step))
    q_table = np.zeros((env.reward.shape[0], env.reward.shape[1], len(agent.action)))
    for i in range(env.reward.shape[0]):
        for j in range(env.reward.shape[1]):
            # 4.2 모든 행동에 대해
            for action in range(len(agent.action)):
                # 4.2.1 에이전트 위치 초기화
                agent.set_pos([i, j])

                # 4.2.2 현재 위치에서 행동 가치 계산
                q_table[i, j, action] = action_value_function(
                    env, agent, action, 0, max_step, 0
                )

    q = np.round(q_table, 2)
    print("Q - table")
    show_q_table(q, env)
    print("High actions Arrow")
    show_q_table_arrow(q, env)
    print()
