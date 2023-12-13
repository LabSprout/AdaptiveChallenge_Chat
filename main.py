import time
from typing import List, Dict

# メッセージを表す構造体
class Message:
    def __init__(self, from_id, to_id, content, time):
        self.from_id = from_id
        self.to_id = to_id
        self.content = content
        self.time = time
        
    # メッセージの整形
    def getMessage(self):
        return "{} -> {}: {}".format(self.from_id, self.to_id, self.content)

# ユーザーリスト
user_list: List[str] = []

# メッセージを保存する辞書
message_dict: Dict[str, Dict[str, List[Message]]]= {}

# ユーザーを追加する
def add_user(user_id):
    # ユーザーIDが既に登録されているかチェック
    if user_id in user_list:
        return "ERROR: ID already used!"
    else:
        # 登録されていなかったらユーザーリストに追加
        user_list.append(user_id)
        # メッセージを保存する辞書に追加
        message_dict[user_id] = {}
        return "{} registered!".format(user_id)

# ユーザーにメッセージを送る
def talk(from_id, to_id, content):
    # ユーザーがユーザーリストに存在するかチェック
    if (from_id not in user_list) or (to_id not in user_list):
        return "ERROR: no user ID"
    elif from_id == to_id:
        return "Error: same user refered"
    else:
        # メッセージを作成
        message = Message(from_id, to_id, content, time.time())

        # メッセージの保存
        if to_id not in message_dict[from_id]:
            message_dict[from_id][to_id] = [message]
        else:
            message_dict[from_id][to_id].append(message)

        return ""

# ログを表示する
def show_log(id_1, id_2):
    # ユーザーがユーザーリストに存在するかチェック
    if (id_1 not in user_list) or (id_2 not in user_list):
        return "ERROR: no user ID"
    elif id_1 == id_2:
        return "Error: same user refered"
    else:
        # メッセージの一覧を取得
        msg_list1 = message_dict[id_1][id_2]
        msg_list2 = message_dict[id_2][id_1]
        msg_list_all = msg_list1 + msg_list2

        # メッセージの時刻でソート
        msg_list_all.sort(key=lambda x: x.time)

        # メッセージの取得
        return "\n".join([msg.getMessage() for msg in msg_list_all])

# メイン関数
def main():
    while True:
        try:
            # 標準入力を受け取り空白で分割する
            cmd = input("input: ").split(' ', 3) # talkコマンドでメッセージに空白が含まれるため3に設定
            res = "" # 出力する文字列

            # add_user コマンド
            if cmd[0] == "add_user" and len(cmd) == 2:
                res = add_user(cmd[1])

            # talk コマンド
            elif cmd[0] == "talk" and len(cmd) == 4:
                res = talk(cmd[1], cmd[2], cmd[3])

            # show_log コマンド
            elif cmd[0] == "show_log" and len(cmd) == 3:
                res = show_log(cmd[1], cmd[2])

            # 標準出力に返答
            if res != "":
                print("OUTPUT: {}".format(res))

        except EOFError:
            # Ctrl + D で終了
            break

if __name__ == "__main__":
    main()
