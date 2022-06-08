
async def getYou():
    phone_number = '+79033671563'
    print ('[+] phone_number:',phone_number)
    client = ''
    answer = 'Отсутствует учетная запись в базе'
    from telethon.sync import TelegramClient
    from telethon.sessions import StringSession
    db,cursor = connect ()
    sql = "select id,name,session from telegram_session where name = '"+str(phone_number)+"' limit 1"
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data: 
        id,name,session = rec.values()
        client = TelegramClient(StringSession(session),api_id=api_id,api_hash=api_hash)
        client.connect()
        if not client.is_user_authorized():
            answer = 'Отсутствует подключение к телеграмм серверу'
        else:
            answer = 'Подключение к телеграмм серверу успешно'
    return await client.get_me()

def make_file (file,name,namebot,user_id):    
    import iz_func
    import iz_telegram
    import docx
    db,cursor = iz_func.connect ()
    message_out,menu,answer = iz_telegram.send_message (user_id,namebot,'Подготовка документа 1','S',0) 
    document = docx.Document(file)
    sql = "select id,name,alliance,answer from bot_quest_answer where name = '"+str(name)+"' and user_id = '"+str(user_id)+"' and namebot = '"+str(namebot)+"' and alliance <> '' ORDER BY id DESC limit 1".format()   
    print ('[+]0',sql)
    cursor.execute(sql)
    data = cursor.fetchall()
    id = 0
    for rec in data: 
        print ('[+]3')
        id,name,alliance,answer = rec.values() 
        for paragraph in document.paragraphs:                
            paragraph.text = paragraph.text.replace(alliance, answer)     
    document.save("send_"+file)
    doc = open("send_"+file, 'rb')
    print ('        [+] Создан документ',"send_"+file)
    token = iz_telegram.get_token (namebot)
    import telebot  
    bot   = telebot.TeleBot(token)  
    bot.send_document(user_id, doc)
    import os 
    if os.path.isfile("send_"+file): 
        os.remove("send_"+file)
        print("success") 
    else: 
        print("File doesn't exists!")    

def menu_select_finish (user_id,namebot,id):
    import iz_func
    from telebot import types
    markup = types.InlineKeyboardMarkup(row_width=4)    
    db,cursor = iz_func.connect ()
    sql = "select id,name,volume from bot_quest_menu_answer where id = "+str(id)+" limit 1;".format()
    cursor.execute(sql)
    data = cursor.fetchall()
    id = 0
    volume = ''
    for rec in data: 
        id,name,volume = rec.values() 
    if volume == 'on':
        volume = 'off'
    else:
        volume = 'on'
    sql = "UPDATE bot_quest_menu_answer SET volume = '"+volume+"' WHERE id = "+str(id)+""
    cursor.execute(sql)
    db.commit() 

    markup = menu_select_start (user_id,namebot,name)
    return markup

def get_param_menu (namebot,user_id,name,line):
    import iz_func
    db,cursor = iz_func.connect ()
    answer = ''
    sql = "select id,volume from bot_quest_menu_answer where name = '"+str(name)+"' and namebot = '"+str(namebot)+"' and user_id = '"+str(user_id)+"' and `line` = "+str(line)+" limit 1;".format()
    cursor.execute(sql)
    data = cursor.fetchall()
    id = 0
    for rec in data: 
        id,volume = rec.values() 
    if id == 0:  
        volume = 'off'
        sql = "INSERT INTO bot_quest_menu_answer (name,namebot,user_id,`line`,volume) VALUES ('{}','{}','{}',{},'{}')".format (name,namebot,user_id,line,volume)
        cursor.execute(sql)
        db.commit()
        lastid = cursor.lastrowid
        id = lastid

    if volume == 'off':
        answer = 'off'
    if volume == 'on':
        answer = 'on'
    return id,answer        

def menu_select_start (user_id,namebot,name):
    import iz_func
    import iz_telegram
    from telebot import types
    markup = types.InlineKeyboardMarkup(row_width=4)    
    db,cursor = iz_func.connect ()
    sql = "select id,name,line01,line02,line03,line04,line05,line06,line07,line08,`type` from bot_quest_menu where name = '"+str(name)+"' ".format()
    cursor.execute(sql)
    data = cursor.fetchall()
    for row in data:
        id_menu,name,line01,line02,line03,line04,line05,line06,line07,line08,type_l = row.values() 
    if type_l == 'on | off':

        if  line01 != '':
            id,answer = get_param_menu (namebot,user_id,name,1)
            answer = iz_telegram.get_namekey (user_id,namebot,answer)
            mn11 = types.InlineKeyboardButton(text=answer+' '+line01,callback_data='select_menu_'+str(id))
            markup.add(mn11)

        if  line02 != '':
            id,answer = get_param_menu (namebot,user_id,name,2) 
            answer = iz_telegram.get_namekey (user_id,namebot,answer)
            mn12 = types.InlineKeyboardButton(text=answer+' '+line02,callback_data='select_menu_'+str(id))
            markup.add(mn12)

        if  line03 != '':
            id,answer = get_param_menu (namebot,user_id,name,3) 
            answer = iz_telegram.get_namekey (user_id,namebot,answer)
            mn13 = types.InlineKeyboardButton(text=answer+' '+line03,callback_data='select_menu_'+str(id))
            markup.add(mn13)

        if  line04 != '':
            id,answer = get_param_menu (namebot,user_id,name,4) 
            answer = iz_telegram.get_namekey (user_id,namebot,answer)
            mn14 = types.InlineKeyboardButton(text=answer+' '+line04,callback_data='select_menu_'+str(id))
            markup.add(mn14)

        if  line05 != '':
            id,answer = get_param_menu (namebot,user_id,name,5)
            answer = iz_telegram.get_namekey (user_id,namebot,answer)
            mn15 = types.InlineKeyboardButton(text=answer+' '+line05,callback_data='select_menu_'+str(id))
            markup.add(mn15)

        if  line06 != '':
            id,answer = get_param_menu (namebot,user_id,name,6) 
            answer = iz_telegram.get_namekey (user_id,namebot,answer)
            mn16 = types.InlineKeyboardButton(text=answer+' '+line06,callback_data='select_menu_'+str(id))
            markup.add(mn16)

        if  line07 != '':
            id,answer = get_param_menu (namebot,user_id,name,7) 
            answer = iz_telegram.get_namekey (user_id,namebot,answer)
            mn17 = types.InlineKeyboardButton(text=answer+' '+line07,callback_data='select_menu_'+str(id))
            markup.add(mn17)

        if  line08 != '':    
            id,answer = get_param_menu (namebot,user_id,name,8) 
            answer = iz_telegram.get_namekey (user_id,namebot,answer)
            mn18 = types.InlineKeyboardButton(text=answer+' '+line08,callback_data='select_menu_'+str(id))
            markup.add(mn18)

        mn21 = types.InlineKeyboardButton(text='Завершить выбор',callback_data='select_end_'+str(id_menu))
        markup.add(mn21)

    if type_l == 'one select':

        if id_menu <10:
            id_menu_k = "00"+str(id_menu)
        if id_menu <100 and id_menu >=10:
            id_menu_k = "0"+str(id_menu)

        mn11 = types.InlineKeyboardButton(text=line01,callback_data='up_menu_'+str(id_menu_k)+'_line_1')
        markup.add(mn11)
        mn12 = types.InlineKeyboardButton(text=line02,callback_data='up_menu_'+str(id_menu_k)+'_line_2')
        markup.add(mn12)
        mn13 = types.InlineKeyboardButton(text=line03,callback_data='up_menu_'+str(id_menu_k)+'_line_3')
        markup.add(mn13)
        mn14 = types.InlineKeyboardButton(text=line04,callback_data='up_menu_'+str(id_menu_k)+'_line_4')
        markup.add(mn14)
        mn15 = types.InlineKeyboardButton(text=line05,callback_data='up_menu_'+str(id_menu_k)+'_line_5')
        markup.add(mn15)
        mn16 = types.InlineKeyboardButton(text=line06,callback_data='up_menu_'+str(id_menu_k)+'_line_6')
        markup.add(mn16)
        mn17 = types.InlineKeyboardButton(text=line07,callback_data='up_menu_'+str(id_menu_k)+'_line_7')
        markup.add(mn17)
        mn18 = types.InlineKeyboardButton(text=line08,callback_data='up_menu_'+str(id_menu_k)+'_line_8')
        markup.add(mn18)
    return markup
        
def start_prog (user_id,namebot,message_in,status,message_id,name_file_picture,telefon_nome):
    import iz_func
    import iz_telegram 

    anketa = 'Yes'
    if message_in == '/start':
        #import iz_telefon
        import iz_func
        status = ''
        iz_telegram.save_variable (user_id,namebot,"status",'')
        anketa = 'No'

    if message_in == 'Начать тест':
        status = ''
        iz_telegram.save_variable (user_id,namebot,"status",'')
    
    if message_in.find ('select_menu_') != -1:
        word  = message_in.replace('select_menu_','')
        message_out = "Меню выбора"
        markup = menu_select_finish (user_id,namebot,word)
        answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,message_id)
        anketa = 'No'

    if message_in.find ('select_end') != -1:
        word  = message_in.replace('select_end_','')
        db,cursor = iz_func.connect ()
        sql = "select id,name,line01,line02,line03,line04,line05,line06,line07,line08,`type` from bot_quest_menu where id = "+str(word)+" "
        cursor.execute(sql)
        data = cursor.fetchall()
        for row in data:
            id,name_menu,line01,line02,line03,line04,line05,line06,line07,line08,type_l = row.values() 
        select_answer = ''
        sql = "select id,name,volume from bot_quest_menu_answer where `line` = 1 and name = '"+str(name_menu)+"' limit 1;".format()
        cursor.execute(sql)
        data = cursor.fetchall()
        volume = ''
        for rec in data: 
            id,name,volume = rec.values() 
            print ('[+] volume:',volume)
        if volume == 'on':
            select_answer = select_answer + line01 + '\n'

        sql = "select id,name,volume from bot_quest_menu_answer where `line` = 2 and name = '"+str(name_menu)+"' limit 1;".format()
        cursor.execute(sql)
        data = cursor.fetchall()
        volume = ''
        for rec in data: 
            id,name,volume = rec.values() 
            print ('[+] volume:',volume)
        if volume == 'on':
            select_answer = select_answer + line02 + '\n'

        sql = "select id,name,volume from bot_quest_menu_answer where `line` = 3 and name = '"+str(name_menu)+"' limit 1;".format()
        cursor.execute(sql)
        data = cursor.fetchall()
        volume = ''
        for rec in data: 
            id,name,volume = rec.values() 
            print ('[+] volume:',volume)
        if volume == 'on':
            select_answer = select_answer + line03 + '\n'

        sql = "select id,name,volume from bot_quest_menu_answer where `line` = 4 and name = '"+str(name_menu)+"' limit 1;".format()
        cursor.execute(sql)
        data = cursor.fetchall()
        volume = ''
        for rec in data: 
            id,name,volume = rec.values() 
            print ('[+] volume:',volume)
        if volume == 'on':
            select_answer = select_answer + line04 + '\n'

        sql = "select id,name,volume from bot_quest_menu_answer where `line` = 5 and name = '"+str(name_menu)+"' limit 1;".format()
        cursor.execute(sql)
        data = cursor.fetchall()
        volume = ''
        for rec in data: 
            id,name,volume = rec.values() 
            print ('[+] volume:',volume)
        if volume == 'on':
            select_answer = select_answer + line05 + '\n'

        sql = "select id,name,volume from bot_quest_menu_answer where `line` = 6 and name = '"+str(name_menu)+"' limit 1;".format()
        cursor.execute(sql)
        data = cursor.fetchall()
        volume = ''
        for rec in data: 
            id,name,volume = rec.values() 
            print ('[+] volume:',volume)
        if volume == 'on':
            select_answer = select_answer + line06 + '\n'

        sql = "select id,name,volume from bot_quest_menu_answer where `line` = 7 and name = '"+str(name_menu)+"' limit 1;".format()
        cursor.execute(sql)
        data = cursor.fetchall()
        volume = ''
        for rec in data: 
            id,name,volume = rec.values() 
            print ('[+] volume:',volume)
        if volume == 'on':
            select_answer = select_answer + line07 + '\n'

        sql = "select id,name,volume from bot_quest_menu_answer where `line` = 8 and name = '"+str(name_menu)+"' limit 1;".format()
        cursor.execute(sql)
        data = cursor.fetchall()
        volume = ''
        for rec in data: 
            id,name,volume = rec.values() 
            #print ('[+] volume:',volume)
        if volume == 'on':
            select_answer = select_answer + line08 + '\n'

        message_in = select_answer



        message_out,menu = iz_telegram.get_message (user_id,'Выбор сделан',namebot)





        message_out = message_out.replace('%%Выбор%%','<code>'+message_in+'</code>')   
        markup = ""
        answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,message_id) 
        anketa = 'Yes'

    if message_in.find ('up_menu_') != -1:
        word1  = message_in.replace('up_menu_','')
        word2  = word1[3:].replace('_line_','')
        word3  = word1[0:3]
        
        db,cursor = iz_func.connect ()
        sql = "select id,name,line01,line02,line03,line04,line05,line06,line07,line08,`type` from bot_quest_menu where id = "+str(word3)+" "
        cursor.execute(sql)
        data = cursor.fetchall()
        for row in data:
            id,name,line01,line02,line03,line04,line05,line06,line07,line08,type_l = row.values() 

        if word2 == '1':
            message_in = line01
        if word2 == '2':
            message_in = line02
        if word2 == '3':
            message_in = line03
        if word2 == '4':
            message_in = line04
        if word2 == '5':
            message_in = line05
        if word2 == '6':
            message_in = line06
        if word2 == '7':
            message_in = line07
        if word2 == '8':
            message_in = line08


        message_out,menu = iz_telegram.get_message (user_id,'Выбор сделан',namebot)
        message_out = message_out.replace('%%Выбор%%','<code>'+message_in+'</code>')   
        message_out = message_out.replace('%%status%%','<code>'+status+'</code>')   
        markup = ""

        correct_answer = ""
        sql = "select id,name,alliance,correct_answer from bot_quest where status_out = '"+str(status)+"'"
        cursor.execute(sql)
        data3 = cursor.fetchall()
        for rec3 in data3: 
            id_3,name_3,alliance3,correct_answer  = rec3.values() 

        if correct_answer == message_in:
            message_out = message_out.replace('%%Ответ%%','<code>'+correct_answer+'</code>'+' 😀')   
        else:
            message_out = message_out.replace('%%Ответ%%','<code>'+correct_answer+'</code>'+' 😞')   

        answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,message_id) 
        anketa = 'Yes'




    if message_in == 'Поделиться ботом':
        anketa = 'No'

        
    if message_in == 'Топ пользователей':
        anketa = 'No'
        message_out,menu = iz_telegram.get_message (user_id,'Список пользователей',namebot)
        db,cursor = iz_func.connect ()
        sql = "select id,user_id,first_name,last_name,username from bot_user where namebot = '"+str(namebot)+"' "
        cursor.execute(sql)
        data = cursor.fetchall()
        list = []
        srt  = []
        kl   = 0        
        pr_v = 0
        #for row in data:
        #    id,user_id_l,first_name,last_name,username = row.values() 
        #    kl = kl + 1
        #    ball    = 0 
        #    sql = "select id,correct_answer,alliance from bot_quest where message_out != '' "
        #    cursor.execute(sql)
        #    data4 = cursor.fetchall()            
        #    for row4 in data4:                
        #        id4,correct_answer,alliance = row4.values()
        #        print ('[+]',user_id_l,correct_answer,alliance)
        #        id = 0
        #        answer_a = ''
        #        sql = "select id,user_id,alliance,answer from bot_quest_answer where user_id = '"+str(user_id_l)+"' and alliance = '"+str(alliance)+"' ORDER BY id DESC limit 1"
        #        cursor.execute(sql)
        #        data1 = cursor.fetchall()
        #        for row1 in data1:
        #            id,user_id_a,alliance_a,answer_a = row1.values()
        #        if id != 0 and answer_a == correct_answer:
        #            ball = ball + 1
        #    person = (ball,user_id_l,first_name,last_name,username)

        #    if str(user_id) == str(user_id_l):
        #        pr_v = ball

        #    list.append(person)
        #a = sorted(list, key=lambda student: student[0],reverse=True)
        #best = ''

        #nm = 0
        #ms = 0
        #for line in a:
        #    nm = nm + 1
        #    if str(user_id) == str(line[1]):
        #        ms = nm            
        #    if nm < 10:
        #        best = best +str(nm)+') '+str(line[0]) + " - " + str(line[2]) +' '+str(line[3])+' '+str(line[4]) + "\n"
                
        
        #kl_q = 0
        #sql = "select id,user_id from bot_quest_answer where user_id = '"+str(user_id)+"' "
        #cursor.execute(sql)
        #data4 = cursor.fetchall()            
        #for row4 in data4:
        #    kl_q = kl_q + 1





        #message_out = message_out  + '\n' + str(best) #+ str(list)
        #markup = ''
        #answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,0)             
        #message_out,menu = iz_telegram.get_message (user_id,'Ваше место в списке',namebot)
        #essage_out = message_out.replace('%%Всего участников%%',str(kl))   
        #message_out = message_out.replace('%%Ваше место%%',str(ms))

        #message_out = message_out.replace('%%Всего задали вопросов%%',str(kl_q))
        #message_out = message_out.replace('%%Ответили правильно%%',str(pr_v))

        #markup = ''
        #answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,0) 






    if message_in == 'Отмена':
        status = ''
        message_out,menu,answer = iz_telegram.send_message (user_id,namebot,'Отмена ввода данных','S',0) 
        iz_telegram.save_variable (user_id,namebot,"status",'')
        anketa = 'No'
    
    label = 'send'
    if anketa == 'Yes':
        db,cursor = iz_func.connect ()
        sql = "select id,name,message_in,message_out,status_in,status_out,file,alliance,menu from bot_quest where name <> '' ".format()
        cursor.execute(sql)
        data = cursor.fetchall()
        id = 0
        for rec in data: 
            id_q,name_q,message_in_q,message_out_q,status_in_q,status_out_q,file,alliance_q,menu_q  = rec.values() 
            if (status == status_in_q and status != '') or (message_in == message_in_q):    
                if menu_q == '':
                    message_out,menu,answer = iz_telegram.send_message (user_id,namebot,message_out_q,'S',0)                     
                else:
                    message_out,menu = iz_telegram.get_message (user_id,message_out_q,namebot)
                    markup = menu_select_start (user_id,namebot,menu_q)
                    answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,0) 
                iz_telegram.save_variable (user_id,namebot,"status",status_out_q)
                alliance2 = ''
                sql = "select id,name,alliance from bot_quest where status_out = '"+str(status_in_q)+"'"
                cursor.execute(sql)
                data2 = cursor.fetchall()
                for rec2 in data2: 
                    id_2,name_2,alliance2  = rec2.values() 
                sql = "INSERT INTO bot_quest_answer (`namebot`,`user_id`,`name`,`answer`,`alliance`) VALUES ('{}','{}','{}','{}','{}')".format (namebot,user_id,name_q,message_in,alliance2)
                cursor.execute(sql)
                db.commit()
                if file != '':
                    make_file (file,name_q,namebot,user_id)


