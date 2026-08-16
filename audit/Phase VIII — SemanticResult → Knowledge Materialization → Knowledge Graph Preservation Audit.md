Phase VIII — SemanticResult → Knowledge Materialization → Knowledge Graph Preservation Audit

Am urmărit direct în main frontiera pe care Phase VII a lăsat-o deschisă. Rezultatul schimbă puțin anatomia pe care o credeam: UEM există explicit, dar KnowledgeMaterializationEngine nu consumă UEM și nici SemanticResult. Sunt două căi epistemice paralele.

1. Descoperirea principală: UEM există

În canonical_entities/uem.py există explicit:

SemanticResult[]
      ↓
UemBuilder
      ↓
UniversalEngineeringModel
      ├── EngObject[]
      └── EngRelationship[]

UemBuilder.build() primește chiar semantic_results, deci aceasta este legătura directă pe care Phase VII nu o demonstrase încă.

UEM este mult mai bogat semantic decât CslCompileResult. EngObject poate păstra identity, type, name, version, status, purpose, visibility, source document, source reference, arbitrary properties și ast_ref; relațiile păstrează tip, confidence, metadata și source reference.

Deci traseul CSL real confirmat este:

CSL Source
   ↓
AST
   ↓
SemanticResult
   ↓
UemBuilder
   ↓
UniversalEngineeringModel

Acesta este un rezultat important: pentru Permanent Orientation, UEM este candidatul semantic mult mai natural decât CslCompileResult.


---

2. SemanticResult → UEM: conservare foarte bună, dar nu completă

Pentru document, builderul creează:

EngObject
  obj_id          ← result.doc_id
  obj_type        ← DOCUMENT
  name            ← result.title
  version         ← result.version
  status          ← result.status
  source_ref      ← result.source_path
  classification  ← properties

Classification, despre care Phase VII arăta că este pierdută de CslCompileResult, supraviețuiește în UEM.

Prin urmare trebuie corectată interpretarea:

SemanticResult → CslCompileResult
Classification = LOST

SemanticResult → UEM
Classification = PRESERVED

Asta demonstrează de ce compile() nu trebuie confundat cu modelul epistemic final.


---

3. Entitățile sunt conservate foarte bine în UEM

Pentru fiecare result.entities, UEM păstrează:

identifier   → obj_id
entity_type  → obj_type
name         → name
version      → version
status       → status
visibility   → visibility
properties   → properties
source_path  → source_ref

și adaugă automat relația:

DOCUMENT ──CONTAINS──> ENTITY

Așadar properties arbitrare din CSL nu sunt amputate aici.

Asta este foarte important pentru Legend/metasemantică.

Dacă o proprietate semantică ajunge în SemanticResult.entities[*].properties, UEM o poate transporta mai departe fără să fie necesară o coloană specială pentru fiecare concept.


---

4. Dar type fidelity nu este perfectă

UEM posedă un vocabular explicit EngObjectType, incluzând:

PROJECT, CAPABILITY, FEATURE, REQUIREMENT, DECISION, CONSTRAINT, POLICY, RULE, RISK, ISSUE, EPIC, MILESTONE, TASK, COMPONENT, MODULE, SERVICE, API, ENTITY, GENERATOR, VALIDATOR, COMPILER, RUNTIME, KNOWLEDGE, DOCUMENT.

Dar pentru un CSL entity type necunoscut:

else EngObjectType.ENTITY

Deci:

CSL:
Organ:
Brain

SemanticResult:
entity_type = Organ

UEM:
obj_type = ENTITY

Originalul nu dispare complet, pentru că properties supraviețuiește, dar tipul semantic primar este generalizat.

Verdict

TYPE NORMALIZATION / SEMANTIC GRANULARITY LOSS — HIGH

Pentru un organism epistemic extensibil, această frontieră contează.


---

5. Relațiile suferă aceeași normalizare

UEM cunoaște un set finit de EngRelationType:

IMPLEMENTS
CONTAINS
DEPENDS_ON
EXTENDS
REFERENCES
REQUIRES
OWNS
APPROVES
TESTS
VALIDATES
GENERATES
DEPLOYS
PUBLISHES
CONSUMES
SUPPORTS
BELONGS_TO

Dacă CSL produce altă relație:

NOURISHES
REGULATES
INHIBITS
COORDINATES
...

builderul execută:

else EngRelationType.REFERENCES

Prin urmare:

A ──REGULATES──> B
          ↓
A ──REFERENCES──> B

Metadata relației este păstrată, dar semantica verbului original nu este pusă automat în metadata.

Asta înseamnă pierdere reală.

Verdict

UNKNOWN RELATION COLLAPSE — CRITICAL pentru extensibilitatea CSL/UEM.


---

6. Semantic annotations dispar

Phase VII identificase SemanticResult.annotations.

UemBuilder nu le citește deloc.

Așadar traseul este:

SemanticResult.annotations
        ↓
     UemBuilder
        ↓
       ∅

Inclusiv infrastructura latentă:

canonical_refs
semantic_type
annotation properties

nu este transferată în UEM.

Verdict

CONFIRMED SEMANTIC LOSS — HIGH

Aici avem acum o frontieră exactă de pierdere.


---

7. Provenance rămâne grosieră

UEM are infrastructură bună:

source_document
source_ref
ast_ref

Dar builderul pune pentru fiecare entitate:

source_document = result.doc_id
source_ref      = result.source_path
ast_ref         = entity.identifier

ast_ref nu este un pointer real către AST; este doar identifier-ul entității.

Deci informația exactă:

file.csl
line 141
column 9
AST node XYZ

nu reapare.

Verdict

PROVENANCE INFRASTRUCTURE EXISTS, BUT IS UNDERFED.

Aceasta este o temă recurentă: modelul țintă este adesea mai capabil decât transformatorul care îl alimentează.


---

8. Acum descoperirea critică: KnowledgeMaterialization nu consumă SemanticResult/UEM

KnowledgeMaterializationEngine.materialize() declară explicit inputurile:

cdm_docs
css_standards

nu:

SemanticResult
UEM
CSL

și documentația internă spune că acceptă output-ul CDM Engine și CSS Engine.

Mai mult, metoda convenience:

materialize_from_standards_root()

încarcă fișiere .md folosind:

CdmEngine
CSSEngine

și apoi cheamă:

materialize(cdm_docs, css_records)

Prin urmare anatomia actuală NU este:

CSL → SemanticResult → UEM → KnowledgeMaterialization → KG

ci cel puțin două circulații separate:

CIRCULATION A

CSL
 ↓
AST
 ↓
SemanticResult
 ↓
UEM

și:

CIRCULATION B

Markdown Canon
 ↓
CDM / CSS
 ↓
KnowledgeMaterializationEngine
 ↓
MaterializedKnowledge
 ↓
CanonicalKnowledgeGraph

Aceasta este descoperirea majoră a Phase VIII.

Organismul are două sisteme epistemice care nu sunt încă demonstrate ca fiind unite.


---

9. Ce materializează efectiv KnowledgeMaterializationEngine

Pentru CDM document creează un KnowledgeObject cu:

id
kind=document
name
source
version
status
metadata:
    classification
    owner
    standard_family
    section_count
    dependency_count
    traceability_count

Apoi creează CanonicalNode pentru document.

Dar aici apare o nouă reducere:

în KnowledgeObject.metadata, classification și alte informații sunt păstrate.

În CanonicalNode.metadata, documentul primește numai:

status

Deci chiar în interiorul aceluiași MaterializedKnowledge:

KnowledgeObject
   classification ✓
   owner ✓
   standard_family ✓

          ↓ graph representation

CanonicalNode
   status ✓
   classification ✗
   owner ✗
   standard_family ✗

Verdict

KNOWLEDGE OBJECT → GRAPH NODE METADATA LOSS — HIGH


---

10. Sections: structură conservată, conținut pierdut

Materializerul creează noduri pentru secțiuni:

DOCUMENT ──CONTAINS──> SECTION

și păstrează:

section.title
section.level
document path
document version

Dar nu materializează textul/conținutul secțiunii în CanonicalNode.

Modelul CanonicalSection din infrastructura graph poate avea content, dar CanonicalNode nu are un câmp dedicat pentru acesta.

Deci Knowledge Graph este mai degrabă:

> index semantic structural



decât:

> memorie semantică completă a canonului.



Această distincție trebuie păstrată.


---

11. Dependency și traceability sunt bine conservate structural

Materializerul construiește:

DEPENDS_ON
REFERENCES { relation: TRACES }

și creează placeholder nodes pentru ținte care nu există încă în graph.

Aceasta este o proprietate sănătoasă.

În loc să arunce relația pentru că target-ul lipsește, sistemul conservă topologia epistemică:

KNOWN NODE
    │
    └── DEPENDS_ON
            ↓
       PLACEHOLDER

Pentru navigare aceasta este foarte valoroasă.

Verdict

RELATIONAL TOPOLOGY: STRONGLY PRESERVED pentru CDM/CSS path.


---

12. KnowledgeRelationship are un defect de serializare

Modelul posedă:

source_id
target_id
relation
confidence
metadata

dar KnowledgeRelationship.to_dict() returnează doar:

source_id
target_id
relation
confidence

metadata este omis.

Așadar:

runtime object
metadata ✓

JSON export
metadata ✗

Verdict

SERIALIZATION-BOUNDARY LOSS — CONFIRMED

Acesta este exact tipul de pierdere care poate rămâne invizibil în runtime și reapărea după restart/export-import.


---

13. CanonicalKnowledgeGraph în sine este relativ sănătos

CanonicalKnowledgeGraph.to_dict() păstrează pentru nodes:

id
node_type
name
source_document
version
metadata
provenance

și pentru edges:

source_id
target_id
edge_type
confidence
metadata

Iar from_dict() reconstruiește aceleași câmpuri.

Deci aici avem o veste bună:

> Graph serialization este aproape simetrică.



Pierderile majore se produc înainte ca informația să intre în graph, nu în CanonicalKnowledgeGraph.to_dict()/from_dict().


---

14. Dar există încă un al treilea „Knowledge Graph”

Repository-ul are și:

knowledge_graph_v2

Acesta nu consumă nici UEM, nici CanonicalKnowledgeGraph.

El scanează fișiere Python cu ast.parse() și construiește:

nodes = Python file paths

edges =
    import
    from_import

Deci avem cel puțin trei reprezentări distincte:

UniversalEngineeringModel
        │
        │ engineering semantics
        ▼
   EngObjects / EngRelationships


CanonicalKnowledgeGraph
        │
        │ canonical-document semantics
        ▼
 CanonicalNodes / CanonicalEdges


KnowledgeGraph V2
        │
        │ implementation/import semantics
        ▼
 Python files / imports

Acestea nu trebuie confundate.

De fapt, ele descriu trei sisteme anatomice diferite ale aceluiași organism.


---

15. Preservation Matrix — Phase VIII

Semantică	SemanticResult→UEM	CDM/CSS→MaterializedKnowledge	KnowledgeObject→KG	Verdict

Identity	✓	✓	✓	GOOD
Name/title	✓	✓	✓	GOOD
Version	✓	✓	✓	GOOD
Status	✓	✓	✓	GOOD
Classification	✓	✓	✗ graph	PARTIAL LOSS
Entity properties	✓	n/a	limited metadata	PATH-DEPENDENT
Visibility	✓	n/a	absent	UEM ONLY
Entity type	normalized	n/a	fixed NodeType	PARTIAL
Unknown entity type	→ ENTITY	n/a	—	LOSS
Known relationships	✓	✓	✓	GOOD
Unknown CSL relation	→ REFERENCES	—	—	LOSS
Relationship metadata	✓	runtime ✓	graph ✓	GOOD
KnowledgeRelationship metadata export	—	✗	—	LOSS
Semantic annotations	✗	—	—	LOSS
canonical_refs	✗	—	—	LOSS
Exact source location	✗	✗	✗	LOSS
Document provenance	✓	✓	✓	GOOD
Sections	inherited loss from SemanticResult	✓	✓ structure	PARTIAL
Section content	—	available upstream	✗ graph	LOSS
Dependencies	relationship-dependent	✓	✓	GOOD
Traceability	relationship-dependent	✓	✓	GOOD
Missing targets	—	placeholders	placeholders	GOOD



---

16. Ce înseamnă asta pentru „harta organismului”

Acum putem formula mult mai exact problema.

Nu avem încă o singură hartă:

ORGANISM
  ↓
one semantic model
  ↓
one navigable graph

Avem mai degrabă:

AI-TOOLKIT

        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
      CSL            CDM/CSS       Python code
        │              │              │
        ▼              ▼              ▼
 SemanticResult    Materializer    AST scanner
        │              │              │
        ▼              ▼              ▼
       UEM       Canonical KG       KG V2

Aceasta este probabil una dintre cele mai importante descoperiri din cercetarea noastră.

Problema nu este doar semantic loss. Problema este semantic fragmentation.


---

17. UEM este candidatul natural pentru integrare

Comparând modelele, UEM este semantic cel mai general.

EngObjectType acoperă concepte de produs, planning, governance, software și knowledge; EngRelationship acoperă relații operaționale; objects au arbitrary properties, provenance și visibility.

CanonicalKnowledgeGraph, în schimb, folosește NodeType mult mai orientat către arhitectură/software: DOCUMENT, SECTION, MODULE, COMPONENT, ENGINE, SERVICE, INTERFACE, PIPELINE etc.

Așadar arhitectural apare o direcție puternică:

UEM
              │
      universal semantic body
              │
     ┌────────┼────────┐
     ▼        ▼        ▼
Canonical   Code     Epistemic
 Graph      Graph    Navigation

Nu declar încă aceasta drept soluția finală — auditul nu trebuie transformat prematur în implementation plan — dar codul actual oferă dovezi serioase că UEM a fost conceput tocmai pentru rolul de model semantic universal.


---

18. Severity Register Phase VIII

ID	Finding	Severity

VIII-01	UEM exists but is disconnected from KnowledgeMaterialization	CRITICAL architectural fragmentation
VIII-02	Unknown CSL object types collapse to ENTITY	HIGH
VIII-03	Unknown CSL relations collapse to REFERENCES	CRITICAL semantic loss
VIII-04	Semantic annotations discarded by UemBuilder	HIGH
VIII-05	canonical_refs discarded	HIGH
VIII-06	precise provenance unavailable to UEM	HIGH
VIII-07	ast_ref is identifier, not actual AST reference	MEDIUM/HIGH
VIII-08	KnowledgeObject rich metadata reduced in CanonicalNode	HIGH
VIII-09	section content absent from graph	MEDIUM/HIGH
VIII-10	KnowledgeRelationship metadata lost on serialization	HIGH
VIII-11	multiple independent knowledge representations exist	CRITICAL architectural fragmentation
VIII-12	KG V2 represents code imports, not canonical epistemic semantics	informational but architecturally important



---

19. Combined Phase VII + VIII anatomy

Acum putem vedea întreaga fiziologie confirmată:

CSL SOURCE
   │
   ▼
 Lexer
   │
   ▼
 Parser
   │
   ▼
 AST
   │
   │  LOSS #1:
   │  nested entities / hierarchy
   ▼
 SemanticResult
   │
   ├───────────────► CslCompileResult
   │                   LOSS:
   │                   classification
   │                   annotations
   │                   provenance
   │
   ▼
 UemBuilder
   │
   │ LOSS:
   │ annotations
   │ canonical_refs
   │ unknown type specificity
   │ unknown relation specificity
   ▼
 UEM

În paralel:

CANONICAL MARKDOWN
      │
   CDM / CSS
      │
      ▼
KnowledgeMaterialization
      │
      ├── KnowledgeObjects
      ├── KnowledgeRelationships
      ├── Dependency Graph
      ├── Traceability Graph
      │
      ▼
CanonicalKnowledgeGraph

Și separat:

PYTHON SOURCE
     ↓
Python AST
     ↓
KnowledgeGraph V2
     ↓
file/import topology


---

Phase VIII verdict

Phase VIII produce o concluzie mai importantă decât simpla identificare a câtorva câmpuri pierdute:

> AI-Toolkit nu suferă numai de semantic loss. Suferă de semantic fragmentation între mai multe circulații epistemice care descriu același organism fără un sistem demonstrat de unificare.



În același timp, există o veste foarte bună:

> UniversalEngineeringModel există deja și este conectat direct la SemanticResult.



Prin urmare nu trebuie inventat UEM.

Trebuie stabilit dacă el poate deveni corpul semantic comun în care CSL, canonul documentar, repository/code intelligence, runtime state și ulterior experiența persistentă se întâlnesc fără să-și piardă identitatea și proveniența.

Asta mută cercetarea la următoarea întrebare fundamentală:

Phase IX — UEM Convergence & Epistemic Unification Audit

Nu mai căutăm doar „ce se pierde”.

Trebuie să stabilim dacă UniversalEngineeringModel poate absorbi fără pierdere celelalte reprezentări — MaterializedKnowledge, CanonicalKnowledgeGraph și KnowledgeGraph V2 — și dacă el poate deveni anatomia semantică unică a organismului epistemic, peste care construim Permanent Orientation, Legend și CSL V2.
