PHASE IV — CONTRACT & INTEGRATION ANATOMY

A. Integration Anatomy Map

Phase IV confirmă că integrarea nu trebuie făcută prin introducerea unui al doilea sistem epistemic. Punctul de inserție este între primirea întrebării și construirea payload-ului final pentru provider.

Fiziologia actuală este:

Human Question
      ↓
AIPlatformService.ask_repository()
      ↓
AIRequestPipeline.run()
      ↓
AIContextBuilder.build()
      ↓
RepositoryEngine.profile()
+ engineering/runtime/workspace/Canon snapshot
      ↓
ProviderAdapter.complete(question, context, model)
      ↓
Answer
      ↓
AISessionEngine.append_interaction()

AIPlatformService construiește AIContextBuilder, AISessionEngine și AIRequestPipeline; ask_repository() trimite promptul în pipeline, iar abia după răspuns persistă interacțiunea. Pentru o sesiune nouă, salvează inclusiv repository_profile și întreg engineering_context.

Contractul țintă trebuie să devină:

Human Question
      ↓
AIPlatformService
      ↓
Permanent Orientation
      ↓
Information Need
      ↓
Epistemic Cognitive Coordination
      │
      ├── semantic orientation: CSL/UEM
      ├── resolve: existing local resolvers
      ├── perceive: Repository / Canon / Memory / Experience
      ├── traverse: Graph / LayeredMemory
      └── authority/provenance: PCC/FUSION
      │
      ↓
Need evaluation
  ┌───┴────┐
  │        │
continue   satisfied / blocked / unknown
  │        │
  └────────┤
           ↓
Working Context
           ↓
Context Budget Governance
           ↓
Provider serialization boundary
           ↓
Provider
           ↓
Answer
           ↓
Session + Journey audit persistence

Punctul exact de integrare: AIRequestPipeline trebuie să înceteze să considere AIContextBuilder.build() drept sursa automată a întregii conștiințe a modelului. Pipeline-ul este locul natural de orchestrare a fazelor, dar nu trebuie să devină el însuși proprietarul Knowledge, Authority sau Resolution.


---

B. Component Responsibility Before/After Matrix

Componentă	Acum	După integrare	Acțiune

AIPlatformService	composition root AI + sessions	composition root; inițiază request-ul cognitiv	CONNECT
AIRequestPipeline	build context → provider	coordonează etapele request-ului și predă Working Context providerului	ADAPT
AIContextBuilder	snapshot masiv pre-reasoning	responsabilități separate de orientation/materialization	ADAPT
Provider adapters	primesc question + context	primesc numai provider-safe cognitive payload	ADAPT
AISessionEngine	conversație, usage, profile/context snapshots	conversație + referințe către journey; nu devine Memory	ADAPT
EpistemicOrganismAccess	read-only runtime state boundary	rămâne boundary FUSION; nu devine automat router	REUSE
CSL/UEM	semantic representation	permanent semantic orientation/resolution input	REUSE
CanonicalRepository	Canon lookup	resolver/perception Canon	REUSE
Knowledge Graph	structural graph	traversal structural selectiv	REUSE
RepositoryEngine	profile/analysis	repository perception selectivă; full profile rămâne diagnostic explicit	REUSE/CONNECT
PCC Provenance	provenance/authority physiology	clasificarea și tracing-ul rezultatelor	REUSE
LayeredMemory	memory navigation	traversal memory	REUSE
Persistent Experience	durable Experience lookup	perception Experience	REUSE


FUSION-01 însuși spune explicit că EpistemicOrganismAccess este „access boundary, not a second organism”, read-oriented și că nu acceptă Sedimentation, nu modifică Canon și nu înlocuiește CSL. Acest contract trebuie păstrat.


---

C. Permanent Orientation Contract

Permanent Orientation trebuie să răspundă numai la:

> Unde sunt, ce sunt, ce există în jurul meu și prin ce mijloace autorizate pot cerceta?



Contractul minim:

ORIENTATION
  organism_identity
  active_project
  active_repository
  active_branch/task identity
  AI role
  Human Authority boundary

  epistemic_classes
    Canon
    Evidence
    Observation
    Repository implementation
    Memory
    Experience
    Conversation
    Runtime state
    Unknown

  available_organs
    semantic model
    Canon
    knowledge graph
    repository
    provenance
    layered memory
    persistent experience
    runtime evidence

  available_capabilities
    SEARCH
    RESOLVE
    READ
    INSPECT
    TRAVERSE
    TRACE_PROVENANCE

  high-level semantic relationships

Nu include implicit:

RepositoryProfile, toate fișierele, Canon integral, Memory integral, reports integrale, graph integral sau conversation history integral.

CSL/UEM poate constitui baza semantică, dar orientation nu trebuie atribuită exclusiv CSL. Runtime position și Human Authority provin din alte organe.

FUSION-01 demonstrează deja explicit limite precum runtime_may_mutate_canon=False, runtime_may_replace_csl=False și lipsa acceptării automate a sedimentării.


---

D. Information Need Contract

Information Need trebuie să exprime ce lipsește din cunoașterea necesară taskului, nu unde presupunem că se află.

Forma conceptuală minimă:

need_id
goal
semantic_target
desired_epistemic_domain
reason
status
parent_need

Exemplu:

goal:
  Explain Owner AI Chat token 429.

semantic_target:
  AI request physiology.

desired_epistemic_domain:
  current implementation.

reason:
  Need causal path from Human request to provider payload.

status:
  OPEN.

Interzis contractual:

semantic_target =
"open lib/python/ai_platform/pipeline.py lines 20-50"

Acesta este deja un rezultat de Resolution, nu un Information Need.

Need poate deveni:

SATISFIED, PARTIAL, UNKNOWN, BLOCKED, HUMAN_REQUIRED.

UNKNOWN este rezultat legitim.


---

E. Epistemic Result Envelope Verdict

Verdict: este necesar un contract transversal minimal nou, dar nu o nouă clasă epistemică.

PCC Provenance are deja o taxonomie mult mai bogată decât actualele obiecte AI: Source → Observation → Evidence → Claim → Verification → Knowledge → Current State, inclusiv surse HUMAN, AI, CANON, REPOSITORY, RUNTIME, TEST etc.

Dar nici UEM, nici Evidence, nici KnowledgeGraph node nu reprezintă singure în mod legitim rezultatele tuturor organelor.

Envelope-ul nu trebuie să reclasifice obiectul. El este doar transport epistemic:

result_identity
epistemic_class
semantic_identity
source
provenance
authority
retrieval_reason
retrieved_via
manifestation_reference
freshness/status
bounded_content

Dacă un rezultat este OBSERVATION, rămâne Observation.

Dacă este CANON, rămâne Canon.

Dacă este MEMORY, retrieval-ul nu îl transformă în Evidence.

Dacă este CONVERSATION, nu devine automat Knowledge.

Aceasta este una dintre cele mai importante frontiere ale arhitecturii.


---

F. Capability Contracts

Cele șase capabilități sunt intenții epistemice, nu filesystem tools.

Capability	Intrare semantică	Rol

SEARCH	concept/need/domain	descoperă identități candidate
RESOLVE	semantic identity	găsește manifestarea curentă
READ	identity deja rezolvată	recuperează reprezentarea autorizată
INSPECT	semantic target + aspect	produce observație structurată
TRAVERSE	identity + relationship intent	urmărește relații prin organul proprietar
TRACE_PROVENANCE	result/evidence identity	urmărește proveniența


Fiecare trebuie să aibă cinci garanții:

semantic input — caller-ul nu trebuie să cunoască path-ul fizic;

eligible-organ constraint — capability routing numai către organe autorizate;

authority check — retrieval-ul nu poate depăși boundary-ul;

bounded output — organul nu poate răspunde implicit cu întregul său corp;

provenance preservation — rezultatul nu poate fi desprins de origine.

Failure-ul trebuie să producă o stare explicită, nu informație inventată.


---

G. Federated Resolution Contract

Nu este justificat un mega-index.

Contractul trebuie să fie:

semantic identity
      ↓
domain discrimination
      ↓
eligible existing resolver(s)
      ↓
delegation
      ↓
resolution result

Domenii demonstrate:

CSL/UEM
Canon
Knowledge Graph
Repository
Layered Memory
Persistent Experience
Provenance

Rezultatul trebuie să permită cel puțin:

RESOLVED

UNRESOLVED

AMBIGUOUS

iar FORBIDDEN trebuie folosit când authority boundary refuză accesul.

STALE este legitim numai când resolverul poate demonstra că manifestarea rezolvată nu mai corespunde identității/current state; nu trebuie inventat universal doar pentru uniformitate.

Foarte important:

> Resolver federation deține routing, nu adevărul.



Resolverul Canon continuă să fie Canon resolver. Experience resolver continuă să fie Experience resolver.


---

H. Cognitive State Machine

State machine-ul minim derivat din anatomie este:

RECEIVE
   ↓
ORIENT
   ↓
FORM_NEED
   ↓
SELECT
   ↓
RESOLVE
   ↓
PERCEIVE / TRAVERSE
   ↓
EVALUATE
   ├──────── SATISFIED
   │              ↓
   │        ASSEMBLE_CONTEXT
   │
   ├──────── CONTINUE → FORM_NEXT_NEED
   │
   ├──────── UNKNOWN
   │
   ├──────── BLOCKED
   │
   └──────── HUMAN_REQUIRED

Invariants de transition

SELECT nu poate inventa un organ.

RESOLVE nu conferă authority.

PERCEIVE este read-only.

EVALUATE nu poate transforma lipsa Evidence în certitudine.

CONTINUE necesită un nou epistemic gain anticipat.

SATISFIED necesită material suficient pentru scop, nu exhaustivitate universală.

Cycle detection

Journey trebuie să păstreze cel puțin:

(need, semantic_identity, capability)

inspectate.

Repetarea fără informație nouă produce NO_EPISTEMIC_GAIN, nu un nou loop.

Contradicție

Contradictory Evidence nu produce automat SATISFIED.

Poate produce:

PARTIAL, UNKNOWN sau HUMAN_REQUIRED.


---

I. Working Context Contract

Journey State și Working Context sunt două obiecte conceptual diferite.

Journey State

Poate conține:

toate needs;

toate hops;

results/references;

rejected results;

resolution failures;

cycles;

stop reasons;

intermediate reasoning metadata.


Poate deveni mare.

Working Context

Trebuie să conțină numai:

question
permanent_orientation subset required by provider
resolved objective

selected observations/evidence
semantic identities
relevant relationships
provenance references
authority classifications
uncertainties/contradictions
Human constraints
compact journey outcome

Working Context este:

temporary

bounded

provider-facing

reconstructible from Journey + organism where possible.

Nu trebuie să conțină întreg Journey-ul.


---

J. Context Budget Contract

Repository-ul demonstrează deja că provider metadata conține limite pe model: ProviderDescriptor.token_limit, iar ProviderRegistry.list_providers() expune token_limits per model.

Prin urmare bugetul nu trebuie hardcodat în AIContextBuilder.

Contractul trebuie derivat conceptual din:

selected provider
+ selected model
+ demonstrated provider/model limits
- provider/system instructions
- Permanent Orientation
- Human Question
- reserved answer capacity
- safety margin
=
maximum Working Context materialization budget

Invariant:

serialized provider payload <= provider-safe request budget

Budget governance poate:

deduplica;

înlocui raw intermediate results cu references;

compacta semantic;

elimina rezultate obsolete;

păstra contradicțiile relevante;

folosi provenance-preserving summaries.


Nu poate:

șterge Knowledge din organism;

ascunde Evidence contrară doar pentru a încăpea;

reclasifica informația;

falsifica certainty.


Adapter-ele existente declară limite de 8K până la 1M în catalog, în funcție de provider/model, ceea ce confirmă că budget-ul trebuie să fie provider/model-aware.


---

K. Provider/Organism/Human Decision Matrix

Decizie	AI Model	Organism	Human

interpretează întrebarea	✓ principal	constrângeri	poate corecta
propune Information Need	✓	validează	poate direcționa
alege capability semantică	✓ poate propune	autorizează	—
resolve identity	—	✓	poate dezambigua
citește organul	—	✓	—
urmărește provenance	poate solicita	✓	—
determină authority existentă	nu	✓	authority finală unde contractul cere
decide următorul research need	✓	verifică boundaries	poate interveni
modifică Canon	✗	✗ prin navigation	numai prin authority workflow
acceptă Sedimentation	✗	✗ automat	Human Authority
construiește bounded payload	poate ajuta la selection	✓ controlează	—
răspunde semantic	✓	furnizează contextul	—
promovează răspunsul la truth	✗	✗ automat	authority workflow


FUSION-01 confirmă deja că runtime-ul nu poate accepta Sedimentation și nu poate modifica Canon/CSL.


---

L. Side-Effect Boundary

Toată fiziologia Phase IV este contractual READ-ONLY.

Acestea:

SEARCH
RESOLVE
READ
INSPECT
TRAVERSE
TRACE_PROVENANCE

nu pot produce:

Canon mutation
Evidence acceptance
Memory sedimentation
repository write
commit
deployment
runtime config mutation
provider configuration mutation
execution

Dacă reasoning-ul ajunge la:

> „Trebuie modificat X”



Journey se termină cu un action proposal, nu execută acțiunea.

Acțiunea trebuie să traverseze un authority/execution contract separat.

Această frontieră este deja compatibilă cu FUSION-01, care se declară explicit READ_ONLY_RUNTIME_OBSERVATION.


---

M. Failure Physiology

Failure	Comportament contractual

resolver failure	păstrează Journey; poate încerca alt resolver eligibil
organ unavailable	BLOCKED/UNKNOWN; nu inventează rezultat
stale identity	re-resolution; dacă persistă → UNKNOWN
ambiguous identity	dezambiguare semantică; Human dacă nu poate fi rezolvată sigur
missing Evidence	UNKNOWN/PARTIAL
contradictory Evidence	păstrează ambele; continuă numai dacă există need legitim
traversal cycle	stop branch; audit cycle
repeated result	stop branch dacă nu există epistemic gain
budget exhaustion	compactează Working Context; nu șterge organism knowledge
provider failure	Journey rămâne intact
provider 429	request failure explicit; fără truth fallback
runtime restart	Journey resumabil dacă persistence contract a fost atins
Human Authority required	HUMAN_REQUIRED
capability forbidden	FORBIDDEN; fail closed


Provider fallback

Un punct critic descoperit în implementare: actualele builtin adapters sunt StaticProviderAdapter; complete() generează local un răspuns sintetic din RepositoryProfile și estimează tokens cu len(str(context)) // 20.

Contractul Phase IV trebuie să interzică explicit:

> provider real failure → silent static/synthetic answer presented as if it came from the requested provider.



Static provider poate exista ca provider explicit de test, nu ca substituție epistemic invizibilă.


---

N. Persistence Contract

Trebuie separate patru durate de viață.

Permanent Orientation — în principal reconstructibilă; nu trebuie salvată integral la fiecare mesaj.

Journey — trebuie să poată supraviețui provider failure și, pentru journey semnificativ, restartului.

Working Context — poate fi efemer; este derivat.

Answer/conversation — rămâne responsabilitatea sesiunii.

AISessionEngine are deja persistence JSON pentru sessions, conversation history, token usage și engineering context.

Dar el nu trebuie transformat în Persistent Experience.

Contractul recomandat este:

AISession
  references Journey identity

Journey persistence
  preserves:
    needs
    resolved identities
    provenance references
    statuses
    stop/failure state

Working Context
  may be reconstructed

Resolved manifestations trebuie considerate potențial stale după restart și revalidate/re-resolve când este necesar.

Journey nu devine automat Experience.

Journey failure nu devine automat Error Memory.


---

O. Invariants

Cele zece invariants propuse sunt validate arhitectural.

I-01 — Knowledge Availability ≠ Working Context

NEW explicit invariant, dar derivat direct din fiziologia necesară.

I-02 — Retrieval Does Not Confer Authority

ALREADY PRESENT IN PRINCIPLE.

Persistent Experience/FUSION separă persistence/existence de authority, iar FUSION păstrează Human Authority.

I-03 — Semantic Identity ≠ Physical Location

DERIVABLE / needs explicit integration invariant.

Resolvers locali deja separă parțial identity de manifestation.

I-04 — Provider Cannot Bypass Organism Mediation

NEW integration invariant.

I-05 — Navigation Is Read-Only

ALREADY PRESENT at FUSION boundary, trebuie extins la cognitive journey.

I-06 — Provenance Survives Retrieval

ALREADY PRESENT conceptually in PCC, dar nou ca cross-organ transport invariant.

I-07 — UNKNOWN Is Valid

ALREADY PRESENT strongly in FUSION.

FUSION folosește deliberat UNKNOWN când persistence/service state nu poate fi demonstrată și refuză să inventeze ErrorMemory service.

I-08 — Context Budget Does Not Delete Organism Knowledge

NEW explicit invariant.

I-09 — Human Authority Cannot Be Promoted or Replaced by AI

ALREADY PRESENT.

I-10 — Full Repository Profile Is Not Default Cognitive Payload

NEW integration invariant, necesar pentru corectarea actualei fiziologii.

Aș adăuga doar un invariant derivat inevitabil:

I-11 — Epistemic Class Survives Transport

Conversation, Memory, Evidence, Canon etc. nu își schimbă clasa doar fiindcă au intrat în Journey sau Working Context.

Nu este o extindere CSL; este o consecință a I-02/I-06.


---

P. 429 Acceptance Architecture

Problema 429 devine primul acceptance scenario end-to-end.

Scenario 1 — hi

Trebuie demonstrat:

Human: hi
↓
small Permanent Orientation
↓
no need for repository-wide investigation
↓
bounded Working Context
↓
provider

Acceptance:

1. RepositoryEngine.profile() complet nu este materializat implicit.


2. RepositoryProfile complet nu apare în provider payload.


3. payload size este măsurată.


4. provider/model budget este cunoscut înainte de request.


5. Human Authority rămâne prezentă.



Scenario 2 — „Why does Owner AI Chat receive OpenAI 429?”

Journey minim demonstrabil:

N1 request physiology
→ resolve AIPlatformService

N2 downstream request path
→ AIRequestPipeline

N3 context materialization
→ AIContextBuilder

N4 repository contribution
→ RepositoryEngine.profile()
→ RepositoryProfileSerializer

N5 provider/request Evidence
→ runtime/provider Evidence

N6 causal sufficiency evaluation
→ SATISFIED / UNKNOWN

Actualul AIPlatformService.ask_repository() demonstrează service → pipeline și salvează contextul/session după request.

Actualul adapter contract primește direct question, context, model; deci provider serialization boundary poate fi localizată precis înaintea complete().

Acceptance obligatoriu:

1. Permanent Orientation bounded.


2. Full RepositoryProfile absent implicit.


3. selective retrieval demonstrat.


4. cel puțin un multi-step Journey real.


5. provenance păstrată.


6. authority păstrată.


7. Working Context măsurat.


8. provider payload sub safe budget.


9. Journey auditabil.


10. provider failure nu generează epistemic fallback fals.


11. static provider nu substituie silent providerul real.


12. Human Authority intactă.


13. UNKNOWN produce răspuns epistemic corect când provider Evidence lipsește.


14. rezultatul trebuie să demonstreze cauza 429 din Evidence, nu doar s-o deducă din existența unui context mare.



Cifrele istorice ~295 KB rămân baseline Evidence pentru comparație, nu un nou contract numeric.


---

Q. Exact Existing Components To Reuse

Trebuie reutilizate, nu recreate:

CslLexer / CslParser / SemanticAnalyzer / UEM — semantic orientation.

CanonicalRepository — Canon resolution.

KnowledgeMaterializationEngine / CanonicalKnowledgeGraph — structural knowledge representation.

Dependency/Traceability graphs — relation traversal.

RepositoryEngine — repository perception.

RepositoryProfileSerializer — legitim când full profile este solicitat explicit; nu default context.

PCC Provenance — provenance/authority traversal.

LayeredMemory / LayeredMemoryRepository — memory traversal.

JsonFileExperienceRepository — Experience resolution/persistence.

Sedimentation authority — Human Authority boundaries.

ProviderRegistry — provider capabilities/token-limit discovery.

AISessionEngine — conversation/session persistence.

FUSION EpistemicOrganismAccess — existing runtime-facing observation boundary, fără extinderea artificială a responsabilității sale.


---

R. Exact Components Requiring Adaptation

AIRequestPipeline

Este principala integrare.

Astăzi:

build giant context
→ select provider/model
→ adapter.complete()

Trebuie să poată găzdui:

orientation
→ journey
→ working-context assembly
→ budget validation
→ provider

fără să devină proprietarul organelor.

AIContextBuilder

Necesită cea mai mare corecție de responsabilitate.

Verdictul Phase IV este C — responsabilitatea actuală trebuie separată conceptual în două:

1. Permanent Orientation assembly;


2. Working Context assembly/materialization.



Nu recomand menținerea unui singur build() semantic care poate însemna ambele.

RepositoryEngine.profile() → full serialization rămâne disponibil pentru:

explicit repository audit;

dashboard/diagnostic;

explicit full-profile request;

offline analysis unde bugetul nu este provider context.


Nu mai este legitim ca default cognitive payload.

Provider adapters

Trebuie să expună suficient provider/model budget information și să primească payload-ul final, nu organism knowledge.

Catalogul actual deja deține token_limit, capabilities și model metadata.

AISessionEngine

Trebuie conectat la Journey identity/status fără să salveze automat sute de KB de engineering snapshot per session.

În prezent schema sa include explicit repository_profile și engineering_context; aceasta trebuie reevaluată la integrare.

AIPlatformService

Adaptare mică: composition/wiring, nu cognitive logic.


---

S. Minimal New Contracts/Components

După eliminarea duplicărilor, anatomia realmente nouă se reduce la șase contracte funcționale.

1. Permanent Orientation contract
Asamblează harta cognitivă minimală.

2. Information Need contract
Reprezintă ce trebuie cunoscut.

3. Epistemic Result Envelope
Transportă rezultate cross-organ fără pierdere de clasă/provenance/authority.

4. Federated Resolution coordination
Alege resolverul existent potrivit; nu păstrează un mega-index.

5. Epistemic Cognitive Coordination
Conduce Need → capability → result → evaluation → next Need/stop.

6. Working Context + Budget contract
Selectează și materializează conștiința temporară sub provider-safe budget.

Journey Audit/Persistence este necesar, dar nu justifică încă un nou sistem de memorie; trebuie construit peste infrastructura existentă de persistence/session/provenance unde responsabilitățile permit.

Niciunul dintre aceste contracte nu justifică:

CSL v3

un nou Knowledge Graph;

un nou Repository Engine;

un nou Memory;

un nou Evidence system;

un nou Canon registry.


---

T. Implementation Dependency Order

Implementarea ulterioară nu trebuie făcută ca big-bang rewrite. Ordinea corectă rezultată din dependențe este:

T1 — Characterization baseline. Îngheață prin teste comportamentul actual: dimensiunea contextului, contribuția repository_profile, request path, session persistence, provider selection și 429 evidence. Nicio schimbare funcțională.

T2 — Provider Budget Introspection. Formalizează citirea limitelor deja existente în ProviderDescriptor/ProviderRegistry, fără schimbarea request pipeline. Acest strat poate fi validat independent.

T3 — Permanent Orientation. Construiește numai orientarea bounded și măsoară dimensiunea. Nu scoate încă legacy context din producție. Acceptance: orientation independentă de RepositoryProfile size.

T4 — Epistemic Result Envelope. Leagă fără reclasificare câteva rezultate existente: Repository observation, Canon, Provenance/Memory. Acceptance: identity/class/source/provenance/authority supraviețuiesc round-trip-ului.

T5 — Federated Resolution. Conectează resolverii existenți incremental. Începe cu două domenii demonstrabile, nu cu toate simultan. Acceptance: semantic identity → correct organ → manifestation, inclusiv UNRESOLVED/AMBIGUOUS.

T6 — Read-only Capability Mediation. Introdu SEARCH/RESOLVE/READ/INSPECT/TRAVERSE/TRACE_PROVENANCE ca intents mediate. Acceptance obligatoriu: nicio cale de write.

T7 — Information Need + Journey State. Introdu reprezentarea need-ului și audit trail fără provider reasoning loop. Poate fi testată determinist.

T8 — Cognitive Loop. Conectează model reasoning la Need/Capability mediation cu stop conditions, UNKNOWN, cycle/repeat detection și authority stops. Acesta este primul punct unde apare cercetarea iterativă reală.

T9 — Working Context Assembly. Din Journey selectează numai rezultatele relevante. Acceptance: Journey poate fi mai mare decât Working Context fără pierderea provenance references.

T10 — Context Budget Governance. Aplică provider/model-aware budget, headroom și compaction înainte de serialization. Acceptance: imposibilitatea de a trimite accidental payload peste safe budget.

T11 — Pipeline Integration în shadow mode. AIRequestPipeline construiește atât legacy context, cât și noul Working Context, dar providerul poate continua temporar pe legacy path. Comparăm semantic output, size și provenance fără risc de schimbare bruscă.

T12 — hi cutover. Pentru requesturi triviale, elimină full RepositoryProfile din provider payload. Acesta este cel mai mic production proof.

T13 — 429 research cutover. Activează multi-hop Journey pentru scenariul real AIPlatformService → Pipeline → ContextBuilder → RepositoryProfile → provider Evidence.

T14 — Session integration. AISessionEngine păstrează conversation + Journey references/status, iar legacy giant snapshots sunt retrase numai după demonstrarea compatibilității/recovery. Astăzi el salvează direct repository_profile și engineering_context, deci migrarea trebuie făcută controlat.

T15 — Failure/restart validation. Provider 429, provider unavailable, ambiguous resolution, missing Evidence, runtime restart, Journey resume, UNKNOWN și HUMAN_REQUIRED.

T16 — Legacy context retirement. Abia după toate acceptance-urile anterioare, AIContextBuilder.build() încetează să fie default pre-request snapshot pentru Owner AI Chat. Full RepositoryProfile rămâne capabilitate explicită a organismului.


---

Phase IV produce astfel un contract suficient de precis pentru a împiedica implementarea să alunece într-un „RAG chatbot”.

Punctul arhitectural decisiv este:

> AI-ul nu primește memoria organismului. Primește orientarea necesară pentru a ști că memoria există, cercetează prin capabilități controlate, iar organismul îi materializează temporar numai țesutul epistemic necesar raționamentului curent.



În forma contractuală finală:

Epistemic access
        =
potentially much larger than model context

Working consciousness
        =
strictly bounded

Authority
        =
remains in the organism/Human

Provider
        =
reasoning participant, never epistemic sovereign

Iar cea mai importantă constatare pentru implementare este că prima intervenție nu trebuie să fie CSL. Cea mai mare parte a lucrării este CONNECT și ADAPT în jurul fiziologiei AI existente, în timp ce CSL/UEM, Repository, Knowledge Graph, Provenance, Memory și Experience rămân organele lor native.
