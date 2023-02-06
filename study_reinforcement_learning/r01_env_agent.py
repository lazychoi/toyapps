import numpy as np


class Environment:
    # 1. 미로밖(절벽), 길, 목적지와 보상 설정
    cliff = -3
    road = -1
    goal = 1

    # 2. 목적지 좌표 설정
    goal_position = [2, 2]

    # 3. 보상 리스트 숫자
    reward_list = [[road, road, road], [road, road, road], [road, road, goal]]

    # 4. 보상 리스트 문자
    reward_list1 = [
        ["road", "road", "road"],
        ["road", "road", "road"],
        ["road", "road", "goal"],
    ]

    # 5. 보상 리스트를 array로 설정
    def __init__(self):
        self.reward = np.array(self.reward_list)

        # 6. 선택된 에이전트의 행동 결과 반환 (미로밖일 경우 이전 좌표로 다시 복귀)

    def move(self, agent, action):
        done = False

        # 6.1 행동에 따른 좌표 구하기.
        # 미로에서의 에이전트 좌표 + 움직일 방향 좌표 = 새로운 좌표
        # eg. agent.pos=(1,1) + agent.action[1]=(0,1) => (1,2) 우측 한 칸 이동
        new_pos = agent.pos + agent.action[action]

        # 6.2 에이전트가 위치한 좌표가 목적지인지 확인
        if self.reward_list1[agent.pos[0]][agent.pos[1]] == "goal":
            reward = self.goal  # 선택한 행동에 따른 보상값 1
            observation = agent.set_pos(agent.pos)  # 에이전트가 이동한 좌표
            done = True  # 도착지여서 더이상 진행 불가

        # 6.3 이동 후 좌표가 미로 밖인지 확인
        elif (
            new_pos[0] < 0
            or new_pos[0] >= self.reward.shape[0]
            or new_pos[1] < 0
            or new_pos[1] >= self.reward.shape[1]
        ):
            reward = self.cliff  # 선택한 행동에 따른 보상값 -3
            observation = agent.set_pos(agent.pos)  # 미로 밖이면 이동 전 좌표로 설정
            done = True  # 미로 밖이어서 더이상 진행 불가

        # 6.4 이동 후 좌표가 움직일 수 있는 길이라면
        else:
            observation = agent.set_pos(new_pos)  # 에이전트가 이동한 좌표
            reward = self.reward[observation[0], observation[1]]  # 선택한 행동에 따른 보상값 -1

        return observation, reward, done


class Agent:
    # 1. 행동에 따른 에이전트의 좌표 이동(위, 오른쪽, 아래, 왼쪽)
    action = np.array([[-1, 0], [0, 1], [1, 0], [0, -1]])

    # 2. 각 행동별 선택확률
    select_action_pr = np.array([0.25, 0.25, 0.25, 0.25])

    # 3. 미로 안에서의 에이전트 초기 위치 저장
    def __init__(self):
        self.pos = (0, 0)

    # 4. 미로 안에서의 에이전트 위치 저장
    def set_pos(self, position):
        self.pos = position
        return self.pos

    # 5. 미로 안에서의 에이전트 위치 불러오기
    def get_pos(self):
        return self.pos
