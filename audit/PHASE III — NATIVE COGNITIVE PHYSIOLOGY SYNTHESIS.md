PHASE III — NATIVE COGNITIVE PHYSIOLOGY SYNTHESIS

Am tratat Phase III ca sinteză arhitecturală, nu implementare. Am reverificat punctele critice din branch-ul fusion/fusion-01-runtime-epistemic-organism, în special AIContextBuilder și AIRequestPipeline. Codul confirmă problema fundamentală: AIContextBuilder.build() construiește necondiționat RepositoryProfile complet plus context de dezvoltare, runtime, Canon și workspace, iar pipeline-ul trimite imediat rezultatul providerului; întrebarea Human nu participă deloc la selecția cunoașterii.

Nu am modificat nimic.

Verdict Phase III

Cea mai mică fiziologie nativă nu necesită un nou sistem de cunoaștere.

Necesită introducerea unei faze cognitive intermediare între întrebarea Human și materializarea Working Context:

Human Question
      ↓
Permanent Epistemic Orientation
      ↓
Information Need
      ↓
Capability / Organ Selection
      ↓
Federated Resolution
      ↓
Perception / Traversal
      ↓
Authority + Provenance Evaluation
      ↓
Need satisfied?
   ┌──┴───┐
   NO     YES
   │       │
   ↓       ↓
Next Need  Working Context
   │       ↓
   └──── Context Budget Governance
           ↓
        Provider
           ↓
         Answer

Elementul nou nu „știe” lucrurile. Coordonează organele care le știu.


---

A. Native Cognitive Physiology

Fiziologia optimă are trei stări distincte ale conștiinței AI.

1. Permanent Orientation

Mică, stabilă, prezentă la fiecare request.

Răspunde la:

> „Cine sunt, unde sunt și ce pot consulta?”



Nu conține repository-ul.

2. Epistemic Journey

Este cercetarea temporară:

need
→ organ
→ resolution
→ retrieval
→ evaluation
→ next need

Poate accesa mult mai multă cunoaștere decât poate încăpea vreodată în context.

3. Working Context

Este rezultatul selectat al cercetării.

Răspunde:

> „Ce trebuie să am acum în conștiință ca să rezolv problema?”



Această separare este fundamentală:

AVAILABLE KNOWLEDGE
       ≠
RETRIEVED KNOWLEDGE
       ≠
WORKING CONTEXT

Astăzi AI-Toolkit aproape le confundă pe primele două: AIContextBuilder materializează informație înainte să știe ce caută.


---

B. Permanent Orientation Contract

Permanent Orientation trebuie să fie suficientă pentru orientare, dar insuficientă pentru rezolvarea problemei.

Propun conceptual următoarele șapte categorii.

Permanent	Conținut

Identity	AI Partner / rol runtime
Organism	AI-Toolkit + active project/repository
Task position	branch, issue, epic, sprint/session relevante
Human Authority	limitele autorității AI și Human
Epistemic classes	Canon, Evidence, Repository, Experience, Memory, Conversation etc.
Organ map	ce organe sunt disponibile
Navigation vocabulary	resolve, inspect, traverse, trace etc.


Nu trebuie să conțină:

RepositoryProfile;

conținutul Canonului;

graph nodes;

toate memories;

toate dependencies;

toate reports;

toate source files.


Poate fi derivată din CSL/UEM?

În mare parte, da, dar nu exclusiv.

CSL/UEM poate furniza orientarea structural-semantică:

identity
type
relationship
source
status

Dar authority runtime trebuie derivată din PCC/FUSION, iar active task/runtime state din organele runtime existente.

Prin urmare:

Permanent Orientation
 =
CSL/UEM semantic orientation
+ Runtime position
+ PCC/FUSION authority boundaries
+ capability registry

Nu avem nevoie ca CSL să fie extins pentru aceasta.


---

C. Information Need Model

Aceasta este într-adevăr anatomie nouă.

Dar trebuie să fie foarte mică.

Un Information Need nu trebuie să fie query language și nici DSL.

Conceptual are nevoie doar de:

Need Identity
Question/Goal
Target concept or phenomenon
Required epistemic class/domain
Reason
Status

Exemplu:

N1

goal:
Determine why Owner AI Chat receives HTTP 429

target:
AI request physiology

desired knowledge:
runtime implementation / request path

reason:
Need to identify where request materialization occurs

status:
OPEN

Nu trebuie să conțină filesystem path.

Nu trebuie să știe deja că pipeline.py există.

Asta ar distruge semantic resolution.

Important

Un Need exprimă:

> ce trebuie cunoscut



nu:

> ce fișier trebuie citit.




---

D. Federated Resolution Model

Nu trebuie construit un index gigantic.

Modelul minim este:

semantic target
      ↓
domain recognition
      ↓
existing resolver selection
      ↓
delegate
      ↓
manifestation
      +
provenance

Exemple:

PCC-01
 ↓
CanonicalRepository
 ↓
CanonicalDocument
 ↓
current source manifestation

sau:

AIRequestPipeline
 ↓
UEM / repository knowledge
 ↓
repository manifestation

sau:

LMEM-...
 ↓
LayeredMemory
 ↓
LayeredMemoryNode

sau:

ExperienceId
 ↓
PersistentExperienceRepository
 ↓
Experience

Colectorul federat nu trebuie să stocheze copii.

El trebuie să știe doar:

> „Pentru această familie semantică, care organ are dreptul să rezolve identitatea?”



Rezultatul conceptual trebuie să fie:

identity
domain
manifestation
resolver_used
source/provenance
resolution confidence/status

Asta păstrează CSL independent de filesystem.


---

E. Cognitive Traversal Loop

Aici este inima fiziologiei.

QUESTION
   ↓
derive NEED
   ↓
select CAPABILITY
   ↓
resolve TARGET
   ↓
PERCEIVE
   ↓
evaluate epistemically
   ↓
Does this satisfy NEED?

Dacă nu:

Result reveals unresolved dependency/concept
                    ↓
                 NEW NEED
                    ↓
              another capability

Crucial: coordonatorul nu implementează traversal algorithms.

Pentru graph:

> folosește KnowledgeGraph.



Pentru provenance:

> folosește PCC Provenance.



Pentru memory depth:

> folosește LayeredMemory.



Pentru repository:

> folosește RepositoryEngine.



Stop conditions

Trebuie să existe cel puțin:

Need satisfied — există suficientă evidență pentru răspuns.

No resolvable next need — organismul nu poate continua.

Authority boundary — următorul pas ar necesita autoritate pe care AI nu o are.

Repeated identity — aceeași manifestare + aceeași întrebare nu se inspectează inutil.

Traversal cycle — A → B → C → A.

Diminishing epistemic gain — rezultatele noi nu schimbă înțelegerea.

Provider/context hard constraint — materializarea trebuie redusă, nu cercetarea neapărat oprită.

Human decision required — problema nu mai este epistemică, ci decizională.

Aș evita o regulă simplă „maximum 5 hops”. Poate exista ca emergency safety bound, dar nu ca principiu epistemic.


---

F. Authority & Provenance Preservation

Aici nu trebuie inventat aproape nimic.

PCC Provenance deja separă Source, Observation, Evidence, Claim, Verification, Knowledge și Current State și diferențiază inclusiv surse HUMAN, AI, CANON, REPOSITORY, RUNTIME, TEST etc.

Fiecare rezultat recuperat în Journey trebuie însă transportat într-un epistemic envelope conceptual:

identity
epistemic_class
source
provenance
authority
retrieval_reason
retrieved_via

Exemplu:

identity:
AIContextBuilder.build

class:
REPOSITORY IMPLEMENTATION

source:
lib/python/ai_platform/context_builder.py

authority:
TECHNICAL OBSERVATION

provenance:
current repository branch/commit

retrieval_reason:
N3 — determine what enters provider context

Retrieval nu schimbă clasa.

Conversation ≠ Evidence
AI conclusion ≠ Canon
Repository observation ≠ Human Authority
Memory ≠ Truth

Aceasta trebuie să rămână proprietatea organismului, nu a providerului AI.


---

G. Working Context Contract

Da: Orientation Context și Working Context trebuie separate conceptual.

Working Context nu trebuie să fie AIContextBuilder.build() redenumit.

Este produsul cercetării.

Structura minimă:

QUESTION

ACTIVE NEED / resolved objective

RELEVANT FACTS
  identity
  compact content
  epistemic class
  authority

EVIDENCE REFERENCES
  source
  provenance

RELEVANT RELATIONSHIPS

UNRESOLVED UNCERTAINTIES

HUMAN AUTHORITY CONSTRAINTS

JOURNEY SUMMARY

Nu trebuie să conțină toate intermediate results.

De exemplu, dacă pentru a găsi AIContextBuilder am traversat:

AIPlatformService
→ AIRequestPipeline
→ AIContextBuilder

Working Context poate păstra relația:

AIPlatformService
→ pipeline.run()
→ AIContextBuilder.build()

plus fragmentele relevante.

Nu trebuie să păstreze toate obiectele intermediare integral.


---

H. Context Budget Physiology

Bugetul trebuie să guverneze conștiința, nu memoria organismului.

Formula corectă este:

Epistemic access: effectively large
Working consciousness: bounded

Politica ar trebui să opereze în ordinea următoare:

1. deduplicate — aceeași evidență nu apare de două ori;


2. references before copies — păstrează identity/provenance când raw content nu mai este necesar;


3. semantic compaction — păstrează relațiile importante;


4. discard obsolete intermediate retrievals;


5. preserve contradictory evidence — nu compacta contradicțiile într-o concluzie falsă;


6. provenance-preserving summarization;


7. progressive retrieval — materializează detalii numai când sunt necesare;


8. reserve provider headroom pentru question + answer;


9. hard-limit enforcement înainte de provider.



Un rezultat poate astfel ieși din Working Context fără să dispară din Journey.

retrieved result
     ↓
used
     ↓
compressed to reference
     ↓
still resolvable later

Asta permite cercetării să fie mai mare decât context window.


---

I. Capability / Tool Boundary

Modelului nu trebuie să i se ofere:

open arbitrary file
execute arbitrary Python
access arbitrary runtime object

Trebuie să i se ofere o suprafață epistemică mediată.

Vocabularul propus de tine este aproape exact ce trebuie:

SEARCH
RESOLVE
READ
INSPECT
TRAVERSE
TRACE_PROVENANCE

Dar acestea sunt capability intents, nu acces direct.

Modelul cere conceptual:

INSPECT semantic_identity=AIRequestPipeline

Organismul decide:

allowed?
which organ?
which resolver?
which manifestation?
what authority classification?
what can safely be returned?

Astfel:

AI reasoning
    ↓
capability request
    ↓
organism mediation
    ↓
existing organ

nu:

AI
↓
filesystem/runtime

Acesta este un boundary foarte important.


---

J. Audit Trail

Epistemic Journey trebuie să fie reproductibilă fără a loga automat tot conținutul.

Urma minimă:

journey identity
question identity
need
selected capability
selected organ
query/semantic target
resolved identity
provenance reference
result classification
next need
stop reason
working-context inclusion/exclusion

De exemplu:

JOURNEY-429

N1
inspect AI request physiology
→ AIPlatformService
→ resolved repository manifestation

N2
follow request path
→ AIRequestPipeline

N3
determine context source
→ AIContextBuilder

...

STOP:
causal path sufficiently demonstrated

Persistent Experience / Error Memory

Journey poate deveni ulterior input candidat pentru acestea.

Dar:

audit trail
≠
Experience automatically

failed journey
≠
Error Memory automatically

successful inference
≠
Knowledge automatically

PCC/Sedimentation authority trebuie să rămână între ele.


---

K. 429 End-to-End Simulation

Acum putem simula exact noua fiziologie.

Human

> Why does Owner AI Chat receive OpenAI 429?



Permanent Orientation

Modelul primește doar aproximativ:

You are AI Partner inside AI-Toolkit.

Active organism:
AI-Toolkit

Active repository:
AI-Toolkit

Human Authority:
preserved

Available epistemic organs:
CSL/UEM
Canon
Knowledge Graph
Repository
Provenance
Layered Memory
Persistent Experience
Runtime

Capabilities:
SEARCH RESOLVE READ INSPECT TRAVERSE TRACE_PROVENANCE

Nu primește RepositoryProfile.


---

NEED 1

Understand Owner AI Chat request physiology.

Organ: semantic orientation/UEM + Repository.

Resolution: AIPlatformService.

Result: ask_repository() calls pipeline.run().

Provenance: current repository implementation.

Next reason: request leaves service through pipeline.


---

NEED 2

Determine what AIRequestPipeline sends to provider.

Organ: RepositoryEngine/perception.

Resolve: AIRequestPipeline.

Inspect: run().

Rezultatul real:

context = self.context_builder.build()
completion = adapter.complete(
    question=question,
    context=context,
    model=selected_model
)

Next reason: context size originates upstream in builder.


---

NEED 3

Determine how provider context is constructed.

Resolve: AIContextBuilder.

Inspect: build().

Rezultatul descoperă:

GitContextProvider.collect
DevelopmentContextProvider.collect
WorkspaceContextProvider.collect
live_context
runtime_status
recent reports
RepositoryEngine.profile()
RepositoryProfileSerializer.to_dict()
canonical documents
engineering session

Next reason: RepositoryProfile este candidat major pentru volum.


---

NEED 4

Determine repository-profile materialization behavior.

Organ: Repository.

Inspect: profile + serializer.

Phase II a demonstrat:

RepositoryProfileSerializer.to_dict(profile)
→ asdict(profile)

Fără selection.

Acum există o explicație structurală puternică.


---

NEED 5

Establish whether request size actually violates provider constraints.

Aici organismul trebuie să consulte Evidence, nu să ghicească.

Organe:

runtime/provider evidence;

Railway/runtime reports;

usage/error evidence;

eventual Error Memory precedent.

Rezultatul necesar:

HTTP 429
provider
request size/token evidence
timestamp
hard/provider limit if demonstrable

Dacă nu există:

UNKNOWN

nu „probabil sigur”.


---

NEED 6

Dacă provider evidence confirmă context overflow:

Trace causal relation.

Se poate formula:

AIContextBuilder
→ unconditional RepositoryProfile materialization
→ large serialized context
→ adapter request
→ provider token/request constraint
→ HTTP 429

STOP

Stop reason:

CAUSAL EXPLANATION SUFFICIENTLY SUPPORTED

Nu este nevoie să inspectăm Memory, Canon sau tot Knowledge Graph dacă acestea nu adaugă informație relevantă.


---

Working Context rezultat

Providerului îi poate ajunge conceptual ceva de forma:

QUESTION
Why does Owner AI Chat receive OpenAI 429?

TECHNICAL EVIDENCE

E1
AIRequestPipeline.run() calls AIContextBuilder.build()
and passes the resulting context directly to adapter.complete().
Source: ai_platform/pipeline.py

E2
AIContextBuilder.build() unconditionally materializes
RepositoryEngine.profile() and serializes the full profile,
plus runtime/development/workspace/canonical state.
Source: ai_platform/context_builder.py

E3
RepositoryProfileSerializer performs full dataclass serialization.
Source: repository_engine/serializer.py

E4
Observed provider/runtime 429 evidence [...]
Source: runtime evidence

CAUSAL RELATION
Owner AI request
→ full context materialization
→ oversized provider request
→ demonstrated provider rejection

UNCERTAINTY
[whatever remains unverified]

Nu 295 KB.

Probabil ordinul ar fi câțiva KB până la câteva zeci de KB, în funcție de raw evidence necesară. Nu voi inventa o dimensiune exactă fără materializarea și măsurarea rezultatului.

Diferența conceptuală însă este enormă:

CURRENT
~295 KB before reasoning

PROPOSED PHYSIOLOGY
small orientation
+
task-selected evidence

Și organismul poate cerceta mult mai mult de 295 KB pe parcurs fără să țină totul simultan în context.


---

L. Reuse-vs-New Matrix

Funcție	Verdict

CSL semantic identity	REUSE
SemanticAnalyzer	REUSE
UEM	REUSE
Canon resolution	REUSE
Knowledge Graph	REUSE
Dependency/Traceability	REUSE
Repository perception	REUSE
Provenance traversal	REUSE
Authority anatomy	REUSE
Layered Memory traversal	REUSE
Persistent Experience storage	REUSE
FUSION runtime reachability	ADAPT
AIContextBuilder	ADAPT
AIRequestPipeline	CONNECT
AISessionEngine	CONNECT
Permanent Orientation assembly	NEW, foarte mic
Information Need representation	NEW
Federated resolver coordination	CONNECT
Capability mediation	NEW/CONNECT
Cognitive traversal coordination	NEW
Working Context assembly	NEW/ADAPT
Context budget governance	NEW
Journey audit	NEW, reutilizând persistence/provenance boundaries


Observația importantă este raportul:

> Majoritatea anatomiei epistemice = REUSE.

Majoritatea noutății = coordonare.




---

M. Minimal Missing Organ

După această sinteză, da: rămâne justificat un organ nou, dar este mult mai mic decât părea după Phase I.

Responsabilitatea sa legitimă este numai:

> Să coordoneze transformarea unei întrebări Human într-o călătorie epistemică controlată prin organele existente și să oprească acea călătorie când există suficient material pentru Working Context.



El NU deține:

Knowledge;

Graph;

Canon;

Repository;

Memory;

Evidence;

Provenance;

Experience;

Authority;

CSL;

filesystem.


El nici măcar nu trebuie să fie proprietarul Working Context permanent.

Fiziologic:

Cognitive Coordinator
                     │
        ┌────────────┼─────────────┐
        ▼            ▼             ▼
     resolve       perceive      traverse
        │            │             │
        └────── existing organs ───┘
                     │
                     ▼
                evaluate need
                     │
              ┌──────┴──────┐
              ▼             ▼
           continue         stop
                            │
                            ▼
                      Working Context

De ce nu poate fi absorbit legitim?

Nu în CSL — CSL exprimă semantica, nu conduce reasoning-ul.

Nu în KnowledgeGraph — graph-ul posedă relații, nu decide scopul cercetării.

Nu în RepositoryEngine — repository-ul este un organ perceput, nu coordonatorul întregului organism.

Nu în Provenance — provenance spune de unde provine realitatea recuperată, nu ce trebuie cercetat.

Nu în Memory — Memory păstrează experiență, nu conduce fiecare investigație.

Nu în AIContextBuilder — builder-ul ar trebui să materializeze rezultatul selecției; dacă îl facem și reasoning coordinator, amestecăm percepția cu conștiința.

Nu în AIRequestPipeline — pipeline-ul poate găzdui fiziologia, dar responsabilitatea cognitivă rămâne conceptual distinctă.

Deci organul nou este justificat.

Dar este un coordonator, nu un nou creier epistemic.


---

N. Naming Verdict

După Phase III, termenul Epistemic Navigator este apropiat, dar incomplet.

„Navigator” sugerează în primul rând:

> traversează ceva.



Dar funcția identificată face mai mult:

interpretează nevoia
selectează organul
coordonează resolution
cere percepție
ordonează traversal
respectă authority
evaluează satisfacerea nevoii
decide următorul hop
oprește cercetarea
predă materialul Working Context

Termenul care descrie mai fidel fiziologia este:

Epistemic Coordination

iar organul minimal ar fi conceptual:

Epistemic Cognitive Coordinator

Nu recomand încă fixarea numelui în Canon sau cod. Dar dintre variante, acesta descrie mai exact anatomia decât EpistemicNavigator.

Navigation este una dintre funcțiile sale.

Coordination este responsabilitatea lui.


---

Verdict final Phase III

Am ajuns la o separare arhitecturală mult mai precisă:

CSL
= semantic orientation

Knowledge / Canon / Repository / Evidence / Memory / Experience
= epistemic organs

Existing resolvers
= local identity → manifestation

Existing traversal
= movement inside individual organs

Epistemic Cognitive Coordination
= task-driven movement BETWEEN those organs

Working Context
= temporary epistemic consciousness

Provider model
= reasoning over that temporary consciousness

Iar noua fiziologie completă devine:

ORGANISM KNOWLEDGE
                    effectively very large
                           │
Human                     │
  │                       │
  ▼                       │
Question                   │
  │                        │
  ▼                        │
Permanent Orientation      │
  │                        │
  ▼                        │
Information Need           │
  │                        │
  ▼                        │
Epistemic Coordination ────┘
  │
  ├─ RESOLVE
  ├─ INSPECT
  ├─ TRAVERSE
  ├─ TRACE PROVENANCE
  ├─ evaluate authority
  └─ formulate next need
          │
          ▼
     Need satisfied
          │
          ▼
 Evidence Selection
          │
          ▼
   Working Context
          │
          ▼
 Context Budget Governance
          │
          ▼
       Provider
          │
          ▼
        Answer

Această sinteză păstrează principiul fundamental: nu micșorăm organismul pentru a încăpea în contextul AI. Separăm ceea ce organismul poate cunoaște de ceea ce AI trebuie să aibă în conștiință într-un anumit moment.

Phase III, în opinia mea, poate fi închis aici fără implementare. Următorul pas corect ar fi un Phase IV de Contract & Integration Anatomy, în care definim exact punctele de integrare cu AIRequestPipeline, AIContextBuilder, FUSION-01 și organele existente, plus invariants și acceptance criteria, înainte de orice cod.
