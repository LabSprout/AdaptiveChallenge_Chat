import time
from typing import List, Dict

ngwords = []
with open("ngwords.txt", "r") as f:
    for word in f.readlines():
        word = word.replace("\n", "")
        ngwords.append(word)
# メッセージを表す構造体
class Message:
    def __init__(self, from_id, to_id, content, time):
        self.from_id = from_id
        self.to_id = to_id
        self.content = content
        self.time = time
        
    # メッセージの整形
    def getMessage(self):
        string = "{} -> {}: {}".format(self.from_id, self.to_id, self.content)
        string = string.replace("<br>", "\n") #改行タグの処理
        for ngword in ngwords:
            string = string.replace(ngword, "*") #ngwordの処理
        return string 

class ChatRoom:
    def __init__(self, room_name, users):
        self.room_name = room_name
        self.users = users
    def __hash__(self):
        return hash(self.room_name)
    def __eq__(self, other: str):
        if isinstance(other, ChatRoom):
            return self.room_name == other.room_name
        else:
            return self.room_name == other


# ユーザーリスト
user_list: List[str] = []

# メッセージを保存する辞書
message_dict: Dict[str, Dict[str, List[Message]]]= {}

# ユーザーを追加する
def add_user(user_id):
    # ユーザーIDが既に登録されているかチェック

    #ここuser_listはsetのほうがいいかもだな(早い)
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
    user1 = user_list[user_list.index(from_id)]
    user2 = user_list[user_list.index(to_id)]
    if from_id == to_id:
        return "Error: same user refered"
    elif to_id in user_list and isinstance(user_list[user_list.index(to_id)], ChatRoom):
        #id_2がchatroomの場合
        chatroom = user_list[user_list.index(to_id)]
        if from_id not in chatroom.users:
            return "Error: not in room"
        message = Message(from_id, to_id, content, time.time())
        # メッセージの保存
        if to_id not in message_dict[from_id]:
            message_dict[from_id][to_id] = [message]
        else:
            message_dict[from_id][to_id].append(message)

        return ""
    
    elif isinstance(user1, UserWithCredit) and isinstance(user1, UserWithCredit):
        if user1.user_type == "D" and user1.credit == 0: return "Error: not enough credit"

        # メッセージを作成
        message = Message(from_id, to_id, content, time.time())

        # メッセージの保存
        if to_id not in message_dict[from_id]:
            message_dict[from_id][to_id] = [message]
        else:
            message_dict[from_id][to_id].append(message)
        if user1.user_type == "D" and user2.user_type == "J":
            user1.credit -= 1.
            user2.credit += 1.

        return ""

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
        # add_user adam
        # add_user eve
        # talk adam eve hi
        # show_log adam eve だとエラーを吐くが, 伝え損ねたため手直し
        try:
            msg_list1 = message_dict[id_1][id_2]
        except:
            msg_list1 = []
        try:
            msg_list2 = message_dict[id_2][id_1]
        except:
            msg_list2 = []
        msg_list_all = msg_list1 + msg_list2

        # メッセージの時刻でソート
        msg_list_all.sort(key=lambda x: x.time)

        # メッセージの取得
        return "\n".join([msg.getMessage() for msg in msg_list_all])

def create_room(room_name, users):
    if room_name in user_list:
        return "ERROR: ID already used!"
    for user in users:
        if user not in user_list:
            return "ERROR: no user ID"
    chatroom = ChatRoom(room_name, users)
    user_list.append(chatroom)
    return ""

def show_room_log(room_name):
    if room_name not in user_list:
        return "ERROR: no room"
    messages = []
    for key in message_dict:
        try:
            messages += message_dict[key][room_name]
        except:
            continue
    messages.sort(key=lambda x: x.time)
     # メッセージの取得
    return "\n".join([msg.getMessage() for msg in messages])

class UserWithCredit:
    def __init__(self, user_name: str, user_type: str):
        self.user_name = user_name
        self.user_type = user_type
        self.credit = 0
    def __hash__(self):
        return hash(self.user_name)
    def __eq__(self, other: str):
        if isinstance(other, UserWithCredit):
            return self.user_name == other.user_name
        else:
            return self.user_name == other

def add_user_with_credit(user_id, user_type):
    if user_id in user_list:
        return "ERROR: ID already used!"
    else:
        # 登録されていなかったらユーザーリストに追加
        user = UserWithCredit(user_id, user_type)
        user_list.append(user)
        # メッセージを保存する辞書に追加
        message_dict[user_id] = {}
        return "{} registered!".format(user_id)

def add_credit(user_id, amount):
    if user_id not in user_list:
        return "ERROR: no user ID"
    amount = float(amount)
    user: UserWithCredit = user_list[user_list.index(user_id)]
    if isinstance(user, UserWithCredit) and user.user_type == "J":
        return "Error: wrong type"
    if amount > 0 and isinstance(user, UserWithCredit):
        user.credit += amount
        return ""
    return ""

def show_credit(user_id):
    if user_id not in user_list:
        return "ERROR: no user ID"
    user: UserWithCredit = user_list[user_list.index(user_id)]
    if isinstance(user, UserWithCredit) and user.user_type == "D":
        return f"{user.credit} remaining"
    elif isinstance(user, UserWithCredit) and user.user_type == "J":
        return f"{user.credit} earned"
    return ""

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
            
            elif cmd[0] == "add_user" and len(cmd) == 3:
                res = add_user_with_credit(cmd[1], cmd[2])
            
            elif cmd[0] == "add_credit" and len(cmd) == 3:
                res = add_credit(cmd[1], cmd[2])
            
            elif cmd[0] == "show_credit" and len(cmd) == 2:
                res = show_credit(cmd[1])
            # talk コマンド
            elif cmd[0] == "talk" and len(cmd) == 4:
                res = talk(cmd[1], cmd[2], cmd[3])

            # show_log コマンド
            elif cmd[0] == "show_log" and len(cmd) == 3:
                res = show_log(cmd[1], cmd[2])
            
            elif cmd[0] == "show_log" and len(cmd) == 2:
                res = show_room_log(cmd[1])

            elif cmd[0] == "create_room":
                room_name = cmd[1]
                users = cmd[2:]
                res = create_room(room_name, users)

            # 標準出力に返答
            if res != "":
                print("OUTPUT: {}".format(res))

        except EOFError:
            # Ctrl + D で終了
            break

if __name__ == "__main__":
    main()
