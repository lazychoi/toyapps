# MC Prediction

import numpy as np
from tqdm import tqdm

from r01_env_agent import Environment, Agent
from r02_show import show_v_table


# 에피소드 생성 함수
def generate_episode(env, agent, first_visit):
    gamma = 0.09

    # 에피소드 저장 리스트
    episode = []

    # 이전 방문 여부 저장 테이블
    visit = np.zeros((env.reward.shape[0], env.reward.shape[1]))

    # 에이전트의 출발지점을 0, 0 으로 설정
    i = 0
    j = 0
    agent.set_pos([i, j])

    # 에피소드 수익률 초기화
    G = 0

    # 감쇄율 지수
    step = 0
    max_step = 100

    # 에피소드 생성
    for k in range(max_step):
        pos = agent.get_pos()
        # 한 방향만 탐색 후 결과 받아오기
        action = np.random.randint(0, len(agent.action))
        observation, reward, done = env.move(agent, action)

        if first_visit:
            # 첫 방문인지 검사
            # visit[pos[0], pos[1]] == 0 : 첫 방문
            # visit[pos[0], pos[1]] == 1 : 중복 방문
            if visit[pos[0], pos[1]] == 0:
                # 에피소드가 끝날 때까지 수익G 계산
                G += gamma**step * reward
                # 방문 이력 표시
                visit[pos[0], pos[1]] = 1
                step += 1
                # 방문 이력 저장
                episode.append((pos, action, reward))
        else:
            # Every-visit MC
            G += gamma**step * reward
            step += 1
            episode.append((pos, action, reward))

        if done:
            break
    # i, j 에피소드 출발 상태 좌표 eg. (0, 1)
    # G : 에피소드에서 얻은 수익 eg. -1.27
    # episode : 에피소드를 진행하면서 방문 정보를 저장한 리스트(방문 상태, 선택 행동, 보상)
    #          eg. [[[0,1], 3, -1],
    #               [[0,0], 0, -3]]
    return i, j, G, episode


# first-visit and every-visit MC Prediction
np.random.seed(0)
env = Environment()
agent = Agent()

# 임의의 상태 가치 함수 V
v_table = np.zeros((env.reward.shape[0], env.reward.shape[1]))

# 상태 방문 횟수 저장 테이블
v_visit = np.zeros((env.reward.shape[0], env.reward.shape[1]))

# 상태별로 에피소드 출발 횟수 저장 테이블
v_start = np.zeros((env.reward.shape[0], env.reward.shape[1]))

# 상태별로 도착지점 도착 횟수 저장 테이블
v_success = np.zeros((env.reward.shape[0], env.reward.shape[1]))

# 최대 에피소드 수 지정
max_episode = 99999

# first-visit MC or every-visit MC 사용 결정
first_visit = True
if first_visit:
    print("start first visit MC")
else:
    print("start every visit MV")
print()

gamma = 0.09

for epi in tqdm(range(max_episode)):
    i, j, G, episode = generate_episode(env, agent, first_visit)

    # 에피소드 분리 시작
    for step_num in range(len(episode)):
        G = 0

        # episode[step_num][0][0] : step_num번째 방문한 상태의 x좌표
        # episode[step_num][0][1] : step_num번째 방문한 상태의 y좌표
        # episode[step_num][1] : step_num번째 상태에서 선택한 행동
        i = episode[step_num][0][0]
        j = episode[step_num][0][1]

        # 에피소드 시작점 카운트
        v_visit[i, j] += 1

        # 서브 에피소드(episode[step_num:])의 출발부터 끝까지 보상 G 계산
        # k[2]: episode[step_num][2]와 같으며 step_num번째 받은 보상
        # step: 감쇄율
        for step, k in enumerate(episode[step_num:]):
            G += gamma**step * k[2]

        # Incremental mean 계산
        v_table[i, j] = v_table[i, j] + 1 / v_visit[i, j] * (G - v_table[i, j])

        # 도착지점에 도착(reward=1)했는지 체크
        # episode[-1][2] : 에피소드 마지막 상태의 보상
        if episode[-1][-1] == 1:
            v_success[i, j] += 1

    # 에피소드 출발 횟수 저장
    for i in range(env.reward.shape[0]):
        for j in range(env.reward.shape[1]):
            v_start[i][j] = v_visit[i, j]

print("V(s)")
show_v_table(np.round(v_table, 2), env)
print("V_start_count(s)")
show_v_table(np.round(v_start, 2), env)
print("V_success_pr(s)")
show_v_table(np.round(v_success / v_start, 2), env)
