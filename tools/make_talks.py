import random, sys
sys.path.insert(0, "/workspace/tools")
from bank_common import dump, words, mc

def Q(stem, correct, wrongs, why):
    opts = [correct, *wrongs]
    order = [0, 1, 2, 3]
    random.Random(stem + correct).shuffle(order)
    return mc(stem, [opts[i] for i in order], order.index(0), why)

talks = []
def add(pool, level, setting, sents):
    script = " ".join(sents)
    wc = len(words(script))
    assert 100 <= wc <= 250, (setting, wc)
    gist, gw, detail, dw, org, ow, inf, iw = sents[-1], None, None, None, None, None, None, None
    # questions are passed separately — this signature is unused
    return script

def T(pool, level, setting, sents, gist, gw, dq, da, dw, oq, oa, ow, iq, ia, iw):
    script = " ".join(sents)
    wc = len(words(script))
    assert 100 <= wc <= 250, (setting, wc)
    questions = [
        Q("What is the main topic of the talk?", gist, gw, "O tema abre a fala e organiza os exemplos."),
        Q(dq, da, dw, "Esse detalhe é afirmado pelo falante."),
        Q(oq, oa, ow, "O exemplo ou o contraste tem uma função na explicação."),
        Q(iq, ia, iw, "A inferência segue o que a fala sugere, sem fato externo."),
    ]
    talks.append({"id": f"tk{len(talks)+1:02d}", "pool": pool, "level": level, "setting": setting,
                  "script": script, "questions": questions})

# 10 practice
T("practice","mid","A short talk in an environmental studies class",
["I want to explain a simple measure called food miles, the distance food travels from farm to plate.","A long distance does not automatically mean a worse choice, because a ship can move grain more efficiently than a small truck moving local fruit in winter.","Still, distance matters when the same product is flown, since air freight uses far more fuel per kilogram.","The useful comparison is therefore method of travel, not the slogan local versus far.","A campus dining hall can cut its impact by swapping one air-freight item for a seasonal dish, even if other ingredients still come from another region.","Students sometimes assume that the nearest farm is always the lowest impact, and that assumption is what this measure corrects.","If you remember one step, compare how the food moved before you judge only the kilometers."],
"A way to think about the impact of transporting food",
["How to cook a campus meal","Why all imports should be banned","The history of one farm"],
"According to the speaker, when is distance especially important?",
"When the product is flown, because air freight uses more fuel",
["When any food leaves its farm","Only when students cook","When grain moves by ship"],
"Why does the speaker mention a ship and a truck?",
"To show that the method of travel can matter more than distance alone",
["To prove ships are always worse","To advertise a truck company","To cancel the dining hall"],
"What does the speaker imply about the nearest farm?",
"It is not automatically the lowest-impact choice",
["It should never be used","It always uses airplanes","It replaces the need to measure"])

T("practice","mid","A talk in an urban studies class",
["Cities often talk about an urban heat island, the extra warmth of streets and roofs compared with nearby countryside.","Dark pavement and little shade hold the afternoon sun, so the evening stays hot.","Trees and light-colored roofs are two ordinary tools, and they work for different reasons.","A tree cools the air by shade and by releasing moisture, while a pale roof mainly reflects sunlight.","A neighborhood with both stays cooler than a neighborhood that plants trees but keeps black roofs, or the reverse.","The speaker's point is that one visible project is not a full plan.","When you evaluate a campus proposal, ask which surfaces are still absorbing heat after the new trees are in the ground."],
"Why cities stay hotter than nearby countryside, and what reduces that heat",
["How to forecast tomorrow's rain","Why winters are longer","A tour of one building's basement"],
"How does a tree cool the air, according to the talk?",
"By shade and by releasing moisture",
["Only by painting the roof","By blocking all wind","By heating the pavement"],
"Why does the speaker contrast trees and pale roofs?",
"To show that they cool in different ways and work best together",
["To argue that roofs should be removed","To prove trees have no effect","To compare two sports"],
"What should a listener ask about a campus proposal?",
"Which surfaces will still absorb heat after trees are planted",
["Whether the countryside can be moved","How to remove every roof","Whether evenings should be canceled"])

T("practice","easy","A talk for new students about study time",
["Students often plan one long study session and then feel surprised when the last hour produces little.","Memory research suggests that several shorter sessions, spread across days, beat one marathon the night before a quiz.","The reason is simple: each return to the material forces you to retrieve it, and retrieval is what strengthens the memory.","Rereading a highlighted page feels smooth, which is why it fools people into thinking they know the page.","A better check is to close the book and write three points from memory.","If you cannot do that, the smooth reading was not learning.","Use the long session only after those short retrievals, not instead of them."],
"Why spaced, shorter study sessions can beat one long session",
["How to avoid all quizzes","Why highlighting is forbidden","The history of one library"],
"What does the speaker recommend as a check?",
"Close the book and write three points from memory",
["Highlight the whole page again","Study only the night before","Skip retrieval"],
"Why does the speaker mention smooth rereading?",
"To explain a feeling that makes students overestimate what they know",
["To praise it as the best method","To compare two highlighters","To introduce a new major"],
"What does the speaker imply about a long session?",
"It should follow short retrieval practice, not replace it",
["It is always useless","It should be the only method","It replaces sleep"])

T("practice","mid","A talk in a biology class about coral",
["Coral reefs are often introduced as pretty underwater gardens, but the speaker wants a plainer description.","A reef is a living structure that shelters fish and also blunts waves before they reach a shore.","Warm water and pollution can weaken the corals so they lose the algae that give them color and food.","When that happens, the shore protection weakens along with the habitat.","Communities that limit damaging fishing give the reef time to recover, but they cannot cool an entire ocean by themselves.","The local rule still matters because it removes one pressure while larger climate policies are debated.","Scientists track which species return, and those counts tell a town whether its rule is working."],
"What coral reefs do for coasts, and what weakens them",
["How to build an aquarium","Why fishing should have no rules","A guide to beach hotels"],
"What do the algae provide, according to the speaker?",
"Color and food",
["Wave protection by themselves","A local fishing law","A count of hotels"],
"Why does the speaker mention shore protection?",
"To show that a weakened reef affects the coast, not only the fish",
["To argue that waves are harmless","To compare two hotels","To cancel local rules"],
"What do returning species indicate?",
"Whether a local rule is helping the reef recover",
["That the ocean has already cooled","That fishing should increase","That color no longer matters"])

T("practice","easy","A talk about bilingual signs on campus",
["New signs on this campus will appear in two languages, and the speaker wants to explain why the second line is not a decoration.","Visitors who are still learning the main language miss room numbers when the sign is crowded or uses an idiom.","A plain translation of the essential instruction, such as where to line up, prevents a wrong turn.","The second language does not replace the first, and it is not offered for every poetic slogan on a poster.","It is reserved for safety and wayfinding, where a mistake costs time or causes a risk.","Designers also keep the type large, because a tiny translation helps nobody.","If you are asked to write a sign, put the action in both languages and cut the joke."],
"Why some campus signs use two languages",
["How to become a translator","Why posters should be removed","A history of printing"],
"What kind of information is prioritized for translation?",
"Safety and wayfinding",
["Every joke on a poster","Only room paint colors","Poetic slogans"],
"Why does the speaker mention a crowded sign or an idiom?",
"To explain how a visitor can miss the instruction",
["To recommend more idioms","To ban large type","To compare two alphabets only as art"],
"What should a student do when writing a sign?",
"State the action in both languages and remove the joke",
["Translate only the joke","Use the smallest type","Omit the room number"])

T("practice","mid","A talk in an economics class about queues",
["A queue looks like a simple line, but the speaker treats it as a design problem.","When people cannot see how long the wait will be, they give up or grow angry, even if the actual wait is short.","Posted wait times and a single visible line reduce that uncertainty.","A hidden line, like a phone menu, feels longer because the person cannot compare their progress with others.","Campuses make this mistake at advising offices that use a closed door and no estimate.","The fix is cheap: a number on a screen and an honest range, such as ten to twenty minutes.","The point is not to entertain people who are waiting, but to give them enough information to decide whether to stay."],
"How uncertainty makes waiting feel worse, and how to reduce it",
["How to remove every office","Why phones should be banned","A history of one company"],
"What makes a hidden line feel longer?",
"People cannot see their progress compared with others",
["The wait is always longer in fact","Screens entertain too much","Advising is free"],
"Why does the speaker mention advising offices?",
"As a campus example of a closed door with no time estimate",
["To close those offices","To praise phone menus","To compare two sports"],
"What is the goal of posting a time range?",
"To let people decide whether to stay",
["To make the wait longer","To hide the line","To entertain the crowd"])

T("practice","hard","A talk about how catalogs hide bias",
["Library catalogs look neutral because they are alphabetical, but the words inside them were chosen by people.","An old subject heading can bury a community under a name that the community no longer uses.","A searcher who types the current name may think the library owns nothing.","Librarians now add cross-references so both names lead to the same records.","That repair does not rewrite history; it stops a label from hiding the books.","The speaker asks students to notice when a search fails and to ask a librarian before concluding that the source does not exist.","A failed search is sometimes a vocabulary problem, not an empty shelf."],
"How subject headings can hide library materials, and how cross-references help",
["How to alphabetize a personal bookshelf","Why libraries should close","A novel about one community"],
"What problem can an outdated subject heading cause?",
"A searcher using the current name may miss books the library owns",
["It deletes the books","It rewrites history automatically","It removes the alphabet"],
"Why does the speaker mention cross-references?",
"To show a repair that connects old and current names",
["To argue against all headings","To replace librarians","To prove the shelf is empty"],
"What does a failed search sometimes mean?",
"The searcher used a different name for a topic the library does hold",
["The library owns nothing on any topic","Alphabetization has failed","History was rewritten"])

T("practice","mid","A talk in a public health class",
["Plain language is not the same thing as saying less.","A nurse who explains a side effect in everyday words often reduces fear more than a poster full of precise numbers.","The numbers still matter, and they can come second, after the person understands what may happen and what to do.","Evening clinic hours are another plain tool: they do not change the medicine, but they let a worker attend.","A reminder the day before an appointment cuts missed visits for the same reason.","It removes a memory task from a busy day.","The speaker's claim is that access is a stack of small designs, not a single slogan about health."],
"Small design choices that help people actually receive care",
["How to invent a new medicine","Why numbers should never be used","A biography of one nurse"],
"What does plain language do, according to the speaker?",
"It explains a side effect in everyday words and can reduce fear",
["It removes all numbers forever","It closes evening hours","It replaces the medicine"],
"Why does the speaker mention a reminder?",
"To show how removing a memory task can cut missed visits",
["To argue that appointments are unnecessary","To compare two posters only","To cancel evening hours"],
"What does the speaker imply about access?",
"It depends on several small designs, not one slogan",
["It is solved by numbers alone","It requires closing clinics","It is unrelated to clinic hours"])

T("practice","easy","A talk for tutors in a writing center",
["A useful tutoring session starts with the writer's goal, not with the tutor's favorite rule.","Ask what the writer wants from the twenty-five minutes, and let them read a paragraph aloud.","Comment on organization before commas, because a clear order makes later grammar easier to see.","Do not rewrite the sentences yourself.","A question that sends the writer back to the draft teaches more than a polished line they did not compose.","End by naming one strength and one next step they can finish that night.","If you fix everything, the writer leaves with a better page and the same habits."],
"How a short writing-center session should be structured",
["How to grade papers with a red pen","Why grammar never matters","A history of printing"],
"What should the tutor ask first?",
"What the writer wants from the session",
["Which comma rule is the tutor's favorite","How to rewrite the whole essay","Whether the writer can stay all evening"],
"Why should organization come before commas?",
"A clear order makes later grammar easier to see",
["Commas are never useful","Organization replaces the draft","Reading aloud is forbidden"],
"What happens if the tutor fixes everything?",
"The writer may leave with a better page but the same habits",
["The writer learns every habit at once","The session becomes shorter and useless in a good way","The strength disappears from the page forever"])

T("practice","mid","A talk about campus wayfinding",
["People get lost on campuses for a boring reason: signs name buildings that newcomers cannot picture.","A useful sign adds a landmark, such as the clock or the bus stop, not only a proper name.","Maps at eye level beat maps flat on a distant board, because a lost person will not cross a plaza to squint.","Arrows should match the direction the person is already facing, or they create a second problem.","The speaker tested this with first-week students and found fewer wrong turns when the arrow and the landmark agreed.","Fancy branding did not help if the arrow was reversed.","Design the sign for someone who is late, not for someone who already knows the campus."],
"How signs and maps can reduce wrong turns on a campus",
["How to rename every building","Why maps should be banned","A history of clocks"],
"What did the speaker's test find?",
"Fewer wrong turns when the arrow and the landmark agreed",
["Branding mattered more than direction","Flat maps were the best","New students never get lost"],
"Why does the speaker prefer maps at eye level?",
"A lost person will not cross a plaza to read a distant board",
["Eye-level maps are more expensive art","They remove the need for arrows","They face the wrong way on purpose"],
"Who should the sign be designed for?",
"Someone who is late and does not know the campus",
["Someone who already works there","A branding committee only","A person reading from across town"])

# mocks: m1 x2, m1u, m1l, m2 x2, m2u, m2l
T("m1","mid","A class talk about note-taking",
["Taking notes is not the same as copying every sentence a lecturer says.","The useful page records the question the lecturer is answering and two pieces of support.","A word-for-word transcript feels safe and leaves no time to think.","After class, a three-line summary from memory shows whether the notes captured the structure.","If the summary is impossible, the page is a script, not an understanding.","Students who review that summary the next day remember more than students who recopy the same sentences in neater handwriting.","Neatness is pleasant, but retrieval is the step that makes the lecture stay."],
"How notes should capture structure rather than every sentence",
["How to type faster","Why lectures should be abolished","A brand of notebook"],
"What does a useful page record?",
"The lecturer's question and two pieces of support",
["Every sentence word for word","Only the date","A drawing of the room"],
"Why does the speaker criticize a word-for-word transcript?",
"It feels safe but leaves no time to think",
["It is the best form of retrieval","It replaces the next-day review","It is always incomplete in a helpful way"],
"What matters more than neat handwriting?",
"Reviewing a short summary from memory",
["Recopying the same sentences","Longer lectures","A new notebook"])

T("m1","easy","A talk about lost-and-found habits",
["Lost items on a campus usually fail for a predictable reason: they are turned in without a place name.","A tablet left at a desk is easier to match when the note says science library, Tuesday, gray case.","A note that says only found a tablet forces the owner and the desk to guess.","The speaker asks finders to include the place, the day, and one visible detail, and then to stop opening the device.","Opening it to look for a name can lock the screen or expose private notes.","Owners should check the circulation desk before they buy a replacement, because many items arrive the same day.","The system works when both sides write concrete facts instead of hoping for a lucky meeting."],
"How clear notes help return lost items",
["How to unlock any tablet","Why desks should close","A story about one famous theft"],
"What should a finder write down?",
"The place, the day, and one visible detail",
["The owner's private notes","A password","Only the word found"],
"Why should finders not open the device?",
"They might lock it or expose private notes",
["The desk refuses all tablets","Tuesday is not a real day","Gray cases cannot be returned"],
"What should owners do before buying a replacement?",
"Check the circulation desk",
["Wait a month without asking","Post the password","Open every device in the library"])

T("m1u","hard","A seminar talk about sample size",
["A striking result from ten people can be true and still be a weak guide for a whole campus.","Small samples swing easily: one unusual person moves the average.","Larger samples do not guarantee wisdom, but they make that swing smaller.","The speaker is not asking you to ignore a small study.","She is asking you to ask what would happen if the next ten people were different.","A result that appears in a second, separate group is more trustworthy than a result that appears once in a dramatic chart.","When you read a campus survey, look for the number of respondents before you adopt its advice as a rule."],
"Why sample size changes how much trust a result deserves",
["How to survey every person on Earth","Why averages are illegal","A biography of one researcher"],
"What problem do small samples have?",
"One unusual person can move the average a lot",
["They never show anything true","They always include a second group","They remove the need to ask questions"],
"Why does the speaker mention a second, separate group?",
"A repeated result is more trustworthy than one dramatic chart",
["The second group cancels the first","Charts are always false","Ten people are enough for any rule"],
"What should a reader check in a campus survey?",
"How many people responded",
["Only the colors of the chart","Whether the study is small enough to ignore automatically","The researcher's biography alone"])

T("m1l","easy","A talk about office hours",
["Office hours are a scheduled time when an instructor expects questions, not an interruption.","Students often skip them because they think they need a perfect question.","A confused sentence is enough: I followed the homework until step three.","Bring the draft or the problem, and point to the exact place you stopped.","Instructors can help faster when they can see the work than when they hear a general worry.","If the posted hour conflicts with a lab, email to ask for a different slot rather than disappearing.","Using the hour once early in the term makes the later visit easier, because the instructor already knows your name."],
"How to use an instructor's office hours",
["How to avoid instructors","Why homework should be abolished","A map of every office"],
"What kind of question is enough?",
"A confused sentence that shows where the student stopped",
["A perfect speech","No question at all","Only a complaint about the lab"],
"Why should students bring the draft or the problem?",
"The instructor can see the exact place they stopped",
["The draft replaces the need to talk","General worry is more useful","Email is forbidden"],
"What should a student do if the hour conflicts with a lab?",
"Email and ask for a different time",
["Skip the course","Disappear quietly","Wait until the final exam"],
)

T("m2","mid","A talk about group decision notes",
["Groups remember decisions poorly when the decision lives only in a conversation.","A shared note should state what was chosen, who will do it, and when it is due.","Without the due date, a task feels assigned and still surprises everyone the night before.","The note also prevents two people from doing the same slide.","Reading the note aloud at the end of the meeting takes one minute and catches those overlaps.","Students who rely on memory often insist later that a different decision was made.","The written line is not a lack of trust; it is a way to keep the work about the project instead of about the argument."],
"Why groups should write down decisions, owners, and dates",
["How to avoid meetings","Why notes are rude","A software manual"],
"What three things should the note include?",
"The choice, the person responsible, and the due date",
["Only the argument","Every word of the meeting","A grade for each person"],
"Why does the speaker mention reading the note aloud?",
"A one-minute reading can catch overlapping tasks",
["Reading replaces the project","It proves nobody listened","It removes due dates"],
"What problem does memory create later?",
"People may insist that a different decision was made",
["The note becomes too long","Tasks finish early automatically","Trust increases without writing"])

T("m2","easy","A talk about noise and study spaces",
["Not every quiet room is a good study room.","Some students need a low hum and freeze in total silence, while others lose the sentence they are reading when a conversation starts nearby.","The useful policy is a choice of zones, not one rule for a whole building.","A library can mark one floor for silence and another for group talk.","The signs must be enforced, or the silent floor becomes a second group floor within a week.","Earplugs help the second kind of student but do nothing for the first, who is startled by silence.","Ask which kind of noise helps you before you blame the building."],
"Why study spaces should offer more than one noise level",
["How to soundproof a city","Why libraries should close","A review of earplug brands"],
"What happens if silent-floor signs are not enforced?",
"The silent floor becomes another group floor",
["Everyone studies better","Earplugs stop working for every person","The building closes"],
"Why does the speaker distinguish two kinds of students?",
"They are helped by different levels of background sound",
["They should be graded differently","One kind should be banned","Silence is always best"],
"What should a listener do first?",
"Notice which kind of noise helps them",
["Blame the building immediately","Avoid every library","Remove all signs"])

T("m2u","hard","A seminar talk about replication",
["A single dramatic experiment can be wrong even when the researchers were careful.","Replication means running the idea again, with a new group, to see whether the result returns.","A failure to replicate does not automatically mean the first team cheated.","It can mean the result depended on a detail nobody wrote down, such as the time of day or the wording of a question.","That is why methods sections matter: another team cannot repeat what was never described.","Students should treat a lone headline as a starting point, not as a rule for policy.","Confidence should rise when an independent team sees the same pattern, and it should stay modest until then."],
"Why repeating a study changes how much confidence it deserves",
["How to fake a result","Why methods sections are optional","A list of headlines"],
"What can a failed replication mean, besides cheating?",
"The result depended on a detail that was not written down",
["The first result was certainly invented","Headlines are always true","Time of day never matters"],
"Why do methods sections matter?",
"Another team cannot repeat a procedure that was never described",
["They replace the need for replication","They hide the time of day on purpose","They turn a headline into policy"],
"When should confidence rise?",
"When an independent team sees the same pattern",
["When a headline is dramatic","When only one team has looked","Before any method is described"])

T("m2l","easy","A welcome talk for a campus job",
["If you are new at the information desk, your job is to send people to the right next step.","You do not need to know every rule.","You do need to know which office owns the problem.","A lost ID goes to the card office, a housing leak goes to facilities, and a grade question goes back to the instructor, not to you.","Write the room number down for the visitor instead of pointing vaguely across the quad.","If you are unsure, call the office while the person is still at the desk.","A wrong confident answer wastes more time than a short phone call."],
"How new desk workers should direct questions they cannot fully answer",
["How to change a grade","Why phones are forbidden","A map of the city"],
"Where should a housing leak be sent?",
"To facilities",
["To the card office","To the visitor's instructor only","Nowhere"],
"Why should the worker write the room number?",
"A vague point across the quad is easy to misunderstand",
["Writing replaces the phone","Room numbers are secret","Visitors should not leave"],
"What does the speaker prefer to a wrong confident answer?",
"A short phone call while the person waits",
["Sending the person away immediately","Guessing a grade","Ignoring leaks"])

print("talks", len(talks))
from collections import Counter
print(Counter(t["pool"] for t in talks))
dump("talk", talks)
