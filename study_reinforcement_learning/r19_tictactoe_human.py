# 틱택토 게임
# 1. 번갈아 가며 보드에 놓을 곳 선택: env.move(p1, p2, player)
#                       -> reward(승자, 1 or -1), done(게임 끝, True or False)
#   - 플레이어별 놓을 곳 선택: p1.select_action(env, player) -> pos(0-8)
#       - 움직일 수 있는 곳 체크: env.get_action()
#       - 사용자에게 입력받기
#   - 수동모드일 경우 pos위치에 말을 출력
#   - 게임을 끝낼 상태인지 검사: env.end_check
# 2. 선택한 위치를 보드에 입력: board_a[pos] = player
# 3. 보드 출력: env.print_board()
# 4. 게임을 끝낼 상태인지 검사: env.end_check()

import numpy as np


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


class Random_player:
    def __init__(self):
        self.name = "Random player"

    def select_action(self, env, player):
        # 가능한 행동 조사
        available_action = env.get_action()

        # 가능한 행동 중 하나를 무작위로 선택
        action = np.random.randint(len(available_action))
        return available_action[action]


# 게임 진행
p1 = Human_player()
p2 = Random_player()

# 지정된 게임 횟수를 자동으로 두게 할 것인지 한 게임씩 두게 할 것인지 설정
# auto = True : 지정된 게임 횟수(games)를 자동으로 진행
# auto = False : 한 게임씩 진행
auto = False

# auto 모드의 게임 횟수
games = 100
print("p1 player : {}".format(p1.name))
print("p2 player : {}".format(p2.name))

# 각 플레이어의 승리 횟수 저장
p1_score = 0
p2_score = 0
draw_score = 0  # 무승부

if auto:
    # 자동 모드 실행
    for j in range(games):
        np.random.seed(j)
        env = Environment()

        for i in range(10000):
            # p1, p2가 번갈아 게임 진행 -> (-1)**i
            # p1(1) -> p2(-1) -> p1(1) -> p2(-1) -> ...
            reward, done = env.move(p1, p2, (-1) ** i)

            # 게임 종료 체크
            if done:
                if reward == 1:
                    print("j = {} winner is p1({})".format(j, p1.name))
                    p1_score += 1
                elif reward == -1:
                    print("j = {} winner is p2({})".format(j, p2.name))
                    p2_score += 1
                else:
                    print("j = {} draw".format(j))
                    draw_score += 1
                break
else:
    # 한 게임씩 진행하는 수동 모드
    while True:
        env = Environment()
        env.print = True  # 사용자가 둔 곳 출력도록 옵션 설정
        for i in range(10000):
            reward, done = env.move(p1, p2, (-1) ** i)  # p1부터 시작((-1)**i -> 1)

            # 게임 종료 체크
            if done:
                if reward == 1:
                    print("winner is p1({})".format(p1.name))
                    p1_score += 1
                elif reward == -1:
                    print("winner is p2({})".format(p2.name))
                    p2_score += 1
                else:
                    print("draw")
                    draw_score += 1
                break

        # 최종 결과 출력
        print("final result")
        env.print_board()

        # 한 게임 더? 출력
        answer = input("More Game? (y/n) : ")
        if answer == "n":
            break

print(
    "p1({}) = {}, p2({}) = {}, draw = {}".format(
        p1.name, p1_score, p2.name, p2_score, draw_score
    )
)
