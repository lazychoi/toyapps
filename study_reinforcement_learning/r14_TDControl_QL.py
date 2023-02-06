# TD(0) Control : Q-learning

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
# 𝑄(𝑠,𝑎) ← 임의의 값
Q_table = np.random.rand(env.reward.shape[0], env.reward.shape[1], len(agent.action))

# Q(𝑡𝑒𝑟𝑚𝑖𝑛𝑎𝑙−𝑠𝑡𝑎𝑡𝑒,𝑎)=0
Q_table[-1, -1, :] = 0

max_episode = 10000
max_step = 100

print("start TD(0) control : Q-learning")
alpha = 0.1
epsilon = 0.8

# 각 에피소드에 대해 반복 :
for epi in tqdm(range(max_episode)):
    dleta = 0
    # S 를 초기화
    i = 0
    j = 0
    agent.set_pos([i, j])

    # 에피소드의 각 스텝에 대해 반복 :
    for k in range(max_step):
        # s에서 행동 정책(Behavior policy)으로 행동 a 선택(ε-greedy)
        pos = agent.get_pos()
        action = e_greedy(Q_table, agent, epsilon)

        # 행동 a 를 취한 후 보상 r과 다음 상태 s'를 관측
        observation, reward, done = env.move(agent, action)

        # s' 에서 타깃 정책(Target policy)으로 행동 a'를 선택(greedy)
        next_action = greedy(Q_table, agent, epsilon)

        # Q(s,a)←Q(s,a) + α[r + 𝛾*maxa'𝑄(s',a')−𝑄(s,a)]
        Q_table[pos[0], pos[1], action] += alpha * (
            reward
            + gamma * Q_table[observation[0], observation[1], next_action]
            - Q_table[pos[0], pos[1], action]
        )

        # s가 마지막 상태라면 종료
        if done:
            break

# 학습된 정책 중 최적 행동을 optimal_policy에 저장
optimal_policy = np.zeros((env.reward.shape[0], env.reward.shape[1]))
for i in range(env.reward.shape[0]):
    for j in range(env.reward.shape[1]):
        optimal_policy[i, j] = np.argmax(Q_table[i, j])

print("Q_table-learning : Q_table(s,a)")
show_q_table(np.round(Q_table, 2), env)
print("Q_table-learning : optimal ploicy")
show_policy(optimal_policy, env)
