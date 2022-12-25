import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message

import firebase_admin
from firebase_admin import credentials,firestore

cred = credentials.Certificate("/etc/secrets/serviceAccount.json")
# cred = credentials.Certificate("serviceAccount.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


load_dotenv()


machine = TocMachine(
    states=["idle", "lobby", "introduction","placeOrder","searchOrder","deliveryMethod","chooseItem","deliveryAddress","checkAddress",
        "boxPotato","sharePotato","heavyPotato","lightPotato","addOther","checkItem","aboutUs","contactUs","copyPhone","copyAddress","inputName",
        "checkName","inputPhone","checkPhone","inputPayMethod","checkFinalOrder","finishOrder","chooseDate","modifyOrder","showOrder","valid"
        ,"changeState"],
    transitions=[
        {
            "trigger": "advance","source": "idle","dest": "lobby","conditions": "is_going_to_lobby",
        },
        {
            "trigger": "advance","source": "lobby","dest": "introduction","conditions": "is_going_to_introduction",
        },
        {
            "trigger": "advance","source": "lobby","dest": "placeOrder","conditions": "is_going_to_placeOrder",
        },
        {
            "trigger": "advance","source": "lobby","dest": "searchOrder","conditions": "is_going_to_searchOrder",
        },
        {
            "trigger": "advance","source": "lobby","dest": "valid","conditions": "is_going_to_valid",
        },
        {
            "trigger": "advance","source": "valid","dest": "changeState","conditions": "is_going_to_changeState",
        },
        {
            "trigger": "advance","source": "changeState","dest": "changeState","conditions": "is_going_to_changeState",
        },
        {
            "trigger": "advance","source": "placeOrder","dest": "deliveryMethod","conditions": "is_going_to_deliveryMethod",
        },
        {
            "trigger": "advance","source": "deliveryMethod","dest": "deliveryAddress","conditions": "is_going_to_deliveryAddress",
        },
        {
            "trigger": "advance","source": "deliveryMethod","dest": "chooseDate","conditions": "is_going_to_chooseDate",
        },
        {
            "trigger": "advance","source": "chooseDate","dest": "chooseItem","conditions": "is_going_to_chooseItem2",
        },
        {
            "trigger": "advance","source": "chooseDate","dest": "checkFinalOrder","conditions": "is_going_to_returnCheck",
        },
        {
            "trigger": "advance","source": "deliveryAddress","dest": "checkAddress","conditions": "is_going_to_checkAddress",
        },
        {
            "trigger": "advance","source": "checkAddress","dest": "chooseItem","conditions": "is_going_to_chooseItem1",
        },
        {
            "trigger": "advance","source": "checkAddress","dest": "deliveryAddress","conditions": "is_going_to_deliveryAddress",
        },
        {
            "trigger": "advance","source": "checkAddress","dest": "checkFinalOrder","conditions": "is_going_to_returnCheck",
        },
        {
            "trigger": "advance","source": "chooseItem","dest": "boxPotato","conditions": "is_going_to_boxPotato",
        },
        {
            "trigger": "advance","source": "chooseItem","dest": "sharePotato","conditions": "is_going_to_sharePotato",
        },
        {
            "trigger": "advance","source": "chooseItem","dest": "heavyPotato","conditions": "is_going_to_heavyPotato",
        },
        {
            "trigger": "advance","source": "chooseItem","dest": "lightPotato","conditions": "is_going_to_lightPotato",
        },
        {
            "trigger": "advance","source": "boxPotato","dest": "addOther","conditions": "is_going_to_addOther",
        },
        {
            "trigger": "advance","source": "sharePotato","dest": "addOther","conditions": "is_going_to_addOther",
        },
        {
            "trigger": "advance","source": "lightPotato","dest": "addOther","conditions": "is_going_to_addOther",
        },
        {
            "trigger": "advance","source": "heavyPotato","dest": "addOther","conditions": "is_going_to_addOther",
        },
        {
            "trigger": "advance","source": "addOther","dest": "boxPotato","conditions": "is_going_to_boxPotato",
        },
        {
            "trigger": "advance","source": "addOther","dest": "sharePotato","conditions": "is_going_to_sharePotato",
        },
        {
            "trigger": "advance","source": "addOther","dest": "heavyPotato","conditions": "is_going_to_heavyPotato",
        },
        {
            "trigger": "advance","source": "addOther","dest": "lightPotato","conditions": "is_going_to_lightPotato",
        },
        {
            "trigger": "advance","source": "addOther","dest": "checkItem","conditions": "is_going_to_checkItem",
        },
        {
            "trigger": "advance","source": "introduction","dest": "placeOrder","conditions": "is_going_to_placeOrder",
        },
        {
            "trigger": "advance","source": "introduction","dest": "lobby","conditions": "is_going_to_lobby",
        },
        {
            "trigger": "advance","source": "lobby","dest": "contactUs","conditions": "is_going_to_contactUs",
        },
        {
            "trigger": "advance","source": "lobby","dest": "aboutUs","conditions": "is_going_to_aboutUs",
        },
        {
            "trigger": "advance","source": "contactUs","dest": "copyPhone","conditions": "is_going_to_copyPhone",
        },
        {
            "trigger": "advance","source": "contactUs","dest": "copyAddress","conditions": "is_going_to_copyAddress",
        },
        {
            "trigger": "advance","source": "contactUs","dest": "lobby","conditions": "is_going_to_lobby",
        },
        {
            "trigger": "advance","source": "contactUs","dest": "idle","conditions": "is_going_to_idle",
        },
        {
            "trigger": "advance","source": "checkItem","dest": "addOther","conditions": "is_going_to_addOther",
        },
        {
            "trigger": "advance","source": "checkItem","dest": "inputName","conditions": "is_going_to_inputName",
        },
        {
            "trigger": "advance","source": "checkItem","dest": "checkFinalOrder","conditions": "is_going_to_returnCheck",
        },
        {
            "trigger": "advance","source": "inputName","dest": "checkName","conditions": "is_going_to_checkName",
        },
        {
            "trigger": "advance","source": "checkName","dest": "inputPhone","conditions": "is_going_to_inputPhone",
        },
        {
            "trigger": "advance","source": "checkName","dest": "inputName","conditions": "is_going_to_inputName",
        },
        {
            "trigger": "advance","source": "inputPhone","dest": "checkPhone","conditions": "is_going_to_checkPhone",
        },
        {
            "trigger": "advance","source": "checkPhone","dest": "inputPayMethod","conditions": "is_going_to_inputPayMethod",
        },
        {
            "trigger": "advance","source": "checkPhone","dest": "inputPhone","conditions": "is_going_to_inputPhone",
        },
        {
            "trigger": "advance","source": "checkPhone","dest": "checkFinalOrder","conditions": "is_going_to_returnCheck",
        },
        {
            "trigger": "advance","source": "inputPayMethod","dest": "checkFinalOrder","conditions": "is_going_to_checkFinalOrder",
        },
        {
            "trigger": "advance","source": "checkFinalOrder","dest": "finishOrder","conditions": "is_going_to_finishOrder",
        },
        {
            "trigger": "advance","source": "checkFinalOrder","dest": "modifyOrder","conditions": "is_going_to_modifyOrder",
        },
        {
            "trigger": "advance","source": "modifyOrder","dest": "inputName","conditions": "is_going_to_changeInfo",
        },
        {
            "trigger": "advance","source": "modifyOrder","dest": "inputPayMethod","conditions": "is_going_to_changePayMethod",
        },
        {
            "trigger": "advance","source": "modifyOrder","dest": "deliveryMethod","conditions": "is_going_to_changeDeliveryMethod",
        },
        {
            "trigger": "advance","source": "modifyOrder","dest": "addOther","conditions": "is_going_to_changeItems",
        },
        {
            "trigger": "advance","source": "finishOrder","dest": "lobby","conditions": "is_going_to_lobby",
        },
        {
            "trigger": "advance","source": "aboutUs","dest": "lobby","conditions": "is_going_to_lobby",
        },
        {
            "trigger": "advance","source": "searchOrder","dest": "showOrder","conditions": "is_going_to_showOrder",
        },
        {
            "trigger": "advance","source": "showOrder","dest": "lobby","conditions": "is_going_to_lobby",
        },
        {
            "trigger": "advance","source": "showOrder","dest": "searchOrder","conditions": "is_going_to_searchOrder",
        },
        {
            "trigger": "advance",
            "source": ["placeOrder","deliveryMethod","deliveryAddress","checkAddress","chooseItem","boxPotato",
                "sharePotato","heavyPotato","lightPotato","checkItem","addOther","inputName","checkName","inputPhone",
                "checkPhone","checkFinalOrder","chooseDate","modifyOrder"],
            "dest": "lobby",
            "conditions": "is_going_to_cancelOrder",
        },
        # {
        #     "trigger": "go_back", 
        #     "source": ["cancelOrder"], 
        #     "dest": "lobby",
        #     # "conditions": "is_going_to_user",
        # },
        {
            "trigger": "advance", "source": "lobby", "dest": "idle","conditions": "is_going_to_idle",
        },
        {
            "trigger": "go_back",
            "source": ["copyPhone","copyAddress"], 
            "dest": "contactUs",
        },
        {
            "trigger": "go_back",
            "source": ["valid","changeState"],
            "dest": "lobby",
        },
    ],
    initial="idle",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
# channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
# channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)

'''
@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"
'''

@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        dbState = db.collection('UserState').document(event.source.user_id)
        # dbState.set({
        #     'state' : 'idle',
        # })
        doc = dbState.get()
        if doc.exists:
            global preState
            machine.state = doc.to_dict()['state']
            preState = machine.state
        else:
            preState = "idle"
            machine.state = 'idle'
            dbState.set({
                'state' : 'idle',
                'deliveryMethod' : 0, # 0 自取 1 宅配
                'address' : '',
                'box' : 0,
                'heavy' : 0,
                'light' : 0,
                'share' : 0,
                'name' : '',
                'phone' : '',
                'totalMoney' : 0,
                'payMethod': 0, # 0 現金 1 轉帳
                'deliveryFee' : 0,
                'productMoney' : 0,
                'takeDate' : 0, # 0 星期六 1 星期日 
                'orderMode' : 0 # 0 ordering 1 final order
            })
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")

        response = machine.advance(event,dbState)
        
        if preState != machine.state:
            dbState.update({
                'state': machine.state,
            })

        # if response == False:
        #     send_text_message(event.reply_token, "請輸入正確指令\n如需啟動Line Bot\n請輸入「主選單」")

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
