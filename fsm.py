from transitions.extensions import GraphMachine

# from utils import send_text_message, showMenu

import pygsheets
import utils
from oauth2client.service_account import ServiceAccountCredentials as SAC



gc = pygsheets.authorize(service_file='/etc/secrets/sweet-potato-370214-3b8a193390de.json')
            


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
        try:
            sht = gc.open_by_url(
'https://docs.google.com/spreadsheets/d/1C6YSY1vgW4abK3XNLDIKPlRGW_YSn1MnleNX9f3pw0Y/edit?usp=sharing'
)
            print("Yes!")
            wks = sht[0]
        except:
            print("No!")

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
        reply_token = event.reply_token
        utils.orderTip(reply_token)
    
    def is_going_to_deliveryMethod(self,event,doc):
        text = event.message.text
        return text == "@繼續訂購"

    def on_enter_deliveryMethod(self,event,doc):
        print("Go to deliveryMethod!")
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
        })
        reply_token = event.reply_token
        utils.deliveryMethod(reply_token)
    

    def is_going_to_searchOrder(self,event,doc):
        text = event.message.text
        return text == "@訂單查詢"

    def on_enter_searchOrder(self,event,doc):
        print("Go to searchOrder!")
        reply_token = event.reply_token
        utils.showMenu(reply_token)

    def is_going_to_deliveryAddress(self,event,doc):
        text = event.message.text
        if text == "@黑貓宅配" or text == "@修改地址":
            if text == "@黑貓宅配":
                doc.update({
                    'deliveryMethod' : 1
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

    def is_going_to_chooseItem(self,event,doc):
        text = event.message.text
        if text == "@店面自取" or text == "@確認地址":
            if text == "@店面自取":
                doc.update({
                    'deliveryMethod' : 0
                })
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
                    buyList = buyList + '運送方式：店面自取\n----------\n'
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
                utils.checkItem(reply_token,buyList)
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
        if text == "@複製地址":
            return True
        return False

    def on_enter_copyAddress(self,event,doc):
        print("Go to copyAddress!")
        reply_token = event.reply_token
        utils.send_text_message(reply_token,'台南市永康區大灣路129號之3')
        self.go_back(event,doc)

    def is_going_to_aboutUs(self,event,doc):
        text = event.message.text
        if text == "@關於我們":
            return True
        return False
    
    def on_enter_aboutUs(self,event,doc):
        print("Go to aboutUs!")
        reply_token = event.reply_token
        utils.send_text_message(reply_token,'台南市永康區大灣路129號之3')

    def is_going_to_inputName(self,event,doc):
        text = event.message.text
        if text == '@繼續填寫訂購資訊' or text == '@修改名字':
            return True
        return False
    
    def on_enter_inputName(self,event,doc):
        print("Go to inputName!")
        reply_token = event.reply_token
        utils.send_text_message(reply_token,'請輸入訂購者姓名')

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
        utils.send_text_message(reply_token,'請輸入訂購者電話')

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
        if text == '@確認電話':
            return True
        return False
    
    def on_enter_inputPayMethod(self,event,doc):
        print("Go to inputPayMethod!")
        reply_token = event.reply_token
        utils.choosePayMethod(reply_token)

    def is_going_to_checkFinalOrder(self,event,doc):
        paymethod = event.message.text
        if paymethod == '@現金支付' :
            doc.update({
                'payMethod' : 0,
            })
            return True
        if paymethod == '@銀行轉帳' :
            doc.update({
                'payMethod' : 1,
            })
            return True
        return False

    def on_enter_checkFinalOrder(self,event,doc):
        print("Go to checkFinalOrder!")
        detailedList = doc.get()
        text = '訂單確認：\n'
        text += '訂購者姓名：' + detailedList.to_dict()['name'] + '\n'
        text += '訂購者電話：' + detailedList.to_dict()['phone'] + '\n'
        if detailedList.to_dict()['deliveryMethod'] == 0:
            text += '付款方式：店鋪自取\n'
        else:
            text += '付款方式：黑貓宅配\n'
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
        text = ''
        if detailedOrder.to_dict()['payMethod'] == 0:
            text += '您選擇的付款方式為「現金支付」\n請於取貨日備妥現金取貨\n如有疑問請播打\n0988888888'
        else:
            text += '您選擇的付款方式為「銀行轉帳」\n請轉「'+str(detailedOrder.to_dict()['totalMoney'])+'」元至以下帳戶\n（822）8888888888888888\n您可於轉帳完成後的一個工作天後\n至查詢訂單查詢付款狀態\n如有疑問請播打\n0988888888'
        reply_token = event.reply_token
        utils.finishOrder(reply_token,text)

