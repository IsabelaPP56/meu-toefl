import random, sys
sys.path.insert(0, "/workspace/tools")
from bank_common import dump, words, mc

def Q(stem, correct, wrongs, why):
    opts = [correct, *wrongs]
    assert len(opts) == 4
    order = [0, 1, 2, 3]
    random.Random(stem).shuffle(order)
    shuffled = [opts[i] for i in order]
    return mc(stem, shuffled, order.index(0), why)

# ---------- announcements ----------
anns = []
def add_ann(pool, level, setting, script, q1, q2):
    while len(words(script)) < 42:
        script += " Please share this update with classmates who need it."
    wc = len(words(script))
    assert 40 <= wc <= 85, (pool, setting, wc)
    anns.append({"id": f"ann{len(anns)+1:02d}", "pool": pool, "level": level, "setting": setting,
                 "script": script, "questions": [q1, q2]})

def closure(pool, level, place, when, reason, alt):
    script = (f"Attention, students. The {place} will be unavailable {when} because of {reason}. "
              f"Please use {alt} instead. We plan to reopen as soon as the work is finished. "
              f"Check the campus app tonight if you need another update.")
    add_ann(pool, level, f"Announcement about the {place}", script,
            Q("What is the main purpose of the announcement?", f"To explain a temporary closure of the {place}",
              ["To cancel the semester", "To advertise a new degree", "To hire staff"],
              "O aviso existe para comunicar o fechamento temporário."),
            Q("What should students do in the meantime?", f"Use {alt}",
              ["Wait inside the closed space", "Repair the problem themselves", "Skip all classes"],
              "A ação substituta é dita no aviso."))

practice_c = [
("music practice rooms","on Thursday from 2 to 4","piano tuning","the basement rooms in the arts building"),
("health clinic","on Tuesday morning","staff training","the urgent desk in the campus center"),
("bike garage","on Friday afternoon","a door repair","the outdoor racks by the library"),
("quiet reading room","on Monday from 1 to 3","window repairs","the tables on the second floor"),
("computer lab","on Wednesday night","an electrical test","the all-night lab in the science building"),
("recording studio","on Saturday morning","equipment cleaning","the media lab next door"),
("greenhouse","on Thursday afternoon","a safety inspection","the outdoor beds behind biology"),
("print shop","on Tuesday from 11 to 1","a machine repair","the self-service printers in the library"),
("student lounge","tomorrow from 1 to 3","a leaking pipe","the campus café"),
("language lab","next Monday at noon","a software update","the open computers in the library"),
]
for row in practice_c:
    closure("practice","mid",*row)

events = [
("practice","mid","A professor speaking in class",
 "Good afternoon. Dr. Ibarra will speak about urban trees this Thursday at 4 p.m. in Room 210. Arrive a little early if you want a handout, because only forty copies were printed. The talk is free for every major.",
 "To announce a guest talk","To close Room 210 for the month","To assign a new textbook","To cancel Thursday classes",
 "Why does the speaker mention the handouts?","There are only forty copies","They are required for a grade","They cost five dollars","They will be mailed later"),
("practice","mid","A staff member in a student lounge",
 "The scholarship workshop on budgets has moved from Friday to Monday at the same hour, 3 p.m., in the career center. If you already registered, do not sign up again. Bring a laptop if you have one.",
 "To report a new day for a workshop","To cancel scholarships","To close the career center","To introduce a new major",
 "What should students who already registered do?","Attend on Monday without a new form","Register a second time","Pay a fee","Bring a printed essay"),
("practice","mid","An announcement after a competition",
 "Congratulations to the debate team, which reached the national semifinals last weekend. A short reception is tomorrow at 5 p.m. in the student lounge. Friends are welcome, but please leave large bags at the desk.",
 "To honor the team and invite people to a reception","To announce a new course","To warn that bags were stolen","To cancel a competition",
 "What should guests do with large bags?","Leave them at the desk","Carry them into the lounge","Mail them home","Give them to the captain"),
("practice","mid","A weather announcement",
 "Because of a storm warning, evening classes in the north building will meet online tonight. Instructors will post a link by 4 p.m. If your class is in another building, plan to meet in person unless you hear otherwise.",
 "To explain which classes will meet online","To cancel the whole day","To close the dorms","To move every class outdoors",
 "What should students in other buildings assume?","They still meet in person unless told otherwise","Every class is canceled","They must go to the north building","Links arrive tomorrow"),
("practice","mid","A gym lobby announcement",
 "The campus blood drive is tomorrow from 10 a.m. to 3 p.m. in the gym lobby. Please eat a normal meal beforehand and bring identification. Appointments are preferred, but a few walk-in chairs will stay open.",
 "To invite people to give blood","To close the gym all week","To announce a sports final","To require a medical course",
 "What should donors bring?","Identification","A doctor's letter","Sports clothes","Cash payment"),
("practice","mid","A library announcement",
 "A black tablet in a gray case was left in the science library on Tuesday. If you found it, please take it to the circulation desk. The owner has locked the screen but still needs the notes saved on the device.",
 "To recover a lost tablet","To sell tablets","To change library hours","To warn about a theft ring",
 "Where should the tablet be taken?","To the circulation desk","To the owner's classroom","To the gym","Home for a week"),
("practice","mid","A housing announcement",
 "Starting next Monday, guests must be met at the front desk of the residence halls after 8 p.m. Please do not prop side doors open. The change is meant to keep the buildings safer on weeknights.",
 "To explain a new evening entry rule","To close the halls","To ban all guests forever","To move students to new rooms",
 "What should hosts do after 8 p.m.?","Meet guests at the front desk","Leave a side door open","Email security the next day","Wait only in their rooms"),
("practice","mid","A box-office announcement",
 "Ten student tickets for Saturday's concert will be released at noon today. Line up at the box office, and each person may buy two tickets. The dress rehearsal itself is closed to the public.",
 "To explain how to get concert tickets","To cancel the concert","To open the rehearsal to everyone","To hire musicians",
 "How many tickets may one person buy?","Two","Ten","One","As many as they want"),
("practice","mid","An advising announcement",
 "Spring course advising opens online at 9 a.m. on Wednesday. Students on academic warning should wait for an email before choosing classes. Everyone else may use the usual portal.",
 "To announce when advising opens","To cancel spring courses","To close the portal permanently","To require paper forms from all students",
 "Who should wait for an email?","Students on academic warning","Every first-year student","Visiting families","Orchestra members only"),
("practice","mid","A museum announcement",
 "The museum study room will stay open until midnight Monday through Thursday of exam week. Please pack up ten minutes early so staff can lock the galleries. Food is still not allowed near the art.",
 "To extend study hours during exams","To close the museum","To allow food near the paintings","To cancel exams",
 "What must visitors do before closing?","Pack up about ten minutes early","Leave notes overnight","Eat in the gallery","Stay on Friday too"),
]
for pool, level, setting, script, purpose, w1, w2, w3, dq, da, b, c, d in events:
    add_ann(pool, level, setting, script,
            Q("What is the main purpose of the announcement?", purpose, [w1, w2, w3], "O propósito é a ação prática anunciada logo no início."),
            Q(dq, da, [b, c, d], "Esse detalhe é dito de forma explícita."))

# mocks: 2 each pool
mock_anns = [
("m1","mid","the east shuttle stop","all this week","road construction","the stop beside the science library"),
("m1","mid","the pottery studio","on Wednesday afternoon","a kiln inspection","the drawing room upstairs"),
("m1u","hard","the archive reading room","on Friday morning","a fire-alarm test","the microfilm desk in the main library"),
("m1u","hard","the night bus","after 9 p.m. tonight","a driver shortage","the regular day shuttle timetable posted online"),
("m1l","easy","the campus café","this Sunday morning","a deep clean","the dining hall"),
("m1l","easy","locker room B","today from 2 to 3","floor cleaning","locker room A"),
("m2","mid","the rooftop garden","tomorrow afternoon","high winds","the indoor plant room"),
("m2","mid","the language exchange table","this Thursday","a room conflict","the lobby of the humanities building"),
("m2u","hard","the microscopy lab","on Monday from 8 to 10","a calibration","the imaging suite next door, by appointment"),
("m2u","hard","the late-night shuttle to the station","tonight only","a road closure","the city bus on College Avenue"),
("m2l","easy","the tennis courts","Saturday morning","wet paint","the indoor gym"),
("m2l","easy","the mail room","from noon to one","a staff break","the front desk of the campus center"),
]
for pool, level, place, when, reason, alt in mock_anns:
    closure(pool, level, place, when, reason, alt)
print("ann", len(anns))
dump("announcement", anns)

# ---------- daily life ----------
dailies = []
def add_daily(pool, level, kind, text, questions):
    assert 15 <= len(words(text)) <= 160, (kind, len(words(text)), text[:80])
    assert len(questions) in (2, 3)
    if len(words(text)) < 20 and len(questions) != 2:
        raise AssertionError((len(words(text)), text))
    dailies.append({"id": f"day{len(dailies)+1:02d}", "pool": pool, "level": level, "kind": kind,
                    "text": text, "questions": questions})

shorts = [
("practice","easy","notice","The library will close at 6 p.m. on Friday for electrical repairs. Books due that evening may be returned on Monday without a late fee. The outdoor return box will be locked.",
 [Q("What is the main purpose of the notice?","To explain a temporary closure",["To introduce a new fee","To advertise a course","To ask for book donations"],"O aviso explica o fechamento e a regra dos livros."),
  Q("What can a borrower do with a book due Friday evening?","Return it Monday without a late fee",["Use the outdoor box Friday night","Pay a fee on Saturday","Keep it for a month"],"A frase sobre a segunda-feira sem multa responde isso.")]),
("practice","easy","email","Dear volunteers, training is on Tuesday at 3 p.m. in Room 204. If you attended last year, you may skip the training, but everyone must confirm by Monday noon.",
 [Q("Who may skip the training?","People who attended last year",["Anyone who confirms early","New volunteers","People who arrive after noon"],"A exceção é para quem já fez o treino no ano passado."),
  Q("What must every volunteer do?","Confirm by Monday noon",["Pay a fee","Bring a project","Attend even if they came last year"],"O aviso diz que todos precisam confirmar.")]),
("practice","mid","messages","Mia: The poster is ready, but the printer is broken. Leo: I can print it downtown this afternoon. Mia: Please use the revised file I sent this morning, not yesterday's. Leo: Sure. Could you bring the display stand tomorrow?",
 [Q("What will Leo probably do next?","Print the revised poster",["Repair the campus printer","Rewrite yesterday's file","Buy a display stand"],"Leo aceita imprimir e Mia aponta o arquivo da manhã."),
  Q("Why does Mia mention this morning?","To identify the correct file",["To change the time of the talk","To apologize for being late","To ask for an earlier delivery"],"Ela contrasta o arquivo da manhã com o de ontem.")]),
("practice","easy","schedule","Campus shuttle, week of the 12th. The stop has moved to the east gate because of construction. Departure times are unchanged. Wheelchair assistance requires a call one day ahead.",
 [Q("What has changed?","The departure location",["Ticket prices","Departure times","The phone number of the office"],"O texto diz que o ponto mudou e os horários não."),
  Q("What can be inferred about assistance?","It must be requested in advance",["It is no longer offered","Every rider must call","Construction has ended"],"A ajuda exige um telefonema com um dia de antecedência.")]),
("practice","mid","email","To: members. The fitness center at 25 Orchid Street opens next Monday. Current members may bring guests, and a one-day discount on new memberships will be offered. Reply to RSVP or call 555-0144.",
 [Q("What is the main purpose of the email?","To invite members to a new branch opening",["To close the old center","To hire trainers","To cancel memberships"],"O e-mail anuncia a abertura e convida membros."),
  Q("What can be inferred about the reader?","The reader is already a member",["The reader is a trainer","The reader has already visited the new site","The reader must pay a fine"],"O texto fala com current members.")]),
("practice","easy","menu","Lunch special: lentil soup and salad, 8 dollars, served 11:30 to 2:00. The soup contains no meat. Bread is extra. Students with a meal plan swipe at the register, not at the table.",
 [Q("What is true of the soup?","It contains no meat",["It costs extra","It is served all day","It includes bread"],"A frase diz que a sopa não tem carne."),
  Q("How should meal-plan students pay?","By swiping at the register",["By paying at the table","By bringing cash only","By ordering online the day before"],"O texto indica o caixa, não a mesa.")]),
("practice","mid","form","Workshop reservation. Date: 20 September, 3 p.m. Supplies are provided. Bring your own apron. Cancel at least one day ahead or the fee is kept. Questions: art@campus.edu.",
 [Q("What should the participant bring?","An apron",["Paint","Proof of payment","A friend"],"O formulário pede o avental."),
  Q("What happens if someone cancels on the same day?","The fee is kept",["The fee is returned","The date moves automatically","The apron is mailed"],"Cancelar com menos de um dia faz perder a taxa.")]),
("practice","easy","receipt","Receipt 441. Used textbook, 18 dollars. Campus card discount already applied. Returns are accepted within seven days with this receipt. Opened software codes cannot be returned.",
 [Q("What discount was applied?","A campus card discount",["A seven-day discount","A software discount","No discount"],"O recibo diz que o desconto do cartão já entrou."),
  Q("What cannot be returned?","Opened software codes",["The used textbook","Any item with a receipt","Items bought on campus"],"A última frase exclui códigos de software abertos.")]),
("practice","mid","post","Sofia's market note: Come early for bread, because the bakery stall sells out. Thompson's vegetables are popular for their quality and friendly service. Live music starts at noon. Handmade gifts are upstairs.",
 [Q("Why should shoppers arrive early?","The bread sells out",["Music starts early","Gifts are cheaper in the morning","The market closes at noon"],"O texto liga a ida cedo ao pão que acaba."),
  Q("What is suggested about Thompson's stall?","People like both the food and the service",["It is the cheapest stall","It sells bread","It is upstairs"],"Qualidade e atendimento são a razão da popularidade.")]),
("practice","easy","invoice","Invoice for lab goggles. Amount due: 12 dollars by Friday. Pay online or at the department office. Unpaid invoices block equipment checkout next week.",
 [Q("When is payment due?","By Friday",["Next month","When the goggles arrive","After checkout"],"A data é sexta-feira."),
  Q("What is a consequence of not paying?","The student cannot check out equipment next week",["The course is dropped","The goggles are donated","The invoice disappears"],"A última frase liga a dívida ao bloqueio do equipamento.")]),
]
for row in shorts:
    add_daily(*row)

# longer 3-question practice texts
longs = [
("practice","mid","email",
 "Dear Ms. Nguyen, You are invited to the grand opening of our north gym next Monday at 25 Orchid Street. The visit includes a tour, a short class, and refreshments. Members may bring two guests. A one-day membership discount applies only to people who attend. Please reply by Sunday if you need a parking pass.",
 [Q("What is the main purpose?","To invite a member to an opening",["To offer Ms. Nguyen a job","To close the north gym","To sell parking passes to the public"],"O e-mail é um convite para a abertura."),
  Q("Who can receive the one-day discount?","People who attend the opening",["Anyone who emails on Monday","Only the two guests","People who already have a parking pass"],"O desconto vale para quem comparece."),
  Q("What should Ms. Nguyen do if she needs to park?","Reply by Sunday",["Arrive without writing","Call on Monday morning","Bring two cars"],"O passe de estacionamento depende de resposta até domingo.")]),
("practice","hard","notice",
 "Research participants needed. The sleep lab will pay 20 dollars for a 40-minute afternoon session this month. You must be at least 18, and you cannot take part if you worked a night shift in the past week. Sign up on the lab door, not by email. If you miss your slot without notice, you cannot reschedule this month.",
 [Q("What is required of participants?","They must be at least 18",["They must work night shifts","They must email the lab","They must stay for a full night"],"A idade mínima é uma condição explícita."),
  Q("Who cannot take part?","Someone who worked a night shift in the past week",["Someone who is 19","Someone who signs the door list","Someone who can come in the afternoon"],"O turno noturno recente exclui a pessoa."),
  Q("What happens if a person misses a slot without notice?","They cannot reschedule this month",["They are paid anyway","They may email to choose another day","They must work a night shift"],"A última frase impede remarcar no mesmo mês.")]),
("practice","mid","messages",
 "Advisor: I can meet Thursday at 2 or Friday at 9. Student: Thursday conflicts with my lab, so Friday is better. I want to ask about dropping Chemistry 2. Advisor: Bring the drop form. Friday at 9 is confirmed, but arrive five minutes early because another student is scheduled at 9:20.",
 [Q("Which time did the student choose?","Friday at 9",["Thursday at 2","Friday at 9:20","Thursday after lab"],"O estudante recusa quinta e aceita sexta às 9."),
  Q("What must the student bring?","The drop form",["A lab report","Payment","A friend"],"A orientadora pede o formulário."),
  Q("Why should the student arrive early?","Another meeting starts at 9:20",["The office opens at 9:20","The lab was moved","The form takes an hour"],"Há outro estudante às 9:20.")]),
("practice","mid","ad",
 "Room for rent near campus, available 1 June. 450 dollars a month, including water but not electricity. No smoking. One quiet roommate already lives there and studies most nights. The lease is six months. Email for a visit on weekday evenings only.",
 [Q("What is included in the rent?","Water",["Electricity","Meals","Internet"],"O anúncio inclui água e exclui eletricidade."),
  Q("What can be inferred about the current roommate?","The person wants a quiet household",["The person is leaving on 1 June","The person smokes","The person owns the building"],"Estudar à noite e a regra de silêncio sugerem isso."),
  Q("When can someone see the room?","On weekday evenings",["Any morning","Only on 1 June","Weekends only"],"As visitas são à noite em dias de semana.")]),
("practice","hard","email",
 "To the project team: The client moved the review from Wednesday to Thursday at 4 p.m. Please use the revised slides I uploaded at 8 a.m., not the version from last night. If your section is still in red, it is not ready. I will lock the file at noon, so send final numbers before then. Remote colleagues should join by video; the room holds only six people.",
 [Q("What changed?","The review is on Thursday",["The review was canceled","The file was deleted","The room holds twenty people"],"A revisão saiu de quarta para quinta."),
  Q("Which slides should the team use?","The ones uploaded at 8 a.m.",["Last night's version","Any version in red","The client's old file"],"O e-mail distingue o arquivo das 8 da versão da noite."),
  Q("Why might some people join by video?","The room holds only six people",["The meeting is secret","The file is locked","Thursday is a holiday"],"O limite da sala explica o vídeo.")]),
("practice","mid","schedule",
 "Writing center, exam week. Sunday closed. Monday to Thursday, 10 a.m. to 8 p.m. Friday, 10 a.m. to 2 p.m. Appointments are 25 minutes. Come with a draft and a question. If you are more than ten minutes late, the slot is given to a walk-in.",
 [Q("When is the center closed?","Sunday",["Friday afternoon only","Every morning","Thursday night"],"Domingo está fechado."),
  Q("What should a student bring?","A draft and a question",["A finished grade","Payment","A laptop only"],"O texto pede rascunho e uma pergunta."),
  Q("What happens if someone is ten minutes late?","The slot may go to a walk-in",["The session becomes 50 minutes","The center closes","The draft is corrected overnight"],"Atraso de mais de dez minutos cede o horário.")]),
("practice","easy","post",
 "Club fair table 12 is the gardening group. We meet Thursdays at 5 by the greenhouse. No experience is needed, but closed-toe shoes are required in the beds. Sign the sheet today if you want seeds next week. Dues are five dollars a term and can be paid later.",
 [Q("What is required in the garden beds?","Closed-toe shoes",["Five years of experience","Payment today","A Thursday exam"],"O calçado é obrigatório; a experiência não."),
  Q("What is the purpose of the sheet?","To request seeds for next week",["To pay dues","To skip the meeting","To reserve table 12"],"Assinar é para receber sementes."),
  Q("When can dues be paid?","Later",["Only today","Never","Before every meeting"],"O texto diz que a taxa pode ser paga depois.")]),
("practice","mid","notice",
 "Exam ID check. Bring a physical campus card or a government photo ID. Phone photos of a card will not be accepted. Arrive 15 minutes early. If your name is missing from the list, see the proctor before the test starts, not after. Bags go at the side of the room.",
 [Q("What identification is acceptable?","A physical campus card or a government photo ID",["A phone photo of a card","A friend's card","A printed schedule"],"O aviso aceita cartão físico ou documento oficial."),
  Q("When should a missing name be reported?","Before the test starts",["After the test","The next day","By email only"],"O texto diz para falar com o fiscal antes."),
  Q("Where do bags go?","At the side of the room",["Under the desk","With the proctor's list","Outside the building"],"As bolsas ficam na lateral da sala.")]),
]
for row in longs:
    add_daily(*row)

# mock dailies: each pool needs one 2q and one 3q
mock_daily = {
"m1": ("mid","email","To: students in Biology 1. The Friday lab will meet in Room 18, not Room 12, because Room 12 has no water pressure. Bring the same worksheet. If you already printed a map, ignore the old room number.",
        [Q("Why was the room changed?","Room 12 has no water pressure",["The worksheet changed","Students asked for a larger room","The Friday lab was canceled"],"A causa é a falta de pressão da água."),
         Q("What should students do about an old map?","Ignore the old room number",["Follow it anyway","Draw a new campus","Email the dean"],"O e-mail manda ignorar o número antigo.")]),
"m1b": ("mid","notice","The career center will review résumés on a drop-in basis next Wednesday from 1 to 4 p.m. Appointments are not required that day, but arrive at least twenty minutes before 4 if you want a full review. Bring a printed copy. Coaches will not edit a phone screen.",
         [Q("What is special about next Wednesday?","Résumé reviews do not need an appointment",["The center is closed","Only phone screens are reviewed","The service starts at 4"],"O texto diz que não precisa de hora marcada nesse dia."),
          Q("What must students bring?","A printed résumé",["A phone only","A job offer","Payment"],"É preciso uma cópia impressa."),
          Q("Why arrive twenty minutes before 4?","To allow time for a full review",["Because the door locks at 1","Because coaches leave at 1:20","Because printing takes an hour"],"O prazo garante a revisão completa antes do fim.")]),
}
# I'll add explicit mock entries below instead of this half structure.
print("daily practice", sum(1 for d in dailies if d["pool"]=="practice"), "qs", sum(len(d["questions"]) for d in dailies))

mock_specs = [
("m1","easy","notice","Lab move: Friday's biology lab is in Room 18, not Room 12. Room 12 has no water. Bring the same worksheet.",
 [Q("Where will the lab meet?","Room 18",["Room 12","The greenhouse","Online"],"O aviso troca a sala para a 18."),
  Q("Why did the room change?","Room 12 has no water",["The worksheet changed","Students voted","The class grew"],"A causa é a falta de água.")]),
("m1","mid","email","Dear project group, I posted the final chart at 9 a.m. Please replace last night's figure before our 2 p.m. call. If your comments are still in the margin, I have not accepted them yet. Join by video if you are off campus; the room fits five.",
 [Q("Which chart should the group use?","The one posted at 9 a.m.",["Last night's figure","Any margin comment","A chart from another class"],"O e-mail manda substituir a figura da noite."),
  Q("What do margin comments mean?","They have not been accepted yet",["They are the final text","They must be deleted unread","They move the call to 9"],"Comentários na margem ainda não foram aceitos."),
  Q("Why might someone join by video?","The person is off campus or the room is small",["The chart failed to upload","The call was canceled","Five people already refused"],"O vídeo é para quem está fora ou por causa do tamanho da sala.")]),
("m1u","hard","email","To: graduate researchers. The microscope calendar now requires a three-day lead time, not one day, because too many unused bookings blocked other labs. Cancel by noon the day before or the slot still counts against your group. First-time users must complete the safety module before the booking is confirmed.",
 [Q("What policy changed?","Bookings now need three days' notice",["The microscope was removed","Safety training was canceled","Groups may book the same day"],"O prazo passou de um dia para três."),
  Q("What happens if a group cancels late?","The slot still counts against the group",["The fee is refunded","Another lab is charged","The safety module is waived"],"Cancelar depois do meio-dia anterior ainda conta."),
  Q("What can be inferred about first-time users?","They are not confirmed until they finish safety training",["They may skip the calendar","They have priority over all labs","They pay a higher fee"],"A reserva só confirma depois do módulo de segurança.")]),
("m1u","hard","notice","Archive request. Orders placed after 2 p.m. are pulled the next business day. Fragile items cannot leave the reading room, and gloves are required for photographs. Staff will refuse a request that lacks a collection number. Phones stay in the locker.",
 [Q("When are afternoon orders pulled?","The next business day",["Immediately","On weekends only","After the reader leaves"],"Pedidos depois das 14h saem no dia útil seguinte."),
  Q("What is required for photographs?","Gloves",["A flash","A phone","Permission to take items home"],"Fotografar exige luvas.")]),
("m1l","easy","menu","Today's lunch: rice, beans, and salad for 7 dollars, from 11 to 2. Water is free. Pay at the counter before you sit.",
 [Q("How much is lunch?","7 dollars",["Free","11 dollars","2 dollars"],"O preço está no aviso."),
  Q("When should students pay?","Before they sit",["After the meal","At 2 only","Online yesterday"],"O pagamento é no balcão antes de sentar.")]),
("m1l","easy","messages","Ana: Can you bring the adapter to the study group? Ben: Yes. Which room should I come to? Ana: Room 106, at 4. Please also bring the printed map from yesterday. Ben: I'll be there a few minutes early.",
 [Q("What will Ben bring?","The adapter",["Lunch","A book","A chair"],"Ana pede o adaptador e Ben aceita."),
  Q("Where will they meet?","Room 106",["Room 4","The library","Ben's dorm"],"Ana responde 106, às 4."),
  Q("What else does Ana want?","The printed map",["A new adapter","Lunch for Ben","A different room"],"Ela pede também o mapa impresso.")]),
("m2","mid","schedule","Pool hours, exam week: Monday to Thursday 7 a.m. to 9 p.m. Friday 7 a.m. to 5 p.m. The pool is closed Saturday for a swim meet. Lanes 1 and 2 are reserved for classes until noon on weekdays.",
 [Q("Why is the pool closed on Saturday?","There is a swim meet",["It is exam week","The heater failed","Classes use every lane"],"O sábado fecha por causa da competição."),
  Q("Which lanes are limited in the morning?","Lanes 1 and 2",["Every lane","Only lane 5","The weekend lanes"],"As raias 1 e 2 ficam para as aulas até o meio-dia."),
  Q("What is true on Friday?","The pool closes at 5 p.m.",["The pool is closed all day","It stays open until 9","There is no class"],"Sexta vai só até as 17h.")]),
("m2","easy","receipt","Café receipt. Tea, 2 dollars. Muffin, 3 dollars. Campus discount, 50 cents. Total paid, 4.50. No refunds on bakery items after you leave the counter.",
 [Q("What was the discount?","50 cents",["2 dollars","4.50","3 dollars"],"O desconto listado é de 50 centavos."),
  Q("What cannot be refunded after you leave?","Bakery items",["Tea","The campus discount","Any drink"],"Itens de padaria não voltam depois do balcão.")]),
("m2u","hard","email","Dear editors, I am sending a revised paragraph, not a new article. Please replace only the second paragraph of the version dated 3 March. The data in Table 1 are unchanged. I will be away from email on Friday, so a question after Thursday noon may wait until Monday.",
 [Q("What should the editors replace?","Only the second paragraph of the 3 March version",["The whole article","Table 1","Every paragraph"],"O pedido é pontual: só o segundo parágrafo."),
  Q("What is true of Table 1?","Its data did not change",["It was deleted","It is the revised paragraph","It arrives on Monday"],"A tabela permanece igual."),
  Q("What can be inferred about Friday?","The writer may not answer email that day",["The article will be published Friday","Editors must not write on Monday","Table 1 changes on Friday"],"A autora estará longe do e-mail na sexta.")]),
("m2u","hard","form","Field trip waiver. The van leaves at 7:10 a.m. and will not wait. Students who miss it must not drive themselves to the site. Lunch is not provided. A signed form is due by 5 p.m. tomorrow, and late forms will not be accepted by email.",
 [Q("What happens if a student misses the van?","They must not drive themselves to the site",["The van returns","They may send an email","Lunch is provided on the road"],"O formulário proíbe ir de carro por conta própria."),
  Q("When is the form due?","By 5 p.m. tomorrow",["At 7:10 a.m.","After the trip","Any time by email"],"O prazo é 17h de amanhã.")]),
("m2l","easy","notice","The bookstore will buy used novels this Friday from 10 to 2. Bring your ID. Books with heavy writing in them will not be purchased.",
 [Q("When will the bookstore buy books?","Friday from 10 to 2",["Every morning","Saturday","Friday night"],"O horário está no aviso."),
  Q("Which books will be refused?","Books with heavy writing in them",["Used novels","Books with an ID","All paperbacks"],"Muita escrita no livro impede a compra.")]),
("m2l","easy","ad","Free film on Wednesday at 7 in Hall C. Doors open at 6:40. Students only. No saved seats. The film lasts about ninety minutes.",
 [Q("Who may attend?","Students",["Anyone in the city","Only film majors","Children"],"O anúncio diz students only."),
  Q("What is not allowed?","Saving seats",["Arriving at 6:40","Sitting in Hall C","Coming on Wednesday"],"Não dá para guardar lugar."),
  Q("About how long is the film?","Ninety minutes",["Seven hours","Six minutes","All evening until midnight"],"O anúncio diz cerca de noventa minutos.")]),
]
for pool, level, kind, text, qs in mock_specs:
    add_daily(pool, level, kind, text, qs)

print("daily", len(dailies), "practice q", sum(len(d["questions"]) for d in dailies if d["pool"]=="practice"))
dump("daily", dailies)
