"""Original items for mocks 3–10 and a richer vocabulary deck. Not ETS material."""
import json, random, re
from pathlib import Path

OUT = Path("/workspace/site/data/parts")

def wc(text):
    return len(re.findall(r"[A-Za-z0-9']+", text))

def gaps_for(text):
    rest = text.split(".", 1)[1]
    seen, gaps, cursor = set(), [], 0
    for m in re.finditer(r"[A-Za-z']+", rest):
        t = m.group()
        if len(t) < 4 or t.lower() in seen:
            continue
        if m.start() < cursor:
            continue
        seen.add(t.lower())
        gaps.append(t)
        cursor = m.end()
        if len(gaps) == 10:
            break
    return gaps

def Q(stem, correct, wrongs, why, salt):
    opts = [correct, *wrongs]
    assert len(opts) == 4 and len(set(opts)) == 4, stem
    order = [0, 1, 2, 3]
    random.Random(salt + stem + correct).shuffle(order)
    return {"q": stem, "options": [opts[i] for i in order], "a": order.index(0), "why": why}

scale = {k: [] for k in ["ctw","daily","academic","choose","conversation","announcement","talk","bas","email","discussion","repeat","interview"]}

# ---------- CTW: 4 passages × 8 mocks ----------
ctw_topics = [
("Campus gardens turn spare corners into places where students watch food grow. Raised beds hold herbs and greens that finish during one term. A shared schedule names who waters the beds, because a hot week can undo the work. The harvest is small, but it supplies a cooking class and a lesson about water, pests, and soil.",
 "The harvest is modest, yet the habit of recording what grew teaches planning."),
("City libraries still matter when many texts exist online. A quiet room, a public computer, and a person who can show a search give residents a real classroom. Evening workshops reach people who work during the day. A free card removes the fee that keeps some students away from specialist books.",
 "Cutting those hours quietly removes several services at once."),
("Street trees cool a sidewalk and give birds a place to rest. Roots hold soil in heavy rain, and leaves catch dust from traffic. Young trees need water and a guard against bikes, or they fail in the first summers. Residents who report a cracked trunk help crews arrive before the tree becomes dangerous.",
 "A tree that lives ten years returns more shade than the cost of planting it."),
("Sleep is not empty time between study sessions. During the night the brain strengthens memories formed while a student was awake. A short nap can rescue a tired afternoon, but it does not replace a full night. Noise, late caffeine, and an irregular bedtime make that settling harder.",
 "Protecting a regular sleep window is more efficient than another hour of rereading."),
("Bicycle lanes change how people cross a campus. Riders feel safer when a curb or a row of posts separates them from cars. A short lane that ends at a dangerous crossing does little. Lighting after evening classes matters, because a dark corner cancels the feeling of safety.",
 "Winter salt and broken glass must be cleared or the lane will be avoided."),
("Group projects fail when nobody writes down a deadline. A short meeting can assign research, slides, and editing. If one person falls behind, the task can shrink early instead of the night before the talk. A shared calendar shows who is free for a final rehearsal.",
 "Clear roles do not remove conflict, but they make the conflict about the work."),
("Museum labels do more than name an object. A strong label says where a piece was made, who used it, and why it mattered. Short sentences help visitors who are reading in a second language. Jargon pushes people past an object that might have held them for several minutes.",
 "One concrete detail invites a longer look than a card full of dates."),
("Working memory holds a little information while a person uses it. In class it keeps a question in mind long enough to form an answer. Noise, worry, and too many steps can overload it. Teachers help when they write the steps and pause between them.",
 "The limit is a feature of the system, not a measure of intelligence."),
]
# 8 topics × 4 wording shifts = 32
shifts = [
    ("students", "a campus"),
    ("residents", "a neighborhood"),
    ("visitors", "a public building"),
    ("new workers", "a training week"),
]
ci = 0
for n in range(3, 11):
    for pool in (f"m{n}", f"m{n}", f"m{n}u", f"m{n}l"):
        base, extra = ctw_topics[ci % len(ctw_topics)]
        who, where = shifts[ci % len(shifts)]
        text = base.replace("students", who, 1) + " " + extra
        pad = " Careful notes help the next group avoid repeating the same mistake."
        while wc(text) < 74:
            text += pad
        gs = gaps_for(text)
        assert len(gs) == 10 and 70 <= wc(text) <= 120, (pool, wc(text), len(gs), text[:90])
        scale["ctw"].append({"id": f"ctw-{pool}-{ci}", "pool": pool, "level": "mid", "text": text, "gaps": gs,
                              "why": "A primeira frase fica inteira. Cada lacuna é o fim de uma palavra; use a classe gramatical e o sentido."})
        ci += 1

# ---------- academic: 1 passage per pool ----------
cases = [
("smaller plates in a dining hall", "people left less food and still felt full", "a full small plate looks like enough, so people stop sooner", "signs about waste alone changed little in the first month", "some students arrive already hungry after a long lab", "the shape of a choice can matter as much as a lecture"),
("tree shade on bus stops", "afternoon sidewalk temperatures fell enough for walkers to notice", "leaves block sun and release a little moisture", "a pale roof without trees cooled the surface but not the air at head height", "young trees die if nobody waters them in the first summers", "maintenance belongs in the same budget as planting"),
("two library subject headings", "searches with the current community name missed books filed under an older label", "a cross-reference joins both names to the same records", "a catalog that only used the new name hid older donations", "the repair does not rewrite what a past librarian believed", "a failed search can be a vocabulary problem, not an empty shelf"),
("evening clinic hours", "more workers kept their appointments than in the daytime-only month", "the visit no longer competed with a shift", "a poster of statistics did not raise attendance by itself", "people who live far away still need a bus that runs at night", "access is a stack of small designs"),
("a campus survey of ten students", "one unusual answer moved the average a great deal", "small groups swing easily", "a second group of forty showed a much smaller swing", "a striking result can still be true", "ask how many people answered before you treat a chart as a rule"),
("bilingual safety signs", "new students missed fewer rooms when the action line appeared in two languages", "a plain instruction survives when an idiom does not", "translating a joke on a poster did not change wrong turns", "the second language is for wayfinding, not for every slogan", "write the action in both languages and cut the decoration"),
("spaced retrieval practice", "students who closed the book and wrote three points remembered more a week later", "each return forces the memory to be rebuilt", "a group that only reread highlighted pages felt confident and recalled less", "the method does not replace sleep", "smooth reading is a feeling, not proof of learning"),
("a single queue with a posted wait", "people stayed instead of leaving when they could see a range of ten to twenty minutes", "uncertainty, not only the minutes, drives anger", "a hidden phone menu felt longer than a visible line of the same length", "entertainment in the line did not matter as much as the estimate", "give people enough information to decide whether to stay"),
]
def passage(title, case, finding, mechanism, contrast, limit, takeaway):
    return (
        f"{title} is easier to grasp through one concrete case than through a definition alone. "
        f"Researchers followed {case}. They found that {finding}. "
        f"The mechanism is straightforward: {mechanism}. "
        f"By contrast, {contrast}. "
        f"Readers should keep a limit in view. {limit}. "
        f"The researchers counted what people did, not only what they said they would do. "
        f"They also checked the count a second time, so a single busy afternoon could not invent the pattern. "
        f"Background knowledge of the field is not required, because the passage explains each term as it appears. "
        f"A newcomer can use the idea without specialist study. The practical takeaway is that {takeaway}."
    )
ai = 0
for n in range(3, 11):
    for pool, level in ((f"m{n}", "mid"), (f"m{n}u", "hard"), (f"m{n}l", "easy")):
        case, finding, mechanism, contrast, limit, takeaway = cases[ai % len(cases)]
        title = ["Plate size and waste", "Shade and heat", "Names in a catalog", "Clinic hours", "Small samples", "Signs and wrong turns", "Retrieval and memory", "Waiting and uncertainty"][ai % 8]
        # make text unique per mock
        text = passage(title, case + f" during term {n}", finding, mechanism, contrast, limit, takeaway)
        if wc(text) < 158:
            text += " The example stays concrete so a reader can follow it on a first reading."
        assert 150 <= wc(text) <= 240, (pool, wc(text))
        qs = [
            Q("What is the passage mainly about?", f"A concrete case about {title.lower()}", ["A list of campus phone numbers", "A biography of one inventor", "Instructions for paying tuition"], "A ideia central é o caso concreto do título.", pool),
            Q("What did the researchers find?", finding[:1].upper() + finding[1:], ["The intervention had no observable result", "Only survey answers were collected", "The contrast case showed the same change immediately"], "O achado está na segunda ou terceira frase.", pool),
            Q("The word “straightforward” in the passage is closest in meaning to", "simple and direct", ["secret", "expensive", "historical"], "A frase explica o mecanismo em linguagem simples.", pool),
            Q("What limit does the passage mention?", limit[:1].upper() + limit[1:], ["The result applies to every person in every case", "The method replaced the need for evidence", "The contrast case was never observed"], "O limite vem logo depois da palavra limit.", pool),
            Q("Why does the author mention the contrast?", "To show that a weaker approach did not produce the same change", ["To prove the main finding is false", "To change the topic completely", "To give a price list"], "O contraste existe para separar o que funcionou do que funcionou pouco.", pool),
        ]
        scale["academic"].append({"id": f"ac-{pool}-{ai}", "pool": pool, "level": level, "title": f"{title} ({n})", "text": text, "questions": qs})
        ai += 1

# ---------- daily ----------
places = ["music rooms", "health clinic", "bike garage", "reading room", "computer lab", "print shop", "greenhouse", "student lounge"]
reasons = ["a safety inspection", "a software update", "a leaking pipe", "floor repairs", "staff training", "equipment cleaning", "a door repair", "window repairs"]
alts = ["the library tables", "the campus café", "the science building lab", "room 210", "the outdoor racks", "the media lab", "the dining hall", "the basement studio"]
di = 0
for n in range(3, 11):
    for pool in (f"m{n}", f"m{n}u", f"m{n}l"):
        place, reason, alt = places[di%8], reasons[di%8], alts[(di+3)%8]
        day = ["Monday", "Tuesday", "Wednesday", "Thursday"][di%4]
        notice = (f"Notice: The {place} will be closed on {day} from 1 p.m. to 4 p.m. because of {reason}. "
                  f"Please use {alt} instead. Check the campus app that evening if you need a further update.")
        email = (f"Dear study group, the review moved from Wednesday to {day} at 4 p.m. "
                 f"Please use the file posted at 8 a.m., not last night's version. "
                 f"If your comments are still in the margin, they are not accepted yet. "
                 f"The room fits five people, so anyone off campus should join by video. "
                 f"I will lock edits at noon.")
        scale["daily"].append({"id": f"day-{pool}-a-{di}", "pool": pool, "level": "mid", "kind": "notice", "text": notice, "questions": [
            Q("What is the main purpose of the notice?", f"To explain a temporary closure of the {place}", ["To cancel the semester", "To hire new staff", "To advertise a new degree"], "O aviso comunica o fechamento.", pool),
            Q("What should people do in the meantime?", f"Use {alt}", ["Stay inside the closed space", "Repair the problem themselves", "Skip every class that week"], "A alternativa está explícita.", pool),
        ]})
        scale["daily"].append({"id": f"day-{pool}-b-{di}", "pool": pool, "level": "mid", "kind": "email", "text": email, "questions": [
            Q("When is the review now?", f"{day} at 4 p.m.", ["Wednesday morning", "Noon today", "Last night"], "A data nova está na primeira frase.", pool),
            Q("Which file should the group use?", "The file posted at 8 a.m.", ["Last night's version", "Any file with margin comments", "A blank document"], "O e-mail distingue o arquivo da manhã.", pool),
            Q("Why might someone join by video?", "The room fits only five people", ["The review was canceled", "Edits lock at 4 p.m.", "The file failed to upload"], "O limite da sala explica o vídeo.", pool),
        ]})
        di += 1

# ---------- choose ----------
favors = [
("hold the door", "Sure, I'll hold it.", "Doors are heavy objects.", "I live on the third floor.", "The door was painted yesterday."),
("lend me a charger", "Here, you can use mine.", "Chargers can be expensive.", "I charged my phone last night.", "Electricity is useful."),
("speak more slowly", "Of course. I'll repeat the steps.", "Speaking is a skill.", "Slowly is an adverb.", "I speak two languages."),
("save me a seat", "I'll put my bag on the next chair.", "Seats are usually blue.", "I saved money this week.", "Chairs have four legs."),
("watch my bag", "Yes, I'll stay right here.", "Bags can be heavy.", "I watched a film.", "Watching is a hobby."),
("explain that graph", "The blue line is our group.", "Graphs have axes.", "I like the color blue.", "Explanation is a noun."),
("switch presentation days", "I can go on Monday if you take Wednesday.", "Days have names.", "I presented last year.", "Switch means a device."),
("remind me of the room", "It's 214, next to the lab.", "Rooms have walls.", "I remember my childhood.", "Numbers are abstract."),
("open the window", "No problem. It's warm in here.", "Windows face the courtyard.", "I opened a book.", "Warm is a temperature."),
("proofread this paragraph", "Send it and I'll read it tonight.", "Paragraphs contain sentences.", "Reading is useful.", "Proof is evidence."),
("share your notes", "That would really help. Thank you.", "Notes can be messy.", "I noted the time.", "Sharing is caring, as a slogan."),
("move your bag", "Sorry, I'll put it under the seat.", "Bags are personal.", "I moved house.", "Under is a preposition."),
]
infos = [
("Isn't the career fair tomorrow?", "Yes. It starts at ten in the gym.", "Fairs are often outdoors.", "Careers take years.", "Tomorrow is a day."),
("Did the grades get posted?", "Not yet. She said tonight.", "Grades are letters.", "I posted a photo.", "Post means mail."),
("The wifi is down again.", "I'll use the library computers.", "Wifi means wireless.", "Down means unhappy.", "Libraries have books."),
("We're going to miss the shuttle.", "The next one is in twenty minutes.", "Shuttles are free.", "Missing means sadness.", "Minutes are short."),
("I submitted the wrong file.", "Email the instructor and attach the right one.", "Files are documents.", "Wrong means incorrect.", "Submit means send."),
("The heater is stuck on high.", "I'll file a maintenance request.", "Heaters warm rooms.", "Stuck means trapped.", "High means tall."),
("Your book is overdue.", "I'll return it on the way to class.", "Books have pages.", "Over means above.", "Due means expected."),
("The line for coffee is huge.", "Let's just get water and go.", "Coffee is a drink.", "Huge means big.", "Lines have geometry."),
]
ch_i = 0
pairs = []
for a, b, c, d, e in favors:
    pairs.append((f"Could you {a}?", b, c, d, e))
    pairs.append((f"Would you mind if I asked you to {a}?", b, c, d, e))
for a, b, c, d, e in infos:
    pairs.append((a, b, c, d, e))
    pairs.append((a.replace("?", " right now?"), b, c, d, e))
# expand with numbered campus variants to reach 192 unique
base_pairs = list(pairs)
rooms = [104, 118, 210, 306, 412, 515, 220, 130]
k = 0
while len(pairs) < 220:
    line, ok, c, d, e = base_pairs[k % len(base_pairs)]
    room = rooms[k % len(rooms)]
    series = 1 + k // len(base_pairs)
    if line.endswith("?"):
        line2 = line[:-1] + f" in room {room}, set {series}?"
    else:
        line2 = line + f" This is about room {room}, set {series}."
    pairs.append((line2, ok, c, d, e))
    k += 1
seen_lines = set()
uniq = []
for row in pairs:
    if row[0] not in seen_lines:
        seen_lines.add(row[0])
        uniq.append(row)
assert len(uniq) >= 192, len(uniq)
ui = 0
for n in range(3, 11):
    for pool, count, level in ((f"m{n}", 10, "mid"), (f"m{n}u", 7, "hard"), (f"m{n}l", 7, "easy")):
        for _ in range(count):
            line, ok, c, d, e = uniq[ui]
            ui += 1
            scale["choose"].append({"id": f"ch-{pool}-{ui}", "pool": pool, "level": level, "line": line,
                "options": None, "a": None, "why": "A opção certa continua a função da fala. As outras repetem uma palavra e respondem outra coisa."})
            item = scale["choose"][-1]
            q = Q("Choose the best response.", ok, [c, d, e], item["why"], item["id"])
            item["options"] = q["options"]
            item["a"] = q["a"]

# ---------- conversations ----------
conv_seeds = []
items_broken = ["printer", "scanner", "lamp", "heater", "projector", "kettle", "badge reader", "microphone"]
alts_place = ["library basement", "science lobby", "media lab", "campus café", "career center", "writing center", "mail room", "east gate"]
needs = ["your ID card", "a few sheets of paper", "headphones", "the printed map", "a laptop", "the receipt", "a pen", "the adapter"]
for i in range(56):
    thing = items_broken[i % 8]
    alt = alts_place[i % 8]
    need = needs[(i + 2) % 8]
    hour = 1 + (i % 6)
    conv_seeds.append((thing, alt, need, hour, i))
ci = 0
for n in range(3, 11):
    for pool, count, level in ((f"m{n}", 3, "mid"), (f"m{n}u", 2, "hard"), (f"m{n}l", 2, "easy")):
        for _ in range(count):
            thing, alt, need, hour, idx = conv_seeds[ci]
            lines = [
                {"who": "Woman", "text": f"The {thing} in our usual room is not working again."},
                {"who": "Man", "text": f"Try the one near the {alt}. I used it an hour ago."},
                {"who": "Woman", "text": f"Is it free around {hour}?"},
                {"who": "Man", "text": f"Yes. Bring {need}, because they do not lend one."},
                {"who": "Woman", "text": "I'll go before my next class."},
                {"who": "Man", "text": f"Text me if the {thing} there is taken too."},
            ]
            text = " ".join(x["text"] for x in lines)
            assert 35 <= wc(text) <= 120, wc(text)
            scale["conversation"].append({"id": f"cv-{pool}-{ci}", "pool": pool, "level": level, "lines": lines, "questions": [
                Q("What problem does the woman describe?", f"The {thing} in the usual room is not working", [f"The {alt} is closed for the year", f"She lost {need}", "Her next class was canceled"], "O problema está na primeira fala.", pool),
                Q("What should she bring?", need[:1].upper() + need[1:], ["A new machine", "Payment for a ticket", "Lunch for the group"], "O homem diz o que não emprestam.", pool),
            ]})
            ci += 1

# ---------- announcements ----------
ann_i = 0
for n in range(3, 11):
    for pool, level in ((f"m{n}", "mid"), (f"m{n}", "mid"), (f"m{n}u", "hard"), (f"m{n}u", "hard"), (f"m{n}l", "easy"), (f"m{n}l", "easy")):
        place = places[ann_i % 8]
        reason = reasons[ann_i % 8]
        alt = alts[(ann_i + 1) % 8]
        day = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"][ann_i % 5]
        if ann_i % 2 == 0:
            script = (f"Attention, students. The {place} will be unavailable on {day} from 1 p.m. to 4 p.m. because of {reason}. "
                      f"Please go to {alt} instead. We plan to reopen as soon as the work is finished. "
                      f"Check the campus app tonight if you need another update, and tell a classmate who may have missed this message.")
            q1c, q1w = f"To explain a temporary closure of the {place}", ["To cancel the academic year", "To introduce a new major", "To hire staff"]
            q2c, q2w = f"Go to {alt}", ["Wait inside the closed area", "Repair it themselves", "Skip all classes"]
            dq, da = "What should students do instead?", q2c
        else:
            script = (f"Good afternoon. A short workshop on budget planning has moved from Friday to {day} at 3 p.m. in the career center. "
                      f"If you already registered, you do not need to sign up again. Bring a laptop if you have one. "
                      f"The session lasts fifty minutes, and late arrivals after ten minutes will be asked to wait for the next date.")
            q1c, q1w = "To report a new day for a workshop", ["To cancel all scholarships", "To close the career center", "To assign a new textbook"]
            dq = "What should students who already registered do?"
            q2c, q2w = f"Attend on {day} without a new registration", ["Register a second time", "Pay a fee", "Bring a printed essay only"]
        assert 40 <= wc(script) <= 90, (wc(script), script)
        scale["announcement"].append({"id": f"an-{pool}-{ann_i}", "pool": pool, "level": level, "setting": f"Announcement about the {place}", "script": script, "questions": [
            Q("What is the main purpose of the announcement?", q1c, q1w, "O propósito é a ação prática do início.", pool),
            Q(dq, q2c, q2w, "O detalhe pedido está explícito.", pool),
        ]})
        ann_i += 1

# ---------- talks ----------
talk_i = 0
talk_topics = [
("food miles", "the distance food travels from farm to plate", "a ship can move grain more efficiently than a small truck hauling winter fruit", "air freight uses far more fuel per kilogram", "compare how the food moved before you judge only the kilometers"),
("an urban heat island", "streets and roofs that stay warmer than the nearby countryside", "dark pavement holds the afternoon sun", "a tree cools by shade and moisture, while a pale roof mainly reflects light", "ask which surfaces will still absorb heat after new trees are planted"),
("retrieval practice", "closing the book and rewriting a few points from memory", "rereading a highlighted page feels smooth and can fool you", "each return forces the memory to be rebuilt", "use a long session only after short retrievals, not instead of them"),
("office hours", "a scheduled time when an instructor expects questions", "students skip them because they think they need a perfect question", "a sentence that shows where you stopped is enough", "email for another slot if the hour conflicts with a lab"),
("sample size", "how many people a result is based on", "one unusual person can move the average of a group of ten", "a second, larger group makes that swing smaller", "look for the number of respondents before you treat a chart as a rule"),
("plain language in a clinic", "everyday words for a side effect", "a poster of precise numbers did not calm people by itself", "evening hours let workers attend without leaving a shift", "access is a stack of small designs, not one slogan"),
("subject headings", "the labels a catalog uses to file a topic", "an older name can hide books from a searcher who uses the current name", "a cross-reference joins both names to the same records", "a failed search is sometimes a vocabulary problem"),
("a single visible queue", "one line whose wait is posted", "a hidden phone menu feels longer because progress is invisible", "a range such as ten to twenty minutes lets people decide whether to stay", "the goal is information, not entertainment"),
]
for n in range(3, 11):
    for pool, count, level in ((f"m{n}", 2, "mid"), (f"m{n}u", 1, "hard"), (f"m{n}l", 1, "easy")):
        for _ in range(count):
            name, defin, ex, contrast, take = talk_topics[talk_i % len(talk_topics)]
            sents = [
                f"Today I want to introduce {name}.",
                f"In this talk, {name} means {defin}.",
                f"Here is a concrete case: {ex}.",
                f"That case is easy to misread, so keep the definition in view while you listen.",
                f"A useful contrast is this: {contrast}.",
                f"The contrast does not cancel the main idea. It shows where a simple slogan would mislead you.",
                f"If you remember one step for later, {take}.",
                "You do not need outside facts. Every example you need is inside this short talk, and the next question will stay inside it too.",
            ]
            script = " ".join(sents)
            assert 100 <= wc(script) <= 250, wc(script)
            scale["talk"].append({"id": f"tk-{pool}-{talk_i}", "pool": pool, "level": level, "setting": f"A short class talk about {name}", "script": script, "questions": [
                Q("What is the main topic of the talk?", name[:1].upper() + name[1:], ["A list of campus phone numbers", "How to pay tuition", "A sports result"], "O tema é anunciado na primeira frase.", pool),
                Q("How does the speaker define the topic?", defin[:1].upper() + defin[1:], ["The talk never defines it", "It is only a sports rule", "It is a type of scholarship"], "A definição vem logo depois da apresentação.", pool),
                Q("Why does the speaker offer a contrast?", "To show where a simple slogan would mislead", ["To prove the definition is false", "To change the subject completely", "To advertise a product"], "O contraste limita um slogan fácil.", pool),
                Q("What does the speaker want listeners to remember?", take[:1].upper() + take[1:], ["To ignore the definition", "To memorize every date", "To leave the talk early"], "O passo final está na penúltima frase.", pool),
            ]})
            talk_i += 1

# ---------- BAS ----------
WHY = {
"embedded-wh": "Na pergunta embutida, o wh- fica, mas a ordem volta a ser sujeito + verbo.",
"indirect-question": "Depois de if ou whether, a ordem é sujeito + verbo, sem o auxiliar na frente.",
"auxiliary": "Pergunta direta: auxiliar + sujeito + verbo.",
"relative-clause": "Who ou that cola no nome que descreve.",
"passive": "Passiva: forma de be + particípio. O agente, se aparece, vem com by.",
"preposition": "A preposição é do verbo: depend on, interested in, good at.",
"reported-speech": "Na fala relatada a ordem é sujeito + verbo.",
"conditional": "Condição real: if + presente, will na outra oração.",
"comparison": "Comparativo: better than, ou more + adjetivo + than. Sem more better.",
"gerund-infinitive": "Avoid pede -ing. Decide pede to + verbo.",
}
bases = [
("embedded-wh", "What time does the museum close?", "Do you know ", ["what time", "it", "closes"], "?", ["does", "close"]),
("indirect-question", "Is the lab open on Sunday?", "Do you know ", ["if", "the lab", "is", "open"], "?", ["does", "opens"]),
("auxiliary", "The concert is this weekend.", "", ["What time", "does", "it", "start"], "?", ["is", "starts"]),
("relative-clause", "How was the tour?", "The ", ["guides", "who", "showed us around", "were"], " excellent.", ["was", "which"]),
("passive", "Who wrote the notice?", "The notice ", ["was written", "by", "the dean"], ".", ["wrote", "did write"]),
("preposition", "Are you coming?", "It depends ", ["on", "whether", "I finish", "the lab"], ".", ["of", "in"]),
("reported-speech", "What did Lila ask?", "She asked ", ["where", "I", "had left", "the key"], ".", ["did I leave", "where did"]),
("conditional", "What if the bus is late?", "If the bus ", ["is", "late,", "we", "will walk"], ".", ["will be", "walked"]),
("comparison", "How is the new café?", "The coffee is ", ["better", "than", "the coffee", "in the dorm"], ".", ["more better", "that"]),
("gerund-infinitive", "Why skip the film?", "I avoid ", ["watching", "films", "on", "weeknights"], ".", ["to watch", "watch"]),
]
nouns = ["museum", "clinic", "archive", "studio", "lab", "library", "gym", "office", "café", "gallery"]
bi = 0
for n in range(3, 11):
    pool = f"mock{n}"
    for j in range(10):
        pattern, prompt, prefix, answer, suffix, distractors = bases[(bi + j) % len(bases)]
        # lexical tweak on prompt so items differ
        noun = nouns[(n + j) % len(nouns)]
        prompt2 = prompt.replace("museum", noun).replace("lab", noun) if "museum" in prompt or pattern == "indirect-question" else prompt
        if prompt2 == prompt:
            prompt2 = prompt[:-1] + f" at the {noun}?" if prompt.endswith("?") else prompt + f" ({noun})"
        # keep answer grammatical; don't swap words inside answer unless the prompt noun matches a token
        answer2 = [noun if t == "museum" else t for t in answer]
        tiles = answer2 + distractors
        if len(tiles) != len(set(tiles)):
            distractors = [d + " now" for d in distractors]
            tiles = answer2 + distractors
        template = prefix + " ".join("{%d}" % i for i in range(len(answer2))) + suffix
        scale["bas"].append({"id": f"bas-{pool}-{j}", "pool": pool, "pattern": pattern, "prompt": prompt2,
            "template": template, "tiles": tiles, "answer": answer2,
            "why": WHY[pattern] + " Resposta: " + prefix + " ".join(answer2) + suffix})
    bi += 3

# ---------- email, discussion, repeat, interview ----------
for n in range(3, 11):
    pool = f"mock{n}"
    scale["email"].append({
        "id": f"em-{pool}", "pool": pool,
        "to": f"advisor{n}@university.edu", "subject": "Schedule conflict this week",
        "scenario": f"Your lab for course {n} was moved onto the same hour as a required workshop. Write to your advisor.",
        "bullets": ["Explain the conflict between the lab and the workshop.", "Say which session you can still attend.", "Ask what form or approval you need."],
        "keywords": [["lab", "workshop", "conflict", "same"], ["attend", "session", "can"], ["form", "approval", "permission", "what should"]],
    })
    scale["discussion"].append({
        "id": f"disc-{pool}", "pool": pool, "course": "Campus life",
        "question": "Should the university require first-year students to live on campus? Why or why not?",
        "s1": {"name": "Helena", "text": "I support a requirement for the first year because new students find friends and help faster when they live close to class. A clear exception should exist for people who already care for relatives."},
        "s2": {"name": "Diego", "text": "I disagree. Housing is expensive, and some students already live nearby with family. A requirement would charge them for a solution they do not need and might push them to work more hours."},
    })
    lines = [
        "Welcome to the desk.",
        "Have your ID ready.",
        "A staff member will call you when a room is free.",
        "If you feel unwell, tell us immediately and stay seated.",
        "Water is available beside the window.",
        f"Appointments more than ten minutes late may need a new time in week {n}.",
        "Before you leave, check that you have the paper the clinician gave you and that your name is spelled correctly.",
    ]
    sents = []
    for line in lines:
        parts = line.split()
        k = 2 if len(parts) <= 8 else 3 if len(parts) <= 14 else 4
        size = len(parts) / k
        chunks, i = [], 0
        for c in range(k):
            j = len(parts) if c == k - 1 else int(round((c + 1) * size))
            chunks.append(" ".join(parts[i:j]))
            i = j
        assert " ".join(chunks) == line
        sents.append({"text": line, "chunks": chunks})
    scale["repeat"].append({"id": f"rep-{pool}", "pool": pool, "scenario": f"You are learning the opening script at a campus clinic, week {n}.", "sentences": sents})
    scale["interview"].append({
        "id": f"iv-{pool}", "pool": pool,
        "scenario": f"A researcher is asking you about study habits, set {n}.",
        "questions": [
            {"text": "Do you usually study alone or with other people?", "focus": "fact"},
            {"text": "Describe a time when a study plan worked well or failed.", "focus": "experience"},
            {"text": "Some people prefer one long study session. Do you agree that it is better? Why or why not?", "focus": "opinion"},
            {"text": "Should universities teach students how to study, or is that each student's own job? Why?", "focus": "opinion"},
        ],
    })

# vocab
VOCAB = [
("analyze","verb","analisar","/ˈæn.əl.aɪz/","analysis, analytical","analyze data, analyze a result","The students analyzed the survey before they wrote the conclusion.","examine, study","academic","B2"),
("approach","noun","abordagem","/əˈproʊtʃ/","approach (verb)","a useful approach, an approach to","Their approach focuses on prevention rather than punishment.","method, way","academic","B2"),
("assume","verb","supor","/əˈsuːm/","assumption","assume that, assume responsibility","Do not assume that a correlation proves a cause.","suppose, presume","academic","B2"),
("benefit","noun","benefício","/ˈben.ɪ.fɪt/","beneficial","a clear benefit, benefit from","One benefit of the later bus is that night-shift workers can attend.","advantage, gain","academic","B1"),
("concept","noun","conceito","/ˈkɑːn.sept/","conceptual","a key concept, the concept of","The concept is easier if you start with one example.","idea, notion","academic","B2"),
("consist","verb","consistir","/kənˈsɪst/","consistent, consistency","consist of","The method consists of three short steps.","be composed of","academic","B2"),
("context","noun","contexto","/ˈkɑːn.tekst/","contextual","in context, historical context","The meaning of the word depends on the context.","setting, situation","academic","B2"),
("contrast","noun","contraste","/ˈkɑːn.træst/","contrast (verb)","in contrast, a sharp contrast","In contrast, the second group showed a smaller change.","difference, opposition","academic","B2"),
("data","noun","dados","/ˈdeɪ.t̬ə/","database","collect data, raw data","The data come from observed behavior, not only from a survey.","evidence, figures","academic","B1"),
("define","verb","definir","/dɪˈfaɪn/","definition","define a term","Define the term before you use it in the essay.","explain, state","academic","B1"),
("derive","verb","derivar, obter","/dɪˈraɪv/","derivation","derive from","The conclusion is derived from the second experiment.","obtain, come from","academic","C1"),
("distribute","verb","distribuir","/dɪˈstrɪb.juːt/","distribution","distribute evenly","The clinic distributed reminders the day before each visit.","give out, spread","academic","B2"),
("economy","noun","economia","/ɪˈkɑː.nə.mi/","economic, economist","the local economy","A higher fee can change behavior in a campus economy.","financial system","academic","B2"),
("environment","noun","meio ambiente; ambiente","/ɪnˈvaɪ.rən.mənt/","environmental","the campus environment, protect the environment","Shade trees change the environment of a hot sidewalk.","surroundings, setting","environment","B1"),
("establish","verb","estabelecer","/ɪˈstæb.lɪʃ/","establishment","establish a link","The study helped establish a link between sleep and memory.","set up, show","academic","B2"),
("estimate","verb","estimar","/ˈes.tə.meɪt/","estimation","a rough estimate","The speaker gave an estimate of ten to twenty minutes.","approximation, guess","academic","B2"),
("evidence","noun","evidência","/ˈev.ɪ.dəns/","evident","supporting evidence","The evidence is what people did, not what they claimed.","proof, support","academic","B2"),
("factor","noun","fator","/ˈfæk.tər/","—","a key factor, factor in","Cost is only one factor in the decision.","element, cause","academic","B2"),
("function","noun","função","/ˈfʌŋk.ʃən/","functional","the function of","The function of the label is to guide, not to decorate.","role, purpose","academic","B2"),
("identify","verb","identificar","/aɪˈden.tɪ.faɪ/","identification, identity","identify a problem","Identify the writer's purpose before you choose an answer.","recognize, name","academic","B1"),
("income","noun","renda","/ˈɪn.kʌm/","—","a low income, income level","A required housing fee hits students with a low income harder.","earnings, pay","academic","B2"),
("indicate","verb","indicar","/ˈɪn.dɪ.keɪt/","indication, indicator","indicate that","A second replication indicates that the result is more stable.","show, suggest","academic","B2"),
("individual","noun","indivíduo","/ˌɪn.dɪˈvɪdʒ.u.əl/","individual (adj)","each individual","Each individual still chooses, even when the default changes.","person","academic","B2"),
("interpret","verb","interpretar","/ɪnˈtɝː.prət/","interpretation","interpret a result","Do not interpret a small sample as a rule for the whole campus.","explain, read","academic","B2"),
("involve","verb","envolver","/ɪnˈvɑːlv/","involvement","involve in","The repair involves a cross-reference, not a rewritten history.","include, require","academic","B2"),
("issue","noun","questão, problema","/ˈɪʃ.uː/","—","a serious issue, address an issue","Noise in the silent floor became an issue within a week.","problem, matter","academic","B1"),
("method","noun","método","/ˈmeθ.əd/","methodical","a research method","The method must be described so another team can repeat it.","procedure, way","academic","B1"),
("occur","verb","ocorrer","/əˈkɝː/","occurrence","occur when","The change occurs slowly, over several summers.","happen","academic","B2"),
("percent","noun","por cento","/pərˈsent/","percentage","ten percent","Attendance counted for ten percent of the grade.","proportion","academic","B1"),
("period","noun","período","/ˈpɪr.i.əd/","periodic","a short period","The closure lasts for a short period, not the whole term.","stretch of time","academic","B1"),
("policy","noun","política, regra","/ˈpɑː.lə.si/","political","a campus policy","The policy asks for two languages only on safety signs.","rule, plan","academic","B2"),
("principle","noun","princípio","/ˈprɪn.sə.pəl/","—","a basic principle","A basic principle of the queue is to show the wait.","rule, idea","academic","B2"),
("proceed","verb","prosseguir","/prəˈsiːd/","procedure","proceed with","Proceed with the experiment only after the safety check.","continue, go on","academic","B2"),
("process","noun","processo","/ˈprɑː.ses/","processing","a slow process","Recovery of a reef is a slow process.","procedure","academic","B2"),
("range","noun","faixa, variação","/reɪndʒ/","—","a wide range","The wait was given as a range, not a single minute.","span, variety","academic","B2"),
("require","verb","exigir","/rɪˈkwaɪər/","requirement","require that","The form requires a signature by 5 p.m.","demand, need","academic","B1"),
("research","noun","pesquisa","/rɪˈsɝːtʃ/","researcher","conduct research","The research counted trays, not opinions.","study, investigation","academic","B1"),
("respond","verb","responder, reagir","/rɪˈspɑːnd/","response","respond to","People respond to a visible wait more calmly.","react, reply","academic","B2"),
("role","noun","papel","/roʊl/","—","play a role","Residents play a role when they report a cracked tree.","part, function","academic","B1"),
("section","noun","seção, parte","/ˈsek.ʃən/","—","the methods section","Read the methods section before you trust a headline.","part","academic","B1"),
("significant","adj","significativo","/sɪɡˈnɪf.ɪ.kənt/","significance, significantly","a significant change","The drop in waste was significant, not a tiny accident.","important, meaningful","academic","B2"),
("similar","adj","semelhante","/ˈsɪm.ə.lər/","similarity","similar to","The second group showed a similar pattern.","alike, comparable","academic","B1"),
("source","noun","fonte","/sɔːrs/","—","a reliable source","Name the source when you borrow an idea.","origin","academic","B1"),
("specific","adj","específico","/spəˈsɪf.ɪk/","specifically, specification","a specific example","Give a specific example, not a general claim.","particular, exact","academic","B2"),
("structure","noun","estrutura","/ˈstrʌk.tʃər/","structural","the structure of","The structure of the reply is opinion, reason, and example.","organization, form","academic","B2"),
("theory","noun","teoria","/ˈθɪr.i/","theoretical","a theory of","The theory explains why uncertainty feels longer than the clock.","model, explanation","academic","B2"),
("vary","verb","variar","/ˈver.i/","various, variable","vary from","Prices vary from one café to the next.","differ, change","academic","B2"),
("achieve","verb","alcançar","/əˈtʃiːv/","achievement","achieve a goal","She achieved the word count without copying the prompt.","reach, accomplish","academic","B2"),
("adequate","adj","adequado","/ˈæd.ə.kwət/","adequately","adequate evidence","An adequate response covers all three bullet points.","enough, sufficient","academic","B2"),
("adjust","verb","ajustar","/əˈdʒʌst/","adjustment","adjust to","The plan adjusts if your exam date moves earlier.","adapt, change","academic","B2"),
("adult","noun","adulto","/ˈæd.ʌlt/","adulthood","young adult","Cooking at home still matters for a young adult.","grown person","academic","B1"),
("affect","verb","afetar","/əˈfekt/","effect (noun)","affect sleep","Noise can affect how well you keep a sentence in mind.","influence","academic","B2"),
("appropriate","adj","apropriado","/əˈproʊ.pri.ət/","appropriately","appropriate to","Choose a greeting appropriate to a professor.","suitable","academic","B2"),
("area","noun","área","/ˈer.i.ə/","—","an area of study","Her area of study is public health.","field, zone","academic","B1"),
("aspect","noun","aspecto","/ˈæs.pekt/","—","one aspect","Cost is one aspect; time is another.","part, feature","academic","B2"),
("assist","verb","ajudar","/əˈsɪst/","assistance, assistant","assist with","The tutor assists with organization before commas.","help","academic","B2"),
("available","adj","disponível","/əˈveɪ.lə.bəl/","availability","available online","The article is available in the library database.","obtainable","academic","B1"),
("aware","adj","consciente","/əˈwer/","awareness","aware of","Be aware of the drop deadline before Monday.","conscious","academic","B2"),
("capacity","noun","capacidade","/kəˈpæs.ə.ti/","—","at full capacity","The room is at full capacity, so join by video.","ability, space","academic","C1"),
("challenge","noun","desafio","/ˈtʃæl.ɪndʒ/","challenging","a real challenge","Remembering the middle of a long sentence is a real challenge.","difficulty","academic","B1"),
("chapter","noun","capítulo","/ˈtʃæp.tər/","—","the next chapter","The quiz covers one chapter, not the whole book.","section","academic","B1"),
("circumstance","noun","circunstância","/ˈsɝː.kəm.stæns/","—","under the circumstances","Under the circumstances, a short email is enough.","situation","academic","C1"),
("comment","noun","comentário","/ˈkɑː.ment/","comment (verb)","a margin comment","A margin comment is not yet an accepted change.","remark","academic","B1"),
("complex","adj","complexo","/kəmˈpleks/","complexity","a complex sentence","Break a complex sentence into meaning chunks.","complicated","academic","B2"),
("conclude","verb","concluir","/kənˈkluːd/","conclusion","conclude that","Do not conclude that the program caused the change.","decide, infer","academic","B2"),
("conduct","verb","realizar","/kənˈdʌkt/","—","conduct a study","The team conducted the count at the end of lunch.","carry out","academic","B2"),
("consequence","noun","consequência","/ˈkɑːn.sə.kwens/","consequently","a direct consequence","A missed slot without notice has a direct consequence.","result","academic","B2"),
("consistent","adj","consistente","/kənˈsɪs.tənt/","consistency","consistent with","The second result is consistent with the first.","matching, steady","academic","B2"),
("constant","adj","constante","/ˈkɑːn.stənt/","constantly","a constant temperature","The lab keeps a constant temperature.","steady","academic","B2"),
("contribute","verb","contribuir","/kənˈtrɪb.juːt/","contribution","contribute to","Several small designs contribute to attendance.","add, help","academic","B2"),
("create","verb","criar","/kriˈeɪt/","creation, creative","create a plan","Create a plan before you accept another meeting.","make","academic","B1"),
("culture","noun","cultura","/ˈkʌl.tʃər/","cultural","campus culture","Club notices are part of campus culture.","way of life","academic","B1"),
("decline","verb","diminuir; recusar","/dɪˈklaɪn/","—","decline an offer","She declined the unpaid internship because of the cost.","decrease, refuse","academic","B2"),
("demonstrate","verb","demonstrar","/ˈdem.ən.streɪt/","demonstration","demonstrate that","The graph demonstrates a drop, not the cause.","show","academic","B2"),
("design","noun","desenho, projeto","/dɪˈzaɪn/","designer","the design of","The design of the line matters as much as its length.","plan","academic","B2"),
("despite","prep","apesar de","/dɪˈspaɪt/","—","despite the cost","Despite the cost, the city planted the trees.","in spite of","academic","B2"),
("dimension","noun","dimensão","/daɪˈmen.ʃən/","—","a new dimension","Cost adds a dimension the poster ignored.","aspect","academic","C1"),
("domestic","adj","doméstico; interno","/dəˈmes.tɪk/","—","domestic students","The rule applies to domestic and international students.","home, internal","academic","B2"),
("emphasis","noun","ênfase","/ˈem.fə.sɪs/","emphasize","place emphasis on","Place emphasis on one strong example.","stress, focus","academic","B2"),
("ensure","verb","garantir","/ɪnˈʃʊr/","—","ensure that","A checklist helps ensure that all three points appear.","make sure","academic","B2"),
("equivalent","adj","equivalente","/ɪˈkwɪv.əl.ənt/","equivalence","equivalent to","Band 4 is the level the scale treats as equivalent to B2.","equal, comparable","academic","C1"),
("evaluate","verb","avaliar","/ɪˈvæl.ju.eɪt/","evaluation","evaluate a source","Evaluate a source before you quote it.","assess","academic","B2"),
("expand","verb","expandir","/ɪkˈspænd/","expansion","expand on","Expand on one reason instead of listing five.","develop, enlarge","academic","B2"),
("expert","noun","especialista","/ˈek.spɝːt/","expertise","an expert in","You do not need to be an expert to follow the passage.","specialist","academic","B2"),
("export","verb","exportar","/ˈek.spɔːrt/","—","export data","The lab can export the spreadsheet.","send out","academic","B2"),
("expose","verb","expor","/ɪkˈspoʊz/","exposure","expose to","Do not expose private notes when you find a lost tablet.","reveal","academic","B2"),
("external","adj","externo","/ɪkˈstɝː.nəl/","—","an external examiner","An external team repeated the study.","outside","academic","B2"),
("facilitate","verb","facilitar","/fəˈsɪl.ə.teɪt/","facilitator","facilitate a discussion","The question is meant to facilitate a discussion, not to end it.","ease, help","academic","C1"),
("final","adj","final","/ˈfaɪ.nəl/","finally","the final draft","Bring the final draft, not the midnight version.","last","academic","B1"),
("focus","verb","focar","/ˈfoʊ.kəs/","focused","focus on","Focus on the task the question actually asks.","concentrate","academic","B1"),
("fund","noun","fundo, verba","/fʌnd/","funding","public funds","Public funds should not hide a club from most students.","money","academic","B2"),
("hence","adv","por isso","/hens/","—","hence the result","The sample was tiny, hence the wide swing.","therefore","academic","C1"),
("hypothesis","noun","hipótese","/haɪˈpɑː.θə.sɪs/","hypothesize","test a hypothesis","They tested the hypothesis with a second group.","proposed explanation","academic","C1"),
("implication","noun","implicação","/ˌɪm.pləˈkeɪ.ʃən/","imply","a practical implication","One implication is that signs should state the action.","consequence","academic","C1"),
("impose","verb","impor","/ɪmˈpoʊz/","imposition","impose a rule","A ban imposes a cost on students who already work.","force, set","academic","C1"),
("incentive","noun","incentivo","/ɪnˈsen.tɪv/","—","a small incentive","A posted wait is an incentive to stay.","motivation","academic","C1"),
("incident","noun","incidente","/ˈɪn.sɪ.dənt/","—","a minor incident","Report the incident before you wipe the spill.","event","academic","B2"),
("initial","adj","inicial","/ɪˈnɪʃ.əl/","initially","the initial result","The initial result came from only ten people.","first","academic","B2"),
("instance","noun","exemplo","/ˈɪn.stəns/","—","for instance","For instance, a walk can leave room for another thought.","example","academic","B2"),
("integrate","verb","integrar","/ˈɪn.tɪ.ɡreɪt/","integration","integrate into","Integrate one example into the paragraph.","combine","academic","C1"),
("internal","adj","interno","/ɪnˈtɝː.nəl/","—","an internal deadline","The group set an internal deadline two days early.","inside","academic","B2"),
("justify","verb","justificar","/ˈdʒʌs.tɪ.faɪ/","justification","justify a claim","Justify the claim with a specific case.","defend, support","academic","B2"),
("label","noun","rótulo","/ˈleɪ.bəl/","label (verb)","a clear label","A clear label tells you what not to touch.","tag","academic","B1"),
("layer","noun","camada","/ˈleɪ.ər/","—","a layer of","Access is a layer of small designs.","level","academic","B2"),
("legal","adj","legal","/ˈliː.ɡəl/","legally","legal advice","This site does not give legal advice about a score cancellation.","lawful","academic","B2"),
("link","noun","ligação","/lɪŋk/","link (verb)","a link between","There is a link between sleep and what you recall.","connection","academic","B1"),
("locate","verb","localizar","/ˈloʊ.keɪt/","location","locate the office","Locate the office on the map before you leave.","find","academic","B2"),
("maintain","verb","manter","/meɪnˈteɪn/","maintenance","maintain a habit","Maintain a sleep window during exam week.","keep","academic","B2"),
("major","adj","principal","/ˈmeɪ.dʒər/","majority","a major change","The room change was major because the sink had no water.","important, main","academic","B2"),
("mental","adj","mental","/ˈmen.təl/","mentally","mental effort","Hard focus spends mental effort quickly.","of the mind","psychology","B2"),
("modify","verb","modificar","/ˈmɑː.dɪ.faɪ/","modification","modify a plan","Modify the plan if the exam date moves.","change","academic","B2"),
("monitor","verb","monitorar","/ˈmɑː.nə.t̬ɚ/","monitoring","monitor progress","Monitor which words you drop in the middle of a sentence.","watch","academic","B2"),
("network","noun","rede","/ˈnet.wɝːk/","—","a network of","A network of lanes works better than one short lane.","system","academic","B2"),
("notion","noun","noção","/ˈnoʊ.ʃən/","—","the notion that","The notion that the nearest farm is always best is too simple.","idea","academic","C1"),
("objective","noun","objetivo","/əbˈdʒek.tɪv/","objectively","the objective of","The objective of the email is to solve a specific problem.","goal","academic","B2"),
("occupy","verb","ocupar","/ˈɑː.kjə.paɪ/","occupation","occupy a room","Another group still occupied the room.","fill, take","academic","B2"),
("option","noun","opção","/ˈɑːp.ʃən/","optional","a clear option","Give the reader one clear option, not five.","choice","academic","B1"),
("outcome","noun","resultado","/ˈaʊt.kʌm/","—","a likely outcome","A likely outcome of a tiny sample is a dramatic chart.","result","academic","B2"),
("overall","adj","geral","/ˌoʊ.vɚˈɔːl/","—","the overall score","The overall score is the average of the four sections.","total","academic","B2"),
("parallel","adj","paralelo","/ˈper.ə.lel/","—","in parallel","Do not run two heavy downloads in parallel on test day.","side by side","academic","B2"),
("parameter","noun","parâmetro","/pəˈræm.ə.t̬ɚ/","—","a key parameter","Sample size is a key parameter.","limit, factor","academic","C1"),
("participate","verb","participar","/pɑːrˈtɪs.ə.peɪt/","participation, participant","participate in","You can participate even if you are new.","take part","academic","B1"),
("perceive","verb","perceber","/pɚˈsiːv/","perception","perceive as","People perceive a hidden wait as longer.","see, regard","academic","C1"),
("portion","noun","porção","/ˈpɔːr.ʃən/","—","a large portion","A large portion of the sentence was the ending she forgot.","part","academic","B2"),
("potential","adj","potencial","/pəˈten.ʃəl/","potentially","a potential problem","A potential problem is a headset, which the Home Edition does not allow.","possible","academic","B2"),
("previous","adj","anterior","/ˈpriː.vi.əs/","previously","the previous study","The previous study used a smaller group.","earlier","academic","B2"),
("primary","adj","primário, principal","/ˈpraɪ.mer.i/","primarily","the primary goal","The primary goal is a fair score on the first attempt.","main","academic","B2"),
("publish","verb","publicar","/ˈpʌb.lɪʃ/","publication","publish a correction","The paper was asked to publish a correction.","issue, print","academic","B2"),
("purchase","verb","comprar","/ˈpɝː.tʃəs/","—","purchase a pass","You can purchase a pass at the counter.","buy","academic","B2"),
("quote","verb","citar","/kwoʊt/","quotation","quote a source","Quote a source instead of copying a whole sentence.","cite","academic","B2"),
("random","adj","aleatório","/ˈræn.dəm/","randomly","a random sample","A random sample still needs to be large enough.","chance","academic","B2"),
("recover","verb","recuperar","/rɪˈkʌv.ər/","recovery","recover from","A reef can recover if one pressure is removed.","get back","academic","B2"),
("region","noun","região","/ˈriː.dʒən/","regional","a coastal region","The talk compared two towns in the same region.","area","academic","B2"),
("register","verb","registrar, inscrever-se","/ˈredʒ.ɪ.stər/","registration","register for","Register for the workshop before Friday.","sign up","campus","B1"),
("relevant","adj","relevante","/ˈrel.ə.vənt/","relevance","relevant to","Include only details relevant to the question.","related","academic","B2"),
("rely","verb","confiar, depender","/rɪˈlaɪ/","reliable, reliance","rely on","Do not rely on memory for a group decision.","depend","academic","B2"),
("remove","verb","remover","/rɪˈmuːv/","removal","remove a rule","Removing the easy option changed the habit faster.","take away","academic","B1"),
("resident","noun","residente","/ˈrez.ɪ.dənt/","residential","a local resident","A local resident reported the cracked trunk.","inhabitant","campus","B2"),
("resource","noun","recurso","/ˈriː.sɔːrs/","—","a useful resource","The writing center is a useful resource before a deadline.","aid","academic","B2"),
("restrict","verb","restringir","/rɪˈstrɪkt/","restriction","restrict access","The archive restricts phones to a locker.","limit","academic","B2"),
("seek","verb","buscar","/siːk/","—","seek help","Seek help before the drop deadline.","look for","academic","B2"),
("select","verb","selecionar","/səˈlekt/","selection","select an option","Select the option that answers the function of the remark.","choose","academic","B1"),
("shift","noun","turno; mudança","/ʃɪft/","shift (verb)","a night shift","A night shift in the past week excludes you from the study.","change, work period","academic","B2"),
("stable","adj","estável","/ˈsteɪ.bəl/","stability","a stable result","A stable result shows up in a second group.","steady","academic","B2"),
("stress","noun","estresse; ênfase","/stres/","stressful","under stress","Under stress, function words are the ones that disappear.","pressure","psychology","B1"),
("sufficient","adj","suficiente","/səˈfɪʃ.ənt/","sufficiently","sufficient evidence","Forty words may not be sufficient for the discussion task.","enough","academic","B2"),
("summary","noun","resumo","/ˈsʌm.ər.i/","summarize","a short summary","Write a three-line summary from memory after class.","brief account","academic","B2"),
("survey","noun","pesquisa, levantamento","/ˈsɝː.veɪ/","survey (verb)","a campus survey","Read how many people answered the survey.","poll","academic","B2"),
("survive","verb","sobreviver","/sɚˈvaɪv/","survival","survive the first summer","Young trees survive the first summer only with water.","last","environment","B2"),
("task","noun","tarefa","/tæsk/","—","the writing task","The writing task gives you seven minutes for the email.","job, assignment","academic","B1"),
("technical","adj","técnico","/ˈtek.nɪ.kəl/","technically","technical vocabulary","Avoid technical vocabulary the reader has not met.","specialized","academic","B2"),
("temporary","adj","temporário","/ˈtem.pə.rer.i/","temporarily","a temporary closure","The closure is temporary, from 1 to 4 p.m.","short-term","campus","B2"),
("trend","noun","tendência","/trend/","—","a clear trend","The trend continued for a decade.","tendency","academic","B2"),
("underlie","verb","estar na base de","/ˌʌn.dɚˈlaɪ/","underlying","underlying cause","The underlying cause was uncertainty, not the length of the line.","lie behind","academic","C1"),
("unique","adj","único","/juˈniːk/","uniquely","a unique detail","Add one unique detail so the example is yours.","one of a kind","academic","B2"),
("visible","adj","visível","/ˈvɪz.ə.bəl/","visibility","highly visible","Keep your face visible to the proctor.","able to be seen","campus","B2"),
("volume","noun","volume","/ˈvɑːl.juːm/","—","the volume of","Check the volume before the listening section.","amount, loudness","campus","B1"),
("welfare","noun","bem-estar","/ˈwel.fer/","—","student welfare","Evening clinics are a welfare decision, not only a medical one.","well-being","academic","C1"),
("whereas","conj","ao passo que","/werˈæz/","—","whereas the other","One hall changed the plates, whereas the other only posted signs.","while","academic","B2"),
("widespread","adj","generalizado","/ˈwaɪd.spred/","—","widespread use","Widespread use of the old heading hid the books.","common","academic","C1"),
("willing","adj","disposto","/ˈwɪl.ɪŋ/","willingness","willing to","She was willing to take the morning shift.","ready","academic","B2"),
("advisor","noun","orientador","/ədˈvaɪ.zɚ/","advise, advice","an academic advisor","Email your advisor before you drop the course.","counselor","campus","B1"),
("deadline","noun","prazo","/ˈded.laɪn/","—","a strict deadline","The deadline for the form is Friday at noon.","due date","campus","B1"),
("dorm","noun","alojamento","/dɔːrm/","—","a dorm room","The heater in the dorm room would not turn down.","residence hall","campus","B1"),
("tuition","noun","mensalidade, anuidade","/tuˈɪʃ.ən/","—","tuition fees","Tuition does not include every lab fee.","school fees","campus","B2"),
("syllabus","noun","programa da disciplina","/ˈsɪl.ə.bəs/","—","on the syllabus","The syllabus lists every quiz.","course outline","campus","B2"),
("transcript","noun","histórico escolar","/ˈtræn.skrɪpt/","—","an official transcript","The program asked for an official transcript.","academic record","campus","B2"),
("scholarship","noun","bolsa","/ˈskɑː.lɚ.ʃɪp/","scholar","a merit scholarship","The scholarship covers tuition but not housing.","grant","campus","B2"),
("plagiarism","noun","plágio","/ˈpleɪ.dʒə.rɪ.zəm/","plagiarize","avoid plagiarism","Copying the prompt is a form of plagiarism.","copying","campus","B2"),
("prerequisite","noun","pré-requisito","/ˌpriːˈrek.wə.zɪt/","—","a prerequisite for","Statistics is a prerequisite for the methods course.","requirement","campus","C1"),
("withdraw","verb","trancar; retirar","/wɪðˈdrɔː/","withdrawal","withdraw from a course","You can withdraw before the deadline.","drop, leave","campus","B2"),
("freshman","noun","calouro","/ˈfreʃ.mən/","—","a freshman seminar","The freshman seminar meets on Tuesdays.","first-year student","campus","B2"),
("midterm","noun","prova de meio de semestre","/ˈmɪd.tɝːm/","—","the midterm exam","The midterm covers the first five chapters.","exam","campus","B1"),
("lecture","noun","aula expositiva","/ˈlek.tʃɚ/","lecturer","skip a lecture","She recorded the lecture for students who work.","class talk","campus","B1"),
("seminar","noun","seminário","/ˈsem.ɪ.nɑːr/","—","a graduate seminar","The seminar asks every student to lead one discussion.","small class","campus","B2"),
("assignment","noun","tarefa","/əˈsaɪn.mənt/","assign","a writing assignment","The assignment asks for your own example.","homework","campus","B1"),
("draft","noun","rascunho","/dræft/","draft (verb)","a first draft","Bring a draft and one question to the writing center.","version","campus","B2"),
("citation","noun","citação","/saɪˈteɪ.ʃən/","cite","a missing citation","Add the year to the citation.","reference","campus","B2"),
("campus","noun","campus","/ˈkæm.pəs/","—","on campus","The shuttle runs across campus until ten.","university grounds","campus","B1"),
("faculty","noun","corpo docente","/ˈfæk.əl.ti/","—","faculty office","The faculty office posts hours on the door.","teaching staff","campus","B2"),
("enrollment","noun","matrícula","/ɪnˈroʊl.mənt/","enroll","enrollment deadline","Enrollment closes if the section is full.","registration","campus","B2"),
("credit","noun","crédito","/ˈkred.ɪt/","—","course credit","The lab is worth one credit.","unit","campus","B2"),
("grade","noun","nota","/ɡreɪd/","grading","a passing grade","The grade appears in the portal tonight.","mark, score","campus","B1"),
("attendance","noun","presença","/əˈten.dəns/","attend","take attendance","Attendance is ten percent of the grade.","presence","campus","B2"),
("extension","noun","prorrogação","/ɪkˈsten.ʃən/","extend","request an extension","She requested an extension because she was ill.","extra time","campus","B2"),
("internship","noun","estágio","/ˈɪn.tɝːn.ʃɪp/","intern","an unpaid internship","An unpaid internship is not realistic for every student.","placement","campus","B2"),
("roommate","noun","colega de quarto","/ˈruːm.meɪt/","—","a quiet roommate","Her roommate studies late and asked for quiet hours.","person you share a room with","campus","B1"),
("cafeteria","noun","refeitório","/ˌkæf.əˈtɪr.i.ə/","—","the cafeteria line","The cafeteria line is shorter after 6:30.","dining hall","campus","B1"),
("laboratory","noun","laboratório","/ˈlæb.rə.tɔːr.i/","lab","a teaching laboratory","Goggles stay on in the laboratory.","lab","campus","B2"),
("hypothesis","noun","hipótese","/haɪˈpɑː.θə.sɪs/","hypothesize","working hypothesis","Wait, duplicate."),
]
# remove accidental duplicate hypothesis if present
seen = set()
clean = []
for row in VOCAB:
    if row[0].lower() in seen:
        continue
    if row[-3] == "Wait, duplicate.":
        continue
    seen.add(row[0].lower())
    clean.append(row)
vocab = []
for i, (w, pos, pt, ipa, family, colloc, ex, syn, theme, level) in enumerate(clean, 1):
    vocab.append({"id": f"v{i:03d}", "w": w, "pos": pos, "pt": pt, "ipa": ipa, "family": family,
                  "colloc": colloc, "ex": ex, "syn": syn, "theme": theme, "level": level, "topic": theme})
assert len(vocab) >= 100, len(vocab)

# checks
from collections import Counter
def pools(key):
    return Counter(x["pool"] for x in scale[key])
for n in range(3, 11):
    p, u, l = f"m{n}", f"m{n}u", f"m{n}l"
    def rq(pool):
        return sum(len(x["gaps"]) for x in scale["ctw"] if x["pool"]==pool) + sum(len(x["questions"]) for x in scale["daily"] if x["pool"]==pool) + sum(len(x["questions"]) for x in scale["academic"] if x["pool"]==pool)
    def lq(pool):
        return sum(1 for x in scale["choose"] if x["pool"]==pool) + sum(len(x["questions"]) for x in scale["conversation"] if x["pool"]==pool) + sum(len(x["questions"]) for x in scale["announcement"] if x["pool"]==pool) + sum(len(x["questions"]) for x in scale["talk"] if x["pool"]==pool)
    assert rq(p)==30 and rq(u)==20 and rq(l)==20, (n, rq(p), rq(u), rq(l))
    assert lq(p)==28 and lq(u)==19 and lq(l)==19, (n, lq(p), lq(u), lq(l))
    tag = f"mock{n}"
    assert sum(1 for x in scale["bas"] if x["pool"]==tag)==10
    assert any(x["pool"]==tag for x in scale["email"])
    assert any(x["pool"]==tag for x in scale["discussion"])
    assert any(x["pool"]==tag for x in scale["repeat"])
    assert any(x["pool"]==tag for x in scale["interview"])

path = OUT / "scale.json"
path.write_text(json.dumps(scale, ensure_ascii=False), encoding="utf-8")
(OUT / "vocab.json").write_text(json.dumps(vocab, ensure_ascii=False, indent=2), encoding="utf-8")
print("scale", {k: len(v) for k, v in scale.items()}, "vocab", len(vocab), "bytes", path.stat().st_size)
