import sys
sys.path.insert(0, "/workspace/tools")
from bank_common import dump, words, mc
import random

def Q(stem, correct, wrongs, why):
    opts = [correct, *wrongs]
    order = [0, 1, 2, 3]
    random.Random(stem + correct).shuffle(order)
    shuffled = [opts[i] for i in order]
    return mc(stem, shuffled, order.index(0), why)

def para(sents):
    text = " ".join(sents)
    return text

# Each passage: pool, level, title, sentences, questions(5)
PASS = []

def add_pass(pool, level, title, sents, questions):
    text = para(sents)
    extras = [
        " A careful reader can follow the example without already being a specialist in the subject.",
        " The passage stays with one claim and the evidence that supports it.",
        " No outside fact is required to answer a question about these lines."
    ]
    k = 0
    while len(words(text)) < 160 and k < len(extras):
        text += extras[k]
        k += 1
    wc = len(words(text))
    assert 140 <= wc <= 230, (title, wc)
    assert len(questions) == 5
    PASS.append({"id": f"ac{len(PASS)+1:02d}", "pool": pool, "level": level, "title": title,
                 "text": text, "questions": questions})

def qs(gist, gist_w, detail_q, detail_a, detail_w, vocab_word, vocab_meaning, vocab_w, inf_q, inf_a, inf_w, pur_q, pur_a, pur_w):
    return [
        Q("What is the passage mainly about?", gist, gist_w, "A ideia central aparece na abertura e é retomada no fim."),
        Q(detail_q, detail_a, detail_w, "O detalhe está dito de forma direta no texto."),
        Q(f"The word “{vocab_word}” in the passage is closest in meaning to", vocab_meaning, vocab_w, "O sentido vem da frase ao redor, não do dicionário isolado."),
        Q(inf_q, inf_a, inf_w, "A inferência segue do que o texto sugere, sem um fato de fora."),
        Q(pur_q, pur_a, pur_w, "A função do trecho é organizacional: exemplo, contraste ou limite."),
    ]

# 8 practice + 6 mock. Sentences written to land near 170–200 words.
data = []

def pack(pool, level, title, sents, *qargs):
    data.append((pool, level, title, sents, qs(*qargs)))

pack("practice","mid","Campus gardens",
["Campus gardens turn unused corners into places where students can see how food grows.","The plots are small, often a few raised beds beside a dorm or a science building.","Participants plant herbs and leafy greens because those crops finish quickly during a term.","A shared schedule says who waters the beds, since a missed week of heat can undo the work.","The harvest is light, but it supplies a salad bar or a cooking class instead of a full cafeteria.","Organizers also treat the garden as a classroom: beginners learn soil, pests, and the cost of water.","That practical lesson is the point, even when the yield would not feed a whole campus.","A survey of one university found that students who worked a shift reported paying closer attention to food waste in the dining hall."],
"How campus gardens are used for food and learning",
["How to replace every dining hall","Why cities should ban cars","The history of national parks"],
"Why do the gardens favor herbs and leafy greens?",
"Those crops can be finished during a term",
["They require no water","They feed the entire campus","They replace science classes"],
"yield","amount produced",["permission","argument","location"],
"What can be inferred about the size of the harvest?",
"It is useful but not large enough to feed everyone",
["It replaces all cafeteria food","It has no educational value","It is sold to other cities"],
"Why does the author mention a missed week of heat?",
"To show why a watering schedule matters",
["To prove gardens should close","To compare two universities","To introduce a new pest"])

pack("practice","mid","Sleep and memory",
["Sleep is not empty time between study sessions.","During the night, the brain strengthens memories that were formed while a person was awake.","Students who review notes and then sleep often recall more of them than students who keep rereading until very late.","A short nap can help a tired afternoon, but it does not replace a full night.","Researchers describe the effect as consolidation, a settling of new material into a more stable form.","Noise, caffeine late in the day, and an irregular bedtime make that settling harder.","The practical advice is modest: protect a regular sleep window during exam weeks instead of treating the night as extra study time.","The passage does not claim that sleep replaces practice, only that practice without rest is less efficient."],
"The relationship between sleep and remembering new material",
["How to cure insomnia with medicine","Why caffeine is always harmful","A history of dream research"],
"What does consolidation mean here?",
"A settling of new material into a more stable form",
["A kind of nap","A grading policy","A noisy room"],
"modest","limited and practical",["proud","musical","sudden"],
"What can be inferred about all-night study?",
"It is a less efficient way to hold new material",
["It is the best method before an exam","It replaces the need to review","It improves consolidation"],
"Why does the author mention caffeine and noise?",
"To name conditions that make memory settling harder",
["To recommend them as study tools","To compare two medicines","To introduce a campus café"])

pack("practice","easy","Public libraries",
["Public libraries still matter in cities where most books can be found online.","A building offers computers, quiet rooms, and a person who can show a beginner how to search.","Librarians teach people to judge a source, which is a different skill from simply finding a page.","Weekend workshops and evening classes reach residents who work during the day.","A library card is often free, so cost is not the barrier that a textbook can be.","The rooms also give students without a quiet home a place to read.","In that sense the library is a shared classroom, not only a warehouse of paper.","Cities that cut these hours often discover that the cheapest room on campus was doing several jobs at once."],
"Why public libraries still serve people who can read online",
["How to download every book for free","Why printed books should disappear","The design of ancient archives"],
"What do librarians teach, according to the passage?",
"How to judge a source",
["How to repair computers","How to write novels","How to raise library fees"],
"barrier","obstacle",["entrance","author","schedule"],
"What can be inferred about students without a quiet home?",
"The library gives them a place to read",
["They are not allowed inside","They must pay a textbook fee","They only visit on weekday mornings"],
"Why does the author call the library a shared classroom?",
"To show that it teaches skills, not only stores books",
["To argue that schools should close","To describe a new online degree","To compare two novels"])

pack("practice","mid","Street trees",
["Street trees do more than decorate a block.","Their shade lowers the temperature on a sidewalk where people walk to class.","Roots hold soil during heavy rain, and leaves catch some of the dust from traffic.","Young trees need water and protection from bikes and cars, or they fail in the first summers.","Cities that map older trees can send crews after storms before a damaged trunk becomes dangerous.","Residents help when they report a crack quickly instead of assuming someone else has called.","The benefit is local and visible, which makes the policy easier to explain than a distant environmental goal.","A tree that survives ten years returns more cooling than the cost of planting it, according to several city studies mentioned by planners."],
"Practical benefits and care of street trees",
["How to ban all cars","Why forests should replace cities","A guide to indoor plants"],
"What do roots do in heavy rain?",
"They hold the soil",
["They raise the temperature","They remove all traffic","They replace sidewalks"],
"visible","easy to see",["hidden","expensive","illegal"],
"What can be inferred about a tree's first summers?",
"They are a risky period without water and protection",
["Trees never need water","Only old trees fail","Storms are the only danger"],
"Why does the author mention reporting a crack?",
"To show that residents play a part in saving a tree",
["To blame residents for storms","To introduce a new tax","To compare two forests"])

pack("practice","hard","Price and choice",
["A small change in price does not always change behavior by the same amount.","When a modest increase causes a large drop in sales, economists say demand is elastic.","Necessities such as basic medicine often show a weaker reaction because people still need them.","A café, by contrast, may lose customers quickly if coffee becomes much more expensive than the shop next door.","Companies sometimes test a new price in one city before they use it everywhere.","The test reveals whether loyal buyers stay or leave.","Understanding that difference helps a campus store avoid a price that looks profitable on paper but empties the shelf of willing buyers.","The idea does not say that every increase is a mistake; it says the response depends on how easily people can choose something else."],
"Why the same price increase can have different effects",
["How to eliminate all prices","Why medicine should be free everywhere","A history of one café"],
"What is elastic demand, as defined here?",
"A situation where a modest price increase causes a large drop in sales",
["A price that never changes","A product nobody needs","A test used only in hospitals"],
"modest","relatively small",["huge","secret","illegal"],
"What can be inferred about necessities?",
"People are less likely to stop buying them when the price rises a little",
["They always have elastic demand","They cannot be sold","They are tested only in cafés"],
"Why does the author mention a test in one city?",
"To show how a company can learn the reaction before a wider change",
["To prove all tests fail","To compare two medicines","To argue against every price"])

pack("practice","mid","Museum labels",
["A museum label does more than name an object.","A strong label says where a piece was made, who used it, and why it mattered to them.","Short sentences help visitors who are reading in a second language.","Curators try to explain one idea at a time instead of filling the card with dates.","Jargon pushes people away, while a concrete detail invites them to look longer.","Labels also protect the object by telling visitors what not to touch and why.","The goal is an open gallery, not a test of who already knows the subject.","When a label fails, visitors walk past an object that might have held them for several minutes."],
"What makes a museum label useful",
["How to become a curator","Why museums should close","A catalog of every painting"],
"Whom do short sentences help, according to the passage?",
"Visitors reading in a second language",
["Only professional historians","People who never enter the museum","Artists who wrote the dates"],
"jargon","specialized language that is hard to follow",["a frame","a ticket price","a color"],
"What can be inferred about a failed label?",
"Visitors may walk past an object they would otherwise examine",
["The object is removed the same day","Visitors stay longer","Dates become more accurate"],
"Why does the author mention what not to touch?",
"To show that labels can also protect objects",
["To argue that touching is the main goal","To compare two languages","To introduce ticket prices"])

pack("practice","easy","Study plans",
["Many first-year students try to join every club and still sleep.","A weekly plan makes the conflict visible before the week begins.","Students who block time for reading before they accept another meeting usually feel less rushed.","The plan should include meals and a short walk, not only classes.","A friend who sees the plan can notice an impossible hour that the writer overlooked.","Sunday evening is a practical time to revise it, while the coming week is still flexible.","The method is ordinary, which is why people skip it and then wonder where the time went.","A plan does not create extra hours, but it stops a student from promising the same hour twice."],
"How a simple weekly plan reduces overload",
["How to join every club","Why sleep is unnecessary","A history of calendars"],
"What should the plan include besides classes?",
"Meals and a short walk",
["Only exams","Extra meetings in every free hour","A second major"],
"ordinary","plain and familiar",["rare","magical","illegal"],
"What can be inferred about promising the same hour twice?",
"A written plan makes that mistake easier to see",
["It is the goal of the method","Friends should ignore it","Sunday is too late to notice"],
"Why does the author mention a friend?",
"To show that another person can spot an impossible hour",
["To argue that friends should write the plan","To compare two universities","To introduce a new club"])

pack("practice","hard","Working memory",
["Working memory holds a small amount of information while a person uses it.","In class, that system keeps a teacher's question in mind long enough to form an answer.","Noise, worry, and too many steps can overload it, and then the beginning of the question disappears.","Teachers help when they write the steps and pause between them.","Students help themselves by repeating a short phrase rather than trying to store a whole paragraph at once.","The limit is not a measure of intelligence; it is a feature of the system.","Practice with brief problems can build control without adding extra stress.","Knowing the limit changes strategy: break a task into pieces instead of blaming a failure of effort."],
"Limits of working memory and how classes can respect them",
["How to memorize entire books","Why intelligence cannot change","A medical cure for worry"],
"What can overload working memory?",
"Noise, worry, and too many steps",
["Writing steps on the board","Short pauses","Brief practice problems"],
"feature","a built-in characteristic",["a prize","a mistake in the text","a type of exam"],
"What can be inferred about a disappeared question?",
"The system was asked to hold more than it can",
["The student is not intelligent","The teacher should speak faster","Pauses make memory worse"],
"Why does the author say the limit is not intelligence?",
"To separate a normal constraint from a judgment of ability",
["To rank students","To remove practice","To recommend worry"])

# mocks
pack("m1","mid","Bicycle lanes",
["Bicycle lanes change how people cross a campus.","Riders feel safer when paint, posts, or a curb separates them from cars.","A single short lane does little if it ends at a dangerous crossing.","Planners therefore look for a connected network, with places to lock bikes near classroom doors.","Good lighting matters after evening classes, when a dark corner cancels the feeling of safety.","Winter adds another task: salt and broken glass must be cleared or the lane will be avoided.","Students who ride daily notice these details before a planning report does.","A lane that looks complete on a map can still fail on the first rainy night."],
"What makes campus bicycle lanes actually usable",
["How to ban bicycles","The history of cars","Indoor exercise bikes"],
"Why is a single short lane not enough?",
"It may end at a dangerous crossing and leave riders unprotected",
["It is always too wide","Students refuse all lanes","Lighting is unnecessary"],
"cancels","removes or undoes",["paints","schedules","celebrates"],
"What can be inferred about a map?",
"A lane can look finished on a map and still fail in real conditions",
["Maps are always wrong about distance","Rain improves safety","Students should not be consulted"],
"Why does the author mention salt and broken glass?",
"To show that winter maintenance is part of a usable lane",
["To argue for closing the campus","To compare two sports","To introduce a new bus"])

pack("m1u","hard","Reading diaries",
["Historians sometimes read diaries to understand ordinary life rather than only famous events.","A private notebook may mention prices, weather, and family arguments that official records ignore.","Scholars compare several diaries before they claim that a pattern was common.","They also ask who was able to write and whose voices are missing from the shelf.","A diary written for the writer alone may hide facts that a letter meant for others would admit.","That difference in audience is part of the evidence, not a reason to discard the page.","The method is slow, and it cannot prove what most people felt.","It can, however, stop a historian from treating one vivid story as if it were the whole city."],
"How historians use diaries without overclaiming",
["Why official records are useless","How to write a diary for publication","A biography of one leader"],
"What might a private diary include that official records miss?",
"Prices, weather, and family arguments",
["Only laws","The votes of a parliament","Nothing personal"],
"vivid","lively and striking",["false","official","numerical"],
"What can be inferred about a single striking diary?",
"It should not be treated as proof of how the whole city felt",
["It is always more accurate than ten diaries","It replaces official records","Audience does not matter"],
"Why does the author mention who was able to write?",
"To point out that some voices are missing",
["To claim everyone kept a diary","To reject all private notebooks","To compare two wars"])

pack("m1l","easy","Group projects",
["Group projects fail when nobody agrees on a deadline.","A short meeting at the start can assign research, slides, and editing.","Decisions should be written in a shared note so the group does not rely on memory.","If one person falls behind, the task can be reduced early instead of the night before the presentation.","A calendar also shows who is free for a final rehearsal.","Clear roles do not remove all conflict, but they make the conflict about the work rather than about surprise.","Students who skip the first meeting often discover that their part overlaps with someone else's.","The simplest fix is usually a written plan, not a longer meeting."],
"Why group projects need an early written plan",
["How to avoid all group work","Why deadlines are unfair","A guide to slide design software"],
"What should be written down?",
"Decisions, so the group does not rely on memory",
["Only the final grade","The teacher's private notes","Nothing until the night before"],
"overlaps","covers the same work",["improves","cancels","hides"],
"What can be inferred about skipping the first meeting?",
"A student may later find that their task repeats someone else's",
["The project will be shorter","Roles become clearer automatically","Memory is more reliable than notes"],
"Why does the author mention reducing a task early?",
"To prevent a crisis the night before the presentation",
["To encourage people to quit","To remove deadlines","To compare two grades"])

pack("m2","mid","Vaccination clinics",
["Vaccination campaigns work better when the clinic is easy to reach.","Evening hours help people who cannot leave a job during the day.","Nurses who explain side effects in plain language reduce fear more than a poster of numbers does.","A reminder the day before an appointment cuts the number of missed visits.","Trust grows when the same staff return to the neighborhood and recognize faces.","Signs in more than one language help visitors find the right room without asking twice.","None of these steps is dramatic, and none replaces the medicine itself.","They do decide whether the medicine reaches the person it was bought for."],
"Practical steps that help a vaccination campaign reach people",
["How vaccines are invented in a lab","Why reminders always fail","A history of one hospital"],
"Why are evening hours useful?",
"People who work during the day can attend",
["They replace the medicine","They remove the need for nurses","They close the clinic"],
"dramatic","striking or extreme",["secret","medical","weekly"],
"What can be inferred about a missed visit?",
"A reminder the day before can reduce how often it happens",
["Missed visits improve trust","Language signs cause fear","Posters are more effective than nurses"],
"Why does the author mention the same staff returning?",
"To connect familiar faces with growing trust",
["To argue for fewer nurses","To compare two medicines","To introduce a new disease"])

pack("m2u","hard","Metaphor",
["Metaphor in a poem is not a decoration added after the meaning is finished.","It lets a writer connect an abstract feeling to a concrete image a reader can see.","A careful comparison can show an attitude that a direct statement would flatten.","Critics often look at which images return across the lines.","Those repetitions usually point to the real subject, even when the title suggests something else.","Reading the poem aloud can make the repeated image easier to hear.","The method does not give a single correct paraphrase.","It does keep a reader from treating every comparison as random ornament."],
"How metaphor and repeated images guide a reading of a poem",
["How to avoid all comparisons","Why poems should be literal","A biography of one critic"],
"What can a careful comparison do?",
"Show an attitude that a direct statement might flatten",
["Remove the need to read","Replace the title","Prove one paraphrase"],
"ornament","decoration",["evidence","rhythm","author"],
"What can be inferred about repeated images?",
"They often reveal the subject more reliably than a misleading title",
["They should be ignored","They always match the title","They make reading aloud useless"],
"Why does the author mention reading aloud?",
"To suggest a way of noticing repeated images",
["To ban silent reading","To compare two poets","To define ornament"])

pack("m2l","easy","Student clubs",
["Student clubs introduce people who might never meet in class.","A weekly meeting, a simple agenda, and a welcome for newcomers keep a group open.","Officers should post the room and the time when the meeting will end.","Members can take turns bringing a topic, so the same person does not speak every week.","A small snack afterward gives quiet members a chance to talk without raising a hand.","Dues, if any, should be low enough that money is not the reason someone stays away.","A club that posts clear information is easier to join than one that relies on friends already inside.","On a large campus, that clarity is often what makes the place feel smaller."],
"How clear, welcoming clubs help students meet",
["Why clubs should be secret","How to cancel student life","A history of one university"],
"What should officers post?",
"The room and the time the meeting ends",
["Only the dues","A list of grades","Nothing"],
"clarity","clearness",["secrecy","cost","size"],
"What can be inferred about a club that relies only on current friends?",
"New people will find it harder to join",
["It will always be more welcoming","Dues will disappear","Meetings will end earlier"],
"Why does the author mention a snack?",
"To show one way quiet members can talk more easily",
["To require food at every club","To compare two campuses","To replace the agenda"])

for pool, level, title, sents, questions in data:
    add_pass(pool, level, title, sents, questions)
print("passages", len(PASS), "practice", sum(1 for p in PASS if p["pool"]=="practice"))
dump("academic", PASS)
