# 틱택토 게임 : Q-learning

import numpy as np
from tqdm import tqdm


class Q_learning_player:
    """
    1. 초기화: qtable, epsilon, gamma, learning_rate(alpha)
    2. select_action() : 정책(policy)에 맞는 행동(action) 반환
    3. policy() : 가능한 행동들에 e-greedy 반영한 확률 반환
    4. learn_qtable() :
    """

    def __init__(self):
        self.name = "Q_player"

        # Q-table을 딕셔너리로 정의
        self.qtable = {}

        # 𝜀-greedy 계수 정의
        self.epsilon = 1

        # 학습률 정의
        self.learning_rate = 0.1
        self.gamma = 0.9
        self.print = False

    def select_action(self, env, player):
        """policy에 따라 상태에 맞는 행동을 선택"""
        action = self.policy(env)
        if self.print:
            print("{} : select action".format(action))
        return action

    def policy(self, env):
        if self.print:
            print("-----------   policy start -------------")
        # 행동 가능한 상태를 저장
        available_action = env.get_action()
        # 행동 가능한 상태의 Q-value를 저장
        qvalues = np.zeros(len(available_action))

        if self.print:
            print("{} : available_action".format(available_action))

        # 행동 가능한 상태의 Q-value를 조사
        for i, act in enumerate(available_action):
            key = (tuple(env.board_a), act)

            # 현재 상태를 경험한 적이 없다면(딕셔너리에 없다면) 딕셔너리에 추가(Q-value = 0)
            if self.qtable.get(key) == None:
                self.qtable[key] = 0
            # 행동 가능한 상태의 Q-value 저장
            qvalues[i] = self.qtable.get(key)

        if self.print:
            for key, val in self.qtable.items():
                print("key = {key}, value={value}".format(key=key, value=val))
            print("policy state_value = {}".format(state_qvalue))
            for key, val in self.qtable1.items():
                print("key = {key}, count={value}".format(key=key, value=val))

        # 𝜀-greedy: 가능한 행동 중 Q-value가 가장 큰 행동 저장
        ## max Q-value가 여러 개라면 그 중에서 다시 선택
        greedy_action = np.argmax(qvalues)

        pr = np.zeros(len(available_action))
        if self.print:
            print("{} : self.epsilon = {}".format(self.epsilon))
            print("{} : greedy_action".format(greedy_action))
            print("{} : qvalues".format(greedy_action, qvalues[greedy_action]))

        # max Q-value와 같은 값이 여러개 있는지 확인한 후 double_check에 상태를 저장
        ## 최댓값은 1로, 나머지는 0으로 변환 np.where(조건, 참, 거짓)
        double_check = np.where(qvalues == np.max(qvalues), 1, 0)

        #  여러개 있다면 중복된 상태중에서 다시 무작위로 선택
        if np.sum(double_check) > 1:
            if self.print:
                print("{} : double_check".format(np.round(double_check, 2)))
            ## 중복값을 모두 같은 확률로 변환
            double_check = double_check / np.sum(double_check)
            greedy_action = np.random.choice(
                range(0, len(double_check)), p=double_check
            )
            if self.print:
                print("{} : greedy_action".format(greedy_action))
                print("{} : double_check".format(np.round(double_check, 2)))
                print("{} : selected state".format(available_state[greedy_action]))

        # 𝜀-greedy로 행동들의 선택 확률을 계산
        pr = np.zeros(len(available_action))

        for i in range(len(available_action)):
            if i == greedy_action:
                pr[i] = 1 - self.epsilon + self.epsilon / len(available_action)
                if pr[i] < 0:
                    print("{} : - pr".format(np.round(pr[i], 2)))
            else:
                pr[i] = self.epsilon / len(available_action)
                if pr[i] < 0:
                    print("{} : - pr".format(np.round(pr[i], 2)))

        action = np.random.choice(range(0, len(available_action)), p=pr)

        if self.print:
            print("pr = {}".format(np.round(pr, 2)))
            print("action = {}".format(action))
            print("state[action] = {}".format(state[action]))
            print("-----------   policy end -------------")

        return available_action[action]

    def learn_qtable(self, board_bakup, action_backup, env, reward):
        # 현재 상태와 행동을 키로 저장
        key = (board_bakup, action_backup)
        if self.print:
            print("-----------   learn_qtable start -------------")
            print(
                "{} : board_bakup, {} : action_backup, {} : reward".format(
                    board_bakup, action_backup, reward
                )
            )
            print("{} : key".format(key))
        # Q-table 학습
        if env.done:
            # 게임이 끝났을 경우 학습
            # Q(s, a) <- Q(s, a) + 𝛼 * [r - Q(s, a)]
            if self.print:
                print("{} : before self.qtable[key]".format(self.qtable[key]))

            self.qtable[key] += self.learning_rate * (reward - self.qtable[key])

            if self.print:
                print("{} : after self.qtable[key]".format(self.qtable[key]))
        else:
            # 게임이 진행중일 경우 학습
            # 다음 상태의 max Q 값 계산
            available_action = env.get_action()
            qvalues = np.zeros(len(available_action))

            for i, act in enumerate(available_action):
                next_key = (tuple(env.board_a), act)
                # 다음 상태를 경험한 적이 없다면(딕셔너리에 없다면) 딕셔너리에 추가(Q-value = 0)
                if self.qtable.get(next_key) == None:
                    self.qtable[next_key] = 0
                qvalues[i] = self.qtable.get(next_key)

            # maxQ 조사
            maxQ = np.max(qvalues)

            if self.print:
                print("{} : before self.qtable[key]".format(self.qtable[key]))

            # 게임이 진행중일 때 학습
            # Q(s, a) <- Q(s, a) + 𝛼 * [r + 𝛾 * maxQ(s', a') - Q(s, a)]
            self.qtable[key] += self.learning_rate * (
                reward + self.gamma * maxQ - self.qtable[key]
            )

            if self.print:
                print("{} : after self.qtable[key]".format(self.qtable[key]))

        if self.print:
            print("-----------   learn_qtable end -------------")


class Environment:
    def __init__(self):
        """
        - 화면에 o, x를 표시하는 보드, 계산에 사용되는 보드
        - 보드는 0으로 초기화된 3x3 = 9 크기의 배열
        - 게임 종료 : done = True
        """
        self.board_a = np.zeros(9)
        self.done = False
        self.reward = 0  # 승자(1 or -1), 무승부(0)
        # self.winner = 0
        self.print = False  # 기본은 자동모드

    def print_board(self):
        """
        - 현재 보드 상태 출력: p1 = O, p2 = X
        - 선공 p1, 후공 p2
        """
        print("+----+----+----+")
        for i in range(3):
            for j in range(3):
                # [0], 1, 2,
                # [3], 4, 5,
                # [6], 7, 8
                if self.board_a[3 * i + j] == 1:
                    print("| 0 ", end=" ")
                elif self.board_a[3 * i + j] == -1:
                    print("| X ", end=" ")
                else:
                    print("|   ", end=" ")
            print("|")
            print("+----+----+----+")

    def get_action(self):
        """
        현재 보드 상태에서 가능한 행동(둘 수 있는 장소)을 탐색하고 리스트로 반환
        """
        observation = []
        for i in range(9):
            if self.board_a[i] == 0:
                observation.append(i)  # 빈 보드칸의 인덱스 추가
        return observation

    def end_check(self, player):
        """
        - 게임 종료(승패 or 비김) 판단
        - 승패 조건은 가로, 세로, 대각선이 -1이나 1로 동일할 때
        """
        end_condition = (
            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),  # 가로
            (0, 3, 6),
            (1, 4, 7),
            (2, 5, 8),  # 세로
            (0, 4, 8),
            (2, 4, 6),  # 대각선
        )
        # end_condition 배열을 돌며
        # 첫 번째 열 == 두 번째 열 (0 == 1), (3 == 4), (6 == 7)
        # 두 번째 열 == 세 번째 열 (1 == 2), (4 == 5), (7 == 8)
        # 체크하는 보드칸이 비어있지 않아야 함 => 가로 일치
        for line in end_condition:
            if (
                self.board_a[line[0]] == self.board_a[line[1]]
                and self.board_a[line[1]] == self.board_a[line[2]]
                and self.board_a[line[0]] != 0
            ):
                # 종료 상태, 승자 저장 후 함수 종료
                self.done = True
                self.reward = player
                return

        # 비긴 상태 : 보드에 빈 공간이 없을 때
        observation = self.get_action()
        if len(observation) == 0:
            self.done = True  # 종료 상태
            self.reward = 0  # 무승부
        # return

    def move(self, p1, p2, player):
        """
        # 게임 진행
        - 각 플레이어 선택 행동 표시하고 게임 상태(진행 or 종료) 판단
        - p1 = 1, p2 = -1로 정의
        - 각 플레이어는 행동을 선택하는 select_action 메서드 가짐
        """
        if player == 1:
            pos = p1.select_action(env, player)
        else:
            pos = p2.select_action(env, player)

        # 보드에 플레이어의 선택 표시
        self.board_a[pos] = player
        if self.print:  # 수동 모드일 경우에만 출력
            print(player)
            self.print_board()

        # 게임 종료 상태 여부 판단
        self.end_check(player)
        return self.reward, self.done


class Human_player:
    """인간 플레이어"""

    def __init__(self):
        self.name = "Human player"

    def select_action(self, env, player):
        while True:
            # 가능한 행동 조사 후 표시
            available_action = env.get_action()
            print("possible actions = {}".format(available_action))

            # 상태 번호 안내 출력
            print("+----+----+----+")
            print("+  0 +  1 +  2 +")
            print("+----+----+----+")
            print("+  3 +  4 +  5 +")
            print("+----+----+----+")
            print("+  6 +  7 +  8 +")
            print("+----+----+----+")

            # 키보드로 가능한 행동 입력받음
            action = input("Select action(human) : ")
            action = int(action)

            # 입력받은 행동이 가능한 행동이면 반복문 탈출
            if action in available_action:
                return action

            # 아니면 행동 입력 반복
            else:
                print("You selected wrong action")


# 게임 진행
p1_Qplayer = Q_learning_player()
p2_Qplayer = Q_learning_player()

p1_Qplayer.epsilon = 0.5
p2_Qplayer.epsilon = 0.5
p1_score = 0
p2_score = 0
draw_score = 0
max_learn = 100000

for j in tqdm(range(max_learn)):
    np.random.seed(j)
    env = Environment()
    for i in range(10000):
        # p1 행동 선택(p1이 둘 곳 선택)
        player = 1
        pos = p1_Qplayer.policy(env)

        # 현재 상태 s, 행동 a 저장
        p1_board_backup = tuple(env.board_a)
        p1_action_backup = pos
        env.board_a[pos] = player  # 보드에 착수
        env.end_check(player)  # 게임 종료 체크

        # 게임이 종료 상태라면 각 플레이어의 Q-table 학습
        if env.done:
            # 비겼으면 보상 0
            if env.reward == 0:
                p1_Qplayer.learn_qtable(p1_board_backup, p1_action_backup, env, 0)
                p2_Qplayer.learn_qtable(p2_board_backup, p2_action_backup, env, 0)
                draw_score += 1
                break
            else:
                p1_Qplayer.learn_qtable(
                    p1_board_backup, p1_action_backup, env, 1
                )  # p1 승리
                p2_Qplayer.learn_qtable(
                    p2_board_backup, p2_action_backup, env, -1
                )  # p2 패배
                p1_score += 1
                break

        # 게임이 끝나지 않았다면 p2의 Q-table을 학습 (게임 시작직후에는 p2는 학습할수 없음)
        if i != 0:
            p2_Qplayer.learn_qtable(p2_board_backup, p2_action_backup, env, -1)

        # p2 행동 선택
        player = -1
        pos = p2_Qplayer.policy(env)
        p2_board_backup = tuple(env.board_a)
        p2_action_backup = pos
        env.board_a[pos] = player
        env.end_check(player)

        # 게임이 종료 상태라면 각 플레이어의 Q-table 학습
        if env.done:
            # 비겼으면 보상 0
            if env.reward == 0:
                p1_Qplayer.learn_qtable(p1_board_backup, p1_action_backup, env, 0)
                p2_Qplayer.learn_qtable(p2_board_backup, p2_action_backup, env, 0)
                draw_score += 1
                break
            else:
                p1_Qplayer.learn_qtable(
                    p1_board_backup, p1_action_backup, env, -1
                )  # p1 패배
                p2_Qplayer.learn_qtable(
                    p2_board_backup, p2_action_backup, env, 1
                )  # p2 승리
                p2_score += 1
                break

        # 게임이 끝나지 않았다면 p1의 Q-table을 학습
        p1_Qplayer.learn_qtable(p1_board_backup, p1_action_backup, env, -1)

    # 1000게임마다 결과 표시
    if j % 1000 == 0:
        print(
            "j = {}, p1 = {}, p2 = {}, draw = {}".format(
                j, p1_score, p2_score, draw_score
            )
        )

print("p1 = {} p2 = {} draw = {}".format(p1_score, p2_score, draw_score))
print("end train")
