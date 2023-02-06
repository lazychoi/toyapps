# TD(0) Control : SARSA

import numpy as np
from tqdm import tqdm
from r01_env_agent import Environment, Agent
from r02_show import show_q_table, show_policy


# 𝜖−𝑔𝑟𝑒𝑒𝑑𝑦 함수 작성
def e_greedy(Q_table, agent, epsilon):
    pos = agent.get_pos()
    greedy_action = np.argmax(Q_table[pos[0], pos[1]])
    pr = np.zeros(4)
    for i in range(len(agent.action)):
        if i == greedy_action:
            pr[i] = 1 - epsilon + epsilon / len(agent.action)
        else:
            pr[i] = epsilon / len(agent.action)
    # 업데이트 된 pr 확률을 반영해서 방향을 랜덤 추출하여 반환
    return np.random.choice(range(0, len(agent.action)), p=pr)


# 𝑔𝑟𝑒𝑒𝑑𝑦  함수 작성
def greedy(Q_table, agent, epsilon):
    pos = agent.get_pos()
    # 최적 방향 반환
    return np.argmax(Q_table[pos[0], pos[1]])


np.random.seed(0)
env = Environment()
agent = Agent()
gamma = 0.9

# 모든 𝑠∈𝑆,𝑎∈𝐴(𝑆)에 대해 초기화:
# 𝑄(𝑠,𝑎)←임의의 값. shape = (3,3,4)
Q_table = np.random.rand(env.reward.shape[0], env.reward.shape[1], len(agent.action))

# Q(𝑡𝑒𝑟𝑚𝑖𝑛𝑎𝑙−𝑠𝑡𝑎𝑡𝑒,𝑎)=0 목적지 상태는 0
Q_table[-1, -1] = 0

max_episode = 10000
max_step = 100

print("Start TD(0) control : SARSA")
alpha = 0.1
epsilon = 0.8

# 각 에피소드 반복
for epi in tqdm(range(max_episode)):
    delta = 0
    i = 0
    j = 0
    agent.set_pos([i, j])
    temp = 0

    # s 에서 행동 정책(Behavior policy)으로 행동 a를 선택. => ε-greedy
    action = e_greedy(Q_table, agent, epsilon)

    # 에피소드의 각 스텝 반복
    for k in range(max_step):
        pos = agent.get_pos()

        # 행동 a 를 취한 후 보상 r과 다음 상태 s'  관측
        observation, reward, done = env.move(agent, action)

        # s' 에서 타깃 정책(Target policy)으로 행동 a'를 선택. => ε-greedy
        next_action = e_greedy(Q_table, agent, epsilon)

        # s <- s'
        # Q(𝑆,𝐴)←Q(𝑆,𝐴) + α[𝑅+𝛾𝑄(𝑆',𝐴')−𝑄(𝑆,𝐴)]
        Q_table[pos[0], pos[1], action] += alpha * (
            reward
            + gamma * Q_table[observation[0], observation[1], next_action]
            - Q_table[pos[0], pos[1], action]
        )

        # a <- a'
        action = next_action

        # s가 마지막 상태라면 종료
        if done:
            break

# 학습된 정책 중 최적 행동을 optimal_policy에 저장
optimal_policy = np.zeros((env.reward.shape[0], env.reward.shape[1]))
for i in range(env.reward.shape[0]):
    for j in range(env.reward.shape[1]):
        optimal_policy[i, j] = np.argmax(Q_table[i, j])

print("SARSA : Q(s,a)")
show_q_table(np.round(Q_table, 2), env)
print("SARSA : optimal ploicy")
show_policy(optimal_policy, env)
