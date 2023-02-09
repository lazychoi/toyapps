# 정책 반복

import random
from L01_environment import GraphicDisplay, Env


class PolicyIteration:
    def __init__(self):
        self.env = Env()

        # 가치함수 : 2차원 리스트로 초기화. width=5, height=5 => 5 x 5
        self.value_table = [[0.0] * self.env.width for _ in range(self.env.height)]
        # 상 하 좌 우를 동일한 확률로 초기화. 5 x 5 x 4
        self.policy_table = [
            [[0.25, 0.25, 0.25, 0.25]] * self.env.width for _ in range(self.env.height)
        ]

        # 종료 상태 설정
        self.policy_table[2][2] = []
        # 감가율
        self.discount_factor = 0.9

    def get_policy(self, state):
        """상태에 따른 정책(확률) 반환. state=좌표"""
        if state == [2, 2]:
            return 0.0
        return self.policy_table[state[0]][state[1]] # [0.25, 0.25, 0.25, 0.25]

    def get_action(self, state):
        """특정 상태에서 정책에 따른 행동 반환. state=좌표"""
        # 0-1 사이 값을 무작위 추출. 소숫점 두자리수까지만 뽑으려고 아래 같은 수식 사용
        random_pick = random.randrange(100) / 100
        policy = self.get_policy(state)  # [0.25, 0.25, 0.25, 0.25]
        policy_sum = 0.0
        # 정책에 담긴 행동 중 무작위로 한 행동 추출
        for index, value in enumerate(policy):
            policy_sum += value
            if random_pick < policy_sum:
                return index

    def get_value(self, state):
        """가치함수 값 반환"""
        return round(self.value_table[state[0]][state[1]], 2)

    def policy_evaluation(self):
        """정책평가: 벨만 기대 방정식을 통해 다음 가치함수를 계산"""
        
        # 업데이트 정보를 담을 상태가치 변수 초기화 (5,5)
        next_value_table = [[0.00] * self.env.width for _ in range(self.env.height)]

        # 모든 상태에 대해 벨만 기대 방정식 계산 
        # 모든 상태 env.get_all_states() => [[0,0], [0,1], ..., [4,4]]
        for state in self.env.get_all_states():
            value = 0.0
            # 종료 상태의 가치 = 0
            if state == [2, 2]:
                next_value_table[state[0]][state[1]] = 0.0
                continue    # [2,2] 상태에서는 아래 코드 실행하지 않고 넘어감
            
            # 벨만 기대 방정식 -> 현재 상태의 모든 행동으로 얻는 가치 합계
            for action in self.env.possible_actions:
                # 현재 상태에서 행동을 했을 때의 보상
                reward = self.env.get_reward(state, action)
                # 행동 후의 상태 좌표 eg. [1, 2]
                next_state = self.env.state_after_action(state, action)
                # 이동한 상태의 가치
                next_value = self.get_value(next_state)
                # 𝚺 <- 𝛑(a|s) * [R_t+1 + 𝛄 v(s')]
                value += self.get_policy(state)[action] * (
                    reward + self.discount_factor * next_value
                )
            # 특정 상태의 모든 행동으로 얻은 가치 합계를 "업데이트 용 상태가치"에 저장
            next_value_table[state[0]][state[1]] = round(value, 2)
        
        # 상태가치 업데이트
        self.value_table = next_value_table

    def policy_improvement(self):
        """현재 가치함수에 대해 탐욕정책개선"""
        # 업데이트 용 행동가치 변수 (5,5,4)
        next_policy = self.policy_table
        # 모든 상태에 대해 벨만 최적 방정식 적용
        for state in self.env.get_all_states():
            if state == [2, 2]:
                continue
            value = -99999   # 최대값 판별 용
            max_index = []   # 받을 보상이 최대인 행동 저장
            # 반환할 정책 초기화
            result = [0.0, 0.0, 0.0, 0.0]
            # 모든 행동에 대해 [보상 + (감가율 * 다음 상태 가치함수)] 계산
            for index, action in enumerate(self.env.possible_actions):
                reward = self.env.get_reward(state, action)
                next_state = self.env.state_after_action(state, action)
                next_value = self.get_value(next_state)
                temp = reward + self.discount_factor * next_value
                # 받을 보상이 최대인 행동의 인덱스(여러 개라면 모두) 추출
                if temp == value:           # 현재 행동의 가치가 최댓값과 같으면
                    max_index.append(index)
                elif temp > value:
                    value = temp
                    max_index.clear()
                    max_index.append(index)
            # 최대값이 여러 개일 때 확률을 똑같이 만듦
            prob = 1 / len(max_index) # 1개이면 1, 2개이면 0.5
            for index in max_index:
                result[index] = prob
            # 행동가치 저장
            next_policy[state[0]][state[1]] = result  # 최댓값의 확률만 저장, 나머지는 기본값 0
        # 행동 가치 업데이트
        self.policy_table = next_policy  # 최댓값 1개 -> eg. [0, 0, 1, 0], 2개 -> eg. [0.5, 0, 0, 0.5]


if __name__ == "__main__":
    policy_iteration = PolicyIteration()
    grid_world = GraphicDisplay(policy_iteration)
    grid_world.mainloop()
