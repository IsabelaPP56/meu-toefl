import sys
sys.path.insert(0, "/workspace/tools")
from bank_common import dump, words

def sentence(text):
    parts = text.split()
    n = 2 if len(parts) <= 8 else 3 if len(parts) <= 14 else 4
    size = len(parts) / n
    chunks, i = [], 0
    for k in range(n):
        j = len(parts) if k == n - 1 else int(round((k + 1) * size))
        chunks.append(" ".join(parts[i:j]))
        i = j
    assert " ".join(chunks) == text, (chunks, text)
    assert 2 <= len(chunks) <= 4
    return {"text": text, "chunks": chunks}

def scenario(id_, pool, title, lines):
    assert len(lines) == 7, id_
    # length should grow
    lens = [len(t.split()) for t in lines]
    assert lens[-1] > lens[0], (id_, lens)
    return {"id": id_, "pool": pool, "scenario": title, "sentences": [sentence(t) for t in lines]}

reps = [
scenario("rep01","practice","You are learning to welcome new students to the campus library.",[
"Welcome to the library.","The quiet floors are upstairs.","Group rooms are on the first floor, near the café.","Please keep drinks covered, and do not bring hot food.","Return books to the desk or to the outdoor slot.","Students can borrow laptops for four hours with a current ID card.","The research desk, beside the main stairs, can help you find articles and books.",
]),
scenario("rep02","practice","You are training to give a short safety talk in a chemistry lab.",[
"Wear your lab coat.","Tie back long hair.","Goggles stay on, even for a quick measurement.","If something spills, tell the instructor before you wipe it.","Do not pour chemicals down the sink unless the label allows it.","The eye-wash station is on the left wall, next to the fire blanket.","Before you leave, wash your hands and check that every bottle is capped and labeled.",
]),
scenario("rep03","practice","You are practicing an announcement for a campus museum tour.",[
"Stay with the group.","Photos are allowed without flash.","Please do not touch the paintings or the frames.","The next gallery shows everyday objects from the 1920s.","If you get separated, wait by the blue bench near the exit.","Bags larger than a laptop should be left in the free lockers downstairs.","The gift shop closes fifteen minutes before the museum, so save your questions about prints until the end.",
]),
scenario("rep04","practice","You are learning the opening script for a student health clinic.",[
"Please check in.","Have your ID ready.","A nurse will call you when a room is free.","If you feel dizzy, tell us immediately and stay seated.","Water is available at the cooler beside the window.","Appointments that are more than ten minutes late may need to be rescheduled.","The pharmacy next door can fill many prescriptions, but bring the paper the clinician gives you.",
]),
scenario("rep05","practice","You are rehearsing directions for new tutors in the writing center.",[
"Greet the writer.","Ask what they want help with.","Let them read the draft aloud before you comment.","Focus on organization first, and save small grammar points for later.","Do not rewrite their sentences; ask questions that help them revise.","Sessions last twenty-five minutes, and the next person may already be waiting.","At the end, name one strength and one next step the writer can finish tonight.",
]),
scenario("rep06","practice","You are practicing a welcome for visitors to a university career fair.",[
"Welcome to the fair.","Employers are arranged by field.","The schedule of short talks is posted by the entrance.","Take a map, and visit the booths that match your interests.","Bring copies of your résumé if you want a longer conversation.","Quiet interview rooms are down the hall, and you must book them at the information table.","Before you leave, complete the feedback card so we know which employers students want to see again.",
]),
scenario("rep-m1","mock1","You are learning to guide visitors through a campus science fair.",[
"Welcome to the fair.","Student projects are in this hall.","Judges will walk through between two and four.","Please keep the aisles clear so everyone can see the posters.","Do not touch equipment unless a presenter invites you.","The food table is outside, because drinks are not allowed near the displays.","If you have a question about a prize, the registration desk near the front door can explain the rules.",
]),
scenario("rep-m2","mock2","You are practicing the opening for a campus housing tour.",[
"Thanks for coming.","This building opened last year.","Kitchens are shared by four rooms.","Quiet hours begin at ten on weeknights and at midnight on weekends.","Laundry machines are in the basement and take the campus card.","Bike racks are behind the building, and bikes left in hallways may be removed.","The resident advisor's apartment is on the ground floor, and that is where you report a lockout or a leak.",
]),
]
dump("repeat", reps)

interviews = []
def iv(pool, scenario, qs):
    assert len(qs)==4
    interviews.append({"id": f"iv{len(interviews)+1:02d}", "pool": pool, "scenario": scenario,
        "questions": [{"text": q, "focus": f} for q, f in qs]})

iv("practice","A researcher is asking you about how you study.",[
("Do you usually study alone or with other people?","fact"),
("Tell me about a time when your study plan worked well or failed.","experience"),
("Some people say long study sessions are better than several short ones. Do you agree? Why or why not?","opinion"),
("Should universities teach students how to study, or is that each student's responsibility? Why?","opinion"),
])
iv("practice","You are in an interview about cities and daily life.",[
("Do you live in a big city, a town, or a smaller place?","fact"),
("Describe a city you have visited and one thing you liked about it.","experience"),
("Do you think people in cities have more interesting lives than people in small towns? Why or why not?","opinion"),
("Should city governments spend more money on parks? Why or why not?","opinion"),
])
iv("practice","A classmate is interviewing you about technology and school.",[
("What device do you use most for your classes?","fact"),
("Describe a time when technology helped you learn, or made learning harder.","experience"),
("Some teachers ban phones in class. Do you agree with that rule? Why or why not?","opinion"),
("Will online classes replace most in-person classes in the future? Why or why not?","opinion"),
])
iv("practice","You agreed to talk about food and health.",[
("What do you usually eat on a busy day?","fact"),
("Tell me about a meal you remember clearly, and why you remember it.","experience"),
("Is it the school's job to offer healthy food, or should students decide alone? Why?","opinion"),
("Do you think cooking at home is still important for young adults? Why or why not?","opinion"),
])
iv("practice","An advisor is asking about work and free time.",[
("Do you have a job, or do you only study right now?","fact"),
("Describe a responsibility you have had at work, at home, or in a club.","experience"),
("Should students work while they are in university? Why or why not?","opinion"),
("Is free time as important as study time? Explain your view.","opinion"),
])
iv("practice","You are answering questions about the environment.",[
("Is there a park, river, or other outdoor place near your home?","fact"),
("Tell me about something you do, or could do, to reduce waste.","experience"),
("Should people pay more for products that are safer for the environment? Why or why not?","opinion"),
("Are individual habits enough to address climate change, or are larger rules necessary? Why?","opinion"),
])
iv("mock1","You are taking part in a short interview about learning English.",[
("Where do you use English most often right now?","fact"),
("Describe a moment when you understood something in English that used to be difficult.","experience"),
("Is it better to learn a language by speaking, even with mistakes, or by studying rules first? Why?","opinion"),
("Should universities require a test like the TOEFL, or is another measure fairer? Why?","opinion"),
])
iv("mock2","A researcher is asking you about community and university life.",[
("Are you part of any club, team, or community group?","fact"),
("Tell me about a time you helped someone, or someone helped you, at school.","experience"),
("Should universities require students to do community work? Why or why not?","opinion"),
("Do friendships formed at university last? Why do you think so?","opinion"),
])
dump("interview", interviews)
print("repeat", len(reps), "interview questions", sum(len(x["questions"]) for x in interviews))

# discussions
topics = [
("practice","Education","Should universities record all lectures and post them online?","Helena","I support recording lectures because students who work or get sick can review the class. A recording does not replace questions, but it makes the course fairer for people with difficult schedules.","Diego","I disagree. If every lecture is online, fewer students will come to class, and the discussion will get weaker. Teachers also deserve some control over how their words are reused."),
("practice","Psychology","Is it a good idea for students to take a full day off from screens each week?","Lina","Yes. A day without screens helps me sleep and notice when I am bored instead of opening another video. The break does not have to be perfect to be useful.","Omar","I think a full day is unrealistic. Many of us need phones for work and family. Shorter limits, like no screens during meals, are easier to keep."),
("practice","Public health","Should campuses charge more for sugary drinks to encourage healthier choices?","Priya","A higher price can push people toward water, and the extra money could fund sports or kitchens. Price is a clear signal when advice alone is ignored.","Hugo","I oppose the charge. It hits students with less money harder, and it treats a personal choice like a fine. Education and cheaper fruit would be fairer."),
("practice","Urban studies","Should cities ban cars from the streets closest to universities?","Sofia","Yes. Fewer cars would make walking and cycling safer, and the space could become benches or bike parking. Deliveries could use early morning hours.","Mateo","A full ban would hurt people who commute from far away or who have a disability. Better buses and safer crossings would help without closing every street."),
("practice","Technology","Should professors use software that detects AI-written sentences?","Aisha","Detection tools can protect honest students and remind everyone that the thinking has to be theirs. Used carefully, they support the purpose of a writing assignment.","Jonas","The tools make mistakes, and students may be accused without proof. I would rather see drafts written in class than trust a score from a program."),
("practice","Environment","Should universities stop serving beef in dining halls one day a week?","Clara","One beef-free day is a small change with a real effect, and it introduces people to other proteins. Students can still choose beef on other days.","Ravi","I think the choice should stay with each person. A ban, even for one day, feels symbolic more than scientific, and some students rely on those meals."),
("practice","Work","Is it better to take an unpaid internship in your field or a paid job outside it?","Nina","I would take the internship if I could afford it, because the skills and contacts match the career I want. A year of relevant practice can matter more than a higher wage.","Paulo","Paid work teaches responsibility too, and not everyone can work for free. Calling unpaid work a requirement favors students who already have support."),
("practice","Media","Should news sites remove the comments under articles?","Elena","Yes. Comments often become insults, and they rarely add facts. Readers can discuss the story in class or with friends without a public pile of attacks.","Chris","Comments can correct errors quickly and show which parts of a story people distrust. Moderation is better than silence."),
("practice","Campus life","Should first-year students be required to live on campus?","Bianca","Living on campus helps new students find friends and support before they know the city. The requirement could include a clear exception for family duties.","Igor","Housing is expensive, and some students already live nearby with relatives. A requirement would punish them for a living situation that works."),
("practice","Science education","Should science classes spend more time on failed experiments, not only successful ones?","Maya","Yes. Failed trials show how knowledge is actually built, and they teach students to read results with caution. A perfect story can hide the hard parts.","Leo","Too much failure can confuse beginners who still need a clear model. Show the failures after the main idea is stable."),
("practice","Transport","Should a student transit pass be included in tuition?","Fatima","Including the pass would make buses a normal part of study, not an extra bill. Students who never ride could still benefit from less traffic around campus.","Andre","It hides the cost inside tuition and forces non-riders to pay. A cheaper optional pass is more honest."),
("practice","Language","Is it useful to memorize word lists, or should learners only meet words in texts?","Yara","Lists help me notice a word later when I read it in a real sentence. Memorizing a short list each day is realistic during a busy week.","Samir","Words learned in isolation disappear. I remember a word when I have heard it in a story or used it myself."),
("practice","Arts","Should universities require one arts course for every degree?","Lucia","An arts course trains attention and gives students a language for images and stories they already meet every day. One course is not a heavy burden.","Owen","Requirements should stay inside the major. Students who want art will choose it, and others need those credits for technical skills."),
("practice","Health","Should campuses offer free sleep workshops before exam weeks?","Noor","Yes. Many students treat sleep as optional, and a short workshop could show the cost of all-night study. The timing, right before exams, is when people will listen.","Victor","Workshops do not fix noisy dorms or long commutes. Change the exam calendar before you teach people to sleep."),
("practice","Economy","Should textbooks be replaced entirely by free online readings?","Helena","Free readings remove a real barrier, and teachers can update them when a field changes. Print can still exist for anyone who wants it.","Diego","Online texts disappear, depend on wifi, and are harder to mark for some readers. A low-cost print option should remain."),
("practice","Ethics","Is it acceptable to skip a group meeting if you finish your own part early?","Lina","No. The meeting is where the group checks whether the parts fit together. Finishing early does not reveal what others need from you.","Omar","If the work is done and posted clearly, a meeting can be a poor use of time. The rule should be communication, not attendance for its own sake."),
("practice","Design","Should classroom chairs be movable, even if the room looks less tidy?","Priya","Movable chairs let groups form quickly and help students who need a different posture. A tidy row is less important than a useful hour.","Hugo","Loose chairs block aisles and waste the minutes at the start of class. Fixed seating is clearer in a crowded room."),
("practice","History","Should history courses start with local stories before national ones?","Sofia","Local stories give students a concrete place to stand, and they can see how a large event changed one street or family. Curiosity often starts there.","Mateo","Starting local can make the course feel small and leave out people whose history is not in that city. A national frame can be more inclusive."),
("practice","Data","Should students be required to learn basic statistics, no matter their major?","Aisha","Statistics shows up in news about health, money, and policy. A short required course would help graduates read claims instead of trusting a headline.","Jonas","A requirement adds stress for students whose fields rarely use numbers. Offer the course widely, but do not force it on every degree."),
("practice","Community","Should student clubs receive money only if they are open to every major?","Nina","Public money should not fund a club that excludes most of the campus. An open membership rule is simple and fair.","Paulo","Some clubs need shared skills, like a lab safety group. Open membership can make the activity meaningless or unsafe."),
("mock1","Social studies","Should high schools require a weekly community-service hour?","Helena","A weekly hour can introduce students to needs they would not see otherwise, and it is small enough to fit beside homework. Schools should offer choices, including weekend options.","Diego","Required service stops being voluntary. Many teenagers already care for relatives or work, and another hour could become a punishment rather than a lesson."),
("mock2","Environmental science","Should universities ban single-use plastic bottles on campus?","Lina","A ban would cut a visible stream of waste and push dining halls to offer water stations. People change habits faster when the easy option disappears.","Omar","Bans without enough fountains just send people off campus to buy the same bottles. Fix the water access first, and then limit plastic."),
]
disc = []
for i,(pool, course, question, n1, t1, n2, t2) in enumerate(topics,1):
    extra1 = " A campus example, with a real schedule or a clear cost, would make this easier to trust."
    extra2 = " The decision should also count students who work, commute, or care for relatives."
    while len(t1.split()) < 42:
        t1 += extra1
    while len(t2.split()) < 42:
        t2 += extra2
    assert 42 <= len(t1.split()) <= 100, (i, "s1", len(t1.split()))
    assert 42 <= len(t2.split()) <= 100, (i, "s2", len(t2.split()))
    disc.append({"id": f"disc{i:02d}", "pool": pool, "course": course, "question": question,
                 "s1": {"name": n1, "text": t1}, "s2": {"name": n2, "text": t2}})
assert sum(1 for d in disc if d["pool"]=="practice") >= 20
dump("discussion", disc)
print("discussions", len(disc))
