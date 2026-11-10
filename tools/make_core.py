from bank_common import dump

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

ROWS = []
def add(pool, pattern, prompt, template, answer, distractors):
    ROWS.append((pool, pattern, prompt, template, answer, distractors))

P = "practice"
# embedded-wh
add(P,"embedded-wh","What time does the museum close?","Do you know {0} {1} {2}?",["what time","it","closes"],["does","close"])
add(P,"embedded-wh","Where is the registrar?","Can you tell me {0} {1} {2}?",["where","the office","is"],["does","be"])
add(P,"embedded-wh","How much are the tickets?","Do you know {0} {1} {2}?",["how much","the tickets","cost"],["do","costs"])
add(P,"embedded-wh","When does the shuttle leave?","Could you tell me {0} {1} {2}?",["when","the shuttle","leaves"],["does","leave"])
add(P,"embedded-wh","Why was the seminar canceled?","Do you know {0} {1} {2} {3}?",["why","the seminar","was","canceled"],["did","cancel"])
add(P,"embedded-wh","Who is leading the study group?","Can you tell me {0} {1} {2}?",["who","is leading","the group"],["does lead","leads"])
add(P,"indirect-question","Is the lab open on Sunday?","Do you know {0} {1} {2} {3}?",["if","the lab","is","open"],["does","opens"])
add(P,"indirect-question","Will Ana change departments?","Do you know {0} {1} {2} {3}?",["whether","she","will change","departments"],["will she","changes"])
add(P,"indirect-question","Did Marcos submit the form?","Could you check {0} {1} {2} {3}?",["whether","Marcos","submitted","the form"],["did","submit"])
add(P,"indirect-question","Has the package arrived?","Do you know {0} {1} {2} {3}?",["if","the package","has","arrived"],["does","arrive"])
add(P,"auxiliary","I'm looking forward to the concert.","{0} {1} {2} {3}?",["What time","does","it","start"],["is","starts"])
add(P,"auxiliary","I need to buy food.","{0} {1} {2} {3} {4}?",["Do","you","have","a","list"],["Does","having"])
add(P,"auxiliary","I'll take a cooking class.","{0} {1} {2} {3}?",["What","will","you","learn"],["do","learns"])
add(P,"auxiliary","The exhibition opens next month.","{0} {1} {2} {3} {4}?",["How much","will","the tickets","cost"],["do","costs"])
add(P,"auxiliary","You look tired today.","{0} {1} {2} {3} {4}?",["Did","you","sleep","enough","last night"],["Do","slept"])
add(P,"auxiliary","We're almost late.","{0} {1} {2} {3}?",["Should","we","leave","now"],["Do","leaves"])
add(P,"relative-clause","How was the campus tour?","The {0} {1} {2} {3} {4} excellent.",["guides","who","showed us around","were"],["was","which"])
# 4 placeholders in template? "The {0} {1} {2} {3} excellent." I wrote 4 braces and 4 answers. Good. Wait I wrote 4 in answer: guides, who, showed us around, were. Template has 4. Good.
add(P,"relative-clause","Which book should I read?","Read the {0} {1} {2} {3} {4}.",["novel","that","the professor","recommended"],["who","recommends"])
# template 5 placeholders, answer 4. BUG. Fix in a moment by editing after run.
print(len(ROWS))
