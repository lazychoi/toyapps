import pandas as pd
from pymongo import MongoClient
from tabulate import tabulate

class Member:
    def __init__(self):
        self.myclient = MongoClient("mongodb://localhost:27017")
        self.mydb = self.myclient["test"]
        self.mycollection = self.mydb["member"]

    def signup(self):
        cnt = self.mycollection.find_one(sort=[("_id", -1)])["_id"]
        name = input("이름을 입력하세요: ")
        age = int(input("나이를 입력하세요: "))
        address = input("주소를 입력하세요: ")
        phone = input("전화번호를 입력하세요: ")

        member = {
            "_id": cnt+1,
            "name": name,
            "age": age,
            "address": address,
            "phone": phone
        }
        self.mycollection.insert_one(member)
        print("회원으로 가입되었습니다.")

    def show_members(self):
        result = list(self.mycollection.find())
        df = pd.DataFrame(result)
        print(tabulate(df, headers="keys", tablefmt="psql", showindex=False))
        print()

    def select_member(self):
        try:
            select_key = input("검색할 키를 입력하세요: ")
            select_value = input("검색할 값 입력하세요: ")
            if select_key == "_id" or select_key == "age":
                select_value = int(select_value)
                select_arg1 = {select_key: select_value}
            else:
                select_arg1 = {select_key: {"$regex": select_value}}
            select_arg2 = {}
            result = self.mycollection.find(select_arg1, select_arg2)
            df = pd.DataFrame.from_dict(result)
            print(tabulate(df, headers="keys", tablefmt="psql", showindex=False))
        except:
            print("안내에 따라 올바로 입력하세요.")

    def update_member(self):
        member.show_members()
        try:
            update_id = int(input("수정할 회원번호를 입력하세요: "))
            update_key = input("수정할 컬럼명을 입력하세요: ")
            update_value = input("수정할 값을 입력하세요: ")
            update_arg1 = {"_id": update_id}
            update_arg2 = {"$set": {update_key: update_value}}
            self.mycollection.update_one(update_arg1, update_arg2)
            member.show_members()
        except:
            print("안내에 따라 올바로 입력하세요.")

    def delete_member(self):
        member.show_members()
        try:
            delete_value = int(input("삭제할 회원번호를 입력하세요: "))
            delete_arg1 = {"_id": delete_value}
            result = self.mycollection.delete_one(delete_arg1)
            if result.deleted_count > 0:
                print(delete_value, "번 회원님의 정보가 삭제되었습니다.")
            else:
                print("회원번호를 잘못 선택했습니다.")
        except:
            print("삭제할 회원번호를 올바로 입력하세요.")

if __name__ == "__main__":

    member = Member()
    while True:
        print("[[전체 회원 조회: 1 | 특정 회원 조회: 2 | 회원 가입: 3 | 회원 수정: 4 | 회원 삭제: 5 | 프로그램 종료: 1~5를 제외한 아무거나]]를 선택하세요")
        user = input("> ")

        if user == "1":
            member.show_members()
        elif user == "2":
            member.select_member()
        elif user == "3":
            member.signup()
        elif user == "4":
            member.update_member()
        elif user == "5":
            member.delete_member()
        else:
            print("프로그램을 종료합니다.")
            break