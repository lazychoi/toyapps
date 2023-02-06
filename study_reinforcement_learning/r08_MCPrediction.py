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

    # 에이전트의 출발지점을 무작위로 설정
    i = np.random.randint(0, env.reward.shape[0])
    j = np.random.randint(0, env.reward.shape[1])
    agent.set_pos([i, j])

    # 에피소드 수익률 초기화
    G = 0

    # 감쇄율 지수
    step = 0
    max_step = 100

    # 에피소드 생성
    for k in range(max_step):
        pos = agent.get_pos()
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

        if done == True:
            break
    # i, j 에피소드 출발 상태 좌료
    # G : 에피소드에서 얻은 수익
    # episode : 에피소드를 진행하면서 방문 정보를 저장한 리스트(방문 상태, 선택 행동, 보상)
    return i, j, G, episode


# first-visit and every-visit MC Prediction
np.random.seed(0)
env = Environment()
agent = Agent()

# 임의의 상태 가치 함수 V
v_table = np.zeros((env.reward.shape[0], env.reward.shape[1]))

# 상태별로 에피소드 출발 횟수 저장 테이블
v_start = np.zeros((env.reward.shape[0], env.reward.shape[1]))

# 상태별로 도착지점 도착 횟수 저장 테이블
v_success = np.zeros((env.reward.shape[0], env.reward.shape[1]))

# Return(s) <- 3x3 빈 리스트(모든 s ∈ S에 대해) 리스트 내의 리스트
Return_s = [
    [[] for j in range(env.reward.shape[1])] for i in range(env.reward.shape[0])
]

# 최대 에피소드 수 지정
max_episode = 100000

# first-visit MC or every-visit MC 사용 결정
first_visit = True
if first_visit:
    print("start first visit MC")
else:
    print("start every visit MV")
print()

for epi in tqdm(range(max_episode)):
    i, j, G, episode = generate_episode(env, agent, first_visit)

    # 수익 G를 Return(s)에 추가
    Return_s[i][j].append(G)

    # 에피소드 발생 횟수 계산
    episode_count = len(Return_s[i][j])

    # 상태별 발생한 수익의 총합 계산
    total_G = np.sum(Return_s[i][j])

    # 상태별 발생한 수익의 평균 계산
    # V(s) <- average(Return(s))
    v_table[i, j] = total_G / episode_count

    # 도착지점에 도착(reward=1)했는지 체크
    # episode[-1][2] : 에피소드 마지막 상태의 보상
    if episode[-1][-1] == 1:
        v_success[i, j] += 1

# 에피소드 출발 횟수 저장
for i in range(env.reward.shape[0]):
    for j in range(env.reward.shape[1]):
        v_start[i][j] = len(Return_s[i][j])

print("V(s)")
show_v_table(np.round(v_table, 2), env)
print("V_start_count(s)")
show_v_table(np.round(v_start, 2), env)
print("V_success_pr(s)")
show_v_table(np.round(v_success / v_start, 2), env)
