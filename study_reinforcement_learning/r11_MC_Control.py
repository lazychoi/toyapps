# MC Control

import numpy as np
from tqdm import tqdm

from r01_env_agent import Environment, Agent
from r02_show import show_q_table, show_policy


# 정책을 받아 에피소드 생성
def generate_episode_with_policy(env, agent, first_visit, policy):
    gamma = 0.09

    # 에피소드 저장 리스트
    episode = []

    # 이전 방문 여부 체크
    visit = np.zeros((env.reward.shape[0], env.reward.shape[1], len(agent.action)))

    # 에이전트는 항상 (0,0)에서 출발
    i = 0
    j = 0
    agent.set_pos([i, j])

    # 에피소드 수익 초기화
    G = 0

    # 감쇄율 지수
    step = 0
    max_step = 100

    # 에피소드 생성
    for k in range(max_step):
        pos = agent.get_pos()

        # 현재 상태의 정책을 이용해 행동을 선택한 후 이동
        action = np.random.choice(
            range(0, len(agent.action)), p=policy[pos[0], pos[1], :]
        )

        observation, reward, done = env.move(agent, action)

        if first_visit:
            # 에피소드가 첫 방문인지 검사
            if visit[pos[0], pos[1], action] == 0:
                # 에피소드가 끝날 때까지 G 계산
                G += gamma**step * reward
                # 방문 이력 표시
                visit[pos[0], pos[1], action] = 1
                step += 1
                # 방문 이력 저장(상태, 행동, 보상)
                episode.append((pos, action, reward))

        else:
            # every-visit MC
            G += gamma**step * reward
            step += 1
            episode.append((pos, action, reward))

        # 에피소드가 종료되면(done==True) 루프에서 탈출
        if done:
            break

    return i, j, G, episode


# 몬테카를로 방법의 Control 알고리즘
np.random.seed(0)

# 환경, 에이전트 초기화
env = Environment()
agent = Agent()

# 모든 𝑠∈𝑆,𝑎∈𝐴(𝑆)에 대해 초기화:
# # 𝑄(𝑠,𝑎)←임의의 값 (행동 개수, 미로 세로, 미로 가로)
Q_table = np.random.rand(env.reward.shape[0], env.reward.shape[1], len(agent.action))

print("Initial Q(s, a)")
show_q_table(Q_table, env)

# 상태 방문 횟수 저장 테이블
Q_visit = np.zeros((env.reward.shape[0], env.reward.shape[1], len(agent.action)))

# 미로의 모든 상태에서의 최적 행동 저장 테이블
optimal_a = np.zeros((env.reward.shape[0], env.reward.shape[1]))

# 각 상태에서 Q값이 가장 큰 행동 선택 후 optimal_a에 저장
for i in range(env.reward.shape[0]):
    for j in range(env.reward.shape[1]):
        optimal_a[i, j] = np.argmax(Q_table[i, j, :])
print("initial optimal_a")
show_policy(optimal_a, env)

# π(𝑠,𝑎)←임의의 𝜖−탐욕 정책
# 무작위로 행동을 선택하도록 지정
policy = np.zeros((env.reward.shape[0], env.reward.shape[1], len(agent.action)))

# 한 상태에서의 가능한 확률의 합이 1이 되도록
# 𝜖−탐욕 정책으로 정책 계산
epsilon = 0.8
for i in range(env.reward.shape[0]):
    for j in range(env.reward.shape[1]):
        for k in range(len(agent.action)):
            if optimal_a[i, j] == k:  # action이 최적이면
                policy[i, j, k] = 1 - epsilon + epsilon / len(agent.action)
            else:  # action이 최적이 아니면
                policy[i, j, k] = epsilon / len(agent.action)

print("Initail Policy")
show_q_table(policy, env)

# 최대 에피소드 수 지정
max_episode = 10000

first_visit = True
if first_visit:
    print("start first visit MC")
else:
    print("start every visit MC")
print()

gamma = 0.09

# 에피소드를 이용해 Q_table의 각 정책(방향) 값 업데이트
for epi in tqdm(range(max_episode)):
    # (a) 𝛑를 이용해 에피소드 1개 생성
    x, y, G, episode = generate_episode_with_policy(env, agent, first_visit, policy)

    for step_num in range(len(episode)):
        G = 0
        i = episode[step_num][0][0]
        j = episode[step_num][0][1]
        action = episode[step_num][1]

        # 에피소드 시작점 카운트
        Q_visit[i, j, action] += 1

        # 서브 에피소드(episode[step_num:])의 출발부터 끝까지 수익 G 계산
        # k[2] = episode[step_num][2] = step_num번째 받은 보상
        for step, k in enumerate(episode[step_num:]):
            G += gamma**step * k[2]

        # Incremental mean: Q(s,a) <- average(Return(s,a))
        Q_table[i, j, action] += 1 / Q_visit[i, j, action] * (G - Q_table[i, j, action])

    # optimal_a(최적 정책) 업데이트
    # by 업데이트 된 Q_table 각 s의 네 방향 중 가장 높은 값을 optimal_a(최적 정책)에 저장
    # (c) 에피소드 안의 각 s에 대해서
    # 미로 모든 상태에서 최적 행동을 저장할 공간 마련
    # 𝑎∗ ←argmax_a 𝑄(𝑠,𝑎)
    for i in range(env.reward.shape[0]):
        for j in range(env.reward.shape[1]):
            optimal_a[i, j] = np.argmax(Q_table[i, j, :])

    # 모든 𝑎∈𝐴(𝑆) 에 대해서 :
    # 새로 계산된 optimal_a 를 이용해서 행동 선택 확률 policy (π) 갱신
    epsilon = 1 - epi / max_episode  # TODO 𝜖 값을 변경하는 이유????

    for i in range(env.reward.shape[0]):
        for j in range(env.reward.shape[1]):
            for k in range(len(agent.action)):
                if optimal_a[i, j] == k:
                    policy[i, j, k] = 1 - epsilon + epsilon / len(agent.action)
                else:
                    policy[i, j, k] = epsilon / len(agent.action)

print("Final Q(s,a)")
show_q_table(Q_table, env)
print("Final policy")
show_q_table(policy, env)
print("Final optimal_a")
show_policy(optimal_a, env)
