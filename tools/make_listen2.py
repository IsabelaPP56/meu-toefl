import random, sys
sys.path.insert(0, "/workspace/tools")
from bank_common import dump, words, mc

def Q(stem, correct, wrongs, why):
    opts = [correct, *wrongs]
    order = [0, 1, 2, 3]
    random.Random(stem + correct).shuffle(order)
    return mc(stem, [opts[i] for i in order], order.index(0), why)

convs = []
def add_conv(pool, level, lines, questions):
    assert len(questions) == 2
    text = " ".join(x["text"] for x in lines)
    assert 35 <= len(words(text)) <= 120, (pool, len(words(text)), text)
    convs.append({"id": f"cv{len(convs)+1:02d}", "pool": pool, "level": level,
                  "lines": lines, "questions": questions})

def L(who, text):
    return {"who": who, "text": text}

# Hand-built conversations. W/M alternating.
specs = []

def C(pool, level, turns, q1, q2):
    lines = [L("Woman" if i % 2 == 0 else "Man", t) for i, t in enumerate(turns)]
    specs.append((pool, level, lines, [q1, q2]))

C("practice","mid",[
"The study room I booked is still full.","Did the last group run over?","Yes, they're still presenting.","Ask the desk for room B. It's usually empty this hour.","I'll do that. Can you hold our notes?","Yes. Text me the new room number."
], Q("What problem does the woman have?","Her booked room is still occupied",["She lost her notes","The desk is closed","Room B is full"],"A sala reservada continua ocupada."),
   Q("What will she probably do next?","Ask the desk for another room",["Cancel the study session","Present with the other group","Leave the building"],"O homem sugere a sala B e ela aceita."))

C("practice","easy",[
"Are you going to the advising office?","I was, but they moved walk-in hours to tomorrow.","So today is appointments only?","Right. I booked Friday at ten instead.","Then I'll try tomorrow morning.","Go early. The line starts before the door opens."
], Q("What changed about advising?","Walk-in hours moved to tomorrow",["The office closed for the term","Friday appointments were canceled","The line was removed"],"O atendimento sem hora marcada passou para amanhã."),
   Q("What does the man suggest about tomorrow?","Arrive before the door opens",["Skip the line","Come at ten tonight","Book Friday instead"],"Ele diz que a fila começa antes da abertura."))

C("practice","mid",[
"I can't find the article for seminar.","Did you check the reserve list?","I checked the shelves, not the list.","It's online under the course page, not on the shelf.","That explains it. I'll download it tonight.","Download the PDF. The link disappears after Friday."
], Q("Why couldn't the woman find the article?","She looked on the shelf, but it is online",["The seminar was canceled","The library is closed","Friday already passed"],"O texto está na página do curso, não na estante."),
   Q("What will she probably do?","Download the PDF tonight",["Buy a copy","Ask for a new topic","Wait until next month"],"Ela diz que vai baixar hoje à noite."))

C("practice","easy",[
"The shuttle left without us.","The next one is in twenty minutes.","We'll be late for the lab.","Email the instructor from here. She accepts a late arrival if you write.","I'll write now.","Mention the east gate. That's the stop that moved."
], Q("Why might they be late?","They missed the shuttle",["The lab was canceled","The instructor is at the east gate","There is no later shuttle"],"O ônibus saiu sem eles."),
   Q("What should the email mention?","The east gate",["A request to cancel the lab","The price of a ticket","A new major"],"O homem pede para citar o ponto que mudou."))

C("practice","mid",[
"Do you still want to trade presentation days?","Yes, if I can go on Monday.","Monday is free. I'll tell the professor.","Ask her before tonight. She locks the schedule at five.","I'll email her now.","Send me a copy so I know it's confirmed."
], Q("What do the speakers want to change?","Their presentation days",["The professor","The classroom lock","The email system"],"Eles querem trocar os dias da apresentação."),
   Q("Why is there a rush?","The schedule locks at five",["Monday is full","The professor already refused","The copy was lost"],"A professora trava a agenda às cinco."))

C("practice","easy",[
"I'm going to the clinic after class.","Do you have your ID?","It's in my room.","They won't check you in without it.","Then I'll stop at the dorm first.","If you feel dizzy, don't wait. Tell them at the desk."
], Q("What must the woman bring?","Her ID",["A payment","A friend","Class notes"],"O homem diz que não há check-in sem o documento."),
   Q("What will she do before the clinic?","Stop at her dorm",["Skip class","Go straight there","Email the clinic"],"O documento está no quarto, então ela passa no alojamento."))

C("practice","mid",[
"The printer jammed again.","Use the one in the library basement.","Is it working?","I used it an hour ago. Bring your own paper.","I have a few sheets.","Good. The basement machine doesn't sell paper."
], Q("What is wrong with the first printer?","It jammed",["It is in the basement","It sells paper","It was fixed an hour ago"],"A impressora atolou de novo."),
   Q("What should the woman bring?","Her own paper",["A new printer","Payment for paper","The jammed machine"],"A máquina do porão não vende papel."))

C("practice","easy",[
"Want to get lunch?","I have a quiz at one.","We could grab something quick.","The line at the main hall is too long.","The café by the gym is faster.","Let's do that. I need to be back by 12:40."
], Q("Why is the man hesitant?","He has a quiz at one",["He dislikes the gym","The café is closed","He already ate"],"Ele tem prova à uma."),
   Q("Why do they choose the gym café?","It is faster than the main hall",["It is free","It serves only dinner","It is next to the quiz room"],"A fila do refeitório principal está longa."))

C("practice","mid",[
"Did you back up the slides?","Yes, they're in the shared folder.","Which version?","The one I saved at noon, not last night's.","I'll open that one.","Don't edit it. I still have to fix the chart."
], Q("Which slides should be used?","The version saved at noon",["Last night's version","A new blank file","The chart only"],"O homem distingue o arquivo do meio-dia."),
   Q("What does the man ask the woman not to do?","Edit the file",["Open the folder","Look at the chart","Save a copy"],"Ele ainda vai corrigir o gráfico."))

C("practice","easy",[
"Is this seat free?","Yes, but I'm saving the next one for Mina.","That's fine. I only need one.","She'll be here in five minutes.","I'll watch your bag if you want to get water.","Thanks. I'll be right back."
], Q("What is the man saving?","The seat next to him for Mina",["Every seat in the row","A bag of water","A five-minute quiz"],"Ele guarda o lugar ao lado para Mina."),
   Q("What does the woman offer?","To watch his bag",["To take Mina's seat","To leave immediately","To buy two seats"],"Ela oferece olhar a bolsa enquanto ele pega água."))

C("practice","mid",[
"The group chat is moving too fast.","I stopped reading after the third message.","We need the decision about the poster.","Leo said to use the morning file and print downtown.","Then I won't use yesterday's version.","Right. And Mia is bringing the stand tomorrow."
], Q("Which file should they print?","The morning file",["Yesterday's version","The third message","A new poster"],"Leo mandou usar o arquivo da manhã."),
   Q("What will Mia do?","Bring the display stand tomorrow",["Print the poster","Rewrite the file","Leave the group"],"O homem diz que Mia traz o suporte amanhã."))

C("practice","easy",[
"I think I submitted the wrong file.","Can you still replace it?","The portal locked at noon.","Email the instructor and attach the right one.","I'll do that now.","Explain that the upload froze, so she knows why it's late."
], Q("What mistake did the woman make?","She submitted the wrong file",["She missed the class","She locked the portal","She lost the instructor's email"],"Ela enviou o arquivo errado."),
   Q("What should the email explain?","That the upload froze",["That the quiz was unfair","That the portal opens at noon","That she does not want a grade"],"O homem pede para explicar o travamento."))

C("practice","mid",[
"We're short one volunteer for the fair.","I can take the morning shift.","It's from nine to twelve at table four.","I know the garden group. That's fine.","They'll want you to bring the sign.","It's in the club office. I'll pick it up tonight."
], Q("What does the man offer?","To work the morning shift",["To cancel the fair","To move table four","To design a new sign"],"Ele cobre o turno da manhã."),
   Q("Where is the sign?","In the club office",["At table four already","At the woman's home","It was not made"],"Ele vai buscá-la na sala do clube."))

C("practice","easy",[
"The heater in our room is stuck on high.","Did you submit a request?","Not yet.","Do it online. Phone calls get lost.","I'll do it after dinner.","Mention room 316 or they'll send someone to the wrong floor."
], Q("What is the problem?","The heater will not turn down",["The website is closed","Dinner was canceled","The room number changed"],"O aquecedor está preso no máximo."),
   Q("Why does the room number matter?","So the repair goes to the right floor",["It proves they already called","It cancels the request","It lowers the heat immediately"],"Sem o número, mandam a pessoa ao andar errado."))

C("practice","mid",[
"Can we rehearse in the empty classroom?","Until four. A class starts then.","That's enough time.","Don't move the desks into the hall.","We'll put them back.","Leave the board clean. The instructor writes before students arrive."
], Q("How long can they use the room?","Until four",["All evening","Until the board is full","Only five minutes"],"Uma aula começa às quatro."),
   Q("What must they do to the board?","Leave it clean",["Fill it with notes","Erase the instructor's quiz","Move it to the hall"],"O professor escreve antes dos alunos."))

C("practice","easy",[
"I lost the receipt for the supplies.","Check your email. The store sends a copy.","I deleted it.","Then go to the front desk with your card. They can reprint it.","I'll go now.","Ask for receipt 441. That's the one with the discount."
], Q("How can the woman get another receipt?","At the front desk with her card",["By buying the supplies again","Only by email","She cannot"],"O balcão reimprime com o cartão."),
   Q("Which receipt does she need?","Number 441",["Any receipt from last year","The one without a discount","A handwritten note"],"O homem identifica o número 441."))

C("practice","mid",[
"Your library book is overdue.","I thought it was due Monday.","It was due Friday. There's a fine.","Can I return it now and stop the fine?","Yes. The outdoor box is locked, so use the desk.","I'll go before my next class."
], Q("When was the book due?","Friday",["Monday","After the next class","There is no due date"],"O homem corrige: era sexta, não segunda."),
   Q("Why must she use the desk?","The outdoor return box is locked",["The desk charges less","The book is not overdue","Her class is in the library"],"A caixa externa está trancada."))

C("practice","easy",[
"Do you want the window or the aisle?","The aisle. I may need to stand.","This row is fine.","The safety talk is about to start.","I'll put my bag under the seat.","Good. The speaker asked us to keep the aisle clear."
], Q("Which seat does the man want?","The aisle seat",["The window seat","A seat in another room","No seat"],"Ele escolhe o corredor porque pode precisar levantar."),
   Q("What did the speaker ask?","To keep the aisle clear",["To stand during the talk","To close the windows","To move every bag to the stage"],"O corredor deve ficar livre."))

C("practice","mid",[
"I'm locked out of the portal.","Try the password reset in your email.","I never got the message.","Check the spam folder, then wait five minutes.","If it isn't there, I'll call the help desk.","Call them. Don't keep guessing or the account will lock again."
], Q("What is the woman's problem?","She cannot enter the portal",["She lost her laptop","The help desk is closed","Her password was published"],"Ela está trancada fora do portal."),
   Q("What does the man warn her not to do?","Keep guessing the password",["Check spam","Call the help desk","Wait five minutes"],"Novas tentativas podem travar a conta de novo."))

C("practice","easy",[
"The orchestra rehearsal is closed, but tickets go on sale at noon.","I can line up.","Each person may buy two.","Then I'll get ours and Nora's.","She already has one. Just buy two, not three.","Right. I'll text you when I have them."
], Q("How many tickets will the man buy?","Two",["Three","One","Ten"],"A mulher corrige: duas, não três, porque Nora já tem uma."),
   Q("What will he do after he has them?","Text the woman",["Give them to the orchestra","Buy a third","Skip the line"],"Ele diz que vai mandar mensagem."))

# mocks
C("m1","mid",[
"The lab report is longer than I expected.","Focus on the section she marked.","I was rewriting the whole thing.","She only asked for the methods and one graph.","That cuts it in half.","Send me the graph if you want a second pair of eyes."
], Q("What should the report emphasize?","The methods and one graph",["A full rewrite of every section","Only the title","A new experiment"],"A professora marcou métodos e um gráfico."),
   Q("What does the man offer?","To look at the graph",["To write the report","To cancel the lab","To change the mark"],"Ele oferece um segundo olhar."))

C("m1","easy",[
"We're out of cups in the lounge.","I'll wash a few.","The sink is full of paint trays.","Then use the kitchen by the mail room.","I didn't know there was one.","It's behind the blue door. Students can use it until six."
], Q("Why can't they use the lounge sink?","It is full of paint trays",["It closes at six","There is no kitchen","The cups are new"],"O homem diz que a pia está cheia de bandejas."),
   Q("Until when can students use the kitchen?","Until six",["All night","Only in the morning","They cannot"],"A cozinha fica disponível até as seis."))

C("m1","mid",[
"I might drop the lab if I fail Friday's quiz.","Talk to the instructor before you decide.","What would I say?","Ask whether the quiz can be replaced by the next report.","That's better than dropping today.","The drop deadline is Monday, so you still have time."
], Q("What is the woman considering?","Dropping the lab",["Skipping the report","Teaching the quiz","Changing the deadline herself"],"Ela pensa em trancar o laboratório."),
   Q("Why is Monday important?","It is the drop deadline",["The quiz is on Monday","The instructor is gone after Monday","Reports are due on Monday"],"Ainda dá tempo porque o prazo é segunda."))

C("m1u","hard",[
"The archive won't release the folder.","Did you include the collection number?","I sent the title only.","They refuse requests without that number.","I'll look it up in the catalog.","Also reserve gloves. Photographs are allowed, but phones stay in the locker."
], Q("Why was the request refused?","It lacked a collection number",["The folder does not exist","Phones are required","Gloves were already reserved"],"Sem o número, o arquivo recusa."),
   Q("What must stay in the locker?","Phones",["Gloves","The catalog","The folder"],"O telefone fica no armário."))

C("m1u","mid",[
"The client moved the review to Thursday at four.","Did the slides change too?","Use the file I posted at eight this morning.","Not last night's?","No. And I'll lock edits at noon.","Then I'll upload the final numbers before noon."
], Q("When is the review?","Thursday at four",["This morning at eight","Noon today","Last night"],"O cliente mudou para quinta às quatro."),
   Q("What will the man do before noon?","Upload the final numbers",["Lock the file himself","Cancel the review","Use last night's slides"],"Ele vai enviar os números finais antes do meio-dia."))

C("m1l","easy",[
"What time is dinner?","From five to seven in the dining hall.","Is Saturday the same?","Saturday is brunch only, ten to one.","Then I'll go at six today.","The line is shorter after 6:30."
], Q("When is dinner served today?","From five to seven",["Ten to one","All night","Only at 6:30"],"O jantar é das cinco às sete."),
   Q("What is different on Saturday?","There is brunch instead of the usual dinner hours",["Dinner is longer","The hall is closed all day","The line starts at five"],"Sábado é brunch, das dez à uma."))

C("m1l","easy",[
"Can I pay with a card?","Yes, or with cash at the counter.","I only have my phone.","A phone payment works if the app is the campus card.","I'll try that.","Pay before you sit. They don't come to the table."
], Q("Where should the woman pay?","At the counter, before she sits",["At the table","After the meal","Only with cash"],"Não pagam na mesa."),
   Q("When does a phone payment work?","If the app is the campus card",["On every phone","Only on Saturday","It never works"],"O aplicativo precisa ser o cartão do campus."))

C("m2","mid",[
"The museum study room is open late this week.","Until midnight?","Monday through Thursday. Pack up ten minutes early.","Can I bring a snack?","No food near the art. There's a bench in the lobby.","I'll eat there first and then go in."
], Q("How late is the study room open?","Until midnight, Monday through Thursday",["All weekend","Ten minutes only","It is closed this week"],"O horário estendido vai até meia-noite nesses dias."),
   Q("Where can the man eat?","On a bench in the lobby",["Next to the art","In the study room","He cannot eat on campus"],"Comida não pode perto da arte; o banco do saguão pode."))

C("m2","easy",[
"Did maintenance fix the light?","Not yet. They come tomorrow morning.","It's hard to read in here.","Use the lamp from the lounge. I'll get it.","Thank you.","Leave it by the window so they see which fixture failed."
], Q("When will maintenance come?","Tomorrow morning",["Tonight","Next month","They already finished"],"Eles vêm amanhã de manhã."),
   Q("Why should the lamp be by the window?","So workers can see which light failed",["Because the lounge is closed","To hide the lamp","The window is the broken part"],"A posição mostra qual luminária falhou."))

C("m2","mid",[
"Spring advising opens Wednesday at nine.","I'm on academic warning.","Then wait for the email before you choose.","I was going to register at nine.","Don't. The portal will block you.","All right. I'll watch my inbox."
], Q("What should the man do?","Wait for an email before choosing classes",["Register at nine anyway","Skip advising","Change his warning status himself"],"Quem está em advertência espera o e-mail."),
   Q("What will happen if he tries to register at nine?","The portal will block him",["He will be first in line","His warning will disappear","The office will call immediately"],"A mulher diz que o portal bloqueia."))

C("m2u","hard",[
"Orders after 2 p.m. are pulled the next business day.","I needed the letter today.","Then you should have requested it this morning.","Can I read a digital copy instead?","Only if the collection allows it. This one doesn't.","I'll come back tomorrow and bring gloves for the photographs."
], Q("Why can't the woman get the letter today?","She ordered it after 2 p.m.",["The collection is digital","Gloves are forbidden","Tomorrow is not a business day"],"Pedidos depois das 14h saem no dia útil seguinte."),
   Q("What is true of a digital copy?","This collection does not allow one",["Every letter is online","It arrives faster after 2 p.m.","It replaces gloves"],"Esta coleção não permite cópia digital."))

C("m2u","mid",[
"The van leaves at 7:10 and will not wait.","What if I miss it?","You must not drive yourself to the site.","Is lunch included?","No. And the form is due by 5 tomorrow. Email won't count.","I'll sign it tonight and pack food."
], Q("What is forbidden if someone misses the van?","Driving themselves to the site",["Signing the form","Packing food","Arriving at 7:10"],"O formulário proíbe ir de carro por conta."),
   Q("What will the man do?","Sign the form tonight and pack food",["Email the form tomorrow","Drive to the site","Skip lunch and the form"],"Ele vai assinar hoje e levar comida."))

C("m2l","easy",[
"The bookstore buys used novels on Friday from ten to two.","Do they take any book?","Not if there's heavy writing in it.","Mine is clean. I'll bring my ID.","Good. They won't buy it without identification.","I'll come at ten so I'm early."
], Q("Which books are refused?","Books with a lot of writing in them",["Clean novels","Books brought at ten","Books with an ID"],"Muita escrita impede a compra."),
   Q("Why will the woman come at ten?","To be early",["Because the store closes at ten","To avoid showing ID","To sell a marked book"],"Ela quer chegar cedo."))

C("m2l","easy",[
"Free film tonight at seven in Hall C.","Can I save you a seat?","No saved seats. Doors open at 6:40.","Then I'll meet you at the door.","Students only, so bring your card.","I have it. The film is about ninety minutes."
], Q("What is not allowed?","Saving seats",["Arriving at 6:40","Bringing a student card","Meeting at the door"],"Não se guarda lugar."),
   Q("How long is the film?","About ninety minutes",["Seven hours","Until 6:40","All night"],"A fala final diz noventa minutos."))

for pool, level, lines, questions in specs:
    add_conv(pool, level, lines, questions)
print("conversations", len(convs))
from collections import Counter
print(Counter(c["pool"] for c in convs))
dump("conversation", convs)
