import sys
sys.path.insert(0, "/workspace/tools")
from bank_common import dump

def choose_items(rows, pool, level):
    import random
    out = []
    for i, (line, ok, a, b, c) in enumerate(rows, 1):
        options = [ok, a, b, c]
        rng = random.Random(pool + line)
        order = [0, 1, 2, 3]
        rng.shuffle(order)
        shuffled = [options[k] for k in order]
        out.append({
            "id": f"{pool}-ch-{i:02d}",
            "pool": pool, "level": level, "line": line,
            "options": shuffled, "a": order.index(0),
            "why": "A opção certa responde à função da fala (pedido, convite, correção ou informação). As outras pegam uma palavra parecida e respondem outra coisa."
        })
    return out

P = [
("Could you hold the elevator?","Sure, I'll keep it open.","The elevator was repaired yesterday.","I live on the third floor.","Elevators are faster than stairs."),
("I'm afraid I can't make the study group tonight.","Then let's meet tomorrow after class.","The group has six people.","Tonight's dinner is pasta.","I already studied that chapter."),
("Have you seen my blue notebook?","It was on the desk a minute ago.","Blue is my favorite color.","Notebooks are on sale.","I saw the movie last night."),
("Would you like a copy of my notes?","That would be really helpful.","The notes are two pages.","I copied the question.","Copies cost ten cents."),
("The bookstore is closed for inventory.","Then I'll order the book online.","I love bookstores.","Inventory means counting.","The store opens at nine."),
("Do you mind if I open the window?","No, go ahead. It's warm in here.","The window was replaced last year.","I mind the children on weekends.","Windows face the courtyard."),
("Isn't the career fair tomorrow?","Yes, it starts at ten in the gym.","Fairs are usually outdoors.","I don't have a career yet.","Tomorrow is Wednesday."),
("Thanks for returning my charger.","No problem. I found it in the lab.","Chargers are expensive.","I returned the library book.","Thank you for the invitation."),
("We should leave now if we want seats.","You're right. I'll get my bag.","Seats are blue in that room.","I left my bag yesterday.","Leaving is difficult."),
("Could you speak a little more slowly?","Of course. I'll repeat the steps.","I speak three languages.","Slowly is an adverb.","The speech is at noon."),
("I think we got off at the wrong stop.","Let's check the map on my phone.","Stops are announced.","I got a good grade.","The wrong answer is B."),
("Are you free to review my draft?","Yes. Send it and I'll read it tonight.","Drafts can be messy.","Freedom is important.","The review is on Friday."),
("The wifi in the dorm is down again.","I'll use the library computers.","Wifi means wireless.","The dorm is near the gym.","Again means one more time."),
("Don't forget your ID for the exam.","Thanks. It's already in my pocket.","IDs are plastic.","I forgot the question.","Exams are stressful."),
("Would Thursday afternoon work for you?","Thursday is fine. How about two?","Afternoons are long.","I work on my thesis.","Thursday comes after Wednesday."),
("I'm sorry I missed your call.","That's okay. I just had a quick question.","Calls cost extra.","I miss my family.","Sorry is a feeling."),
("Shall we split the cost of the poster?","Good idea. I'll send you half.","Posters are colorful.","The cost of living is high.","Split the class into groups."),
("You left your umbrella in the seminar room.","Oh, thanks. I'll go back for it.","Umbrellas are useful in rain.","I left the room at noon.","Seminars are small classes."),
("Is this seat taken?","No, you can sit here.","Seats are numbered.","I took the test.","This is my favorite seat."),
("Could you remind me of the room number?","It's 214, next to the lab.","Numbers are on the door.","I remember the lecture.","Reminders help."),
("I'm going to the clinic after class.","I hope you feel better soon.","The clinic is open.","Class ends at three.","After means later."),
("Let's take the earlier shuttle.","Okay. I'll meet you at the stop.","Shuttles are free.","Earlier means before.","I took the train."),
("Did the professor post the grades?","Not yet. She said tonight.","Professors post articles.","Grades are letters.","I posted a photo."),
("I can't find a quiet place to read.","The third floor of the library is silent.","Reading is useful.","Quiet people listen.","I found my keys."),
("Would you mind swapping presentation days?","I can switch if I go on Monday.","Days of the week.","Swapping means trading.","Presentations use slides."),
("The printer jammed again.","I'll get paper from the other lab.","Printers use ink.","Jam is a food.","Again and again."),
("Do you have a minute?","Yes. What do you need?","Minutes are short.","I have a watch.","Time flies."),
("I already ate, but thanks.","No worries. I'll save you a seat anyway.","Eating is important.","Thanks means thank you.","I already left."),
("The line for coffee is huge.","Then let's just get water and go.","Coffee is hot.","Huge means big.","Lines have geometry."),
("Can I borrow your calculator until Friday?","Sure, just bring it back before the quiz.","Calculators are electronic.","Friday is a day.","I borrowed a novel."),
("I didn't catch the last example.","She compared two prices in one market.","Examples are useful.","Catch the ball.","Last means final."),
("We're out of clean cups in the lounge.","I'll wash a few in the sink.","Cups hold liquid.","Clean means not dirty.","The lounge has sofas."),
("Should I attach the chart or paste it in?","Attach it so the file stays clear.","Charts show data.","Paste is sticky.","Attach means connect."),
("The guest speaker arrived early.","Then we should open the auditorium now.","Speakers are loud.","Early means not late.","Guests need name tags."),
("I might drop the lab if I fail the quiz.","Talk to the instructor before you decide.","Labs have equipment.","Fail means not pass.","Quizzes are short."),
("Could you watch my bag while I buy a ticket?","Yes, I'll stay right here.","Bags are heavy.","Watch the time.","Tickets cost money."),
("It's pouring, and I don't have a jacket.","Take mine. I'm getting a ride.","Rain is water.","Jackets are warm.","Pouring means serving."),
("The group chat is moving too fast.","I'll summarize the decisions in one note.","Chats are online.","Fast means quick.","Groups have members."),
("Do you want the window seat or the aisle?","The aisle, please. I need to stand up later.","Seats are chairs.","Windows are glass.","Aisles are paths."),
("I think I submitted the wrong file.","Email the instructor and attach the right one.","Files are documents.","Wrong means incorrect.","Submit means send."),
("Nora asked me to bring markers.","There are some in the supply closet.","Markers write.","Bring means carry.","Nora is a name."),
("This soup tastes a bit salty.","Mine is fine. Maybe ask for another bowl.","Soup is food.","Salty means salt.","Taste is a sense."),
]
assert len(P) >= 42, len(P)

U = [
("Who signed the equipment form?","I did, right after the safety video.","Forms have lines.","Equipment is heavy.","Who means a person."),
("The auditorium doors lock at nine.","Then we should finish the rehearsal earlier.","Doors are wood.","Nine is a number.","Locks need keys."),
("Would a morning slot be better?","Yes, mornings are clearer for me.","Slots are openings.","Better means improved.","Morning is early."),
("I still owe you for the shared taxi.","Send it whenever. There's no rush.","Taxis are cars.","Owe means debt.","Shared means together."),
("Has anyone claimed the lost scarf?","Not yet. It's still at the front desk.","Scarves are warm.","Lost means missing.","Claim means say."),
("The reading is longer than I expected.","Focus on the section she marked.","Reading takes time.","Longer means more long.","Expected means thought."),
("Can the interview be remote?","Yes, they sent a video link.","Interviews ask questions.","Remote means far.","Links connect."),
]
L = [
("Where is the nearest printer?","Down the hall, next to the stairs.","I printed it yesterday.","Printers use paper.","Near means close."),
("What time is dinner at the dining hall?","It starts at five.","Dinner is food.","Halls are big rooms.","Time flies."),
("May I sit with you?","Of course. There's space here.","Sitting is comfortable.","You are a pronoun.","Space is large."),
("Is the gym open today?","Yes, until eight tonight.","Gyms have equipment.","Open means not closed.","Today is now."),
("Do you sell bus passes here?","Yes, at the counter on the left.","Buses have wheels.","Passes allow entry.","Sell means exchange."),
("How do I join the mailing list?","Use the link in the welcome email.","Mail arrives daily.","Lists have items.","Join means connect."),
("Could you point me to room 12?","It's the second door on the right.","Points are dots.","Rooms have walls.","Twelve is a number."),
]
# build pools with enough items
def take(src, n, pool, level):
    rows = []
    i = 0
    while len(rows) < n:
        rows.append(src[i % len(src)])
        i += 1
    # avoid duplicate lines inside a pool by altering only if repeated — practice uses unique P
    return choose_items(rows[:n], pool, level)

# Practice must be unique. P has 42.
practice = choose_items(P[:42], "practice", "mid")
# For mocks, use slices and extra unique lines so we don't repeat the same audio inside one mock.
extra_m1 = [
("The advisor moved my appointment to Friday.","Thanks for telling me. I'll update my calendar.","Appointments take time.","Friday is later.","Moved means changed."),
("We're short one volunteer for the fair.","I can cover the morning shift.","Volunteers help.","Short means not tall.","Fairs are events."),
("Did you back up the slides?","Yes, they're in the shared folder.","Slides are glass.","Back means behind.","Folders hold paper."),
("The noise from the construction is awful.","Let's study on the other side of campus.","Noise is sound.","Awful means bad.","Construction builds."),
("I need a stamp for this envelope.","The front desk sells them.","Stamps are small.","Envelopes hold letters.","Need means require."),
("Could we start the meeting without Lee?","Yes. She said to begin at three.","Meetings have agendas.","Start means begin.","Without means lacking."),
("This citation is missing the year.","I'll add 2019 before I submit.","Citations name sources.","Missing means gone.","Years have months."),
("The museum tickets are half price for students.","Then we should go this weekend.","Museums have art.","Half is 50 percent.","Price is cost."),
("I'm locked out of the portal.","Try resetting the password from your email.","Portals are gates.","Locked means shut.","Out means outside."),
("Shall I bring printed copies?","Yes, bring eight, one for each person.","Copies are duplicates.","Printed means on paper.","Bring means carry."),
]
extra_m2 = [
("The lab coats are in the cabinet.","I'll grab two before we start.","Coats are clothing.","Cabinets store things.","Labs do experiments."),
("Your library book is overdue.","I'll return it on my way to class.","Books have pages.","Overdue means late.","Libraries lend books."),
("Can you proofread just the introduction?","Yes. Send the paragraph and I'll reply tonight.","Introductions come first.","Proof means evidence.","Read means look."),
("The heater in our room is stuck on high.","I'll submit a maintenance request.","Heaters warm rooms.","Stuck means trapped.","High means up."),
("We need a neutral background for the video.","The white wall in the lounge will work.","Backgrounds are behind.","Neutral means not biased.","Video is film."),
("Is the quiz open-book?","No. She said notes must stay in your bag.","Quizzes test knowledge.","Open means not shut.","Books have covers."),
("I lost the receipt for the club supplies.","Check your email. The store sent a copy.","Receipts show payment.","Lost means missing.","Supplies are materials."),
("The workshop was moved to the art building.","Okay. I'll tell the rest of the group.","Workshops teach skills.","Moved means relocated.","Art is creative."),
("Do you want to practice the dialogue once more?","Yes. You start, and I'll answer.","Dialogues are talks.","Practice means rehearse.","Once means one time."),
("I'll be in the writing center until four.","Then I'll meet you there at 3:30.","Centers are middle.","Writing is words.","Until means up to."),
]
items = []
items += practice
items += choose_items(extra_m1, "m1", "mid")
items += choose_items(U, "m1u", "hard")
items += choose_items(L, "m1l", "easy")
items += choose_items(extra_m2, "m2", "mid")
items += choose_items([
("Who is covering the front desk at noon?","Mina is, until one.","Desks are furniture.","Noon is midday.","Covering means hiding."),
("The data file won't open on my laptop.","Try the lab computers. They have the software.","Files store data.","Open means begin.","Laptops are portable."),
("Should the chart include last year's numbers?","Yes. She wants both years side by side.","Charts display numbers.","Include means contain.","Last year is past."),
("I'm not sure which source is reliable.","Use the journal article, not the anonymous post.","Sources provide information.","Sure means certain.","Reliable means trustworthy."),
("Can we rehearse in the empty classroom?","Yes, until the next class at four.","Classrooms have desks.","Empty means vacant.","Rehearse means practice."),
("The scholarship essay has a 500-word limit.","Then I'll cut the second example.","Essays are texts.","Limits restrict size.","Words are language."),
("Did maintenance fix the flickering light?","Not yet. They come tomorrow morning.","Lights illuminate.","Fix means repair.","Flickering means blinking."),
], "m2u", "hard")
items += choose_items([
("What day is the club picnic?","Saturday at noon.","Picnics are outdoors.","Days have names.","Clubs have members."),
("Where do I return this tray?","On the cart by the door.","Trays hold food.","Return means give back.","Doors open."),
("How late is the gym open?","Until ten tonight.","Gyms have machines.","Late means not early.","Open means available."),
("Can I pay with a card?","Yes, card or cash.","Cards are plastic.","Pay means give money.","Cash is money."),
("Is there a lost and found?","Yes, at the security desk.","Lost means missing.","Found means discovered.","Desks are tables."),
("Do you have this shirt in a medium?","I'll check in the back.","Shirts are clothes.","Medium is a size.","Have means possess."),
("Which bus goes to the train station?","The number 4, from this stop.","Buses travel.","Stations are places.","Goes means moves."),
], "m2l", "easy")
# unique ids already include pool. Check counts
from collections import Counter
c = Counter(x["pool"] for x in items)
print("choose", c, "total", len(items))
assert c["practice"] >= 42
assert c["m1"] >= 10 and c["m1u"] >= 7 and c["m1l"] >= 7
assert c["m2"] >= 10 and c["m2u"] >= 7 and c["m2l"] >= 7
dump("choose", items)

# emails
emails = []
def email(pool, to, subject, scenario, bullets, keywords):
    emails.append({"id": f"em{len(emails)+1:02d}", "pool": pool, "to": to, "subject": subject, "scenario": scenario, "bullets": bullets, "keywords": keywords})

email("practice","professor.nunes@university.edu","Request to switch discussion section",
"You signed up for a discussion section that conflicts with your lab. Write to your professor.",
["Explain the conflict between the section and your lab.","Propose another section that you can attend.","Ask what you should do to make the change official."],
[["lab","conflict","overlap","same time"],["section","tuesday","another","switch"],["official","permission","form","approve"]])
email("practice","library@university.edu","Noise in the group study rooms",
"You reserved a study room, but the room next door was very loud and there was no staff nearby.",
["Say why you were in the library.","Describe the noise problem.","Request a solution for future reservations."],
[["study","reserve","room","exam"],["noise","loud","next door"],["staff","quiet","solution","future"]])
email("practice","housing@university.edu","Broken heater in the dorm",
"The heater in your dorm room has not worked for three days, and nights are cold.",
["Explain the problem and how long it has lasted.","Describe how it affects your sleep or study.","Ask for a repair time."],
[["heater","heat","cold","broken"],["sleep","study","night"],["repair","fix","technician","when"]])
email("practice","club.president@university.edu","Proposal for a weekend workshop",
"You belong to a photography club and want to organize a free workshop for beginners.",
["Say what workshop you want to offer.","Explain who it would help.","Ask for a room and a date."],
[["workshop","photography","beginner"],["help","new","students","members"],["room","date","weekend","space"]])
email("practice","clinic@university.edu","Request to move an appointment",
"You have a clinic appointment during a midterm and need a different time.",
["State the current appointment time.","Explain the conflict with your exam.","Ask for a new time this week."],
[["appointment","time","scheduled"],["exam","midterm","conflict"],["another","reschedule","this week","new time"]])
email("practice","roommate.lee@university.edu","Sharing the fridge fairly",
"Your roommate leaves old food in the shared fridge, and you have no space for your meals.",
["Describe the problem politely.","Explain why you need the space.","Suggest a simple rule you can both follow."],
[["fridge","food","old"],["space","meals","cook"],["rule","label","share","clean"]])
email("practice","writing.center@university.edu","Appointment before a paper deadline",
"Your academic discussion post is due in four days and you want feedback on the organization.",
["Say what you are writing and when it is due.","Explain what kind of help you want.","Ask for the earliest available appointment."],
[["paper","discussion","due","deadline"],["organization","structure","feedback"],["appointment","earliest","available","time"]])
email("practice","transport@university.edu","Shuttle stop closed by construction",
"The usual shuttle stop is closed, and you could not find a sign explaining the temporary stop.",
["Say which stop you use.","Describe the problem you had today.","Ask where students should wait this week."],
[["stop","east","usual"],["construction","sign","closed"],["where","temporary","wait","this week"]])
email("practice","advisor.costa@university.edu","Question about dropping a course",
"You are considering dropping a course because of your workload, but you are unsure about the deadline and your credits.",
["Explain your workload.","Ask about the drop deadline.","Ask how dropping the course would affect your credits."],
[["workload","busy","too many"],["deadline","drop","date"],["credits","affect","financial","progress"]])
email("practice","cafe.manager@university.edu","Allergic reaction to an unlabeled item",
"You bought a snack at the campus café that was not labeled, and it contained nuts.",
["Say what you bought and when.","Describe the labeling problem.","Request clearer labels."],
[["bought","snack","café","yesterday"],["label","nuts","allergy"],["clearer","please","labels","staff"]])
email("practice","it.help@university.edu","Cannot submit an online form",
"The scholarship form freezes after you upload a file, so you are not sure it was received.",
["Say which form you are trying to submit.","Describe what happens when you upload the file.","Ask them to confirm whether it arrived."],
[["scholarship","form","submit"],["upload","freeze","file","loading"],["confirm","received","arrived","status"]])
email("practice","coach.silva@university.edu","Missing practice because of a lab",
"A required lab was moved to the same time as practice, and you will miss two sessions.",
["Explain the schedule conflict.","Say which sessions you will miss.","Ask how you can make up the work."],
[["lab","conflict","same time"],["miss","two","sessions","practice"],["make up","extra","what should"]])
email("practice","landlord@email.com","Request for a quieter study hour",
"You rent a room near campus. Neighbors play loud music every night during your exam week.",
["Explain that it is exam week.","Describe the noise and when it happens.","Ask for a reasonable quiet time at night."],
[["exam","study","week"],["music","loud","night","neighbors"],["quiet","night","please","hours"]])
email("practice","editor@campuspaper.edu","Correction to a published quote",
"The campus paper quoted you, but one sentence changes what you meant about volunteer hours.",
["Identify the article.","Explain the incorrect sentence.","Ask them to print a short correction."],
[["article","paper","quote"],["sentence","meant","incorrect","volunteer"],["correction","print","clarify"]])
email("practice","events@museum.edu","Question about a student discount",
"You want to bring your class to a museum exhibit, but the website does not explain student group prices.",
["Say who you want to bring.","Explain what information is missing.","Ask for the group price and the rules."],
[["class","students","bring"],["website","missing","discount","price"],["group","rules","how much","policy"]])
email("practice","security@university.edu","Lost student ID after a game",
"You lost your ID at the stadium and need a temporary card to enter the dorm tonight.",
["Say where and when you lost the card.","Explain why you need access tonight.","Ask how to get a temporary card."],
[["lost","stadium","game","id"],["tonight","dorm","enter"],["temporary","replacement","how"]])
email("practice","professor.okafor@university.edu","Asking to join a research meeting",
"You are interested in the professor's project on sleep, but you are not in that class.",
["Say what interests you about the project.","Explain your relevant experience briefly.","Ask whether visitors may attend one meeting."],
[["sleep","project","interest"],["class","experience","read"],["meeting","attend","visitor","may I"]])
email("practice","volunteer.office@university.edu","Cannot attend the training",
"You registered for volunteer training, but you now have a doctor's appointment at the same time.",
["Apologize for the change.","Explain the appointment conflict.","Ask if there is another training date."],
[["sorry","apologize","cannot"],["doctor","appointment","conflict"],["another","date","next","reschedule"]])
email("practice","group.member@university.edu","Clarifying your part of the slides",
"You and two classmates are presenting tomorrow, and the slide file has two versions.",
["Say which version you think is current.","Explain the confusion.","Ask the group to confirm the final file tonight."],
[["version","slides","current"],["confusion","two","files"],["confirm","tonight","final","which"]])
email("practice","bookstore@university.edu","Wrong book in a paid order",
"You ordered a required novel and received a different title, but the charge has already posted.",
["Say what you ordered and what arrived.","Mention that you were charged.","Ask for an exchange or a refund."],
[["ordered","novel","received","different"],["charged","paid","price"],["exchange","refund","return"]])
email("mock1","editor@cityarts.org","Problem with a submission form",
"You tried to submit two short stories to a student arts journal, but the form never confirmed the upload.",
["Say what you like about the journal.","Describe the problem with the form.","Ask whether your stories were received."],
[["like","enjoy","journal","stories"],["form","upload","problem","loading"],["received","confirm","status","arrived"]])
email("mock2","facilities@university.edu","Water leak near the language lab",
"A leak in the ceiling outside the language lab is forcing students to walk through water with laptops.",
["Say where the leak is.","Explain the risk to students and equipment.","Ask for a temporary safe path and a repair."],
[["leak","ceiling","language lab","outside"],["laptop","water","risk","walk"],["repair","path","temporary","fix"]])
assert sum(1 for e in emails if e["pool"]=="practice") >= 20
dump("email", emails)
print("emails", len(emails))
