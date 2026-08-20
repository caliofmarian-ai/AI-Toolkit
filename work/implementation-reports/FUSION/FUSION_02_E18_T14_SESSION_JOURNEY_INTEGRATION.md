# FUSION-02 — E18/T14 Session / Journey Integration

## Sens uman

Organismul poate lega conversația persistentă de parcursul cognitiv fără să
confunde cele două structuri.

Conversation este containerul durabil al dialogului.

Journey este parcursul cognitiv al unei nevoi informaționale.

O conversație poate avea succesiv mai multe Journey-uri, deoarece fiecare
cerere nouă poate produce o nevoie informațională și un parcurs cognitiv nou.

Sesiunea păstrează numai referința compactă către Journey-ul curent.

## Separări conservate

- Conversation != Journey
- Journey != Working Context
- Journey reference != Memory
- Journey binding != Experience creation

## Persistență

Referința compactă păstrează:

- journey_id;
- need_id;
- status;
- step_count;
- epistemic_gain;
- stopping_reason.

Sesiunile istorice fără Journey rămân lizibile.

Referința Journey supraviețuiește restartului prin persistence-ul existent al
AISessionEngine.

## Erori recuperate

### E18-ERR-001

SESSION_JOURNEY_LIFETIME_IDENTITY_REGRESSION

Prima implementare a legat prea strict Conversation de primul Journey și a
refuzat o cerere ulterioară care producea legitim un Journey nou.

Recovery: sesiunea păstrează Journey-ul curent, nu un Journey unic pe durata
întregii conversații.

### E18-ERR-002

SERVICE_TEST_DOUBLE_PERSISTENCE_BOUNDARY_REGRESSION

Prima integrare service-level a presupus existența fizică a sesiunii și a
încălcat boundary-ul testelor care folosesc sesiuni sintetice.

Recovery: binding-ul persistent se execută numai când sesiunea este prezentă
în AISessionEngine.

## Acceptance

Focused E18/T14 acceptance: PASS.

Complete FUSION regression: PASS.

Structural conservation: PASS.

Human Authority: CONSERVED.

## Stare

E18 — FINALIZAT / CERTIFICAT.

T14 — FINALIZAT / CERTIFICAT.

FUSION-02 — 19 / 21 = 90.5%.

Următorul nod autorizat:

E19 — Comportamentul organismului la eroare, oprire și repornire.

T15 — Failure / Restart / Human Authority Validation.

## Arbore complet FUSION-02

# FUSION-02 — Arborele evoluției organismului epistemic

## Rolul acestui document

Acesta este registrul permanent de progres pentru FUSION-02.

El trebuie citit ca un arbore al evoluției organismului epistemic, nu ca o
simplă listă de taskuri software.

Fiecare etapă trebuie să arate:

1. funcția organismului în semantică umană;
2. identitatea arhitecturală E;
3. taskul tehnic T căruia îi corespunde, atunci când există;
4. starea actuală;
5. erorile apărute în acea ramură;
6. recuperările executate;
7. dovada de acceptare;
8. commitul de conservare, atunci când este cunoscut.

## Legendă

- `[x]` = funcție finalizată și conservată
- `[ ]` = funcție nefinalizată
- `[>]` = funcția curentă / următoarea funcție autorizată
- `[!]` = eroare istorică
- `[R]` = recuperare după eroare
- `[A]` = acceptance / dovadă
- `[C]` = commit de conservare

## Regula de autoritate

Codurile E reprezintă ordinea evolutivă principală.

Codurile T reprezintă taskurile tehnice din planul de implementare și sunt
atașate ramurii E căreia îi servesc.

E și T nu sunt două liste independente.

Arborele nu poate inventa o etapă nouă și nu poate muta o etapă fără
reconciliere cu auditurile și planurile autoritative.

Erorile nu sunt șterse din istoria evoluției. Ele se atașează nodului în care
au apărut, împreună cu recuperarea și acceptance-ul ulterior.

---

# Arbore

## [x] E0 — Înțelegerea și măsurarea organismului existent

└── [x] T1 — Caracterizarea fiziologiei existente

Scop uman:
Organismul trebuie mai întâi să știe ce anatomie și ce comportamente are deja,
înainte ca acestea să fie modificate.

Stare:
FINALIZAT / CONSERVAT

---

## [x] E1 — Urmărirea conservării semanticii

└── Nu provine direct dintr-un task T vechi; este o obligație evolutivă
    introdusă și consolidată prin auditurile semantice.

Scop uman:
Organismul trebuie să poată observa dacă sensul unei informații se pierde,
se reduce sau se modifică în timpul trecerii prin organele sale.

Stare:
FINALIZAT / CONSERVAT

---

## [x] E2 — Conservarea semanticii din CSL în UEM

└── Extensie evolutivă rezultată din auditurile semantice.

Scop uman:
Ceea ce organismul înțelege din sursă trebuie să ajungă în modelul epistemic
fără pierderea sensului necesar.

Stare:
FINALIZAT / CONSERVAT

---

## [x] E3 — Conservarea UEM în cunoașterea materializată

└── Extensie evolutivă rezultată din auditurile semantice.

Scop uman:
Cunoașterea stocată de organism trebuie să păstreze sensul rezultatului
epistemic din care a provenit.

Stare:
FINALIZAT / CONSERVAT

---

## [x] E4 — Identitatea semantică și manifestările ei

└── Extensie evolutivă rezultată din auditurile de identitate semantică.

Scop uman:
Organismul trebuie să distingă un lucru de formele, reprezentările și
manifestările acelui lucru.

Stare:
FINALIZAT / CONSERVAT

---

## [x] E5 — Reconcilierea timpului și autorității

└── Extensie evolutivă rezultată din auditurile de adevăr curent,
    temporalitate și autoritate.

Scop uman:
Organismul trebuie să distingă informația istorică de adevărul curent și să
nu transforme simpla existență a unei informații în autoritate.

Stare:
FINALIZAT / CONSERVAT

---

## [x] E6 — Conștientizarea limitelor furnizorului AI

└── [x] T2 — Provider Budget Introspection

Scop uman:
Organismul trebuie să știe ce limite are furnizorul AI înainte să-i ceară
mai mult decât poate primi în siguranță.

Stare:
FINALIZAT / CONSERVAT

---

## [x] E7 — Orientarea epistemică permanentă

└── [x] T3 — Permanent Orientation

Scop uman:
Organismul trebuie să-și păstreze orientarea: cine este, ce repository
analizează, ce autoritate are și ce limite trebuie respectate.

Stare:
FINALIZAT / CONSERVAT

---

## [x] E8 — Transportul sigur al rezultatelor epistemice

└── [x] T4 — Epistemic Result Envelope

Scop uman:
Informația trebuie transportată între organe împreună cu identitatea,
proveniența, autoritatea, incertitudinea și statutul ei epistemic.

Stare:
FINALIZAT / CONSERVAT

---

## [x] E9 — Găsirea organului care poate răspunde nevoii

└── [x] T5 — Federated Resolution

Scop uman:
Organismul trebuie să poată identifica organul potrivit pentru o nevoie de
cunoaștere fără să construiască o a doua fiziologie paralelă.

Stare:
FINALIZAT / CONSERVAT

---

## [x] E10 — Percepția controlată și numai pentru citire

└── [x] T6 — Read-only Capability Mediation

Scop uman:
Organismul poate căuta și citi informație în mod controlat fără ca simpla
citire să îi permită să modifice repository-ul sau să confere autoritate.

Ramuri demonstrate:

├── [x] Căutare read-only
├── [x] Citire bounded read-only
├── [x] Prima sursă selectată poate fi citită
├── [x] Candidații de căutare rămân conservați
└── [x] Sursa lipsă poate produce UNKNOWN fără autoritate inventată

Erori istorice relevante:

├── [!] Constructorul coordonatorului a fost presupus greșit ca acceptând
│       repository_root.
├── [R] Constructorul existent a fost conservat; repository_root a rămas
│       dependență explicită a operației.
├── [!] Path a fost folosit fără import.
├── [R] Dependența pathlib.Path a fost făcută explicită.
├── [!] Integrarea service a presupus self.repository_root inexistent.
├── [R] A fost reutilizat root-ul existent al infrastructurii de sesiune.
├── [!] Missing source a permis FileNotFoundError să evadeze.
└── [R] Missing/unreadable source a fost reconciliat cu UNKNOWN.

Dovezi de conservare cunoscute:

├── [C] a55393feb0eb7aed1f68391127bddbc4ddecce3f
└── [C] 2817cc29b5812144b7e02242f7587ba3ef020f8f

Stare:
FINALIZAT / CONSERVAT

---

## [x] E11 — Formarea nevoii de cunoaștere și urmărirea parcursului

└── [x] T7 — Information Need + Journey State

Scop uman:
Organismul trebuie să poată spune ce încearcă să afle și să păstreze urma
parcursului cognitiv fără să confunde parcursul cu cunoașterea însăși.

Ramuri demonstrate:

├── [x] Information Need
├── [x] Journey State
├── [x] starea vizitată este conservată
├── [x] numărul de pași este conservat
└── [x] input Journey nu este modificat arbitrar

Stare:
FINALIZAT / CONSERVAT

---

## [x] E12 — Coordonarea procesului de gândire

└── [x] T8 — Cognitive Coordination Loop

Scop uman:
Organismul coordonează un pas cognitiv: formulează nevoia, selectează,
percepe, evaluează rezultatul și decide controlat dacă poate continua sau
trebuie să se oprească.

Rezultate epistemice demonstrate:

├── [x] SATISFIED
├── [x] PARTIAL
├── [x] UNKNOWN
├── [x] BLOCKED
├── [x] HUMAN_REQUIRED
├── [x] FORBIDDEN
└── [x] NO_EPISTEMIC_GAIN

Reflexe de oprire demonstrate:

├── [x] nevoie repetată
├── [x] rezultat repetat
├── [x] identitate/capabilitate repetată
├── [x] ciclu de traversal
├── [x] organ indisponibil
├── [x] ambiguitate
├── [x] limită de autoritate
└── [x] lipsă de câștig epistemic

Conservarea Journey demonstrată:

├── [x] BLOCKED
├── [x] HUMAN_REQUIRED
├── [x] FORBIDDEN
├── [x] provider failure
├── [x] visited state
├── [x] step count
└── [x] fără fabricated hop

Erori istorice relevante:

├── [!] Verificatorul Bash al mutation boundary a omis un test untracked.
└── [R] Verificatorul a fost corectat fără resetarea implementării.

Dovezi de conservare cunoscute:

├── [C] 149c456cd5e1285eaadd1dd6edd8f844649f33d6
├── [C] d5954c9d5a1bf73334d88b9ebffc37ca3b92e095
├── [C] 20d2aa1d86ca190d1ae900cd67f4c5fbbf616280
└── [C] 482baab3d89cf2db59e2711844b3a4c465855ad5

Stare:
FINALIZAT / CERTIFICAT

---

## [x] E13 — Formarea contextului mental de lucru

└── [x] T9 — Working Context Assembly

Scop uman:
Organismul trebuie să formeze o memorie de lucru limitată și relevantă pentru
problema curentă.

Contextul de lucru trebuie să poată transporta ceea ce este necesar pentru
raționamentul curent fără să devină o copie a repository-ului și fără să
devină o copie integrală a Journey.

Trebuie păstrată separarea:

Knowledge != Journey != Working Context

Trebuie caracterizate și apoi demonstrate cel puțin:

├── [x] întrebarea umană relevantă
├── [x] constrângerile relevante
├── [x] rezultatele epistemice relevante
├── [x] identitățile semantice relevante
├── [x] clasa epistemică
├── [x] autoritatea
├── [x] proveniența
├── [x] incertitudinea
├── [x] relațiile relevante
└── [x] concluzia compactă a Journey

Erori istorice E13/T9:
├── [!] E13-ERR-002 — WRONG_EVOLUTION_TREE_PATH
│   └── [R] calea autoritativă work/fusion/FUSION_02_EVOLUTION_TREE.md
├── [!] E13-ERR-003 — TERMUX_BATCH_MESSAGE_FRAGMENTATION
│   └── [R] batch-uri compacte; arbore persistent reutilizat
├── [!] E13-ERR-004 — STALE_RETRIEVAL_AUTHORITY_FIXTURE
│   └── [R] authority_conferred=False restaurat
├── [!] E13-ERR-005 — INCOMPLETE_T9_SYNTHETIC_RETRIEVAL_CONTRACT
│   └── [R] working_context_materialized=False restaurat din contractul existent
├── [!] E13-ERR-006 — GENERATED_REPORT_BLANK_LINE_AT_EOF
│   └── [R] Markdown normalizat la exact un newline final
└── [!] E13-ERR-008 — AUTHORITY_BRANCH_LEFT_UNCHECKED_AFTER_CERTIFICATION
    └── [R] authority_conferred=False + Human Authority proof reconciled with tree

Stare:
FINALIZAT / CERTIFICAT

---

## [x] E14 — Controlul dimensiunii contextului mental

└── [x] T10 — Context Budget Governance
    ├── [x] capacitatea providerului trebuie să fie cunoscută
    ├── [x] spațiul pentru răspuns este rezervat înainte de context
    ├── [x] orientarea, întrebarea și instrucțiunile au headroom separat
    ├── [x] Working Context este măsurat înainte de provider
    ├── [x] compactarea păstrează obiecte epistemice întregi
    ├── [x] proveniența rămâne legată de evidența păstrată
    ├── [x] hard overflow produce refuz explicit
    ├── [x] capacitatea necunoscută produce fail-closed
    ├── [x] Journey și cunoașterea organismului nu sunt reduse
    ├── [x] capacitatea modelului este preluată direct din ProviderRegistry
    ├── [x] payload-ul guvernat este conectat la provider boundary
    └── [x] acceptance multi-provider/model asupra requestului serializat

Erori istorice E14/T10:
└── [!] E14-ERR-001 — REPRESENTATIVE_BUDGET_FIXTURE_OMITTED_RELATIONSHIPS
    └── [R] fixture-ul măsoară candidatul complet; producția nu a fost slăbită

Scop uman:
Organismul știe acum cât spațiu mental poate folosi în siguranță și poate
reduce numai conștiința temporară trimisă furnizorului AI, fără să taie
informații epistemice la jumătate și fără să-și reducă memoria, Journey sau
cunoașterea.

Stare:
FINALIZAT / CERTIFICAT

---

## [x] E15 — Funcționarea în paralel a fiziologiei vechi și a celei cognitive

└── [x] T11 — Shadow Pipeline

Scop uman:
Noua fiziologie trebuie observată în paralel cu cea existentă înainte ca
organismul să depindă implicit de ea.

Ramuri demonstrate:

├── [x] fiziologia legacy rămâne calea reală către provider
├── [x] fiziologia cognitivă este observată în paralel
├── [x] Working Context este guvernat separat
├── [x] payload-ul cognitiv nu este trimis providerului
├── [x] comparația legacy/cognitivă este observabilă
├── [x] proveniența cognitivă rămâne observabilă
├── [x] autoritatea nu este conferită de shadow
├── [x] Human Authority rămâne conservată
├── [x] provider/model selection rămâne conservată
├── [x] provider answer behavior rămâne conservat
├── [x] shadow nu dublează persistence-ul
└── [x] contractul istoric service→pipeline.run rămâne compatibil

Stare:
FINALIZAT / CERTIFICAT

---

## [x] E16 — Prima trecere reală la noua fiziologie pentru cererea simplă „hi”

└── [x] T12 — Default Cognitive Cutover

Scop uman:
O cerere simplă trebuie să poată folosi noua fiziologie fără încărcarea
implicită a profilului complet al repository-ului.

Ramuri demonstrate:

├── [x] Working Context cognitiv devine payload-ul real către provider
├── [x] cererea simplă „hi” traversează fiziologia cognitivă
├── [x] Context Budget Governance rămâne activ înainte de provider
├── [x] provider/model selection rămâne conservată
├── [x] UNKNOWN rămâne stare epistemică validă
├── [x] autoritatea nu este inventată
├── [x] Human Authority rămâne conservată
├── [x] fiziologia shadow nu mai este calea implicită
├── [x] default cutover este consumat exact o dată per request
└── [x] contractul istoric service→pipeline.run rămâne compatibil

Stare:
FINALIZAT / CERTIFICAT

---

## [x] E17 — Cercetarea reală fără supraîncărcarea care producea OpenAI 429

└── [x] T13 — Research-path Cognitive Cutover / Provenance Validation

Scop uman:
Organismul trebuie să poată cerceta repository-ul real prin noua fiziologie
fără să reintroducă supraîncărcarea vechiului context și fără să piardă
proveniența.

Ramuri demonstrate:

├── [x] nevoia de cercetare activează navigarea read-only
├── [x] search produce identități repository-relative
├── [x] read este limitat la o sursă selectată din retrieval
├── [x] read-ul real precede materializarea Working Context
├── [x] conținutul citit intră ca evidență bounded
├── [x] fiecare evidență păstrează source_path
├── [x] proveniența corespunde evidenței păstrate
├── [x] read-ul nu conferă autoritate
├── [x] UNKNOWN nu produce conținut inventat
├── [x] Working Context rămâne selectiv la maximum 8 surse
├── [x] Context Budget Governance rămâne activ
└── [x] fiziologia cognitivă rămâne calea reală către provider

Stare:
FINALIZAT / CERTIFICAT

---

## [x] E18 — Legarea sesiunii de parcursul cognitiv

└── [x] T14 — Session / Journey Integration

Scop uman:
Conversația persistentă și parcursul cognitiv cooperează fără să devină
același lucru. Sesiunea păstrează referința compactă către Journey-ul curent,
iar o conversație persistentă poate continua cu un Journey nou atunci când
apare o nouă cerere umană.

Ramuri demonstrate:

├── [x] sesiunea păstrează referința compactă către Journey-ul curent
├── [x] Journey ID rămâne distinct de Session ID
├── [x] Need ID rămâne observabil
├── [x] statusul Journey rămâne observabil
├── [x] checkpoint-ul Journey poate evolua
├── [x] aceeași conversație poate începe un Journey nou
├── [x] Conversation != Journey
├── [x] Journey != Working Context
├── [x] Journey reference != Memory
├── [x] legarea Journey nu creează automat Experience
├── [x] sesiunile istorice fără Journey rămân lizibile
├── [x] referința Journey supraviețuiește restartului
└── [x] service-level synthetic session compatibility este conservată

Erori istorice E18/T14:

├── [!] E18-ERR-001 — SESSION_JOURNEY_LIFETIME_IDENTITY_REGRESSION
│   └── [R] Conversation păstrează Journey-ul curent și poate avansa legitim
│       la un Journey nou pentru o nouă cerere
└── [!] E18-ERR-002 — SERVICE_TEST_DOUBLE_PERSISTENCE_BOUNDARY_REGRESSION
    └── [R] persistence binding respectă boundary-ul sesiunilor sintetice
        folosit de fiziologia service-level existentă

Stare:
FINALIZAT / CERTIFICAT

---

## [>] E19 — Comportamentul organismului la eroare, oprire și repornire

└── [ ] T15 — Failure / Restart / Human Authority Validation

Scop uman:
Organismul trebuie să-și păstreze limitele epistemice și autoritatea umană
atunci când apare o eroare, este întrerupt sau este repornit.

Stare:
NEÎNCEPUT

---

## [ ] E20 — Retragerea fiziologiei vechi ca mecanism implicit

└── [ ] T16 — Legacy Default Context Retirement

Scop uman:
După ce noua fiziologie este demonstrată, vechiul context implicit poate fi
retras din rolul de mecanism principal fără distrugerea compatibilității
necesare.

Stare:
NEÎNCEPUT

---

# Poziția curentă

Etape evolutive totale: 21

Etape finalizate: 19

Etapa curentă: E19 — Comportamentul organismului la eroare, oprire și repornire

Task tehnic curent: T15 — Failure / Restart / Human Authority Validation

Progres evolutiv brut:

19 / 21 = 90.5%

Progres afișat:

90.5% FUSION-02

## Regula de actualizare după fiecare Bash

După fiecare Bash executat cu succes:

1. nodul afectat se actualizează;
2. acceptance-ul se atașează nodului;
3. commitul se atașează nodului;
4. procentul se recalculează;
5. următorul nod autorizat se marchează `[>]`;
6. arborele complet este afișat utilizatorului.

După fiecare Bash care eșuează:

1. eroarea primește o ramură `[!]` sub nodul unde s-a produs;
2. producția nu este declarată finalizată;
3. recuperarea primește o ramură `[R]`;
4. eroarea rămâne în istoria arborelui după recuperare;
5. nodul poate deveni `[x]` numai după acceptance și conservare.

## Invariant de progres

Un nod nu este bifat pentru că a fost scris cod.

Un nod este bifat numai când funcția sa este:

IMPLEMENTATĂ
+
TESTATĂ
+
AUDITATĂ
+
CONSERVED ÎN GIT

Acest arbore este registrul uman al evoluției FUSION-02.
