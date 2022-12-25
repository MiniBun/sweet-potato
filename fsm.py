from transitions.extensions import GraphMachine

# from utils import send_text_message, showMenu
import os
import pygsheets
import utils
from oauth2client.service_account import ServiceAccountCredentials as SAC
import firebase_admin
from firebase_admin import credentials,firestore

# gc = pygsheets.authorize(service_file='/etc/secrets/sweet-potato-370214-3b8a193390de.json')
# gc = pygsheets.authorize(service_file='sweet-potato-370214-3b8a193390de.json')
            

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
#         try:
#             sht = gc.open_by_url(
# 'https://docs.google.com/spreadsheets/d/1C6YSY1vgW4abK3XNLDIKPlRGW_YSn1MnleNX9f3pw0Y/edit?usp=sharing'
# )
#             print("Yes!")
#             wks = sht[0]
#         except:
#             print("No!")

    #template
    '''
    def is_going_to_lobby(self,event):
        text = event.message.text
        return text == "主選單"

    def on_enter_lobby(self,event):
        print("Go to lobby!")
        reply_token = event.reply_token
        utils.showMenu(reply_token)
    
    def on_exit_state1(self):
        print("Leaving state1")

    '''

    def is_going_to_lobby(self,event,doc):
        text = event.message.text
        return text == "主選單" or text == "@回主選單"

    def on_enter_lobby(self,event,doc):
        print("Go to lobby!")
        reply_token = event.reply_token
        utils.showMenu(reply_token)
    
    def is_going_to_idle(self, event,doc):
        text = event.message.text
        return text == "@離開商店"

    def on_exit_state1(self,event,doc):
        print("Go to idle!")
        reply_token = event.reply_token
        utils.sayGoodbye(reply_token)
        return True

    def on_enter_idle(self,event,doc):
        print("Go to idle!")
        reply_token = event.reply_token
        utils.sayGoodbye(reply_token)
    
    def is_going_to_introduction(self,event,doc):
        text = event.message.text
        return text == "@產品介紹"

    def on_enter_introduction(self,event,doc):
        print("Go to introduction!")
        reply_token = event.reply_token
        utils.showMenu(reply_token)

    def is_going_to_placeOrder(self,event,doc):
        text = event.message.text
        return text == "@產品訂購" or text == "@立即訂購"

    def on_enter_placeOrder(self,event,doc):
        print("Go to placeOrder!")
        doc.update({
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
                'orderMode' : 0,
                'takeDate' : 0,
            })
        reply_token = event.reply_token
        utils.orderTip(reply_token)
    
    def is_going_to_deliveryMethod(self,event,doc):
        text = event.message.text
        ref = doc.get().to_dict()
        if ref['orderMode'] == 0 and text == "@繼續訂購":
            return True
        elif ref['orderMode'] == 1 and text == "@修改付款方式":
            return True
        return False
        

    def on_enter_deliveryMethod(self,event,doc):
        print("Go to deliveryMethod!")
        reply_token = event.reply_token
        utils.deliveryMethod(reply_token)
    

    def is_going_to_searchOrder(self,event,doc):
        text = event.message.text
        return text == "@訂單查詢" or text == '@查詢下一筆資料'

    def on_enter_searchOrder(self,event,doc):
        print("Go to searchOrder!")
        reply_token = event.reply_token
        utils.send_text_message(reply_token,"請輸入訂單編號")

    def is_going_to_deliveryAddress(self,event,doc):
        text = event.message.text
        if text == "@黑貓宅配" or text == "@修改地址":
            if text == "@黑貓宅配":
                doc.update({
                    'deliveryMethod' : 1,
                    'box' : 0
                })
            return True
        return False 

    def on_enter_deliveryAddress(self,event,doc):
        print("Go to deliveryAddress!")
        reply_token = event.reply_token
        utils.send_text_message(reply_token,"請輸入欲宅配地址\n（目前僅接受寄送台灣本島）")

    def is_going_to_checkAddress(self,event,doc):
        return True

    def on_enter_checkAddress(self,event,doc):
        print("Go to checkAddress!")
        text = event.message.text
        doc.update({
            'address' : text
        })
        reply_token = event.reply_token
        utils.checkAddress(reply_token,text)

    def is_going_to_chooseItem1(self,event,doc):
        text = event.message.text
        if doc.get().to_dict()['orderMode']==0 and text == "@確認地址":
            return True
        return False

    def is_going_to_chooseItem2(self,event,doc):
        text = event.message.text
        if doc.get().to_dict()['orderMode'] == 0:
            if text == "@星期六":
                doc.update({'takeDate' : 0})
                return True
            elif text == "@星期日":
                doc.update({'takeDate' : 1})
                return True
        return False

    def on_enter_chooseItem(self,event,doc):
        print("Go to chooseItem!")
        reply_token = event.reply_token
        showBox = doc.get().to_dict()['deliveryMethod']
        utils.showItems(reply_token,showBox)

    def is_going_to_cancelOrder(self,event,doc):
        text = event.message.text
        return text == "@取消訂購"

    def on_enter_cancelOrder(self,event,doc):
        print("Go to cancelOrder!")
        self.go_back(event,doc)

    def on_exit_cancelOrder(self,event,doc):
        print("Exit cancelOrder!")
    
    def is_going_to_boxPotato(self,event,doc):
        text = event.message.text
        if text == "@盒裝地瓜":
            return True
        return False

    def on_enter_boxPotato(self,event,doc):
        print("Go to boxPotato!")
        reply_token = event.reply_token 
        utils.inputNumber(reply_token,"盒裝地瓜")    
    
    def is_going_to_sharePotato(self,event,doc):
        text = event.message.text
        if text == "@真空分享包":
            return True
        return False

    def on_enter_sharePotato(self,event,doc):
        print("Go to sharePotato!")
        reply_token = event.reply_token 
        utils.inputNumber(reply_token,"真空分享包")  
    
    def is_going_to_heavyPotato(self,event,doc):
        text = event.message.text
        if text == "@真空重量包":
            return True
        return False

    def on_enter_heavyPotato(self,event,doc):
        print("Go to heavyPotato!")
        reply_token = event.reply_token 
        utils.inputNumber(reply_token,"真空重量包")    

    def is_going_to_checkItem(self,event,doc):
        text = event.message.text
        if text == "@確認品項":
            numberList = doc.get()
            boxNum = numberList.to_dict()['box']
            heavyNum = numberList.to_dict()['heavy']
            lightNum = numberList.to_dict()['light']
            shareNum = numberList.to_dict()['share']
            if boxNum == 0 and heavyNum == 0 and lightNum == 0 and shareNum == 0 :
                reply_token = event.reply_token
                utils.send_text_message(reply_token,'目前無任何訂購品項')
                return False
            else:
                money = 0
                buyList = '訂單明細：\n'
                deliveryMethod = numberList.to_dict()['deliveryMethod']
                if deliveryMethod == 0:
                    buyList = buyList + '運送方式：店面自取\n'
                    takeDate = numberList.to_dict()['takeDate']
                    if takeDate == 0:
                        buyList = buyList + '取貨日：星期六\n----------\n'
                    else:
                        buyList = buyList + '取貨日：星期日\n----------\n'
                else:
                    address = numberList.to_dict()['address']
                    buyList = buyList + '運送方式：黑貓宅配\n地址 ： '+ address + '\n----------\n'
                if boxNum > 0 :
                    buyList = buyList + '盒裝地瓜 ' + str(boxNum) + ' 盒\n'
                    money += 100*boxNum
                if shareNum > 0 :
                    buyList = buyList + '真空分享包 ' + str(shareNum) + ' 包\n'
                    money += 100*shareNum
                if heavyNum > 0 :
                    buyList = buyList + '真空重量包 ' + str(heavyNum) + ' 包\n'
                    money += 50*heavyNum
                if lightNum > 0 :
                    buyList = buyList + '真空輕量包 ' + str(lightNum) + ' 包\n'
                    money += 35*lightNum
                buyList = buyList+'----------\n'+'總計 ' + str(money) + ' 元'
                reply_token = event.reply_token
                utils.checkItem(reply_token,buyList,numberList.to_dict()["orderMode"])
            return True
        return False

    def on_enter_checkItem(self,event,doc):
        print("Go to checkItem!")

    def is_going_to_lightPotato(self,event,doc):
        text = event.message.text
        if text == "@真空輕量包":
            return True
        return False

    def on_enter_lightPotato(self,event,doc):
        print("Go to lightPotato!")
        reply_token = event.reply_token 
        utils.inputNumber(reply_token,"真空輕量包")    

    def is_going_to_addOther(self,event,doc):
        orederDetailed = doc.get()
        text = event.message.text
        if orederDetailed.to_dict()['state'] == 'checkItem' and text == '@修改品項':
            return True
        elif orederDetailed.to_dict()['orderMode'] == 1 and text == "@修改商品品項":
            return True
        try:
            status = float(text).is_integer()
            if status == False:
                return False
            else:
                number = int(text)
                state = orederDetailed.to_dict()['state']
                
                if state == 'boxPotato':
                    orderedNum = orederDetailed.to_dict()['box']
                    if orderedNum + number >= 0 :
                        doc.update({
                            'box' : orderedNum + number
                        })
                    else:
                        reply_token = event.reply_token
                        utils.send_text_message(reply_token,'無足夠數量\n請重新輸入')
                        return False
                elif state == 'heavyPotato':
                    orderedNum = orederDetailed.to_dict()['heavy']
                    if orderedNum + number >= 0 :
                        doc.update({
                            'heavy' : orderedNum + number
                        })
                    else:
                        reply_token = event.reply_token
                        utils.send_text_message(reply_token,'無足夠數量\n請重新輸入')
                        return False
                elif state == 'lightPotato':
                        orderedNum = orederDetailed.to_dict()['light']
                        if orderedNum + number >= 0 :
                            doc.update({
                                'light' : orderedNum + number
                            })
                        else:
                            reply_token = event.reply_token
                            utils.send_text_message(reply_token,'無足夠數量\n請重新輸入')
                            return False
                elif state == 'sharePotato':
                    orderedNum = orederDetailed.to_dict()['share']
                    if orderedNum + number >= 0 :
                        doc.update({
                            'share' : orderedNum + number
                        })
                    else:
                        reply_token = event.reply_token
                        utils.send_text_message(reply_token,'無足夠數量\n請重新輸入')
                        return False

                return True
        except:
            return False
        return False

    def on_enter_addOther(self,event,doc):
        print("Go to addOther!")
        reply_token = event.reply_token
        showBox = doc.get().to_dict()['deliveryMethod']
        utils.showAddItems(reply_token,showBox)

    def is_going_to_introduction(self,event,doc):
        text = event.message.text
        if text == "@產品介紹":
            return True
        return False

    def on_enter_introduction(self,event,doc):
        print("Go to introduction!")
        reply_token = event.reply_token 
        utils.showIntroduction(reply_token)

    def is_going_to_contactUs(self,event,doc):
        text = event.message.text
        if text == "@聯絡我們":
            reply_token = event.reply_token
            utils.contactUs(reply_token)
            return True
        return False
    
    def on_enter_contactUs(self,event,doc):
        print("Go to contactUs!")
        

    def is_going_to_copyPhone(self,event,doc):
        text = event.message.text
        if text == "@複製電話":
            return True
        return False

    def on_enter_copyPhone(self,event,doc):
        print("Go to copyPhone!")
        reply_token = event.reply_token
        utils.send_text_message(reply_token,'0963576407')
        self.go_back(event,doc)

    def is_going_to_copyAddress(self,event,doc):
        text = event.message.text
        if text == "@位置資訊":
            return True
        return False

    def on_enter_copyAddress(self,event,doc):
        print("Go to copyAddress!")
        reply_token = event.reply_token
        utils.sendLocation(reply_token)
        self.go_back(event,doc)

    def is_going_to_aboutUs(self,event,doc):
        text = event.message.text
        if text == "@關於我們":
            return True
        return False
    
    def on_enter_aboutUs(self,event,doc):
        print("Go to aboutUs!")
        reply_token = event.reply_token
        utils.sendAboutUs(reply_token)

    def is_going_to_inputName(self,event,doc):
        text = event.message.text
        ref = doc.get().to_dict()
        if ref['orderMode'] == 0 and text == '@繼續填寫訂購資訊':
            return True
        elif ref['state'] == "checkName" and text == "@修改名字":
            return True 
        elif ref['orderMode'] == 1 and text == "@修改訂購人資訊":
            return True
        return False
    
    def on_enter_inputName(self,event,doc):
        print("Go to inputName!")
        reply_token = event.reply_token
        utils.send_text_message(reply_token,'請輸入訂購者姓名\n如填寫非法資料\n則會被取消訂單')

    def is_going_to_checkName(self,event,doc):
        return True
    
    def on_enter_checkName(self,event,doc):
        print("Go to checkName!")
        name = event.message.text
        doc.update({
            'name' : name
        })
        reply_token = event.reply_token
        utils.checkName(reply_token,name)

    def is_going_to_inputPhone(self,event,doc):
        text = event.message.text
        if text == '@確認名字' or text == '@修改電話':
            return True
        return False
    
    def on_enter_inputPhone(self,event,doc):
        print("Go to inputPhone!")
        reply_token = event.reply_token
        utils.send_text_message(reply_token,'請輸入訂購者電話\n如填寫非法資料\n則會被取消訂單')

    def is_going_to_checkPhone(self,event,doc):
        return True
    
    def on_enter_checkPhone(self,event,doc):
        print("Go to checkPhone!")
        phone = event.message.text
        doc.update({
            'phone' : phone
        })
        reply_token = event.reply_token
        utils.checkPhone(reply_token,phone)

    def is_going_to_inputPayMethod(self,event,doc):
        text = event.message.text
        if doc.get().to_dict()['orderMode'] == 0 and text == '@確認電話':
            return True
        elif doc.get().to_dict()['orderMode'] == 1 and text == "@修改付款方式":
            return True
        return False
    
    def on_enter_inputPayMethod(self,event,doc):
        print("Go to inputPayMethod!")
        reply_token = event.reply_token
        deliveryMethod = doc.get().to_dict()['deliveryMethod']
        utils.choosePayMethod(reply_token,deliveryMethod)

    def is_going_to_checkFinalOrder(self,event,doc):
        paymethod = event.message.text
        if paymethod == '@現金支付' :
            doc.update({
                'payMethod' : 0,
                'orderMode' : 1,
            })
            return True
        if paymethod == '@銀行轉帳' :
            doc.update({
                'payMethod' : 1,
                'orderMode' : 1,
            })
            return True
        return False

    def is_going_to_returnCheck(self,event,doc):
        ref = doc.get().to_dict()
        text = event.message.text
        if ref["orderMode"] == 1 and ref["state"] == "chooseDate":
            if text == "@星期六":
                doc.update({'takeDate' : 0})
                return True
            elif text == "@星期日":
                doc.update({'takeDate' : 1})
                return True
            else:
                return False
        elif ref["orderMode"] == 1 and ref["state"] == "checkPhone":
            if text == "@確認電話":
                return True
            else:
                return False
        elif ref["orderMode"] == 1 and ref["state"] == "checkAddress":
            if text == "@確認地址":
                return True
            else:
                return False
        elif ref["orderMode"] == 1 and ref["state"] == "checkItem":
            if text == "@回結帳頁":
                return True
            else:
                return False
        return False
        


    def on_enter_checkFinalOrder(self,event,doc):
        print("Go to checkFinalOrder!")
        detailedList = doc.get()
        text = '訂單確認：\n'
        text += '訂購者姓名：' + detailedList.to_dict()['name'] + '\n'
        text += '訂購者電話：' + detailedList.to_dict()['phone'] + '\n'
        if detailedList.to_dict()['deliveryMethod'] == 0:
            text += '取貨方式：店鋪自取\n'
            takeDate = detailedList.to_dict()['takeDate']
            if takeDate == 0:
                text += '取貨日：星期六\n'
            else:
                text += '取貨日：星期日\n'
        else:
            text += '取貨方式：黑貓宅配\n'
            text += '宅配地址：'+ detailedList.to_dict()['address'] + '\n'
        if detailedList.to_dict()['payMethod'] == 0:
            text += '付款方式：現金支付\n'
        else:
            text += '付款方式：銀行轉帳\n'
        text += '---------------\n'
        productMoney = 0
        if detailedList.to_dict()['box'] > 0:
            num = detailedList.to_dict()['box']
            text += '盒裝地瓜 ' + str(num) + '盒 共' + str(num*100) + '元\n'
            productMoney += num*100
        if detailedList.to_dict()['share'] > 0:
            num = detailedList.to_dict()['share']
            text += '真空分享包 ' + str(num) + '包 共' + str(num*100) + '元\n'
            productMoney += num*100
        if detailedList.to_dict()['heavy'] > 0:
            num = detailedList.to_dict()['heavy']
            text += '真空重量包 ' + str(num) + '包 共' + str(num*50) + '元\n'
            productMoney += num*50
        if detailedList.to_dict()['light'] > 0:
            num = detailedList.to_dict()['light']
            text += '真空輕量包 ' + str(num) + '包 共' + str(num*35) + '元\n'
            productMoney += num*35
        deliveryFee = 200
        if productMoney >= 3000 or detailedList.to_dict()['deliveryMethod'] == 0:
            deliveryFee = 0
        text += '---------------\n'
        text += '商品總額 共'+str(productMoney)+'元\n'
        text += '運費 共'+str(deliveryFee)+'元\n'
        text += '---------------\n'
        totalMoney = productMoney+deliveryFee
        text += '訂單總額 共'+str(totalMoney)+'元\n'
        doc.update({
            'deliveryFee' : deliveryFee,
            'productMoney' : productMoney,
            'totalMoney' : totalMoney,
        })
        reply_token = event.reply_token
        utils.checkFinalOrder(reply_token,text)


    def is_going_to_finishOrder(self,event,doc):
        text = event.message.text
        if text == '@完成訂購':
            return True
        return False

    def on_enter_finishOrder(self,event,doc):
        detailedOrder = doc.get()
        text1 = ''
        if detailedOrder.to_dict()['payMethod'] == 0:
            text1 += '您選擇的付款方式為「現金支付」\n請於取貨日備妥現金取貨\n如有疑問請播打\n0988888888'
        else:
            text1 += '您選擇的付款方式為「銀行轉帳」\n請轉「'+str(detailedOrder.to_dict()['totalMoney'])+'」元至以下帳戶\n（822）8888888888888888\n並備註您的訂購姓名（否則會查不到）\n您可於轉帳完成後的一個工作天後\n至查詢訂單查詢付款狀態\n如有疑問請播打\n0988888888'
        reply_token = event.reply_token

        detailedList = doc.get().to_dict()

        # cred = credentials.Certificate("/etc/secrets/serviceAccount.json")
        # cred = credentials.Certificate("serviceAccount.json")
        # firebase_admin.initialize_app(cred)
        db = firestore.client()

        temp = db.collection("variable").document("series")
        orderNum = temp.get().to_dict()['series']
        temp.update({
            'series' : orderNum+1
        })

        dataSet = {
            'orderPID' : "",
            'name' : "",
            'phone' : "",
            'deliveryMethod' : 0,
            'takeDate' : 0,
            'deliveryAddress' : "",
            'payMethod' : 0,
            'box' : 0,
            'light' : 0,
            'heavy' : 0,
            'share' : 0,
            'productMoney' : 0,
            'deliveryFee' : 0,
            'totalMoney' : 0,
            'stateOfOrder' : "",
        }
        dataSet.update({'orderPID' : event.source.user_id})
        text = '新訂單：\n'
        text += '訂單編號：'+str(orderNum)+'\n'
        text += '訂購者姓名：' + detailedList['name'] + '\n'
        dataSet.update({'name' : detailedList['name']})
        text += '訂購者電話：' + detailedList['phone'] + '\n'
        dataSet.update({'phone' : detailedList['phone']})
        if detailedList['deliveryMethod'] == 0:
            text += '取貨方式：店鋪自取\n'
            takeDate = detailedList['takeDate']
            if takeDate == 0:
                text += '取貨日：星期六\n'
                dataSet.update({
                    'deliveryMethod' : 0,
                    'takeDate' : 0,
                })
            else:
                text += '取貨日：星期日\n'
                dataSet.update({
                    'deliveryMethod' : 0,
                    'takeDate' : 1,
                })
        else:
            text += '取貨方式：黑貓宅配\n'
            text += '宅配地址：'+ detailedList['address'] + '\n'
            dataSet.update({
                'deliveryMethod' : 1,
                'deliveryAddress' : detailedList['address'],
            })
        if detailedList['payMethod'] == 0:
            text += '付款方式：現金支付\n'
            dataSet.update({
                'payMethod' : 0,
                'stateOfOrder' : '訂單處理中'
            })
        else:
            text += '付款方式：銀行轉帳\n'
            dataSet.update({
                'payMethod' : 1,
                'stateOfOrder' : '待付款'
            })
        text += '---------------\n'
        productMoney = 0
        if detailedList['box'] > 0:
            num = detailedList['box']
            text += '盒裝地瓜 ' + str(num) + '盒 共' + str(num*100) + '元\n'
            productMoney += num*100
            dataSet.update({'box' : detailedList['box']})
        if detailedList['share'] > 0:
            num = detailedList['share']
            text += '真空分享包 ' + str(num) + '包 共' + str(num*100) + '元\n'
            productMoney += num*100
            dataSet.update({'share' : detailedList['share']})
        if detailedList['heavy'] > 0:
            num = detailedList['heavy']
            text += '真空重量包 ' + str(num) + '包 共' + str(num*50) + '元\n'
            productMoney += num*50
            dataSet.update({'heavy' : detailedList['heavy']})
        if detailedList['light'] > 0:
            num = detailedList['light']
            text += '真空輕量包 ' + str(num) + '包 共' + str(num*35) + '元\n'
            productMoney += num*35
            dataSet.update({'light' : detailedList['light']})
        deliveryFee = 200
        dataSet.update({'deliveryFee' : 200})
        if productMoney >= 3000 or detailedList['deliveryMethod'] == 0:
            deliveryFee = 0
            dataSet.update({'deliveryFee' : 0})
        text += '---------------\n'
        text += '商品總額 共'+str(productMoney)+'元\n'
        text += '運費 共'+str(deliveryFee)+'元\n'
        text += '---------------\n'
        totalMoney = productMoney+deliveryFee
        text += '訂單總額 共'+str(totalMoney)+'元\n'
        dataSet.update({
            'totalMoney' : totalMoney,
            'productMoney' : productMoney,
        })
        db.collection('order').document(str(orderNum)).set(dataSet)
        
        utils.finishOrder(reply_token,text1,orderNum,text)

    def is_going_to_chooseDate(self,event,doc):
        text = event.message.text
        if text == '@店面自取':
            doc.update({
                'deliveryMethod' : 0
            })
            return True
        return False

    def on_enter_chooseDate(self,event,doc):
        print("Go to chooseDate!")
        reply_token = event.reply_token
        utils.chooseDate(reply_token=reply_token)

    def is_going_to_modifyOrder(self,event,doc):
        text = event.message.text
        if text == '@訂單修改':
            return True
        return False
    
    def on_enter_modifyOrder(self,event,doc):
        print("Go to modifyOrder!")
        reply_token = event.reply_token
        utils.modifyOrder(reply_token)

    def is_going_to_changeInfo(self,event,doc):
        text = event.message.text
        if text == '@修改訂購人資訊':
            return True
        return False
    
    def is_going_to_changeDeliveryMethod(self,event,doc):
        text = event.message.text
        if text == '@修改取貨方式':
            return True
        return False

    def is_going_to_changePayMethod(self,event,doc):
        text = event.message.text
        if text == '@修改付款方式':
            return True
        return False

    def is_going_to_changeItems(self,event,doc):
        text = event.message.text
        if text == '@修改商品品項':
            return True
        return False

    def is_going_to_showOrder(self,event,doc):
        oid = event.message.text
        uid = event.source.user_id
        reply_token = event.reply_token
        

        if oid == "@回主選單" or oid == "主選單":
            self.go_back(event,doc)
            return False
        db = firestore.client()
        orderList = db.collection('order').document(oid).get()
        if orderList.exists != 1 :
            utils.send_text_message(reply_token,'查無訂單\n請重新輸入或輸入「主選單」回主選單')
            return False
        else:
            ref = orderList.to_dict()
            if ref['orderPID'] == uid or uid == os.getenv('ADMIN_UID',None):
                text = '訂單明細：\n'
                text += '訂單編號：' + oid + '\n'
                text += '訂單狀態：' + ref['stateOfOrder'] + '\n'
                text += '訂購者姓名：' + ref['name'] + '\n'
                text += '訂購者電話：' + ref['phone'] + '\n'
                if ref['deliveryMethod'] == 0:
                    text += '取貨方式：店鋪自取\n'
                    takeDate = ref['takeDate']
                    if takeDate == 0:
                        text += '取貨日：星期六\n'
                    else:
                        text += '取貨日：星期日\n'
                else:
                    text += '取貨方式：黑貓宅配\n'
                    text += '宅配地址：'+ ref['deliveryAddress'] + '\n'
                if ref['payMethod'] == 0:
                    text += '付款方式：現金支付\n'
                else:
                    text += '付款方式：銀行轉帳\n'
                text += '---------------\n'
                if ref['box'] > 0:
                    num = ref['box']
                    text += '盒裝地瓜 ' + str(num) + '盒 共' + str(num*100) + '元\n'
                if ref['share'] > 0:
                    num = ref['share']
                    text += '真空分享包 ' + str(num) + '包 共' + str(num*100) + '元\n'
                if ref['heavy'] > 0:
                    num = ref['heavy']
                    text += '真空重量包 ' + str(num) + '包 共' + str(num*50) + '元\n'
                if ref['light'] > 0:
                    num = ref['light']
                    text += '真空輕量包 ' + str(num) + '包 共' + str(num*35) + '元\n'
                text += '---------------\n'
                text += '商品總額 共'+str(ref['productMoney'])+'元\n'
                text += '運費 共'+str(ref["deliveryFee"])+'元\n'
                text += '---------------\n'
                text += '訂單總額 共'+str(ref["totalMoney"])+'元\n'
                utils.showOrder(reply_token,text)
                return True
            else:
                utils.send_text_message(reply_token,'您非該訂單擁有者\n請重新輸入或輸入「主選單」回主選單')
                return False

    def is_going_to_valid(self,event,doc):
        text = event.message.text
        reply_token = event.reply_token
        if text == "@回主選單" or text == "主選單":
            self.go_back(event,doc)
            return False
        if text == '@驗證管理員身份':
            if event.source.user_id != os.getenv('ADMIN_UID',None):
                utils.send_text_message(reply_token=reply_token,text='您無此權限')
                return False
            else:
                return True
        else:
            return False

    def on_enter_valid(self,event,doc):
        reply_token = event.reply_token
        utils.send_text_message(reply_token=reply_token,text='請輸入管理員密碼')

    def is_going_to_changeState(self,event,doc):
        reply_token = event.reply_token
        text = event.message.text
        if text == "@回主選單" or text == "主選單":
            self.go_back(event,doc)
            return False
        ref = doc.get().to_dict()
        if ref["state"] == "valid":
            if text == os.getenv("VALID_PASSWORD",None):
                utils.send_text_message(reply_token,"密碼正確\n請輸入欲修改的訂單編號\n換行寫狀態\n例如：\n1000001\n付款完成")
                return True
            else:
                utils.send_text_message(reply_token,"密碼錯誤\n請重新輸入")
                return False
        elif ref["state"] == "changeState":
            arr = text.split('\n')
            db = firestore.client()
            target = db.collection("order").document(arr[0])
            if target.get().exists :
                if len(arr) < 2:
                    utils.send_text_message(reply_token,"修改失敗\n狀態不可為空")
                    return False
                else:
                    target.update({
                    'stateOfOrder' : arr[1],
                    })
                    utils.send_text_message(reply_token,"修改成功\n如欲輸入下一筆資料\n請直接輸入即可\n或打「主選單」回主選單")
                    return True
            else:
                utils.send_text_message(reply_token,"訂單不存在")
                return False