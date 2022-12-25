import os

from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ButtonsTemplate, MessageTemplateAction, CarouselColumn, CarouselContainer, CarouselTemplate, ImageCarouselColumn, ConfirmTemplate, MessageAction, LocationMessage, ImageSendMessage


# channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)

channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)


def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"
'''
def showMenu(reply_token):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TemplateSendMessage(
            alt_text='Button template',
            template=ButtonsTemplate(
                title='歡迎光臨癸屋的甕烤地瓜',
                text='請選擇服務項目',
                actions=[
                    MessageTemplateAction(
                        label = '產品介紹',
                        text='@產品介紹'
                    ),
                    MessageTemplateAction(
                        label = '產品訂購',
                        text='@產品訂購'
                    ),
                    MessageTemplateAction(
                        label = '訂單查詢',
                        text='@訂單查詢'
                    ),
                    
                    MessageTemplateAction(
                        label = '離開',
                        text='@離開'
                    ),
                ]
            )
        )
    )
'''

def showMenu(reply_token):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token,TemplateSendMessage(
        alt_text='主選單',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    title="關於癸屋",
                    text = "獲取癸屋的相關資訊",
                    actions=[
                        MessageTemplateAction(
                            label="產品介紹",
                            text='@產品介紹',
                        ),
                        MessageTemplateAction(
                            label="關於我們",
                            text='@關於我們',
                        ),
                    ]
                ),
                CarouselColumn(
                    title="訂單資訊",
                    text = "您可以在此下訂或查詢訂單",
                    actions=[
                        MessageTemplateAction(
                            label="產品訂購",
                            text='@產品訂購',
                        ),
                        MessageTemplateAction(
                            label="訂單查詢",
                            text='@訂單查詢',
                        ),

                    ]
                ),
                CarouselColumn(
                    title="其他",
                    text = "請選擇您需要的服務",
                    actions=[
                        MessageTemplateAction(
                            label="聯絡我們",
                            text='@聯絡我們',
                        ),
                        MessageTemplateAction(
                            label="離開商店",
                            text='@離開商店',
                        ),
                    ]
                ),
            ]
        )
    )
    )

def sayGoodbye(reply_token):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text="謝謝您的光臨\n期待與您再次相會\n有任何需要都可以輸入「主選單」呼叫我們喔！"))

def orderTip(reply_token):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, [
        TextSendMessage(
            text="親愛的顧客您好！\n歡迎使用Line訂購系統\n取貨方式可選則店面自取或宅配\n自取可選擇現金付款或轉帳\n宅配僅限轉帳\n過程中若想取消訂購\n可隨時輸入「@取消訂購」\n\n可訂購品項：\n盒裝地瓜 100元 （限自取）\n真空分享包 100元\n真空重量包 50元\n真空輕量包 35元\n\n訂購方式：\n先選擇您要的品名後\n待系統詢問數量時n再輸入數量即可\n（可參考附圖範例）\n到貨日期：\n如選擇店面自取\n請選擇當週的禮拜六或日\n宅配的到貨日皆為隔週二\n\n如有其他客製需求\n歡迎直接來電預訂"
        ),
        ImageSendMessage(original_content_url="https://i.imgur.com/OIqKvRF.jpg",preview_image_url="https://i.imgur.com/OIqKvRF.jpg"),
        TemplateSendMessage(
            alt_text='訂購系統',
            template=ButtonsTemplate(
                title='訂購須知',
                text='若已悉知訂購須知\n請選擇以下選項',
                actions=[
                    MessageTemplateAction(
                        label = '繼續訂購',
                        text='@繼續訂購'
                    ),
                    MessageTemplateAction(
                        label = '取消訂購',
                        text='@取消訂購'
                    ),
                ]
            )
        ),
    ]
    )

def deliveryMethod(reply_token):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, [
        TemplateSendMessage(
            alt_text='運送方式',
            template=ButtonsTemplate(
                title='運送方式',
                text='請選擇店面自取或宅配\n店面自取:台南市永康區大灣路129號之3\n宅配：運費200 滿3000免運',
                actions=[
                    MessageTemplateAction(
                        label = '店面自取',
                        text='@店面自取'
                    ),
                    MessageTemplateAction(
                        label = '黑貓宅配',
                        text='@黑貓宅配'
                    ),
                ]
            )
        ),
    ]
)

def chooseDate(reply_token):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, [
        TemplateSendMessage(
            alt_text='店面取貨日',
            template=ButtonsTemplate(
                title='店面取貨日',
                text="請選擇店面取貨日",
                actions=[
                    MessageTemplateAction(
                        label = '星期六',
                        text='@星期六'
                    ),
                    MessageTemplateAction(
                        label = '星期日',
                        text='@星期日'
                    ),
                ]
            )
        ),
    ]
)

def checkAddress(reply_token,address):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, [
        TemplateSendMessage(
            alt_text='地址確認',
            template=ButtonsTemplate(
                title='地址確認',
                text=address+"\n（若不符合寄送條件，將會取消訂單，敬請見諒）",
                actions=[
                    MessageTemplateAction(
                        label = '修改地址',
                        text='@修改地址'
                    ),
                    MessageTemplateAction(
                        label = '確認地址',
                        text='@確認地址'
                    ),
                ]
            )
        ),
    ]
)

def showItems(reply_token,showBox):
    line_bot_api = LineBotApi(channel_access_token)
    actions = []
    if showBox == 0:
        actions.append(
            MessageTemplateAction(
                label = '盒裝地瓜(限自取) 100元',
                text='@盒裝地瓜'
            )
        )
    actions.append(
        MessageTemplateAction(
            label = '真空分享包 100元',
            text='@真空分享包'
        )
    )
    actions.append(
        MessageTemplateAction(
            label = '真空重量包 50元',
            text='@真空重量包'
        )
    )
    actions.append(
        MessageTemplateAction(
            label = '真空輕量包 35元',
            text='@真空輕量包'
        )
    )
    line_bot_api.reply_message(reply_token, TemplateSendMessage(
            alt_text='選擇品項',
            template=ButtonsTemplate(
                title='選擇品項',
                text='請選擇欲訂購項目',
                actions= actions
            )
        )
    )

def showAddItems(reply_token,showBox):
    line_bot_api = LineBotApi(channel_access_token)
    actions = []
    if showBox == 0:
        actions.append(
            MessageTemplateAction(
                label = '盒裝地瓜(限自取) 100元',
                text='@盒裝地瓜'
            )
        )
    actions.append(
        MessageTemplateAction(
            label = '真空分享包 100元',
            text='@真空分享包'
        )
    )
    actions.append(
        MessageTemplateAction(
            label = '真空重量包 50元',
            text='@真空重量包'
        )
    )
    actions.append(
        MessageTemplateAction(
            label = '真空輕量包 35元',
            text='@真空輕量包'
        )
    )
    message = [
        TemplateSendMessage(
            alt_text='追加品項',
            template=ButtonsTemplate(
                title='追加品項',
                text='請選擇欲追加或修改項目\n（1、如欲刪除特定品項，請選擇後於數量輸入負數\n 2、如無欲追加項目，請點選「確認訂購」）',
                actions= actions
            )
        ), 
        TemplateSendMessage(
            alt_text='確認品項',
            template=ConfirmTemplate(
                text='確認品項',
                actions=[
                    MessageAction(
                        label='確認品項',
                        text='@確認品項'
                    ),
                    MessageAction(
                        label='取消訂購',
                        text='@取消訂購'
                    ),
                ]
            )
        ),
    ]
    line_bot_api.reply_message(reply_token, message)

def showIntroduction(reply_token):
    line_bot_api = LineBotApi(channel_access_token)
    
    line_bot_api.reply_message(reply_token,TemplateSendMessage(
        alt_text='產品介紹',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url="https://i.imgur.com/Vezkinj.jpg",
                    title="盒裝地瓜",
                    text = "100元 限自取",
                    actions=[
                        MessageTemplateAction(
                            label="立即訂購",
                            text='@立即訂購',
                        ),
                        MessageTemplateAction(
                            label="回主選單",
                            text='@回主選單',
                        ),
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url="https://i.imgur.com/Xiul85a.jpg",
                    title="真空分享包",
                    text = "100元 一個一個單顆裝",
                    actions=[
                        MessageTemplateAction(
                            label="立即訂購",
                            text='@立即訂購',
                        ),
                        MessageTemplateAction(
                            label="回主選單",
                            text='@回主選單',
                        ),

                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url="https://i.imgur.com/gMGFwL2.jpg",
                    title="真空重量包",
                    text = "50元 真空重量包",
                    actions=[
                        MessageTemplateAction(
                            label="立即訂購",
                            text='@立即訂購',
                        ),
                        MessageTemplateAction(
                            label="回主選單",
                            text='@回主選單',
                        ),
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url="https://i.imgur.com/f0094gz.jpg",
                    title="真空輕量包",
                    text = "35元 真空輕量包",
                    actions=[
                        MessageTemplateAction(
                            label="立即訂購",
                            text='@立即訂購',
                        ),
                        MessageTemplateAction(
                            label="回主選單",
                            text='@回主選單',
                        ),
                    ]
                ),
            ]
        )
    )
)

def contactUs(reply_token):
    line_bot_api = LineBotApi(channel_access_token)
    
    line_bot_api.reply_message(reply_token,TemplateSendMessage(
        alt_text='聯絡我們',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    title="店舖電話",
                    text = "請播打：0963-576-407",
                    actions=[
                        MessageTemplateAction(
                            label="複製電話",
                            text='@複製電話',
                        )
                    ]
                ),
                CarouselColumn(
                    title="店鋪地址",
                    text = "歡迎前往「台南市永康區大灣路129號之3」",
                    actions=[
                        MessageTemplateAction(
                            label="位置資訊",
                            text='@位置資訊',
                        ),

                    ]
                ),
                CarouselColumn(
                    title="線上客服",
                    text = "將會帶您離開商店\n直接留言即可\n人工客服將會在一個工作天內回覆您！\n感謝您的配合",
                    actions=[
                        MessageTemplateAction(
                            label="離開商店",
                            text='@離開商店',
                        ),
                    ]
                ),
                CarouselColumn(
                    title="回主選單",
                    text = "這裡沒有我要的資訊\n回主選單",
                    actions=[
                        MessageTemplateAction(
                            label="回主選單",
                            text='@回主選單',
                        ),
                    ]
                ),
            ]
        )
    )
    )


def inputNumber(reply_token,item):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage("請輸入您欲訂購的"+"「"+item+"」數量\n（如欲訂購五包，請直接輸入「5」（不用量詞））"))
    
def checkItem(reply_token,text,mode):
    line_bot_api = LineBotApi(channel_access_token)
    actions = []
    actions.append(MessageTemplateAction(
                        label = '修改品項',
                        text='@修改品項'
                    ))
    # texts = "如商品正確無誤 請點擊「繼續填寫訂購資訊」"
    if mode == 0:
        actions.append(MessageTemplateAction(
                        label = '繼續填寫訂購資訊',
                        text='@繼續填寫訂購資訊'
                    ))
    else:
        actions.append(MessageTemplateAction(
                        label = '回結帳頁',
                        text='@回結帳頁'
                    ))
    actions.append(MessageTemplateAction(
                        label = '取消訂購',
                        text='@取消釘購'
                    ))
    messages = [
        TextSendMessage(text),
        TemplateSendMessage(
            alt_text='確認品項',
            template=ButtonsTemplate(
                title='確認品項',
                text = "如商品正確無誤 請點選「繼續填寫訂購資訊」或「回結帳頁」",
                actions=actions,
            )
        ),
    ]
    line_bot_api.reply_message(reply_token,messages)

def checkName(reply_token,name):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, [
        TemplateSendMessage(
            alt_text='名字確認',
            template=ButtonsTemplate(
                title='名字確認',
                text="訂購者姓名 : "+name,
                actions=[
                    MessageTemplateAction(
                        label = '修改名字',
                        text='@修改名字'
                    ),
                    MessageTemplateAction(
                        label = '確認名字',
                        text='@確認名字'
                    ),
                ]
            )
        ),
    ]
)

def checkPhone(reply_token,phone):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, [
        TemplateSendMessage(
            alt_text='電話確認',
            template=ButtonsTemplate(
                title='電話確認',
                text="訂購者電話 : "+phone,
                actions=[
                    MessageTemplateAction(
                        label = '修改電話',
                        text='@修改電話'
                    ),
                    MessageTemplateAction(
                        label = '確認電話',
                        text='@確認電話'
                    ),
                ]
            )
        ),
    ]
)

def checkFinalOrder(reply_token,text):
    line_bot_api = LineBotApi(channel_access_token)
    messages = [
        TextMessage(text=text),
        TemplateSendMessage(
            alt_text='訂單確認',
            template=ButtonsTemplate(
                title='訂單確認',
                text="如正確無誤 請點擊完成訂購",
                actions=[
                    MessageTemplateAction(
                        label = '訂單修改',
                        text='@訂單修改'
                    ),
                    MessageTemplateAction(
                        label = '取消訂購',
                        text='@取消訂購'
                    ),
                    MessageTemplateAction(
                        label = '完成訂購',
                        text='@完成訂購'
                    ),
                ]
            )
        ),
    ]
    line_bot_api.reply_message(reply_token,messages)

def choosePayMethod(reply_token,deliveryMethod):
    line_bot_api = LineBotApi(channel_access_token)
    actions = []
    text = "請選擇付款方式\n宅配僅接受銀行轉帳\n造成您的不便\n敬請見諒"
    if deliveryMethod==0 :
        actions.append(MessageTemplateAction(
                        label = '現金支付',
                        text='@現金支付'
                    ))
        text = "請選擇付款方式\n"
    actions.append(MessageTemplateAction(
                        label = '銀行轉帳',
                        text='@銀行轉帳'
                    ))
    line_bot_api.reply_message(reply_token,TemplateSendMessage(
            alt_text='付款方式',
            template=ButtonsTemplate(
                title='付款方式',
                text=text,
                actions=actions,
            )
        ))

def finishOrder(reply_token,text,orderNum,push):
    line_bot_api = LineBotApi(channel_access_token)
    messages = [
        TextMessage(text=text),
        TemplateSendMessage(
            alt_text='完成訂購',
            template=ButtonsTemplate(
                title='完成訂購',
                text="感謝您的訂購！\n訂單已成功建立！\n訂單編號為："+str(orderNum)+"\n",
                actions=[
                    MessageTemplateAction(
                        label = '回主選單',
                        text='@回主選單'
                    ),
                ]
            )
        ),
    ]
    line_bot_api.reply_message(reply_token,messages)
    admin_uid = os.getenv("ADMIN_UID", None)
    line_bot_api.push_message(admin_uid,TextSendMessage(text=push))

def modifyOrder(reply_token):
    line_bot_api = LineBotApi(channel_access_token)
    text = "請選擇欲修改的項目"
    line_bot_api.reply_message(reply_token,TemplateSendMessage(
            alt_text='訂單修改',
            template=ButtonsTemplate(
                title='訂單修改',
                text=text,
                actions=[
                    MessageTemplateAction(
                        label = '修改訂購人資訊',
                        text='@修改訂購人資訊'
                    ),
                    MessageTemplateAction(
                        label = '修改取貨方式',
                        text='@修改取貨方式'
                    ),
                    MessageTemplateAction(
                        label = '修改付款方式',
                        text='@修改付款方式'
                    ),
                    MessageTemplateAction(
                        label = '修改商品品項',
                        text='@修改商品品項'
                    ),
                ],
            )
        ))

def sendLocation(reply_token):
    line_bot_api = LineBotApi(channel_access_token)
    text = "請選擇欲修改的項目"
    line_bot_api.reply_message(reply_token,LocationMessage(
        title= "癸屋的甕烤地瓜",
        address="台南市永康區大灣路129號之3",
        latitude=23.009565,
        longitude=120.269361,
    ))

def sendAboutUs(reply_token):
    line_bot_api = LineBotApi(channel_access_token)
    messages = [
        TextSendMessage('我們是位在大灣國聖宮旁的一間甕烤地瓜\n地瓜盛產時就會發現我們的蹤影\n但每日限量出爐\n因此想吃的朋友要儘早預定或來現場碰碰運氣\n我們也即將於2023年1月開始新一輪的販售囉！\n營業時間也更動為六日的10:00到賣完為止\n歡迎各位蒞臨～\n以下是我們的DM'),
        ImageSendMessage(original_content_url="https://i.imgur.com/k7ud90X.jpg",preview_image_url="https://i.imgur.com/k7ud90X.jpg"),
        TextSendMessage('您可輸入「主選單」返回主選單'),
    ]
    line_bot_api.reply_message(reply_token,messages)

def showOrder(reply_token,text):
    line_bot_api = LineBotApi(channel_access_token)
    messages = [
        TextSendMessage(text=text),
        TemplateSendMessage(
            alt_text='查詢訂單',
            template=ButtonsTemplate(
                title='查詢訂單',
                text="如需修改訂單或有其他疑慮\n請播打客服專線：0988-888-888",
                actions=[
                    MessageTemplateAction(
                        label = '查詢下一筆資料',
                        text='@查詢下一筆資料'
                    ),
                    MessageTemplateAction(
                        label = '回主選單',
                        text='@回主選單'
                    ),
                ],
            )
        )
    ]
    line_bot_api.reply_message(reply_token,messages)
"""
def send_image_url(id, img_url):
    pass

def send_button_message(id, text, buttons):
    pass
"""
