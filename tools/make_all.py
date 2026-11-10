import sys
sys.path.insert(0, "/workspace/tools")
from bank_common import dump, words, mc

WHY = {
"indirect-question": "Depois de if ou whether, a ordem é sujeito + verbo. Não puxe o auxiliar para a frente como numa pergunta direta.",
"embedded-wh": "Na pergunta embutida, o wh- fica, mas a ordem volta a ser sujeito + verbo. Não deixe do, does ou did no meio.",
"relative-clause": "Who, that ou which cola logo depois do nome que descreve. O verbo principal concorda com esse nome.",
"passive": "Passiva: forma de be + particípio. Se o agente aparece, use by.",
"auxiliary": "Pergunta direta: auxiliar + sujeito + verbo. O tempo fica no auxiliar.",
"word-order": "Frequência (always, usually) vem antes do verbo principal. Lugar e tempo vêm depois do objeto.",
"preposition": "A preposição é do verbo ou do adjetivo: depend on, interested in, good at. Não traduza do português.",
"reported-speech": "Na fala relatada, a ordem é sujeito + verbo: she asked where I lived, não where did I live.",
"conditional": "Condição real: if + presente, e will na outra oração. Will não entra no if.",
"comparison": "Curto: colder than. Longo: more useful than. Não junte more com -er.",
"gerund-infinitive": "Enjoy e avoid pedem -ing. Decide e want pedem to + verbo.",
"agreement": "O verbo concorda com o sujeito real, não com o nome que está mais perto.",
}

def S(pool, pattern, prompt, prefix, answer, suffix, distractors):
    template = prefix + " ".join("{%d}" % i for i in range(len(answer))) + suffix
    tiles = list(answer) + list(distractors)
    assert len(tiles) == len(set(tiles)), (prompt, tiles)
    assert pattern in WHY
    return {"pool": pool, "pattern": pattern, "prompt": prompt, "template": template,
            "tiles": tiles, "answer": list(answer), "why": WHY[pattern] + " Resposta: " + prefix + " ".join(answer) + suffix}

P, M1, M2 = "practice", "mock1", "mock2"
bas_src = []
def b(*a):
    bas_src.append(S(*a))

b(P,"embedded-wh","What time does the museum close?","Do you know ",["what time","it","closes"],"?",["does","close"])
b(P,"embedded-wh","Where is the registrar?","Can you tell me ",["where","the office","is"],"?",["does","be"])
b(P,"embedded-wh","How much are the tickets?","Do you know ",["how much","the tickets","cost"],"?",["do","costs"])
b(P,"embedded-wh","When does the shuttle leave?","Could you tell me ",["when","the shuttle","leaves"],"?",["does","leave"])
b(P,"embedded-wh","Why was the seminar canceled?","Do you know ",["why","the seminar","was","canceled"],"?",["did","cancel"])
b(P,"indirect-question","Is the lab open on Sunday?","Do you know ",["if","the lab","is","open"],"?",["does","opens"])
b(P,"indirect-question","Will Ana change departments?","Do you know ",["whether","she","will change","departments"],"?",["will she","changes"])
b(P,"indirect-question","Did Marcos submit the form?","Could you check ",["whether","Marcos","submitted","the form"],"?",["did","submit"])
b(P,"indirect-question","Has the package arrived?","Do you know ",["if","the package","has","arrived"],"?",["does","arrive"])
b(P,"auxiliary","I'm looking forward to the concert.","",["What time","does","it","start"],"?",["is","starts"])
b(P,"auxiliary","I need to buy food.","",["Do","you","have","a list"],"?",["Does","having"])
b(P,"auxiliary","I'll take a cooking class.","",["What","will","you","learn"],"?",["do","learns"])
b(P,"auxiliary","The exhibition opens next month.","",["How much","will","tickets","cost"],"?",["do","costs"])
b(P,"auxiliary","You look tired.","",["Did","you","sleep","enough"],"?",["Do","slept"])
b(P,"auxiliary","We're almost late.","",["Should","we","leave","now"],"?",["Do","leaves"])
b(P,"relative-clause","How was the campus tour?","The ",["guides","who","showed us around","were"]," excellent.",["was","which"])
b(P,"relative-clause","Which novel should I borrow?","Borrow the book ",["that","the professor","recommended"],".",["who","recommends"])
b(P,"relative-clause","Do you know the woman by the door?","She is the advisor ",["who","helps","first-year students"],".",["which","help"])
b(P,"relative-clause","The printer is broken again.","The technician ",["who","fixed it","yesterday","is","busy"],".",["which","are"])
b(P,"passive","How did you prepare?","I used the guide ",["that","was provided","by","the professor"],".",["provided","did provide"])
b(P,"passive","Was the room cleaned?","The room ",["was cleaned","before","the guests","arrived"],".",["cleaned","did clean"])
b(P,"passive","Who wrote the announcement?","The announcement ",["was written","by","the dean"],".",["wrote","did write"])
b(P,"passive","Can I still join the club?","New members ",["are accepted","until","Friday"],".",["accept","is accepted"])
b(P,"preposition","Are you coming to the lecture?","It depends ",["on","whether","I finish","my lab"],".",["of","in"])
b(P,"preposition","What are you reading?","I'm interested ",["in","the article","about","memory"],".",["on","at"])
b(P,"preposition","Is Maya good at math?","She is good ",["at","explaining","graphs"],".",["in","on"])
b(P,"preposition","Why are you waiting here?","I'm waiting ",["for","the advisor","to","return"],".",["to the","at"])
b(P,"reported-speech","What did Lila ask you?","She asked ",["where","I","had left","the key"],".",["did I leave","where did"])
b(P,"reported-speech","What did the librarian say?","She said ",["that","the book","was","on reserve"],".",["is","did say"])
b(P,"reported-speech","What did Tom want?","He wanted to know ",["whether","we","could","meet later"],".",["can we","if could we"])
b(P,"conditional","Should we reserve seats?","If you ",["want","a seat,","you","will","need"]," a ticket.",["would want","needed"])
b(P,"conditional","What if the bus is late?","If the bus ",["is","late,","we","will","walk"],".",["will be","walked"])
b(P,"comparison","How is the new café?","The coffee is ",["better","than","the coffee","in the dorm"],".",["more better","that"])
b(P,"comparison","Which route should we take?","The river path is ",["more","pleasant","than","the main road"],".",["pleasanter more","that"])
b(P,"gerund-infinitive","Why did you skip the movie?","I avoid ",["watching","films","on","weeknights"],".",["to watch","watch"])
b(P,"gerund-infinitive","Have you chosen a topic?","I decided ",["to","write","about","public health"],".",["writing","for writing"])
b(P,"word-order","Does Nina miss class?","She ",["usually","arrives","before","the bell"],".",["arrives usually","is arrive"])
b(P,"word-order","Where did you put the form?","I left it ",["on","the desk","this","morning"],".",["this morning on","in morning"])
b(P,"agreement","Is the list ready?","The box of papers ",["is","on","the","front desk"],".",["are","were"])
b(P,"agreement","Who is presenting?","The student with the slides ",["is","ready","to","begin"],".",["are","be"])

# mocks: 10 each, fresh sentences
b(M1,"embedded-wh","Where can I print this?","Do you know ",["where","I","can","print this"],"?",["do","can I"])
b(M1,"indirect-question","Did the tutor reply?","Do you know ",["if","the tutor","has","replied"],"?",["did","replies"])
b(M1,"auxiliary","The match is tonight.","",["What time","does","it","begin"],"?",["is","begins"])
b(M1,"relative-clause","Who handled your housing form?","The clerk ",["who","handled","my form","was"]," helpful.",["which","were"])
b(M1,"passive","When will the results appear?","The results ",["will be","posted","on","Friday"],".",["post","are post"])
b(M1,"preposition","Can you join the team?","I'm not very good ",["at","playing","in","the evening"],".",["in playing","on"])
b(M1,"reported-speech","What did the coach ask?","He asked ",["whether","we","had","practiced"],".",["did we","if did"])
b(M1,"conditional","Is it worth waiting?","If the line ",["is","short,","I","will","wait"],".",["will be","waited"])
b(M1,"comparison","How was the second exam?","It was ",["harder","than","the","first one"],".",["more harder","that"])
b(M1,"gerund-infinitive","Are you going to the talk?","I enjoy ",["hearing","about","new","research"],".",["to hear","hear"])
b(M2,"embedded-wh","How do I get to the clinic?","Could you tell me ",["how","I","can","get there"],"?",["do","can I"])
b(M2,"indirect-question","Has class been moved?","Do you know ",["whether","class","has been","moved"],"?",["did","moves"])
b(M2,"auxiliary","You have been to the archive.","",["Did","you","find","the letter"],"?",["Do","found"])
b(M2,"relative-clause","Which laptop is yours?","The laptop ",["that","has","a blue","sticker"]," is mine.",["who","have"])
b(M2,"passive","Who approved the budget?","The budget ",["was approved","by","the","committee"],".",["approved","did approve"])
b(M2,"preposition","Why did you choose this course?","It depends ",["on","what","I","want to teach"],".",["of","in"])
b(M2,"reported-speech","What did your sister ask?","She wanted to know ",["where","we","would","eat"],".",["where would","did we"])
b(M2,"conditional","Should I bring a jacket?","If it ",["rains,","you","will","need"]," one.",["will rain","needed"])
b(M2,"word-order","Do you visit your aunt often?","I ",["always","visit","her","in June"],".",["visit always","am visit"])
b(M2,"agreement","Are the notes in the folder?","The stack of notes ",["is","beside","the","printer"],".",["are","were"])

bas = []
for i, row in enumerate(bas_src, 1):
    row = dict(row)
    row["id"] = f"bas{i:02d}"
    bas.append(row)
assert sum(1 for x in bas if x["pool"]=="practice") >= 40
assert sum(1 for x in bas if x["pool"]=="mock1") == 10
assert sum(1 for x in bas if x["pool"]=="mock2") == 10
dump("bas", bas)
print("bas ok", len(bas))
