# PCC-01 — PROTECTION PERSISTENCE PHYSIOLOGY DESIGN INSPECTION — RUN 024

**Purpose:** Determine the correct anatomical relationship between Protection and Persistence before any Protection persistence implementation.

**Expected baseline:** `058e12c3ebd753eb43d47e40714a4ce21011c5d5`

**Software modification:** NONE

**Git conservation:** NONE

---

## 1. Baseline

```text
Expected:    058e12c3ebd753eb43d47e40714a4ce21011c5d5
LOCAL:       058e12c3ebd753eb43d47e40714a4ce21011c5d5
origin/main: 058e12c3ebd753eb43d47e40714a4ce21011c5d5
PASS
```

## 2. Predecessor Evidence

RUN 023 established:

- RUN 022 failed because of an experimental harness defect.
- corrected real-process experiment passes.
- Experience identity continuity remains demonstrated locally.
- current Experience serialization does not contain Protection state.
- Protection continuity across restart remains NOT DEMONSTRATED.

## 3. Accepted Specification — Protection/Persistence References

```text
3:**Capability:** PCC-01 — Persistent Experience  
7:**Human Authority:** Owner  
17:This document specifies the first executable organ of PCC-01 — Persistent Experience.
27:It does not claim that Persistent Experience has been demonstrated.
31:It defines the software contract that must be accepted by the Human Authority before implementation begins.
53:Persistence is not authority.
68:- Experience Identity represents its persistent identity;
90:It does not yet establish the complete physiology of Persistent Experience.
104:7. Storage != Experience
106:9. Persistence != authority
137:- a storage path;
192:No Session, Memory, Evidence, retention, forgetting or protection implementation belongs inside these modules merely for convenience.
233:- remain serializable without becoming equivalent to its serialized representation.
239:The model MUST NOT declare authority.
251:The implementation MAY contain additional internal versioning metadata where required for safe serialization.
253:Additional fields MUST NOT silently introduce Session, Memory, Evidence, Provenance, authority, retention or protection semantics before their respective phases.
265:- be serializable;
267:- remain identical after reconstruction from persisted representation;
271:- be independent from storage filenames.
285:Recovery of an existing Experience MUST NOT generate a replacement identity.
287:Deserialization MUST preserve the stored Experience identity.
299:unless both objects are explicitly representations of the same persisted Experience.
349:Future phases MAY extend lifecycle semantics for retention, archival, forgetting, conflict or protection.
363:- persistence;
366:- authority;
384:- canonical authority.
460:- whether a storage file exists;
475:Storage is not Experience.
498:- supported serialization version metadata.
529:## 32. Repository Serialization Boundary
531:Serialization is a representation of Experience.
533:Serialization is not Experience.
535:The repository MAY serialize the model into a deterministic structured representation.
541:## 33. Serialization Requirements
543:Core serialization MUST preserve at least:
550:Serialization MUST NOT embed arbitrary runtime objects.
552:Serialization MUST NOT depend on live process memory for reconstruction.
556:## 34. Storage Boundary
558:The physical storage mechanism is an implementation detail behind Experience Repository.
564:A serialized record is not authority.
566:The repository abstraction MUST prevent higher-level services from depending unnecessarily on storage layout.
572:The first Core Experience repository SHOULD use the simplest deterministic storage strategy compatible with the repository's existing architecture.
574:Before implementation, existing repository/storage infrastructure MUST be reused where behaviorally compatible.
616:Whether creation immediately persists the Experience MUST be explicit in implementation and tests.
630:5. persist the resulting state when repository-backed operation is used;
643:5. persist the resulting state when repository-backed operation is used;
666:`serialization/storage`
682:Infrastructure MUST depend on domain contracts rather than forcing storage semantics into the domain model where practical.
708:Experience MUST NOT become a Memory record merely because it can persist.
758:## 49. Authority Boundary
760:Persistence does not grant authority.
770:Authority remains governed separately.
772:Human Authority remains with the Owner where Human Acceptance is required.
782:The Experience identity must remain capable of surviving that death through later persistence/recovery phases.
796:## 52. Protection Against Concept Collapse
805:- storage location is treated as Experience identity;
806:- persisted data is treated as authoritative because it persisted;
832:- persistence/repository failure.
842:a failed load MUST NOT create a new Experience with a new UUID and return it as if recovery succeeded.
871:5. serialization round-trip preserves identity;
885:6. lifecycle does not imply authority.
898:6. storage representation remains behind repository boundary.
929:## 61. Serialization Versioning
931:If persisted Core Experience records require a schema marker, that marker MUST be explicit.
939:## 62. Creation Versus Recovery
941:Creation and recovery are distinct operations.
947:Recovery:
949:`persisted existing Experience -> reconstructed same Experience + same Experience ID`
951:Recovery MUST NEVER silently execute creation semantics.
955:## 63. Loading Versus Recovery
957:Core Repository load is a prerequisite for later recovery behavior.
959:A successful load proves that a persisted representation can reconstruct the domain object.
961:It does not alone prove recovery across real process death.
963:Real restart recovery belongs to a subsequent PCC-01 phase.
967:## 64. Core Persistence Boundary
969:The Repository milestone introduces enough persistence behavior to test deterministic save/load.
971:This is not yet the complete PCC-01 persistence/recovery demonstration.
973:The later restart harness MUST start a genuinely new process and recover the Experience from durable state.
983:3. persists it;
986:6. loads/recover the Experience;
987:7. obtains the recovered Experience ID;
1066:## 72. Core Test — Serialization Round Trip
1068:Serialize and reconstruct an Experience.
1115:- retrieval semantics behave according to the selected persistence contract.
1151:## 79. Core Test — Storage Is Not Identity
1155:Storage naming may use Experience ID for deterministic addressing.
1169:- no persisted substitute record.
1227:- storage.
1235:Before reusing existing repository/storage components, implementation review MUST establish behavioral compatibility.
1261:## 88. Explicitly Out of Scope — Protection
1263:Experience Protection is NOT implemented in this milestone.
1265:Protection belongs after the Core organ exists and before the complete persistence/recovery acceptance loop.
1328:Any future canonization requires an explicit Human Authority gate.
1364:2. recovery test;
1367:5. protection;
1385:It MUST NOT silently invent architectural authority.
1405:Existing organs remain valid unless explicitly superseded through accepted architectural authority.
1448:## 104. Human Authority Rule
1450:The Human Authority for this gate is:
1454:Only the Human Authority may accept or reject this implementation specification.
1513:No later artifact may retroactively convert an earlier research artifact into Canon without explicit authority.
1527:This success does NOT yet mean PCC-01 Persistent Experience is fully implemented.
1541:Persistent Experience ultimately requires the organism to preserve an identifiable Experience across genuine process death and process restart without confusing it with Session, Memory or Evidence.
1561:These statuses may change only through their respective future evidence and authority gates.
1591:Storage into Experience.
1593:Persistence into authority.
```

## 4. Contract and Build Plan References

### Implementation Contract

```text
1:# PCC-01 — Persistent Experience Implementation Contract
4:Capability: Persistent Experience
6:Human Authority: Owner
19:Acest document transformă anatomia reconciliată și acceptată a PCC-01 — Persistent Experience într-un contract executabil pentru construcția software.
43:**Ce trebuie să existe efectiv în software pentru ca organismul epistemic să poată trăi, identifica, lega, proteja, păstra, recupera și uita controlat Experience fără să falsifice trecutul și fără să confunde Experience cu Session, Memory, Evidence, raw dialogue sau Storage?**
51:Persistent Experience nu este un fișier.
69:Persistent Experience este o **funcție a organismului epistemic**.
71:Fișierele, bazele de date, obiectele, indexurile și mecanismele de serializare sunt numai țesutul fizic prin care funcția poate fi realizată.
91:**Storage != Experience**
95:**Persistence != authority**
114:6. corpul persistent;
167:Persistarea conversației nu demonstrează Persistent Experience.
207:Fiecare Experience persistentă trebuie să primească o identitate stabilă.
219:Identitatea trebuie să fie serializabilă.
263:O Experience persistentă trebuie să aibă un corp reprezentabil.
295:# 16. Persistența
297:O Experience declarată persistentă trebuie să supraviețuiască terminării procesului.
299:Dacă organismul moare operațional și repornește, Experience persistentă trebuie să poată fi recuperată.
310:4. Experience este persistată;
313:7. registrul persistent este reconstituit;
325:# 18. Persistența nu este memorie RAM
335:Persistența trebuie demonstrată peste o frontieră reală de restart.
339:# 19. Integritatea corpului persistent
341:Corpul persistent trebuie să poată detecta cel puțin situațiile în care datele necesare sunt:
404:Persistent Experience trebuie să respecte principiul:
650:Recuperarea este funcția prin care organismul regăsește Experience persistentă.
755:- persisted;
789:- candidate -> persisted fără criteriul de acceptare atunci când acesta este obligatoriu;
811:- corrupted persistent body;
816:- persistence failure.
822:Nicio eroare de persistență nu poate fi raportată ca succes.
836:- persistarea Experience;
849:În special, aceeași comandă de persistare nu trebuie să creeze automat mai multe Experience identice dacă intenția este aceeași operație.
870:- timpul persistării;
884:Ordinea accidentală a citirii din storage nu trebuie tratată drept adevăr istoric.
890:Corpul persistent trebuie să aibă o strategie de versiune.
900:Dacă schema persistentă evoluează, migrarea trebuie să fie:
929:- storage;
930:- persistence;
951:5. nu face storage-ul autoritatea semantică;
990:# 73. Storage adapter
992:Backend-ul persistent trebuie accesat printr-o frontieră care nu obligă restul organismului să considere backend-ul drept model semantic.
999:- adapterul de persistență.
1007:# 74. Serializarea
1009:Serializarea trebuie să păstreze informația necesară reconstruirii obiectului logic.
1013:**Experience -> serialized body -> persistent storage -> load -> Experience**
1019:# 75. Determinismul serializării
1021:Acolo unde fingerprinting-ul, comparația sau Evidence depind de serializare, forma trebuie să fie suficient de deterministă pentru scopul respectiv.
1029:Implementarea trebuie să poată verifica integritatea minimă a corpului persistent.
1050:- dar corpul persistent lipsește;
1080:# 80. Recovery
1082:Dacă la boot este detectată o stare recuperabilă, mecanismul de recovery trebuie să fie explicit.
1084:Recovery nu trebuie să ascundă pierderea de date.
1092:Închiderea normală trebuie să lase corpul persistent într-o stare coerentă.
1108:- persist Experience;
1178:Logurile nu sunt storage-ul Experience.
1191:- persist;
1196:- recovery semnificativ;
1203:Human Authority rămâne distinctă de mecanismele automate.
1252:Dacă un corp persistent este corupt, organismul trebuie să poată raporta corupția.
1276:# 97. Conflict persistent
1294:Dacă o operație de forgetting este în curs sau necesită stare persistentă, restartul nu trebuie să producă o stare imposibil de explicat.
1316:Dacă organismul își amintește conținutul, dar nu mai știe de unde provine, Persistent Experience este incompletă.
1353:Înainte sau în timpul persistării trebuie aplicată politica de protecție necesară.
1355:Nu trebuie să existe o fereastră în care materialul protejat este persistat neprotejat și ulterior „reparat” fără justificare.
1359:# 107. Bucla de viață — persistență
1361:Experience este serializată și persistată prin corpul fizic ales.
1363:Succesul este declarat numai după satisfacerea criteriului de persistență stabilit de adapter.
1409:**candidate -> Experience -> identity -> protection -> persistence -> Session binding -> process death -> process restart -> recovery -> inspection -> retention/forgetting behavior**
1429:- persistence;
1432:- protection;
1440:Cel puțin un test trebuie să creeze o frontieră reală între procesul care persistă și procesul care recuperează.
1456:pentru aceeași Experience persistentă.
1476:După restart, proveniența trebuie să fie echivalentă semantic cu cea persistată înainte de restart.
1512:Trebuie introdusă cel puțin o stare persistentă coruptă sau incompatibilă controlat.
1561:- dovada binding-ului persistent;
1623:# 138. Condiția 2 — persistența
1637:Experience <-> Session binding trebuie să fie explicit, persistent, inspectabil și sigur în fața ambiguității/conflictului.
1659:# 144. Condiția 8 — recovery
1685:Dacă procesul de guvernanță PCC-01 cere acceptare umană finală, numai Human Authority poate acorda acea acceptare.
1718:- backup/recovery;
1760:7. adapterul persistent;
1761:8. serializarea și integritatea;
1767:14. recovery;
1801:# 156. Faza III — corpul persistent
1803:După stabilizarea modelului logic, corpul persistent trebuie conectat prin adapter.
1807:Schema storage nu trebuie să dicteze anatomia Experience.
1827:Protection, retention, archive și forgetting trebuie integrate în ciclul de viață.
1833:# 159. Faza VI — recovery
1837:Această fază transformă persistența din presupunere în comportament demonstrabil.
1893:- tratează storage-ul drept adevăr semantic;
1924:Persistent Experience trebuie să rămână independentă semantic de furnizorul AI.
1987:- storage-ul;
2040:Duplicarea identității, Session management-ului sau persistence-ului trebuie evitată.
2054:Persistența trebuie să funcționeze în mediile suportate de AI-Toolkit fără să depindă de o particularitate accidentală a telefonului de dezvoltare.
2110:Persistența nu conferă autoritate.
2130:Un test de persistence nu demonstrează automat privacy.
2143:- persistence;
2150:- protection;
2154:- recovery;
2211:- demonstrația protection;
2332:- apariția unui al doilea storage incompatibil;
2358:- storage complete;
2374:3. identități persistente;
2377:6. protection metadata;
2378:7. persistence;
2381:10. recovery;
2395:Persistent Experience include și capacitatea sănătoasă de a nu păstra ceea ce nu mai trebuie păstrat.
2427:Trebuie alterat controlat un corp persistent de test.
2445:Aceasta este frontiera minimă prin care se demonstrează că experiența aparține organismului persistent și nu memoriei volatile a procesului anterior.
2495:- persistence;
2498:- protection;
2501:- recovery;
2511:Storage nu trebuie să controleze semantic Experience.
2513:Dashboard nu trebuie să controleze storage.
2535:**Protection**
2537:**Persistence**
2541:**Recovery**
2557:**raw dialogue -> database -> "Persistent Experience implemented"**
2611:O arhitectură frumoasă fără persistență reală nu satisface PCC-01.
2770:6. persista Experience;
2798:7. confunda Storage cu Experience;
2799:8. confunda persistence cu authority;
2826:**Protection**
2829:**Persistent Body**
2850:**Recovery**
2873:Protection seamănă cu barierele și mecanismele de protecție.
2875:Persistent Body este țesutul în care experiența poate supraviețui stării operaționale de moment.
2889:Recovery este reamintirea după o întrerupere.
2927:Persistent Experience există pentru a oferi continuitate epistemică.
2937:Persistența trebuie să conserve istoria, nu să o reinventeze.
2981:Persistent Experience nu trebuie să devină o justificare pentru retenție nelimitată.
2989:Persistența fără protecție nu este o funcție sănătoasă.
3019:Anatomia acceptată a PCC-01 poate fi transformată într-o implementare software coerentă numai dacă Persistent Experience este construită ca o fiziologie de continuitate și nu ca o simplă funcție de stocare.
3035:- persistent storage boundary;
3036:- serialization;
3038:- protection;
3044:- restart recovery;
3094:- storage;
3098:- privacy/protection;
3211:**Storage**
3212:= suport fizic pentru persistență.
3226:**Human Authority**
3247:**Storage != Experience**
3251:**Persistence != authority**
3259:Pentru o Experience persistentă sănătoasă:
3307:Ambiguitatea nu poate deveni certitudine doar prin serializare și reîncărcare.
3313:Persistarea unei afirmații nu îi crește automat autoritatea epistemică.
3333:Necesită decizia Human Authority.
3337:# 286. Întrebarea pentru Human Authority
3399:- Storage;
3400:- Human Authority.
3402:Contractul cere persistență reală peste restart.
3426:Persistent Experience trebuie construită ca o funcție vie a organismului epistemic.
3456:Acesta este contractul candidat pentru construirea primei implementări reale PCC-01 — Persistent Experience.
3468:END OF PCC-01 — PERSISTENT EXPERIENCE IMPLEMENTATION CONTRACT
```

### Build Plan

```text
1:# PCC-01 — Persistent Experience Implementation Inventory and Build Plan
4:Capability: Persistent Experience  
6:Human Authority: Owner  
20:Acest document transformă PCC-01 Implementation Contract acceptat de om într-un inventar concret al corpului software existent și într-un plan de construcție pentru funcția Persistent Experience.
55:- storage-ul poate reprezenta țesut de conservare;
115:- o înregistrare accidentală într-un storage.
133:Session trebuie să poată dispărea fără ca Experience persistentă să dispară.
169:# 10. Frontiera Storage
171:Storage este infrastructură de conservare.
173:Storage nu este obiectul conservat.
177:**Storage != Experience**
179:Schimbarea backend-ului de storage nu trebuie să schimbe identitatea semantică a Experience.
193:# 12. Frontiera Authority
195:Persistența unei informații nu îi conferă autoritate.
199:**Persistence != authority**
219:Auditul anterior nu a demonstrat existența unui organ Python PCC-01 care să implementeze complet identitatea și ciclul Persistent Experience.
231:`work/persistent-experience/active/`
239:Nu le tratăm automat ca storage.
259:- protection state;
260:- persistence state;
306:candidate -> Experience -> identified -> protected -> persisted -> bound -> recoverable
310:recoverable -> retained
312:recoverable -> archived
314:recoverable -> forgotten
316:recoverable -> conflicted
318:recoverable -> ambiguous
326:Trebuie să existe o frontieră între materialul candidat și Experience persistentă.
344:Înainte de persistență trebuie validate invariantele minime.
352:# 23. Experience protection
354:Contractul cere protejarea Experience înainte ca aceasta să intre în persistența durabilă.
358:Protection trebuie să fie o stare observabilă, nu doar o presupunere.
362:# 24. Experience persistence
364:Persistența Experience trebuie implementată explicit.
372:# 25. Semantic persistence existent
374:Repository-ul conține infrastructură de persistență în alte subsisteme, inclusiv semantic repository intelligence.
386:PCC-01 are nevoie de o frontieră de repository/storage dedicată Experience.
399:- restart recovery.
403:# 27. Persistența atomică
405:Nu trebuie să existe stări în care Experience pare persistentă runtime-ului, dar nu este conservată durabil.
411:# 28. Recovery
413:Recovery după restart este funcție obligatorie.
417:Recovery nu înseamnă reconstruirea unei Experience noi din text.
419:Trebuie recuperată aceeași identitate persistentă.
439:- storage.
493:# 35. Binding persistence
501:# 36. Binding recovery
508:- relația persistentă poate fi inspectată.
524:Aceasta este una dintre diferențele fundamentale dintre runtime state și Persistent Experience.
552:Storage-ul Memory poate oferi precedent tehnic.
614:- persistence;
616:- recovery;
620:- protection;
650:Fiecare Experience persistentă trebuie să poată indica originea sa.
714:Persistent Experience nu trebuie cuplată exclusiv la execuția autonomă.
782:Retention trebuie separată de storage existence.
818:# 65. Protection policy
835:Persistența fără control de acces nu satisface contractul.
848:- persistence;
849:- recovery;
870:Un obiect invalid trebuie refuzat înainte de a deveni Experience persistentă validă.
888:# 72. Corrupted persistence
890:Dacă storage-ul persistent este corupt, recovery nu trebuie să pretindă succes.
918:Dacă recovery după restart eșuează, PCC-01 nu poate trece poarta IMPLEMENTED.
924:Persistent Experience trebuie să fie inspectabilă prin interfețe controlate.
946:Dashboard-ul poate deveni suprafață de observare pentru Persistent Experience.
974:Experience persistentă nu trebuie să depindă de existența procesului care a creat-o.
986:# 84. Serialization
988:Experience are nevoie de serializare stabilă.
994:# 85. Serialization invariant
996:Serializare -> persistență -> reload nu trebuie să schimbe identitatea semantică.
1008:Persistența trebuie să poată identifica versiunea structurii Experience.
1021:- persisted_at;
1022:- recovered_at, când este Evidence/runtime metadata;
1046:Acesta nu trebuie să fie doar un wrapper peste storage.
1057:- protection;
1058:- persistence;
1069:# 93. Experience Service nu este Storage
1073:Repository-ul păstrează corpul persistent.
1089:Modelul este anatomia obiectului persistent.
1209:Construim persistența Experience.
1215:# 110. Build Phase 5 — Recovery
1217:Construim recovery după restart.
1237:# 113. Build Phase 8 — Protection
1283:UI nu poate compensa lipsa persistence.
1285:Evidence nu poate compensa lipsa recovery.
1311:Serializarea și reload-ul nu trebuie să schimbe identity.
1315:# 125. Test — persistence
1317:Experience trebuie să existe în storage după operația de persistence confirmată.
1333:# 128. Test — recovery
1335:Procesul nou trebuie să recupereze Experience persistentă.
1363:Trebuie demonstrat că dispariția runtime-ului Session nu șterge automat Experience persistentă.
1373:# 134. Test — protection
1433:# 144. Test — serialization round trip
1435:Experience -> serialization -> persistence -> load -> Experience
1443:Schimbarea providerului nu trebuie să schimbe identitatea Experience deja persistente.
1469:**candidate -> Experience -> identity -> protection -> persistence -> Session binding -> process death -> process restart -> recovery -> inspection -> retention/forgetting behavior**
1482:- persistence confirmată;
1487:- recovered state;
1565:- recovery;
1571:- failure recovery;
1605:**Experience Protection**
1701:# 169. Interdicția storage-as-Experience
1705:**Storage != Experience**
1709:# 170. Interdicția persistence-as-authority
1711:O Experience persistentă nu devine automat adevăr.
1713:**Persistence != authority**
1727:Persistent Experience trebuie să supraviețuiască morții procesului fără pierderea identității.
1746:- Storage;
1754:Recovery nu trebuie să producă o Experience fără trasabilitate atunci când proveniența este obligatorie.
1770:# 178. Invariantul de protection
1800:**PCC-01 PERSISTENCE AND RESTART**
1804:- durable persistence;
1807:- recovery;
1819:- persistent binding;
1820:- recovery of relationship;
1827:**PCC-01 PROVENANCE AND PROTECTION**
1872:După Persistence and Restart trebuie demonstrat:
1953:- protection;
1998:- persistence infrastructure.
2000:Dar auditul nu a demonstrat existența organului fiziologic complet Persistent Experience.
2036:Protection  
2038:Persistence  
2046:Recovery  
2060:Persistent Experience există cu adevărat numai dacă organismul poate trece printr-o întrerupere reală a procesului și poate reveni cu aceeași Experience identificabilă și inspectabilă.
2068:**same persistent Experience identity across real process restart**
2096:Cel mai mare risc nu este lipsa storage-ului.
2140:Persistența nu este demonstrată până când procesul nu moare cu adevărat și un proces nou recuperează corpul persistent.
2146:Nicio stare persistentă nu înlocuiește autoritatea umană asupra Canonului.
2163:10. recovery test;
2166:13. protection;
2189:**persistent experience**
2205:- persistence patterns.
2225:Dacă schema persistentă evoluează, migrarea trebuie tratată explicit înainte de production-ready.
2241:Persistența doar în RAM este insuficientă.
2267:# 227. Forgetting authority
2285:# 230. Recovery semantics
2287:Recovery trebuie să restabilească o reprezentare validă, nu doar bytes.
2293:După recovery, organismul trebuie să poată inspecta Experience într-o formă controlată.
2311:# 234. Direct storage mutation
2313:Modificarea directă a storage-ului în afara contractului trebuie considerată neautorizată sau unsupported.
2331:# 237. Recovery from archive
2502:# 259. Starea Experience persistence
2508:# 260. Starea Experience recovery
2550:| Experience Identity | CONSTRUIM NOU | identitate persistentă |
2580:| Storage / Experience | Storage != Experience |
2582:| Persistence / authority | Persistence != authority |
2593:| Persistence Demonstrated | durable save/load |
2622:- Experience este persistată;
2741:+ Persistence  
2743:+ Protection  
2760:persista,  
2788:Persistent Experience nu trebuie construit ca un organism paralel.
2858:El nu confundă persistența cu autoritatea.
2868:END OF PCC-01 — PERSISTENT EXPERIENCE IMPLEMENTATION INVENTORY AND BUILD PLAN
```

## 5. Current Organ Anatomy


### lib/python/experience/protection.py

```python
"""Protection physiology for Persistent Experience.

Protection is an explicit domain organ.

It does not make persistence authoritative.
It does not replace lifecycle.
It does not replace retention or forgetting.
It does not derive authority from storage.

Its responsibility is to make the protection condition of an
Experience explicit and to reject operations that violate that
condition.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .identity import ExperienceId


class ExperienceProtectionError(Exception):
    """Base error for Experience protection violations."""


class InvalidProtectionIdentityError(ExperienceProtectionError):
    """Raised when protection is requested for an invalid Experience identity."""


class ProtectedExperienceMutationError(ExperienceProtectionError):
    """Raised when a protected Experience is subjected to prohibited mutation."""


class UnauthorizedExperienceOperationError(ExperienceProtectionError):
    """Raised when an operation lacks explicit authorization."""


class ProtectionState(str, Enum):
    """Observable protection condition of an Experience."""

    UNPROTECTED = "unprotected"
    PROTECTED = "protected"


@dataclass(frozen=True, slots=True)
class ExperienceProtection:
    """Protection state associated with exactly one Experience identity.

    The protector references the Experience identity but does not own
    or replace that identity.

    Protection is deliberately distinct from persistence and authority.
    """

    experience_id: ExperienceId
    state: ProtectionState

    @classmethod
    def unprotected(
        cls,
        experience_id: ExperienceId,
    ) -> "ExperienceProtection":
        return cls(
            experience_id=_require_experience_id(experience_id),
            state=ProtectionState.UNPROTECTED,
        )

    @classmethod
    def protected(
        cls,
        experience_id: ExperienceId,
    ) -> "ExperienceProtection":
        return cls(
            experience_id=_require_experience_id(experience_id),
            state=ProtectionState.PROTECTED,
        )

    @property
    def is_protected(self) -> bool:
        return self.state is ProtectionState.PROTECTED

    def protect(self) -> "ExperienceProtection":
        """Return the protected condition without changing identity."""

        if self.is_protected:
            return self

        return ExperienceProtection(
            experience_id=self.experience_id,
            state=ProtectionState.PROTECTED,
        )

    def require_mutation_allowed(self) -> None:
        """Reject ordinary mutation while the Experience is protected."""

        if self.is_protected:
            raise ProtectedExperienceMutationError(
                "protected Experience cannot be mutated by an ordinary operation"
            )

    def require_authorized(self, *, authorized: bool) -> None:
        """Require explicit authorization for a protected operation.

        Persistence itself never supplies this authorization.
        """

        if not isinstance(authorized, bool):
            raise TypeError("authorized must be bool")

        if self.is_protected and not authorized:
            raise UnauthorizedExperienceOperationError(
                "operation on protected Experience requires explicit authorization"
            )


def _require_experience_id(value: ExperienceId) -> ExperienceId:
    """Validate the identity consumed by the Protection organ."""

    if not isinstance(value, ExperienceId):
        raise InvalidProtectionIdentityError(
            "experience_id must be an ExperienceId"
        )

    return value
```

### lib/python/experience/persistence.py

```python
"""Serialization boundary for PCC-01 Persistent Experience.

Serialization is a transport/storage representation of Experience.

Storage != Experience.
Persistence != authority.
Interpretation != historical fact.

Recovery must reconstruct the persisted Experience identity.
It must never generate a replacement identity.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Mapping

from .identity import ExperienceId, ExperienceIdentityError
from .lifecycle import ExperienceState
from .model import Experience


class ExperiencePersistenceError(RuntimeError):
    """Base error for Experience persistence representation failures."""


class ExperienceSerializationError(ExperiencePersistenceError):
    """Raised when an Experience cannot be serialized safely."""


class ExperienceRecoveryError(ExperiencePersistenceError):
    """Raised when persisted Experience data cannot be recovered safely."""


_REQUIRED_FIELDS = frozenset(
    {
        "experience_id",
        "created_at",
        "state",
    }
)


def serialize_experience(experience: Experience) -> dict[str, str]:
    """Serialize exactly the minimum Core Experience state."""

    if not isinstance(experience, Experience):
        raise ExperienceSerializationError(
            "serialize_experience requires an Experience"
        )

    return {
        "experience_id": str(experience.experience_id),
        "created_at": experience.created_at.isoformat(),
        "state": experience.state.value,
    }


def recover_experience(data: Mapping[str, Any]) -> Experience:
    """Recover one existing Experience without regenerating identity."""

    if not isinstance(data, Mapping):
        raise ExperienceRecoveryError(
            "persisted Experience representation must be a mapping"
        )

    fields = frozenset(data.keys())

    if fields != _REQUIRED_FIELDS:
        missing = sorted(_REQUIRED_FIELDS - fields)
        unexpected = sorted(fields - _REQUIRED_FIELDS)

        raise ExperienceRecoveryError(
            "invalid persisted Experience fields; "
            f"missing={missing}, unexpected={unexpected}"
        )

    experience_id_raw = data["experience_id"]
    created_at_raw = data["created_at"]
    state_raw = data["state"]

    if not isinstance(experience_id_raw, str):
        raise ExperienceRecoveryError(
            "persisted experience_id must be a string"
        )

    if not isinstance(created_at_raw, str):
        raise ExperienceRecoveryError(
            "persisted created_at must be a string"
        )

    if not isinstance(state_raw, str):
        raise ExperienceRecoveryError(
            "persisted state must be a string"
        )

    try:
        experience_id = ExperienceId.from_string(experience_id_raw)
    except ExperienceIdentityError as exc:
        raise ExperienceRecoveryError(
            "persisted Experience identity is invalid"
        ) from exc

    try:
        created_at = datetime.fromisoformat(created_at_raw)
    except ValueError as exc:
        raise ExperienceRecoveryError(
            "persisted created_at is invalid"
        ) from exc

    if created_at.tzinfo is None:
        raise ExperienceRecoveryError(
            "persisted created_at must be timezone-aware"
        )

    try:
        state = ExperienceState(state_raw)
    except ValueError as exc:
        raise ExperienceRecoveryError(
            "persisted Experience state is invalid"
        ) from exc

    return Experience(
        experience_id=experience_id,
        created_at=created_at,
        state=state,
    )
```

### lib/python/experience/persistent_repository.py

```python
"""File-backed repository for PCC-01 Persistent Experience.

This repository implements the established ExperienceRepository
contract using a JSON file as a persistence substrate.

The JSON file is storage.
It is not Experience.
Its existence does not create authority.
"""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any

from .identity import ExperienceId
from .model import Experience
from .persistence import (
    ExperiencePersistenceError,
    ExperienceRecoveryError,
    recover_experience,
    serialize_experience,
)
from .repository import (
    ExperienceAlreadyExistsError,
    ExperienceNotFoundError,
    ExperienceRepository,
    ExperienceRepositoryError,
)


class PersistentExperienceRepositoryError(ExperienceRepositoryError):
    """Base error for persistent Experience repository failures."""


class ExperienceStoreCorruptionError(PersistentExperienceRepositoryError):
    """Raised when the persisted store cannot be trusted or recovered."""


class JsonFileExperienceRepository(ExperienceRepository):
    """JSON-backed Experience repository.

    The repository persists Experience state beyond object lifetime.

    RUN 016 verifies recovery using independent repository instances.
    It does NOT claim real process-death continuity.
    """

    _FORMAT_VERSION = 1

    def __init__(self, path: str | Path) -> None:
        self._path = Path(path)

        if self._path.exists() and self._path.is_dir():
            raise PersistentExperienceRepositoryError(
                f"Experience store path is a directory: {self._path}"
            )

    @property
    def path(self) -> Path:
        return self._path

    def add(self, experience: Experience) -> None:
        store = self._read_store()

        key = str(experience.experience_id)

        if key in store["experiences"]:
            raise ExperienceAlreadyExistsError(
                f"Experience already exists: {experience.experience_id}"
            )

        store["experiences"][key] = serialize_experience(experience)
        self._write_store(store)

    def get(self, experience_id: ExperienceId) -> Experience:
        _require_experience_id(experience_id)

        store = self._read_store()
        key = str(experience_id)

        try:
            representation = store["experiences"][key]
        except KeyError as exc:
            raise ExperienceNotFoundError(
                f"Experience not found: {experience_id}"
            ) from exc

        try:
            recovered = recover_experience(representation)
        except ExperiencePersistenceError as exc:
            raise ExperienceStoreCorruptionError(
                f"Persisted Experience is corrupt: {experience_id}"
            ) from exc

        if recovered.experience_id != experience_id:
            raise ExperienceStoreCorruptionError(
                "persisted Experience identity does not match repository key"
            )

        return recovered

    def save(self, experience: Experience) -> None:
        store = self._read_store()

        key = str(experience.experience_id)

        if key not in store["experiences"]:
            raise ExperienceNotFoundError(
                f"Cannot save unknown Experience: {experience.experience_id}"
            )

        store["experiences"][key] = serialize_experience(experience)
        self._write_store(store)

    def contains(self, experience_id: ExperienceId) -> bool:
        _require_experience_id(experience_id)

        store = self._read_store()

        return str(experience_id) in store["experiences"]

    def _empty_store(self) -> dict[str, Any]:
        return {
            "format_version": self._FORMAT_VERSION,
            "experiences": {},
        }

    def _read_store(self) -> dict[str, Any]:
        if not self._path.exists():
            return self._empty_store()

        try:
            raw = self._path.read_text(encoding="utf-8")
        except OSError as exc:
            raise PersistentExperienceRepositoryError(
                f"cannot read Experience store: {self._path}"
            ) from exc

        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ExperienceStoreCorruptionError(
                "Experience store contains invalid JSON"
            ) from exc

        if not isinstance(data, dict):
            raise ExperienceStoreCorruptionError(
                "Experience store root must be an object"
            )

        if set(data.keys()) != {"format_version", "experiences"}:
            raise ExperienceStoreCorruptionError(
                "Experience store has invalid top-level fields"
            )

        if data["format_version"] != self._FORMAT_VERSION:
            raise ExperienceStoreCorruptionError(
                "Experience store format version is unsupported"
            )

        experiences = data["experiences"]

        if not isinstance(experiences, dict):
            raise ExperienceStoreCorruptionError(
                "Experience store experiences field must be an object"
            )

        for key, representation in experiences.items():
            if not isinstance(key, str):
                raise ExperienceStoreCorruptionError(
                    "Experience store identity key must be a string"
                )

            try:
                recovered = recover_experience(representation)
            except ExperienceRecoveryError as exc:
                raise ExperienceStoreCorruptionError(
                    f"invalid persisted Experience entry: {key}"
                ) from exc

            if str(recovered.experience_id) != key:
                raise ExperienceStoreCorruptionError(
                    "Experience store key and embedded identity disagree"
                )

        return data

    def _write_store(self, store: dict[str, Any]) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)

        payload = json.dumps(
            store,
            ensure_ascii=False,
            sort_keys=True,
            indent=2,
        ) + "\n"

        fd: int | None = None
        temporary_path: Path | None = None

        try:
            fd, temporary_name = tempfile.mkstemp(
                prefix=f".{self._path.name}.",
                suffix=".tmp",
                dir=str(self._path.parent),
                text=True,
            )

            temporary_path = Path(temporary_name)

            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                fd = None
                handle.write(payload)
                handle.flush()
                os.fsync(handle.fileno())

            os.replace(temporary_path, self._path)

        except OSError as exc:
            raise PersistentExperienceRepositoryError(
                f"cannot write Experience store: {self._path}"
            ) from exc

        finally:
            if fd is not None:
                os.close(fd)

            if temporary_path is not None and temporary_path.exists():
                try:
                    temporary_path.unlink()
                except OSError:
                    pass


def _require_experience_id(value: ExperienceId) -> ExperienceId:
    if not isinstance(value, ExperienceId):
        raise TypeError("experience_id must be an ExperienceId")

    return value
```

### lib/python/experience/repository.py

```python
"""Repository boundary for PCC-01 Core Experience."""

from __future__ import annotations

from abc import ABC, abstractmethod

from .identity import ExperienceId
from .model import Experience


class ExperienceRepositoryError(RuntimeError):
    """Base error for Experience repository operations."""


class ExperienceNotFoundError(ExperienceRepositoryError):
    """Raised when an Experience cannot be found by its identity."""


class ExperienceAlreadyExistsError(ExperienceRepositoryError):
    """Raised when creation would replace an existing Experience."""


class ExperienceRepository(ABC):
    """Storage-independent contract for Core Experience.

    The repository stores and retrieves Experience state.

    Storage is not Experience.
    Persistence is not authority.
    """

    @abstractmethod
    def add(self, experience: Experience) -> None:
        """Store a newly admitted Experience without replacement."""

    @abstractmethod
    def get(self, experience_id: ExperienceId) -> Experience:
        """Return one Experience by stable Experience identity."""

    @abstractmethod
    def save(self, experience: Experience) -> None:
        """Persist the current state of an already admitted Experience."""

    @abstractmethod
    def contains(self, experience_id: ExperienceId) -> bool:
        """Return whether this repository knows the Experience identity."""


class InMemoryExperienceRepository(ExperienceRepository):
    """Minimal repository implementation for Core behavioral tests.

    This implementation is intentionally process-local.

    It does NOT demonstrate persistence across real process death.
    """

    def __init__(self) -> None:
        self._experiences: dict[ExperienceId, Experience] = {}

    def add(self, experience: Experience) -> None:
        if experience.experience_id in self._experiences:
            raise ExperienceAlreadyExistsError(
                f"Experience already exists: {experience.experience_id}"
            )

        self._experiences[experience.experience_id] = experience

    def get(self, experience_id: ExperienceId) -> Experience:
        try:
            return self._experiences[experience_id]
        except KeyError as exc:
            raise ExperienceNotFoundError(
                f"Experience not found: {experience_id}"
            ) from exc

    def save(self, experience: Experience) -> None:
        if experience.experience_id not in self._experiences:
            raise ExperienceNotFoundError(
                f"Cannot save unknown Experience: {experience.experience_id}"
            )

        self._experiences[experience.experience_id] = experience

    def contains(self, experience_id: ExperienceId) -> bool:
        return experience_id in self._experiences
```

### lib/python/experience/model.py

```python
"""Domain anatomy of one PCC-01 Core Experience."""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime, timezone

from .identity import ExperienceId
from .lifecycle import ExperienceState, transition


@dataclass(frozen=True, slots=True)
class Experience:
    """One Core Experience domain entity.

    Experience remains distinct from Session, Memory, Evidence,
    raw dialogue, process, provider, storage, and authority.
    """

    experience_id: ExperienceId
    created_at: datetime
    state: ExperienceState

    def __post_init__(self) -> None:
        if self.created_at.tzinfo is None:
            raise ValueError("Experience created_at must be timezone-aware")

    @classmethod
    def create(cls) -> "Experience":
        """Create a new Experience in CREATED state."""
        return cls(
            experience_id=ExperienceId.create(),
            created_at=datetime.now(timezone.utc),
            state=ExperienceState.CREATED,
        )

    def activate(self) -> "Experience":
        """Transition CREATED -> ACTIVE while preserving identity."""
        return replace(
            self,
            state=transition(self.state, ExperienceState.ACTIVE),
        )

    def close(self) -> "Experience":
        """Transition ACTIVE -> CLOSED while preserving identity."""
        return replace(
            self,
            state=transition(self.state, ExperienceState.CLOSED),
        )
```

### lib/python/experience/service.py

```python
"""Application physiology for PCC-01 Core Experience."""

from __future__ import annotations

from .identity import ExperienceId
from .model import Experience
from .repository import ExperienceRepository


class ExperienceService:
    """Coordinates Core Experience behavior.

    The service does not own Experience identity.
    The service does not become Session, Memory, Evidence, or authority.
    """

    def __init__(self, repository: ExperienceRepository) -> None:
        self._repository = repository

    def create_experience(self) -> Experience:
        """Create and admit a new Experience."""
        experience = Experience.create()
        self._repository.add(experience)
        return experience

    def get_experience(self, experience_id: ExperienceId) -> Experience:
        """Inspect an admitted Experience by stable identity."""
        return self._repository.get(experience_id)

    def activate_experience(
        self,
        experience_id: ExperienceId,
    ) -> Experience:
        """Activate an admitted Experience while preserving identity."""
        current = self._repository.get(experience_id)
        active = current.activate()
        self._repository.save(active)
        return active

    def close_experience(
        self,
        experience_id: ExperienceId,
    ) -> Experience:
        """Close an active Experience while preserving identity."""
        current = self._repository.get(experience_id)
        closed = current.close()
        self._repository.save(closed)
        return closed
```

## 6. Structural Relationship Index

```text
lib/python/experience/__init__.py:14:    ExperienceRepository,
lib/python/experience/__init__.py:15:    ExperienceRepositoryError,
lib/python/experience/__init__.py:16:    InMemoryExperienceRepository,
lib/python/experience/__init__.py:26:    "ExperienceRepository",
lib/python/experience/__init__.py:27:    "ExperienceRepositoryError",
lib/python/experience/__init__.py:30:    "InMemoryExperienceRepository",
lib/python/experience/__init__.py:35:    ExperienceProtection,
lib/python/experience/__init__.py:36:    ExperienceProtectionError,
lib/python/experience/__init__.py:38:    ProtectedExperienceMutationError,
lib/python/experience/__init__.py:39:    ProtectionState,
lib/python/experience/__init__.py:47:    recover_experience,
lib/python/experience/__init__.py:48:    serialize_experience,
lib/python/experience/__init__.py:53:    JsonFileExperienceRepository,
lib/python/experience/__init__.py:54:    PersistentExperienceRepositoryError,
lib/python/experience/model.py:17:    raw dialogue, process, provider, storage, and authority.
lib/python/experience/repository.py:11:class ExperienceRepositoryError(RuntimeError):
lib/python/experience/repository.py:15:class ExperienceNotFoundError(ExperienceRepositoryError):
lib/python/experience/repository.py:19:class ExperienceAlreadyExistsError(ExperienceRepositoryError):
lib/python/experience/repository.py:23:class ExperienceRepository(ABC):
lib/python/experience/repository.py:29:    Persistence is not authority.
lib/python/experience/repository.py:49:class InMemoryExperienceRepository(ExperienceRepository):
lib/python/experience/service.py:7:from .repository import ExperienceRepository
lib/python/experience/service.py:14:    The service does not become Session, Memory, Evidence, or authority.
lib/python/experience/service.py:17:    def __init__(self, repository: ExperienceRepository) -> None:
lib/python/experience/session_binding.py:17:    Persistence != authority
lib/python/experience/protection.py:8:It does not derive authority from storage.
lib/python/experience/protection.py:23:class ExperienceProtectionError(Exception):
lib/python/experience/protection.py:27:class InvalidProtectionIdentityError(ExperienceProtectionError):
lib/python/experience/protection.py:31:class ProtectedExperienceMutationError(ExperienceProtectionError):
lib/python/experience/protection.py:32:    """Raised when a protected Experience is subjected to prohibited mutation."""
lib/python/experience/protection.py:35:class UnauthorizedExperienceOperationError(ExperienceProtectionError):
lib/python/experience/protection.py:39:class ProtectionState(str, Enum):
lib/python/experience/protection.py:42:    UNPROTECTED = "unprotected"
lib/python/experience/protection.py:43:    PROTECTED = "protected"
lib/python/experience/protection.py:47:class ExperienceProtection:
lib/python/experience/protection.py:53:    Protection is deliberately distinct from persistence and authority.
lib/python/experience/protection.py:57:    state: ProtectionState
lib/python/experience/protection.py:60:    def unprotected(
lib/python/experience/protection.py:63:    ) -> "ExperienceProtection":
lib/python/experience/protection.py:66:            state=ProtectionState.UNPROTECTED,
lib/python/experience/protection.py:70:    def protected(
lib/python/experience/protection.py:73:    ) -> "ExperienceProtection":
lib/python/experience/protection.py:76:            state=ProtectionState.PROTECTED,
lib/python/experience/protection.py:80:    def is_protected(self) -> bool:
lib/python/experience/protection.py:81:        return self.state is ProtectionState.PROTECTED
lib/python/experience/protection.py:83:    def protect(self) -> "ExperienceProtection":
lib/python/experience/protection.py:84:        """Return the protected condition without changing identity."""
lib/python/experience/protection.py:86:        if self.is_protected:
lib/python/experience/protection.py:89:        return ExperienceProtection(
lib/python/experience/protection.py:91:            state=ProtectionState.PROTECTED,
lib/python/experience/protection.py:95:        """Reject ordinary mutation while the Experience is protected."""
lib/python/experience/protection.py:97:        if self.is_protected:
lib/python/experience/protection.py:98:            raise ProtectedExperienceMutationError(
lib/python/experience/protection.py:99:                "protected Experience cannot be mutated by an ordinary operation"
lib/python/experience/protection.py:103:        """Require explicit authorization for a protected operation.
lib/python/experience/protection.py:111:        if self.is_protected and not authorized:
lib/python/experience/protection.py:113:                "operation on protected Experience requires explicit authorization"
lib/python/experience/persistence.py:6:Persistence != authority.
lib/python/experience/persistence.py:44:def serialize_experience(experience: Experience) -> dict[str, str]:
lib/python/experience/persistence.py:49:            "serialize_experience requires an Experience"
lib/python/experience/persistence.py:59:def recover_experience(data: Mapping[str, Any]) -> Experience:
lib/python/experience/persistent_repository.py:3:This repository implements the established ExperienceRepository
lib/python/experience/persistent_repository.py:8:Its existence does not create authority.
lib/python/experience/persistent_repository.py:24:    recover_experience,
lib/python/experience/persistent_repository.py:25:    serialize_experience,
lib/python/experience/persistent_repository.py:30:    ExperienceRepository,
lib/python/experience/persistent_repository.py:31:    ExperienceRepositoryError,
lib/python/experience/persistent_repository.py:35:class PersistentExperienceRepositoryError(ExperienceRepositoryError):
lib/python/experience/persistent_repository.py:39:class ExperienceStoreCorruptionError(PersistentExperienceRepositoryError):
lib/python/experience/persistent_repository.py:43:class JsonFileExperienceRepository(ExperienceRepository):
lib/python/experience/persistent_repository.py:58:            raise PersistentExperienceRepositoryError(
lib/python/experience/persistent_repository.py:76:        store["experiences"][key] = serialize_experience(experience)
lib/python/experience/persistent_repository.py:93:            recovered = recover_experience(representation)
lib/python/experience/persistent_repository.py:116:        store["experiences"][key] = serialize_experience(experience)
lib/python/experience/persistent_repository.py:139:            raise PersistentExperienceRepositoryError(
lib/python/experience/persistent_repository.py:179:                recovered = recover_experience(representation)
lib/python/experience/persistent_repository.py:224:            raise PersistentExperienceRepositoryError(
tests/experience/test_experience_repository.py:8:    InMemoryExperienceRepository,
tests/experience/test_experience_repository.py:13:    repository = InMemoryExperienceRepository()
tests/experience/test_experience_repository.py:25:    repository = InMemoryExperienceRepository()
tests/experience/test_experience_repository.py:36:    repository = InMemoryExperienceRepository()
tests/experience/test_experience_repository.py:46:    repository = InMemoryExperienceRepository()
tests/experience/test_experience_repository.py:53:    repository = InMemoryExperienceRepository()
tests/experience/test_experience_repository.py:67:    repository = InMemoryExperienceRepository()
tests/experience/test_experience_service.py:9:    InMemoryExperienceRepository,
tests/experience/test_experience_service.py:16:    repository = InMemoryExperienceRepository()
tests/experience/test_experience_core.py:2:from lib.python.experience.repository import InMemoryExperienceRepository
tests/experience/test_experience_core.py:7:    repository = InMemoryExperienceRepository()
tests/experience/test_experience_core.py:31:    repository = InMemoryExperienceRepository()
tests/experience/test_experience_core.py:41:    repository = InMemoryExperienceRepository()
tests/experience/test_experience_core.py:57:        "authority",
tests/experience/test_experience_protection.py:5:    ExperienceProtection,
tests/experience/test_experience_protection.py:7:    ProtectedExperienceMutationError,
tests/experience/test_experience_protection.py:8:    ProtectionState,
tests/experience/test_experience_protection.py:17:def test_unprotected_state_is_explicit():
tests/experience/test_experience_protection.py:20:    protection = ExperienceProtection.unprotected(identity)
tests/experience/test_experience_protection.py:23:    assert protection.state is ProtectionState.UNPROTECTED
tests/experience/test_experience_protection.py:24:    assert protection.is_protected is False
tests/experience/test_experience_protection.py:27:def test_protected_state_is_explicit():
tests/experience/test_experience_protection.py:30:    protection = ExperienceProtection.protected(identity)
tests/experience/test_experience_protection.py:33:    assert protection.state is ProtectionState.PROTECTED
tests/experience/test_experience_protection.py:34:    assert protection.is_protected is True
tests/experience/test_experience_protection.py:40:    before = ExperienceProtection.unprotected(identity)
tests/experience/test_experience_protection.py:44:    assert after.state is ProtectionState.PROTECTED
tests/experience/test_experience_protection.py:50:    protection = ExperienceProtection.protected(identity)
tests/experience/test_experience_protection.py:56:    protection = ExperienceProtection.protected(new_identity())
tests/experience/test_experience_protection.py:59:        protection.state = ProtectionState.UNPROTECTED
tests/experience/test_experience_protection.py:64:        ExperienceProtection.protected("not-an-experience-id")
tests/experience/test_experience_protection.py:67:def test_unprotected_experience_allows_ordinary_mutation_gate():
tests/experience/test_experience_protection.py:68:    protection = ExperienceProtection.unprotected(new_identity())
tests/experience/test_experience_protection.py:73:def test_protected_experience_rejects_ordinary_mutation():
tests/experience/test_experience_protection.py:74:    protection = ExperienceProtection.protected(new_identity())
tests/experience/test_experience_protection.py:76:    with pytest.raises(ProtectedExperienceMutationError):
tests/experience/test_experience_protection.py:80:def test_protected_operation_requires_explicit_authorization():
tests/experience/test_experience_protection.py:81:    protection = ExperienceProtection.protected(new_identity())
tests/experience/test_experience_protection.py:87:def test_explicit_authorization_allows_protected_operation_gate():
tests/experience/test_experience_protection.py:88:    protection = ExperienceProtection.protected(new_identity())
tests/experience/test_experience_protection.py:94:    protection = ExperienceProtection.protected(new_identity())
tests/experience/test_experience_protection.py:101:    protection = ExperienceProtection.protected(new_identity())
tests/experience/test_experience_persistence.py:11:    recover_experience,
tests/experience/test_experience_persistence.py:12:    serialize_experience,
tests/experience/test_experience_persistence.py:19:    data = serialize_experience(experience)
tests/experience/test_experience_persistence.py:31:    data = serialize_experience(experience)
tests/experience/test_experience_persistence.py:39:    data = serialize_experience(before)
tests/experience/test_experience_persistence.py:40:    after = recover_experience(data)
tests/experience/test_experience_persistence.py:48:    data = serialize_experience(before)
tests/experience/test_experience_persistence.py:61:    after = recover_experience(data)
tests/experience/test_experience_persistence.py:69:    after = recover_experience(
tests/experience/test_experience_persistence.py:70:        serialize_experience(before)
tests/experience/test_experience_persistence.py:79:    after = recover_experience(
tests/experience/test_experience_persistence.py:80:        serialize_experience(before)
tests/experience/test_experience_persistence.py:88:        serialize_experience(object())
tests/experience/test_experience_persistence.py:109:        recover_experience(data)
tests/experience/test_experience_persistence.py:114:    data = serialize_experience(experience)
tests/experience/test_experience_persistence.py:118:        recover_experience(data)
tests/experience/test_experience_persistence.py:123:    data = serialize_experience(experience)
tests/experience/test_experience_persistence.py:127:        recover_experience(data)
tests/experience/test_experience_persistence.py:132:    data = serialize_experience(experience)
tests/experience/test_experience_persistence.py:136:        recover_experience(data)
tests/experience/test_experience_persistence.py:141:    data = serialize_experience(before)
tests/experience/test_experience_persistence.py:144:    recover_experience(data)
tests/experience/test_experience_recovery.py:8:    JsonFileExperienceRepository,
tests/experience/test_experience_recovery.py:18:    repository = JsonFileExperienceRepository(store)
tests/experience/test_experience_recovery.py:29:    writer = JsonFileExperienceRepository(store)
tests/experience/test_experience_recovery.py:33:    reader = JsonFileExperienceRepository(store)
tests/experience/test_experience_recovery.py:43:    first = JsonFileExperienceRepository(store)
tests/experience/test_experience_recovery.py:51:    second = JsonFileExperienceRepository(store)
tests/experience/test_experience_recovery.py:60:    repository = JsonFileExperienceRepository(store)
tests/experience/test_experience_recovery.py:71:    repository = JsonFileExperienceRepository(store)
tests/experience/test_experience_recovery.py:79:    repository = JsonFileExperienceRepository(store)
tests/experience/test_experience_recovery.py:84:    replacement_repository = JsonFileExperienceRepository(store)
tests/experience/test_experience_recovery.py:95:    repository = JsonFileExperienceRepository(store)
tests/experience/test_experience_recovery.py:108:    repository = JsonFileExperienceRepository(store)
tests/experience/test_experience_recovery.py:117:    repository = JsonFileExperienceRepository(store)
tests/experience/test_experience_recovery.py:135:    replacement = JsonFileExperienceRepository(store)
tests/experience/test_experience_recovery.py:143:    repository = JsonFileExperienceRepository(store)
tests/experience/test_experience_recovery.py:153:def test_storage_does_not_supply_authority(tmp_path):
tests/experience/test_experience_recovery.py:156:    repository = JsonFileExperienceRepository(store)
tests/experience/test_experience_recovery.py:160:    recovered = JsonFileExperienceRepository(store).get(
tests/experience/test_experience_recovery.py:164:    assert not hasattr(recovered, "authority")
tests/experience/test_experience_recovery.py:165:    assert not hasattr(repository, "authority")
tests/experience/harness/pcc01_restart_writer.py:18:    JsonFileExperienceRepository,
tests/experience/harness/pcc01_restart_writer.py:31:    repository = JsonFileExperienceRepository(store_path)
tests/experience/harness/pcc01_restart_reader.py:18:    JsonFileExperienceRepository,
tests/experience/harness/pcc01_restart_reader.py:41:    repository = JsonFileExperienceRepository(store_path)
tests/experience/harness/pcc01_protection_restart_writer.py:10:    JsonFileExperienceRepository,
tests/experience/harness/pcc01_protection_restart_writer.py:13:    ExperienceProtection,
tests/experience/harness/pcc01_protection_restart_writer.py:23:    protection = ExperienceProtection.protected(
tests/experience/harness/pcc01_protection_restart_writer.py:27:    repository = JsonFileExperienceRepository(store_path)
tests/experience/harness/pcc01_protection_restart_writer.py:35:        "is_protected": protection.is_protected,
tests/experience/harness/pcc01_protection_restart_reader.py:10:    JsonFileExperienceRepository,
tests/experience/harness/pcc01_protection_restart_reader.py:27:    repository = JsonFileExperienceRepository(store_path)
tests/experience/test_experience_protection_restart.py:78:    assert before["is_protected"] is True
tests/experience/test_experience_protection_restart.py:79:    assert before["protection_state"] == "protected"
tests/experience/test_experience_protection_restart.py:108:    # ExperienceProtection as part of recovered Experience.
```

## 7. Runtime Serialization Observation

```text
Experience identity: 2a113755-06de-4eac-a86b-cb44d2ad95d1
Protection identity: 2a113755-06de-4eac-a86b-cb44d2ad95d1
Protection state: protected
Serialized fields: ['created_at', 'experience_id', 'state']
Serialized representation: {'experience_id': '2a113755-06de-4eac-a86b-cb44d2ad95d1', 'created_at': '2026-08-13T18:26:48.488413+00:00', 'state': 'CREATED'}
```

PASS: Protection references Experience identity.
PASS: Protection does not own or replace Experience identity.
PASS: current Experience serialization remains Protection-free.

## 8. Candidate Anatomical Designs

The following are DESIGN CANDIDATES ONLY.

No candidate is accepted or implemented by RUN 024.

### Candidate A — Collapse Protection into Experience serialization

Persist Protection fields directly inside the serialized Experience representation.

**Assessment:** REJECT AS DEFAULT DIRECTION.

Reason:

- risks collapsing Protection into Experience;
- changes the deliberately minimal Core Experience serialization;
- weakens organ separation;
- could make persisted representation appear authoritative.

### Candidate B — Independent Protection Repository

Protection remains an independent organ keyed by ExperienceId and receives its own persistence repository.

Conceptual anatomy:

```text
Experience
    |
    +---- ExperienceId ----> Experience Repository
    |
    +---- ExperienceId ----> Protection Repository
```

Recovery would reconstruct the Experience and independently recover the Protection condition associated with the same ExperienceId.

**Assessment:** STRONG CANDIDATE.

### Candidate C — Composite Persistence Envelope

A higher-level persistence envelope stores representations from multiple independent organs without making any one organ part of another.

Conceptual anatomy:

```text
Persistent Experience Envelope
    |
    +---- Core Experience representation
    +---- Protection representation
```

The envelope coordinates persistence but does not redefine Experience.

**Assessment:** POSSIBLE LATER INTEGRATION PATTERN.

### Candidate D — Derive Protection after recovery

Protection is reconstructed from some external policy or authority rather than persisted as historical state.

**Assessment:** NOT JUSTIFIED BY CURRENT EVIDENCE.

No existing accepted artifact inspected by this RUN demonstrates that Protection is intended to be derived.


## 9. Mandatory Protection Persistence Constraints

Any future implementation must preserve all of the following:

1. Experience remains independent from Protection.
2. Protection remains associated with exactly one ExperienceId.
3. Protection persistence must not generate a replacement ExperienceId.
4. Recovery must not silently change PROTECTED into UNPROTECTED.
5. Missing Protection persistence must be represented explicitly.
6. Corrupt Protection persistence must fail explicitly.
7. Storage does not become Experience.
8. Persistence does not become authority.
9. Persisted PROTECTED state does not itself grant authorization.
10. Explicit authorization remains separate from stored Protection state.
11. Protection persistence must not introduce Session ownership.
12. Protection persistence must not introduce Memory.
13. Protection persistence must not introduce Evidence.
14. Protection persistence must not introduce raw dialogue.
15. Protection persistence must not modify Canon.
16. Real process restart behavior must eventually be demonstrated.
17. Existing Experience identity continuity evidence must remain valid.
18. Existing Core Experience regression behavior must remain intact.

## 10. Proposed Protection Persistence Physiology

**Proposed direction for Human/GPT review:**

Protection should remain a separate organ with a separate persistence contract keyed by ExperienceId.

Proposed tissue:

```text
ExperienceProtection
        |
        v
Protection Serialization
        |
        v
Protection Repository
        |
        v
persistent storage

Recovery:

ExperienceId
   |
   +--> Experience Repository --> Experience
   |
   +--> Protection Repository --> ExperienceProtection
```

The two recovered organs meet through the same ExperienceId.

They do not become the same object.

The Protection repository records protection condition.

It does NOT record or grant operation authorization.

Authorization remains an explicit input to protected operations.

This preserves:

- Experience != Protection
- Storage != Experience
- Persistence != authority
- identity ownership by Experience
- explicit authorization semantics

## 11. Required Future Behavioral Tests

Before Protection continuity can be declared demonstrated, future implementation must prove at least:

1. unprotected Protection state serializes and recovers.
2. protected Protection state serializes and recovers.
3. recovered Protection preserves ExperienceId exactly.
4. recovery never calls ExperienceId.create().
5. missing Protection record is handled explicitly.
6. corrupt Protection representation is rejected explicitly.
7. repository key and embedded ExperienceId disagreement is rejected.
8. protected state survives repository instance replacement.
9. protected state survives real Process A death and Process B recovery.
10. Process A PID != Process B PID.
11. Experience identity before restart == Experience identity after restart.
12. Protection state before restart == Protection state after restart.
13. persisted PROTECTED state does not authorize an operation automatically.
14. unauthorized protected operation remains rejected after restart.
15. explicit authorization remains required after restart.
16. Experience serialization remains independent from Protection serialization.
17. complete tests/experience regression remains PASS.

## 12. Inspection Boundary

```text
tests/experience/harness/pcc01_protection_restart_reader.py
tests/experience/harness/pcc01_protection_restart_writer.py
tests/experience/test_experience_protection_restart.py
work/implementation-reports/PCC-01/PCC-01_PROTECTION_PERSISTENCE_PHYSIOLOGY_DESIGN_INSPECTION_RUN_024.md
work/implementation-reports/PCC-01/PCC-01_PROTECTION_RESTART_CAUSAL_INSPECTION_RUN_023.md
work/implementation-reports/PCC-01/PCC-01_PROTECTION_RESTART_CONTINUITY_REPORT_RUN_022.md
work/implementation-reports/PCC-01/PCC-01_RUN020_EVIDENCE_CONSERVATION_REPORT_RUN_021.md
```

PASS: no tracked software modified by RUN 024.

## 13. Design Finding

**Recommended architecture for next review:** Independent Protection persistence keyed by ExperienceId.

This is a proposal derived from the accepted boundaries and current executable anatomy.

It is NOT Canon.

It is NOT implementation.

It does NOT constitute Human Acceptance.

## 14. Central Invariant

`ID_before_restart == ID_after_restart`

**Status:** DEMONSTRATED LOCALLY for Core Experience identity.

**Protection continuity:** NOT DEMONSTRATED.

## 15. PCC-01 Status

**Implementation Status:** NOT DEMONSTRATED

**Canonical Status:** NOT CANON

**Production Status:** NOT PRODUCTION-READY

## 16. Conservation

No `git add` performed.

No commit performed.

No push performed.

## 17. Final Result

**RUN 024: PASS**

**Recommended next organ:** Protection Persistence Repository.

**NEXT REQUIRED ACTION:** GPT/Human review of this design inspection before software construction.

---

END OF PCC-01 PROTECTION PERSISTENCE PHYSIOLOGY DESIGN INSPECTION — RUN 024
