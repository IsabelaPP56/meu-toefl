from bank_common import dump, words
import re

PARAS = [
("ctw01","practice","mid",
"Sleep helps students store what they studied during the day. Researchers have found that a regular night of rest improves attention and makes new vocabulary easier to recall. Short naps can also help, but they do not replace a full night. Students who review notes and then sleep often remember more than those who keep studying very late. A calm routine, with dim lights and a fixed bedtime, supports this process."),
("ctw02","practice","mid",
"Street trees cool a neighborhood and give birds a place to nest. Their roots hold soil during heavy rain, and their leaves filter dust from the air. Cities that plant trees along busy roads also create shade for people walking to class. Young trees need water and protection from bikes and cars. When residents report damaged trunks quickly, garden crews can save the tree."),
("ctw03","practice","easy",
"A campus food pantry supports students who cannot always afford meals. Volunteers sort donations, check dates, and stock shelves with rice, beans, and fresh fruit. The pantry keeps personal information private and lets students choose what they need. Staff also share lists of nearby kitchens that serve a free dinner. Using the pantry does not affect grades or financial aid."),
("ctw04","practice","hard",
"Price changes influence how many people buy a product, but the effect is not always equal. When a small increase causes a large drop in sales, economists call the demand elastic. Necessities such as basic medicine often show a weaker reaction. Companies study these patterns before they raise a price. Understanding the pattern helps them avoid losing loyal customers."),
("ctw05","practice","mid",
"Museum labels do more than name an object. A good label tells where the piece was made, who used it, and why it mattered. Short sentences help visitors who are reading in a second language. Curators avoid jargon and explain one idea at a time. Clear labels make the gallery feel open rather than exclusive."),
("ctw06","practice","easy",
"Many first-year students struggle to balance clubs, classes, and sleep. A simple weekly plan can show which hours are already full. Students who block time for reading before they accept another meeting usually feel less rushed. The plan should include meals and a short walk. Reviewing it every Sunday keeps the week realistic."),
("ctw07","practice","hard",
"Working memory holds a small amount of information while a person uses it. In class, that system keeps the teacher's question in mind long enough to form an answer. Noise, worry, and too many steps can overload it. Teachers can help by writing the steps and pausing between them. Practice with short problems builds control without adding stress."),
("ctw08","practice","mid",
"Coral reefs protect coasts and shelter a huge variety of fish. Warm water and pollution can weaken the corals and cause them to lose color. Local communities that limit harmful fishing give the reef time to recover. Scientists measure water temperature and track which species return. Their reports guide rules that keep the habitat alive."),
("ctw-m1a","m1","mid",
"Public libraries remain important even when many books exist online. Librarians teach people how to judge a source and how to search a database. Quiet rooms, public computers, and weekend workshops serve students who lack those tools at home. A library card is usually free for local residents. These services turn the building into a classroom for the whole city."),
("ctw-m1b","m1","mid",
"Bicycle lanes change how people move through a campus. Riders feel safer when paint, posts, or a curb separates them from cars. Planners also need places to lock bikes near classroom doors. Good lighting matters after evening classes. A connected network, not a single short lane, is what makes daily riding practical."),
("ctw-m1u","m1u","hard",
"Historians read diaries to understand ordinary life, not only famous events. A personal notebook may describe prices, weather, and family arguments that official records ignore. Scholars compare several diaries before they claim a pattern. They also ask who could write and whose voices are missing. That caution keeps the conclusion tied to the evidence."),
("ctw-m1l","m1l","easy",
"Campus gardens give students a place to learn how food grows. Participants plant seeds, water beds, and share the harvest with the dining hall. The work is physical, so organizers post a clear schedule and provide gloves. Beginners start with herbs because those plants grow quickly. The garden also becomes a quiet spot between classes."),
("ctw-m2a","m2","mid",
"Group projects fail when members never agree on a deadline. A short meeting at the start can assign research, slides, and editing. Students should write decisions in a shared note so nobody relies on memory. If someone falls behind, the group can reduce that person's task early. Clear roles reduce conflict and improve the final presentation."),
("ctw-m2b","m2","mid",
"Vaccination campaigns work better when clinics are easy to reach. Evening hours help people who cannot leave a job during the day. Nurses who explain side effects in plain language reduce fear. Reminder messages the day before an appointment cut the number of missed visits. Trust grows when the same staff return to the neighborhood."),
("ctw-m2u","m2u","hard",
"Metaphor in poetry is not decoration added at the end. It lets a writer connect an abstract feeling to a concrete image the reader can see. A careful comparison can reveal an attitude that a direct statement would flatten. Critics look at which images repeat across a poem. Those repetitions often show the real subject."),
("ctw-m2l","m2l","easy",
"Student clubs introduce people who might never meet in class. A weekly meeting, a simple agenda, and a welcome for newcomers keep the group open. Officers should post the room number and the end time. Members can take turns bringing a topic. Small clubs often create the friendships that make a large campus feel smaller."),
]

def gaps_for(text):
    rest = text.split(".", 1)[1]
    tokens = re.findall(r"[A-Za-z']+", rest)
    seen, gaps = set(), []
    for t in tokens:
        if len(t) < 4: continue
        low = t.lower()
        if low in seen: continue
        seen.add(low)
        gaps.append(t)
        if len(gaps) == 10: break
    return gaps

EXTRA = {
"ctw02": " City maps now mark older trees so crews can inspect them after major storms.",
"ctw03": " Evening hours make it easier for students who work during the day.",
"ctw04": " A careful test of a new price can reveal the reaction before a national change.",
"ctw05": " Visitors stay longer when they understand the story behind a single object on the wall.",
"ctw06": " Sharing the plan with a friend makes it harder to ignore the limits you set each week.",
"ctw07": " Even a brief pause can keep the question from disappearing too soon.",
"ctw08": " Visitors who stay on marked paths also reduce damage to the living coral below them.",
"ctw-m1a": " Evening literacy classes fill quickly, so people are asked to register online.",
"ctw-m1b": " Winter maintenance, including salt and broken glass, must be part of the yearly safety plan for every rider.",
"ctw-m1u": " A diary written for a private reader may hide facts that a public letter would admit.",
"ctw-m1l": " At the end of the term, the group writes what grew well and what failed.",
"ctw-m2a": " A shared calendar also shows who is free before the final Friday evening rehearsal.",
"ctw-m2b": " Clear signs in two languages help visitors find the right clinic room without asking twice.",
"ctw-m2u": " Reading the poem aloud often makes those repeated images easier to hear and then notice.",
"ctw-m2l": " A shared snack after the meeting gives quiet members a real chance to talk freely.",
}
items = []
for id_, pool, level, text in PARAS:
    text = (text + EXTRA.get(id_, "")).strip()
    wc = len(words(text))
    gaps = gaps_for(text)
    problems = []
    if not (70 <= wc <= 100):
        problems.append(f"{id_} words {wc}")
    if len(gaps) != 10:
        problems.append(f"{id_} gaps {len(gaps)} {gaps}")
    if problems:
        raise SystemExit("; ".join(problems))
    # ensure order and unique presence after first period
    rest = text.split(".", 1)[1]
    cursor = 0
    for g in gaps:
        i = rest.lower().find(g.lower(), cursor)
        if i < 0:
            raise SystemExit(f"{id_} missing {g}")
        cursor = i + len(g)
    items.append({"id": id_, "pool": pool, "level": level, "text": text, "gaps": gaps, "why": "A primeira frase fica inteira. Cada lacuna é a segunda metade de uma palavra de conteúdo; use a classe gramatical e o sentido da frase."})

dump("ctw", items)

VOCAB = [
("deadline","noun","prazo final","The deadline for the essay is Friday at noon.","campus"),
("syllabus","noun","programa da disciplina","The syllabus lists every quiz and the grading policy.","campus"),
("office hours","noun","horário de atendimento","Professor Rahman holds office hours on Tuesday afternoon.","campus"),
("advisor","noun","orientador","My advisor suggested a lighter course load this term.","campus"),
("withdraw","verb","trancar ou desistir de","You must withdraw before the deadline to avoid a penalty.","campus"),
("prerequisite","noun","pré-requisito","Statistics is a prerequisite for the research methods class.","campus"),
("transcript","noun","histórico escolar","The graduate program asked for an official transcript.","campus"),
("scholarship","noun","bolsa de estudos","She won a scholarship that covers tuition and books.","campus"),
("tuition","noun","mensalidade ou anuidade","Tuition rises if you register after the posted date.","campus"),
("dorm","noun","alojamento estudantil","The dorm closes the front door at midnight.","campus"),
("plagiarism","noun","plágio","Plagiarism can result in a failing grade for the paper.","campus"),
("assignment","noun","tarefa","The assignment asks for two sources and a clear thesis.","campus"),
("lecture","noun","aula expositiva","The lecture moved too fast for me to copy every point.","campus"),
("seminar","noun","seminário","In the seminar, every student leads one discussion.","campus"),
("midterm","noun","prova de meio de período","The midterm covers chapters one through five.","campus"),
("final","noun","prova final","The final is cumulative, so review the early units too.","campus"),
("credit","noun","crédito acadêmico","This lab is worth one credit.","campus"),
("major","noun","curso principal","She changed her major from chemistry to public health.","campus"),
("elective","noun","disciplina optativa","I still need one elective in the arts.","campus"),
("attendance","noun","presença","Attendance counts for ten percent of the grade.","campus"),
("extension","noun","prorrogação","He asked for an extension because he was ill.","campus"),
("draft","noun","rascunho","Bring a draft to the writing center before you submit.","campus"),
("peer review","noun","revisão por colegas","Peer review helped her see the missing example.","campus"),
("lab report","noun","relatório de laboratório","The lab report must include your raw data.","campus"),
("campus shuttle","noun","ônibus do campus","The campus shuttle leaves from the east gate.","campus"),
("dining hall","noun","refeitório","The dining hall stops serving lunch at two.","campus"),
("resident advisor","noun","monitor do alojamento","The resident advisor organized a fire drill.","campus"),
("financial aid","noun","ajuda financeira","Financial aid can include grants and loans.","campus"),
("registration","noun","matrícula","Registration for spring classes opens on Monday.","campus"),
("waitlist","noun","lista de espera","I am on the waitlist for the only open section.","campus"),
("drop a course","verb","cancelar uma disciplina","You can drop a course during the first week.","campus"),
("office","noun","sala do professor","Her office is on the third floor of the science building.","campus"),
("textbook","noun","livro-texto","The textbook is expensive, so she rented a copy.","campus"),
("notes","noun","anotações","Compare notes with a classmate after the lecture.","campus"),
("quiz","noun","teste curto","There is a short quiz at the start of every Friday class.","campus"),
("grade","noun","nota","The grade will appear in the online portal tonight.","campus"),
("participation","noun","participação","Participation means asking questions, not only attending.","campus"),
("citation","noun","citação","Every citation needs the author and the year.","campus"),
("bibliography","noun","bibliografia","The bibliography comes after the conclusion.","campus"),
("plagiarize","verb","plagiar","Do not plagiarize sentences from the class slides.","campus"),
("dean","noun","diretor acadêmico","The dean approved the new language requirement.","campus"),
("faculty","noun","corpo docente","The faculty voted to change the exam schedule.","campus"),
("undergraduate","noun","graduando","The program is open to every undergraduate.","campus"),
("graduate","adj","de pós-graduação","Graduate seminars are smaller than first-year lectures.","campus"),
("internship","noun","estágio","Her internship is at the city museum.","campus"),
("career center","noun","central de carreiras","The career center will review your résumé.","campus"),
("roommate","noun","colega de quarto","My roommate studies engineering and keeps different hours.","campus"),
("laundry","noun","lavanderia","The laundry room is in the basement of the dorm.","campus"),
("mailbox","noun","caixa de correio","Check your mailbox for the new student card.","campus"),
("ID card","noun","carteirinha","You need an ID card to enter the gym.","campus"),
("however","adv","porém","The results were promising; however, the sample was small.","academic"),
("therefore","adv","portanto","The soil was dry; therefore, the plants grew slowly.","academic"),
("evidence","noun","evidência","The evidence comes from three separate experiments.","academic"),
("significant","adj","significativo","The difference was significant, not just a small change.","academic"),
("approach","noun","abordagem","Their approach focuses on prevention rather than treatment.","academic"),
("assume","verb","supor","Do not assume that correlation proves a cause.","academic"),
("contrast","verb","contrastar","The author contrasts city life with rural routines.","academic"),
("factor","noun","fator","Cost is only one factor in the decision.","academic"),
("method","noun","método","The method must be described so others can repeat it.","academic"),
("theory","noun","teoria","The theory explains why the pattern appears in several cultures.","academic"),
("benefit","noun","benefício","One benefit of the policy is cleaner air.","academic"),
("consequence","noun","consequência","A consequence of the delay was a smaller harvest.","academic"),
("establish","verb","estabelecer","The study helped establish a link between sleep and memory.","academic"),
("imply","verb","implicar, sugerir","The results imply that earlier warnings would help.","academic"),
("previous","adj","anterior","Previous research used a much smaller group.","academic"),
("require","verb","exigir","The task will require careful reading, not memorization.","academic"),
("source","noun","fonte","Name the source when you borrow an idea.","academic"),
("vary","verb","variar","Prices vary from one market to another.","academic"),
("analyze","verb","analisar","Analyze the graph before you write the conclusion.","academic"),
("consistent","adj","consistente","The findings are consistent with the earlier study.","academic"),
("contribute","verb","contribuir","Several factors contribute to the decline.","academic"),
("demonstrate","verb","demonstrar","The experiment did not demonstrate a clear effect.","academic"),
("occur","verb","ocorrer","The change occurs slowly over many years.","academic"),
("process","noun","processo","The process has three stages.","academic"),
("range","noun","variação, gama","The ages range from eighteen to thirty.","academic"),
("relevant","adj","relevante","Include only the details that are relevant to the question.","academic"),
("specific","adj","específico","Give a specific example, not a general claim.","academic"),
("structure","noun","estrutura","The structure of the essay is introduction, body, and conclusion.","academic"),
("trend","noun","tendência","The trend has continued for a decade.","academic"),
("although","conj","embora","Although the sample was small, the pattern was clear.","academic"),
("despite","prep","apesar de","Despite the cost, the city built the new clinic.","academic"),
("increase","verb","aumentar","Temperatures increase during the afternoon.","academic"),
("decrease","verb","diminuir","Noise levels decrease after the shops close.","academic"),
("affect","verb","afetar","Lack of sleep can affect attention.","academic"),
("effect","noun","efeito","The effect was stronger in the second trial.","academic"),
("cause","noun","causa","The main cause was contaminated water.","academic"),
("result","noun","resultado","The result surprised the research team.","academic"),
("support","verb","sustentar, apoiar","The data support the author's claim.","academic"),
("argue","verb","argumentar","The writer argues that the rule should change.","academic"),
("claim","noun","afirmação","The claim needs more evidence.","academic"),
("context","noun","contexto","Word meaning depends on context.","academic"),
("define","verb","definir","Define the term before you use it.","academic"),
("compare","verb","comparar","Compare the two graphs, not just one number.","academic"),
("predict","verb","prever","The model can predict next year's demand.","academic"),
("observe","verb","observar","Students observe the reaction and write what they see.","academic"),
("conclude","verb","concluir","We cannot conclude that the program caused the change.","academic"),
("likely","adj","provável","A shorter deadline is likely to increase stress.","academic"),
("rather","adv","em vez disso","They chose prevention rather than punishment.","academic"),
("policy","noun","política, regra","The new policy limits visitors during exam week.","academic"),
("available","adj","disponível","The article is available in the library database.","academic"),
]
assert len(VOCAB) == 100, len(VOCAB)
seen=set()
items=[]
for i,(w,pos,pt,ex,topic) in enumerate(VOCAB,1):
    key=w.lower()
    assert key not in seen
    seen.add(key)
    items.append({"id": f"v{i:03d}", "w": w, "pos": pos, "pt": pt, "ex": ex, "topic": topic})
dump("vocab", items)
