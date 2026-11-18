"""Original model answers. Not copied from ETS or TST Prep."""
import json
import re
from pathlib import Path

P = Path("/workspace/site/data/parts")

def load(name):
    base = json.loads((P / f"{name}.json").read_text())
    extra = json.loads((P / "scale.json").read_text()).get(name, [])
    return base + extra

def words(s):
    return re.findall(r"[A-Za-z0-9']+", s)

NOTE_W = "A banda 5–6 cobre os três pedidos, com um motivo e um pedido educado. A versão B2 faz o mesmo com frases mais curtas. As duas são autorais, não são um gabarito da ETS."
NOTE_D = "A versão alta abre com a posição, cita os dois colegas, dá um exemplo com uma situação concreta e fecha com um limite. A versão B2 faz o mesmo em menos frases. Meta realista: banda 4, com cerca de 100 palavras e um exemplo."
NOTE_R = "Na prova, a meta 5 é repetir a frase inteira. Uma troca pequena que não muda o sentido fica perto de 4, que é B2. Treine a frase exata."
NOTE_I = "A resposta alta começa na pergunta, dá um motivo e um exemplo com tempo ou lugar. A versão B2 faz o mesmo com menos palavras. Em 45 segundos, essa estrutura vale mais do que um texto decorado."

def pack(high, b2, phrases, note):
    phrases = [p for p in phrases if p in high]
    return {"high": high.strip(), "b2": b2.strip(), "phrases": phrases, "note": note}

EMAILS = {}

def add_email(i, high, b2):
    EMAILS[i] = pack(high, b2, ["I am writing because", "Could you please", "Thank you for considering"], NOTE_W)

add_email("em01", """
Dear Professor Alvarez,

I am writing because I missed yesterday's biology lab. A clinic visit ran long, so I could not attend.

Could you please send the worksheet or the slides from that session? I would also like to review the experiment. I can come to your office on Thursday at 3 p.m., or Friday morning if that is better for you.

Thank you for considering this.
Best regards
""", """
Dear Professor Alvarez,

I am writing because I missed the lab. My clinic visit ran long, and I could not attend.

Could you please send the worksheet or the slides? I can come to your office on Thursday to review the experiment.

Thank you for considering this.
Best regards
""")

add_email("em02", """
Dear Registrar,

I am writing because my family name is misspelled on my student record. The incorrect spelling is missing one letter. The correct spelling is the one on my passport.

Could you please tell me how long the processing time will be after I send a copy of that document?

Thank you for considering this.
Best regards
""", """
Dear Registrar,

I am writing because my name is misspelled. The incorrect form is on the record, and the correct spelling is on my passport.

Could you please tell me the processing time?

Thank you for considering this.
Best regards
""")

add_email("em03", """
Dear Sam,

I am writing because I have a job interview on Friday, so I cannot present that day. There is a conflict with our seminar.

Could you please trade dates with me? I would take your original date, and you would take my Friday slot. I can also share my slides early so the switch is easy.

Thank you for considering this.
Best regards
""", """
Dear Sam,

I am writing because my interview is on Friday, and I cannot present. Could you please switch dates? I will take your original date.

Thank you for considering this.
Best regards
""")

add_email("em04", """
Dear Film Club,

I am writing because I would like to suggest a screening of a short documentary about city libraries. The film fits the club because it leaves room for a discussion afterward.

Could you please hold it on a Thursday evening in the small screening room? I can also volunteer. What do you need me to do?

Thank you for considering this.
Best regards
""", """
Dear Film Club,

I am writing because I have a film for next month. It fits a short discussion. Could you please use a Thursday evening and a small room? I can volunteer. What do you need?

Thank you for considering this.
Best regards
""")

add_email("em05", """
Dear Circulation Desk,

I am writing because a book I had reserved was returned to the shelf. The title is Urban Trees. I was off campus when the hold expired, so I could not pick it up.

Could you please place a new hold on the same book?

Thank you for considering this.
Best regards
""", """
Dear Circulation Desk,

I am writing because my hold expired while I was away. The title is Urban Trees. Could you please place a new hold?

Thank you for considering this.
Best regards
""")

add_email("em06", """
Dear Building Manager,

I am writing because the heater in apartment 4B has been out for three days. The room is too cold to study or sleep well.

Could you please schedule a repair visit? I am home on Tuesday after 4 p.m. and on Wednesday morning.

Thank you for considering this.
Best regards
""", """
Dear Building Manager,

I am writing because the heater has been cold for three days. I cannot study or sleep well. Could you please send a repair visit? I am home Tuesday after 4 and Wednesday morning.

Thank you for considering this.
Best regards
""")

add_email("em07", """
Dear Professor Okonkwo,

I am writing because one line of the essay prompt is unclear to me. It says we should use reliable sources, but it does not say what that includes.

Could you please tell me whether a news article may be used? An example of an acceptable source would help me start.

Thank you for considering this.
Best regards
""", """
Dear Professor Okonkwo,

I am writing because the prompt is unclear. Could you please tell me if a news article is allowed? I would like one example of an acceptable source.

Thank you for considering this.
Best regards
""")

add_email("em08", """
Dear Housing Office,

I am writing because my room faces a loading dock. The noise starts at dawn, and I lose sleep before class.

Could you please tell me what other rooms are available next month? I am ready to switch.

Thank you for considering this.
Best regards
""", """
Dear Housing Office,

I am writing because of the noise from the loading dock at dawn. It affects my sleep and my class. Could you please tell me if another room is available next month?

Thank you for considering this.
Best regards
""")

add_email("em09", """
Dear Club Secretary,

I am sorry to cancel the plan to host this week's meeting. I am writing because my residence has a fire drill that evening, so the room will not be quiet.

Could you please ask someone else, or use the campus lounge? I can still bring the notes.

Thank you for considering this.
Best regards
""", """
Dear Club Secretary,

I am sorry. I cannot host because of a fire drill. Could you please use the campus lounge or another room?

Thank you for considering this.
Best regards
""")

add_email("em10", """
Dear Professor Silva,

I am writing because I am applying for a research assistant post. I took your lab course last spring, and the deadline for the application is next Friday.

Could you please write a recommendation if you feel you know my work well enough? I can send the description today.

Thank you for considering this.
Best regards
""", """
Dear Professor Silva,

I am writing because I need a recommendation for a research assistant post. I took your lab course, and the deadline is next Friday. Could you please let me know if you can write it?

Thank you for considering this.
Best regards
""")

add_email("em11", """
Dear Landlord,

I am writing because my parents will visit for three nights, from the 12th to the 15th. The lease is not clear about this.

Could you please tell me whether three nights are allowed? I can send their names in advance.

Thank you for considering this.
Best regards
""", """
Dear Landlord,

I am writing because my parents will stay three nights, from the 12th to the 15th. Could you please confirm that this is allowed? I can send their names in advance.

Thank you for considering this.
Best regards
""")

add_email("em12", """
Dear Jordan,

I am writing to confirm our grammar session on Thursday at the library. I would like to review the introduction of my draft.

Could you please bring a printed copy if you can? I will bring mine as well.

Thank you for considering this.
Best regards
""", """
Dear Jordan,

I am writing to confirm Thursday at the library. I want to review the introduction of the draft. Could you please bring a printed copy?

Thank you for considering this.
Best regards
""")

add_email("em13", """
Dear Student Health Center,

I am writing because a form for my program is due before my checkup. The appointment is in three weeks, which is too late.

Could you please move my appointment earlier? I am free on Tuesday and Thursday morning.

Thank you for considering this.
Best regards
""", """
Dear Student Health Center,

I am writing because a form is due before my checkup. Could you please give me an earlier appointment? I am free Tuesday and Thursday morning.

Thank you for considering this.
Best regards
""")

add_email("em14", """
Dear Professor Rahman,

I am writing because one member of our project group has not answered messages for a week. The rest of us have already finished the shared slides and the method section.

Could you please advise how the grade should be divided if the silence continues?

Thank you for considering this.
Best regards
""", """
Dear Professor Rahman,

I am writing because a group member has not answered for a week. We have already finished the slides. Could you please tell us how the grade would be divided?

Thank you for considering this.
Best regards
""")

add_email("em15", """
Dear Bookstore,

I am writing because I bought the sociology textbook yesterday, but I received an older edition. The professor requires the newer edition for the course, and the chapter numbers do not match.

Could you please exchange it or give me a refund? I still have the receipt.

Thank you for considering this.
Best regards
""", """
Dear Bookstore,

I am writing because the sociology edition I received is not the newer one the professor requires. Could you please exchange it or refund it?

Thank you for considering this.
Best regards
""")

add_email("em16", """
Dear Photography Club,

I am writing because my visual studies class has a night-photo assignment. Could you please let me borrow a camera on Monday and Tuesday?

I will return it in the same condition on Wednesday morning.

Thank you for considering this.
Best regards
""", """
Dear Photography Club,

I am writing because I need a camera for a night class assignment on Monday and Tuesday. I will return it in the same condition. Could you please let me borrow one?

Thank you for considering this.
Best regards
""")

add_email("em17", """
Dear Advisor,

I am writing because I hope to postpone one course next term. I need a lighter spring so I can meet a family responsibility.

Could you please tell me whether dropping that course would delay graduation?

Thank you for considering this.
Best regards
""", """
Dear Advisor,

I am writing because I want to postpone one course for a family responsibility. Could you please tell me if that delay affects graduation?

Thank you for considering this.
Best regards
""")

add_email("em18", """
Dear Laundry Desk,

I am writing because machine 4 charged my card twice for one wash on March 3 at 7 p.m. I ran a single cycle, and the reader took the money two times.

Could you please put the extra money back on the card as a refund?

Thank you for considering this.
Best regards
""", """
Dear Laundry Desk,

I am writing because machine 4 charged me twice on March 3 at 7 p.m. Could you please refund the second charge on the card?

Thank you for considering this.
Best regards
""")

add_email("em19", """
Dear Professor Nguyen,

I am writing because a train delay will make me about twenty minutes late for the midterm.

Could you please let me start late? I also need to know how much time I will still have.

Thank you for considering this.
Best regards
""", """
Dear Professor Nguyen,

I am writing because my train is late, so I will arrive about twenty minutes late. Could you please let me start late, and tell me how much time will be left?

Thank you for considering this.
Best regards
""")

add_email("em20", """
Dear Mei,

I am sorry about this week. I am writing because my lab conflicts with our usual time.

Could you please meet at another time, either Thursday at 5 or Friday at noon?

Thank you for considering this.
Best regards
""", """
Dear Mei,

I am sorry. My lab conflicts with our meeting. Could you please meet Thursday at 5 or Friday at noon instead?

Thank you for considering this.
Best regards
""")

add_email("em-m1", """
Dear Professor Costa,

I am writing because rain canceled the soil samples for my geography field report, so I could not collect them before Monday.

Could you please give me a three-day extension? On the original date I can still submit my notes and the map.

Thank you for considering this.
Best regards
""", """
Dear Professor Costa,

I am writing because the rain meant I could not collect the samples. Could you please give me three more days? I can submit my notes on the original date.

Thank you for considering this.
Best regards
""")

add_email("em-m2", """
Dear Help Desk,

I am writing because the files for my statistics course will not open. The error says the format is not supported. I already tried a restart, and the file still fails.

Could you please offer an appointment or a remote help session?

Thank you for considering this.
Best regards
""", """
Dear Help Desk,

I am writing because my statistics course files show an error. I already restarted the laptop. Could you please book a remote help session?

Thank you for considering this.
Best regards
""")

def advisor_email(n):
    high = f"""Dear Advisor,

I am writing because my lab for course {n} was moved onto the same hour as a required workshop. The conflict means I cannot be in both rooms.

I can still attend the workshop, because that session meets only once. Could you please tell me what form or approval I need so I can join another lab section?

Thank you for considering this.
Best regards"""
    b2 = f"""Dear Advisor,

I am writing because my lab for course {n} and a required workshop are at the same time. I can still attend the workshop. Could you please tell me what approval or form I need?

Thank you for considering this.
Best regards"""
    add_email(f"em-mock{n}", high, b2)

for n in range(3, 11):
    advisor_email(n)

# Discussions: stance, example, limit. Names come from the item.
DISC = {
    "di01": ("a short public-speaking course should be required", "in a lab section, a clear idea of mine was ignored because I could not explain it in one minute", "the course should be one credit and offered in the evening, so heavy majors are not punished"),
    "di02": ("some downtown parking should become bus and bike lanes", "last month I lost forty minutes looking for a space and then walked farther than the bus would have taken me", "delivery vans and people who cannot cycle still need a few spaces near the shops"),
    "di03": ("a small participation grade can help", "when my seminar gave two points for a prepared comment, I read the article the night before instead of staying quiet", "the points should reward a prepared comment, not the fastest speaker"),
    "di04": ("single-use bottles should leave ordinary campus sales", "I already refill at the library, and the bottle I bought between classes was a habit, not a need", "the gym and visitor desks should still sell water when someone arrives without a bottle"),
    "di05": ("popular majors should not cost more", "a friend almost left engineering when she heard a lab fee might rise, even though she was doing well", "crowded programs can charge a lab fee for materials, not a higher tuition for the whole major"),
    "di06": ("dorm students should show the vaccinations the clinic lists", "in a shared hall, one illness moved through our floor in a week and closed a study group", "students with a medical reason need a clear form to wait, not a lost housing place"),
    "di07": ("photos without flash should be allowed", "a picture of a composition helped me write about it later, when I could not return to the museum", "staff can still stop photos when a crowd blocks the painting"),
    "di08": ("online group work can match an in-person meeting when the rules are clear", "last term my group posted a short agenda and finished the slides before the video call, so nobody hid on mute", "a library table is still better for the one meeting that decides the argument"),
    "di09": ("virtual labs can replace some introductory lessons", "a simulation let every student repeat a step that only two people could try at the real bench", "the smell, the timing, and the small mistakes of a live lab should stay in the course later"),
    "di10": ("laptops should be closed during most of a lecture", "I sit behind screens, and I notice shopping sites more often than the diagram", "a student who types faster, or who needs to search one term, should be able to ask for an exception"),
    "di11": ("students should memorize a small set of dates", "I could not order two causes until I knew which year came first, so the story stayed fuzzy", "a long list of years is less useful than a short timeline tied to causes"),
    "di12": ("the cafeteria should drop fried food on ordinary weekdays", "the meal plan is where many students eat, so the daily menu teaches a habit", "a fried option once a week is enough, or students will buy the same food off campus"),
    "di13": ("beginner courses should limit code-generation tools", "when a tool wrote a loop for me, I could not explain the bug in the next class", "later courses should teach students to check and test generated code, not pretend the tools do not exist"),
    "di14": ("student voting should be easy, not compulsory", "last year our council was chosen by a small group, so a simple online ballot would help", "treating a missed vote as a penalty punishes new students who do not know the candidates yet"),
    "di15": ("practice rooms should stay free", "a small hourly fee would keep me out during the weeks before a recital, which is when I need the room most", "a booking limit of one hour would free rooms without charging the students who already pay tuition"),
    "di16": ("introductory geography should include a field trip", "a slope on a map made sense only after I stood on a similar hill and saw where the water ran", "students who work or commute need a second date, or a local walk they can do alone"),
    "di17": ("clubs should not sign exclusive contracts", "after the business club took a gift from one company, other speakers were harder to invite", "a public gift is fine when the terms are open and no other company is blocked"),
    "di18": ("universities should offer local languages as well as international ones", "in my city, many families use a language that never appears in the course list", "students with few free terms can choose, so a local language is an option, not a new requirement for everyone"),
    "di19": ("new campus buildings should use less glass", "full glass walls look open, but in our climate they heat the room and the blinds stay down", "glass still helps at an entrance, where students can see activity and walk in"),
    "di20": ("detection software can be a first signal, not a judge", "a strange paragraph should lead to a conversation, not an automatic zero", "the tools are often wrong, and a false flag can frighten a student who simply writes in a plain style"),
    "di-m1": ("campus cafes should keep cash", "a visitor without a campus card had to leave the line, and a small purchase should not need a full account", "card lines can stay faster if one register still takes cash"),
    "di-m2": ("first-year students should live on campus when a room is free", "the first months are when people find a study partner, and that happened for me in the hall, not in class", "students who support a family or already have a quiet home nearby should be able to opt out"),
}

def disc_models(item):
    key = item["id"]
    if key.startswith("disc-mock"):
        stance, example, limit = DISC["di-m2"]
    else:
        stance, example, limit = DISC[key]
    a, b = item["s1"]["name"], item["s2"]["name"]
    q = item["question"].strip()
    high = (
        f"I agree with {a} that {stance}. {q} "
        f"In my view, the useful answer is yes only when the rule stays flexible. "
        f"{a} is right about the main benefit, and I want to add a campus example rather than repeat the post. "
        f"For example, {example}. "
        f"At the same time, I understand {b}'s point. {limit}. "
        f"So I support the idea with that limit, and I would say so in my own words."
    )
    b2 = (
        f"I agree with {a}. {q} I think the answer is yes, but the rule should be flexible. "
        f"For example, {example}. "
        f"I also understand {b}, because the cost and the time are real. {limit}. "
        f"That is my opinion."
    )
    phrases = [f"I agree with {a}", "For example", f"I understand {b}", "So I support"]
    return pack(high, b2, phrases, NOTE_D)

def soften(sentence):
    for a, b in ((" the ", " a "), (" your ", " the "), (" will ", " can "), (" should ", " can ")):
        if a in sentence:
            return sentence.replace(a, b, 1)
    if sentence.endswith("."):
        return sentence[:-1] + " today."
    return sentence + " today."

def repeat_models(item):
    out = []
    for s in item["sentences"]:
        exact = s["text"]
        out.append(pack(exact, soften(exact), exact.split()[:3], NOTE_R))
    return out

IV = {
    "int01": [
        ("I usually study in the late afternoon, from about four to seven, at a desk on the second floor of the campus library. I go there because the room is quiet after most classes end. On weekdays I keep the same seat so I do not lose time choosing a place. On Sundays I stay home and use the kitchen table.",
         "I study in the afternoon at the library, because it is quiet. On Sunday I study at home."),
        ("Last month a three-block plan worked well before a quiz. After each short block I closed the book and wrote the main point from memory. I could explain the idea in class the next day, not only recognize it on the page. When I skipped the last block, I forgot the example, so the failure taught me something too.",
         "Last month I studied in three short parts and wrote notes from memory. It worked, because I could explain the idea later. One day I skipped a part and forgot the example."),
        ("I think students should study alone first and with a group later. Alone, I can find what I do not understand. In a group, I have to explain it, and that shows the gap. For example, I understood a chart only after I described it to a classmate. A group from the start is noisy for me.",
         "I prefer to study alone first and with a group later. Alone, I find the gap. In a group, I have to explain it. That worked with a chart I could not read at first."),
        ("Phones should stay out of silent study areas. A lit screen is a small class for everyone nearby, even with no sound. I put mine in my bag, and I check it only outside the room. A student who waits for a family message can sit near the door.",
         "Phones should stay out of quiet study rooms. The screen distracts other people. I leave mine in my bag and check it outside."),
    ],
    "int02": [
        ("The place I visit most is the river path near the market. I go there two or three evenings a week because it is flat and I can walk without planning. On Saturdays I buy fruit at the start of the path and walk for half an hour.",
         "I often walk on the river path near the market. I go in the evening because it is easy and quiet."),
        ("Last June I showed the city to my cousin for one day. We started at the market, took a bus to the old square, and ate lunch at a counter she chose. The day worked because I kept the list short. She still talks about the square, not about the museum we skipped.",
         "I showed the city to my cousin. We saw the market and the old square, then ate lunch. A short list worked better than many stops."),
        ("The change that would help most is a bus that runs later at night. Many people finish work after the last bus, so they pay for a car or a ride. A bus until midnight would make ordinary days easier.",
         "A later bus would help most. People finish work after the last bus and then need a car."),
        ("I prefer to live a little farther out, if the bus is reliable. The center is lively, but the rent and the noise make study hard. Farther out, I have a quieter room and I still reach campus in thirty minutes.",
         "I prefer to live a little farther out. The center is noisy and expensive. A good bus still gets me to campus."),
    ],
    "int03": [
        ("The device I use most is a laptop. I read the slides, type notes, and send work on it. My phone is only for messages and for a reading when I am on the bus.",
         "I use a laptop most. I read slides and type notes on it. My phone is for the bus."),
        ("In a biology class we used a shared document during a lab. Each pair typed one result, and the teacher projected the table. It helped because we saw a wrong number before we left the room. A video alone would not have done that.",
         "In a lab we typed results in one shared document. We saw a mistake before we left. That was more useful than a video."),
        ("Recorded lectures should not replace live classes. A recording is excellent when I miss a day or when I want to hear a definition again. The live class is where I ask the question that the recording cannot answer. I would keep both.",
         "Recorded lectures should add to live classes, not replace them. A recording helps me review. The live class is where I ask questions."),
        ("I learn more when I take some notes by hand. Typing keeps every word, but I do not choose what matters. On paper I write only the point I might forget. For a fast lecture I still type, then I copy three lines by hand that night.",
         "I learn more with some notes by hand, because I choose what matters. For a fast lecture I type, then I copy three lines later."),
    ],
    "int04": [
        ("My main meal is lunch, usually rice, beans, and a vegetable. I eat it at home when I can, around noon, because I study better after a real plate than after a snack.",
         "My main meal is lunch: rice, beans, and vegetables. I eat it at home around noon."),
        ("Last month I cooked a simple pasta and salad for two classmates before a group meeting. I kept the recipe short so the food was ready when they arrived. They stayed to work, and the meal made the meeting easier than meeting hungry in the library.",
         "I cooked pasta and a salad for two classmates. The meal was simple, and we could start the work on time."),
        ("Yes, schools should teach a few simple meals. Many students leave home and then eat only what is fastest. One class on rice, eggs, and a vegetable would save money and time. It does not need to be a full cooking course.",
         "Schools should teach a few simple meals. Students who leave home often eat only what is fast. A short class is enough."),
        ("Trying food from other regions matters, but it is not a duty. It teaches me what other people eat on an ordinary day, not only on a holiday. I try a new dish when a friend cooks it. I do not need to like all of it.",
         "Trying food from other places is useful, because I learn an ordinary meal, not only a holiday dish. I try it when a friend cooks."),
    ],
    "int05": [
        ("I have not had a formal job, but I have regular family duties. I shop for the week and I help my younger cousin with homework on Wednesdays. That is steady work, even without a paycheck.",
         "I have not had a paid job. I shop for my family and I help my cousin with homework on Wednesdays."),
        ("Helping my cousin with math taught me to explain a step without doing it for her. The first week I gave the answer, and she learned nothing. After that I asked one question and waited. She got further, and I got more patient.",
         "I used to give my cousin the answer. Then I asked one question and waited. She learned more, and I became more patient."),
        ("A part-time job can help if the hours stay small. Ten hours a week taught people I know how to arrive on time. More than that hurt their reading. I would work only if the job ended before my hardest course.",
         "A small job can help students learn to be on time. Too many hours hurt their reading. I would keep the hours low."),
        ("In a first job, the learning matters more than the pay, if the pay still covers the bus and food. A higher salary with no new skill leaves me in the same place next year. I would ask what I will be able to do after six months.",
         "Learning matters more than pay in a first job, if I can still pay for the bus and food. I want a skill I can use next year."),
    ],
    "int06": [
        ("People in my area talk most about flooding after hard rain. Streets near the river stay closed for a day, and the bus changes its route. That is the issue I hear about every summer.",
         "People talk about flooding after hard rain. Streets close, and the bus changes its route."),
        ("I started taking a cloth bag to the market and I unplug the small lamp when I leave my room. The bag was the harder habit, because I forgot it twice. Now it hangs on the door. The change is small, but I produce less trash each week.",
         "I take a cloth bag to the market and I unplug my lamp. I forgot the bag at first. Now I use less plastic."),
        ("Cities should limit car traffic in the center during the day. The street is then safer for the bus and for people walking. Delivery vans can enter early in the morning. A full ban at all hours would hurt shops.",
         "Cities should limit cars in the center during the day. The bus and people walking are safer. Vans can come in the morning."),
        ("The city should pay for most of cleaner public transport, and riders should pay a fare they can afford. If only riders pay, the people who need the bus most stop using it. A low fare plus public money keeps the service frequent.",
         "The city should pay most of the cost, and riders should pay a fare they can afford. A high fare pushes people back into cars."),
    ],
    "int-m1": [
        ("The class that meets most often is my writing class. It meets three times a week, on Monday, Wednesday, and Friday, in the morning. The other courses meet twice.",
         "My writing class meets most often: Monday, Wednesday, and Friday morning."),
        ("I still remember a discussion about a short article on city parks. Two students disagreed about who the park was for, and the teacher made us point to a sentence. I remember it because I had to defend a line, not a feeling.",
         "I remember a discussion about a park article. We had to point to a sentence. That is why I still remember it."),
        ("Attendance can be a small part of the grade, not the main part. Showing up matters in a seminar, because the talk is the class. It should not punish a student who was ill and later did the reading. I would count attendance as ten percent.",
         "Attendance can be a small part of the grade in a seminar. It should not punish someone who was ill and did the work later."),
        ("I learn more when I take fewer courses and go deeper. Four hard courses left me skimming every reading. Three courses let me finish one book and talk about it. More courses look busy, but I remember less.",
         "Fewer courses are better for me. With four classes I only skimmed. With three I could finish a book and talk about it."),
    ],
    "int-m2": [
        ("On Saturday morning I buy bread, clean my desk, and walk for twenty minutes before I open a book. I keep that order so the rest of the day is quieter.",
         "On Saturday morning I buy bread, clean my desk, and take a short walk. Then I study."),
        ("Two weeks ago my sister and I spent Saturday at a neighborhood fair. We listened to one band and ate lunch there. We left after two hours, which was enough. The short visit was better than a whole day of plans.",
         "My sister and I went to a neighborhood fair. We stayed two hours. A short visit was better than a long plan."),
        ("Students should protect one day, or at least one long morning, from new schoolwork. Rest is when I notice what I did not understand. I still review lightly, but I do not start a new chapter that day.",
         "Students should keep one morning free. I rest, and I only review a little. I do not start a new chapter."),
        ("Time outdoors is better for me than a long stretch online, but not for every hour. A walk clears my head before I study. After that, an online call with a friend is fine. All day on a screen leaves me tired and behind.",
         "A walk is better before I study. After that, some time online is fine. A whole day on a screen makes me tired."),
    ],
    "mock": [
        ("I usually study alone. I sit at the same library desk in the afternoon. I meet a classmate only after I have a list of questions. That way the meeting is short and useful.",
         "I usually study alone at the library. I meet a classmate only when I already have questions."),
        ("A two-evening plan worked before my last quiz. I read on Monday and explained the chapter out loud on Tuesday. The plan failed when I left both nights for Wednesday, because I ran out of time and forgot the example.",
         "I read one night and explained the chapter the next night. When I left both nights for one day, I forgot the example."),
        ("I do not agree that one long session is better. I feel busy, but I remember less the next day. For example, two evenings on one chapter worked better than one long night. A long session is useful only for a final review, not for the first reading.",
         "I disagree. One long session feels productive, but I forget more. Two shorter nights worked better for me."),
        ("Universities should teach a few study habits, and the rest stays the student's job. A short workshop on planning and recall would have helped me in the first month. After that, I have to choose the hours myself. A required course all year is more than I need.",
         "Universities should teach a few study habits at the start. After that, the hours are my job. A short workshop is enough."),
    ],
}

def interview_models(item):
    key = item["id"]
    if key.startswith("iv-mock"):
        rows = IV["mock"]
    else:
        rows = IV[key]
    out = []
    for (high, b2), q in zip(rows, item["questions"]):
        entry = pack(high, b2, ["For example", "I usually", "I do not agree", "The"], NOTE_I)
        entry["q"] = q["text"]
        out.append(entry)
    return out

def main():
    emails = {}
    for e in load("email"):
        if e["id"] not in EMAILS:
            raise SystemExit("missing email " + e["id"])
        emails[e["id"]] = EMAILS[e["id"]]
    discs = {d["id"]: disc_models(d) for d in load("discussion")}
    reps = {r["id"]: repeat_models(r) for r in load("repeat")}
    ivs = {i["id"]: interview_models(i) for i in load("interview")}
    short = []
    for k, v in emails.items():
        n = len(words(v["high"]))
        if n < 40 or "Dear " not in v["high"]:
            short.append(f"{k}:{n}")
    if short:
        raise SystemExit("short email " + ", ".join(short))
        # keywords of the source item should mostly appear; checked below
    for k, v in discs.items():
        hw, bw = len(words(v["high"])), len(words(v["b2"]))
        if hw < 90 or bw < 40:
            raise SystemExit(f"short disc {k} {hw} {bw}")
    for k, arr in reps.items():
        if len(arr) != 7:
            raise SystemExit("repeat " + k)
    for k, arr in ivs.items():
        if len(arr) != 4 or any(len(words(x["high"])) < 25 for x in arr):
            raise SystemExit("iv " + k)
    # keyword coverage for emails
    for e in load("email"):
        text = emails[e["id"]]["high"].lower()
        for group in e["keywords"]:
            if not any(k.lower() in text for k in group):
                raise SystemExit("keyword miss " + e["id"] + " " + str(group))
    out = {"email": emails, "discussion": discs, "repeat": reps, "interview": ivs}
    path = P / "models.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print("ok", path.stat().st_size)

if __name__ == "__main__":
    main()
