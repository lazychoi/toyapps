# 정책 반복

import random
from L01_environment import GraphicDisplay, Env


class PolicyIteration:
    def __init__(self):
        self.env = Env()
        
        # 가치함수 : 2차원 리스트로 초기화. width=5, height=5 => 5 x 5
        self.value_table = [[0.00 * self.env.width for _ in
                             range(self.env.height)]]
        # 상 하 좌 우를 동일한 확률로 초기화. 5 x 5 x 4
        self.policy_table = [[[0.25, 0.25, 0.25, 0.25]] * self.env.width
                             for _ in range(self.env.height)]
        
        # 종료 상태 설정
        self.policy_table[2][2] = []
        # 감가율
        self.discount_factor = 0.9
    
    def get_policy(self, state):
        """상태에 따른 정책(확률) 반환. state=좌표"""
        if state == [2, 2]:
            return 0.0
        return self.policy_table[state[0]][state[1]]      
        
    def get_action(self, state):
        """특정 상태에서 정책에 따른 행동 반환. state=좌표"""
        # 0-1 사이 값을 무작위 추출. 소숫점 두자리수까지만 뽑으려고 아래 같은 수식 사용
        random_pick = random.randrange(100) / 100
        policy = self.get_policy(state) # [0.25, 0.25, 0.25, 0.25]
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
        # 다음 가치함수 초기화
        next_value_table = [[0.00 * self.env.width for _ in
                             range(self.env.height)]]
        
        # 모든 상태에 대해 벨만 기대 방정식 계산
        for state in self.env.get_all_states():
            value = 0.0
            # 종료 상태의 가치함수 = 0
            if state == [2, 2]:
                next_value_table[state[0]][state[1]] = 0.0
                continue    # 없어도 되지 않을까?
            # 벨만 기대 방정식
            for action in self.env.possible_actions:
                next_state = self.env.state_after_action(state, action)
                reward = self.env.get_reward(state, action)
                next_value = self.get_value(next_state)
                value += self.get_policy(state)[action] * \
                        (reward + self.discount_factor * next_value)
            next_value_table[state[0]][state[1]] = round(value, 2)
        
        
if __name__ == '__main__':
    policy_iteration = PolicyIteration()
    grid_world = GraphicDisplay(policy_iteration)
    grid_world.mainloop()