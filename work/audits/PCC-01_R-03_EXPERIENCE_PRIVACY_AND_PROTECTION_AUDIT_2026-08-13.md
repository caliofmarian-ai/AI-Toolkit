# R-03 — Intimitatea organismului — ce are voie să păstreze și ce trebuie să protejeze

Version: 0.1.0

Status: Research / Reconciliation Audit — Human Decisions Required

Production Capability: `PCC-01 — Persistent Experience`

Reconciliation Item: `R-03 — Security / Secrets / Privacy`

Human Authority: Owner

Date: 2026-08-13

---

# 1. Scopul auditului

Acest audit cercetează hotarul dintre:

- experiența pe care organismul trebuie să o poată păstra;
- informația pe care organismul nu are voie să o expună;
- informația care trebuie protejată;
- informația care trebuie mascată;
- informația care trebuie exclusă din anumite forme de persistență;
- informația care poate necesita ștergere;
- informația care poate fi accesată numai de anumite identități sau organe.

R-02 a răspuns la întrebarea:

**Ce merită organismul să păstreze?**

R-03 introduce o întrebare diferită:

**Chiar dacă ceva este important, are organismul voie să îl păstreze și, dacă da, în ce formă și cine are voie să îl vadă?**

---

# 2. Sensul uman al problemei

Un organism matur nu poate confunda memoria cu expunerea totală.

Un om poate trăi o experiență fără ca fiecare detaliu al acelei experiențe să fie disponibil tuturor.

La fel, AI-Toolkit trebuie să poată spune:

**„Am trăit acest eveniment, dar anumite părți ale lui sunt intime sau periculoase și trebuie protejate.”**

Intimitatea nu înseamnă uitare.

Protecția nu înseamnă falsificarea trecutului.

Secretul nu înseamnă că evenimentul nu a existat.

---

# 3. De ce R-03 este necesar

Persistent Experience poate primi experiență din:

- conversații Human–AI;
- terminal;
- Git;
- GitHub;
- dashboard;
- runtime;
- fișiere;
- integrări;
- procese de dezvoltare;
- instrumente externe;
- viitoare interfețe.

Aceste surse pot conține accidental sau intenționat informații care nu trebuie reproduse liber în memoria organismului.

---

# 4. Problema fundamentală

Dacă organismul păstrează totul fără protecție, poate conserva și expune:

- parole;
- tokenuri;
- chei API;
- chei private;
- secrete de integrare;
- configurații sensibile;
- informații personale;
- conversații private;
- date despre alte persoane;
- informații comerciale sensibile;
- identificatori de sesiune;
- credențiale temporare;
- materiale care ulterior trebuie eliminate.

Prin urmare:

**fidelitatea experienței nu poate însemna copiere necontrolată.**

---

# 5. Ce există deja în AI-Toolkit — Runtime Secret Manager

Repository-ul conține:

`lib/python/runtime/secrets.py`

Acesta definește un `SecretManager`.

Comportamentul declarat este:

- secretele sunt încărcate din environment variables;
- valorile secrete nu trebuie scrise pe disc;
- valorile secrete nu trebuie introduse în loguri;
- rapoartele trebuie să arate numai existența sau absența secretului;
- valoarea efectivă nu trebuie expusă.

Acesta este un precedent software important pentru R-03.

---

# 6. Secrete recunoscute deja de runtime

Implementarea existentă recunoaște explicit exemple precum:

- `GITHUB_TOKEN`;
- `GITHUB_WEBHOOK_SECRET`;
- `TELEGRAM_BOT_TOKEN`;
- `TELEGRAM_CHAT_ID`.

Această listă nu trebuie interpretată ca lista definitivă a tuturor informațiilor sensibile.

Ea demonstrează numai că organismul ancestral posedă deja noțiunea de secret runtime.

---

# 7. Principiu moștenibil din Secret Manager

Din comportamentul existent poate fi extras următorul principiu candidat:

**Organismul poate cunoaște existența unui secret fără să păstreze sau să expună valoarea secretului în experiența sa obișnuită.**

Exemplu:

în loc să păstreze:

`GITHUB_TOKEN=<valoare-secretă>`

organismul poate păstra semantic:

`GITHUB_TOKEN was present`

fără valoarea efectivă.

---

# 8. Ce există deja — Conversation Engine

Documentul existent:

`CANON-039 — AI CTO Conversation Engine Specification`

declară că istoricul conversațiilor nu trebuie să expună:

- Secrets;
- Tokens;
- Passwords;
- Private Keys;
- Sensitive Configuration.

Aceasta este o regulă direct relevantă pentru experiența provenită din conversații.

---

# 9. Tensiunea Conversation Engine ↔ Persistent Experience

Conversation Engine cere continuitate.

Persistent Experience cere păstrarea experienței.

Security cere neexpunerea secretelor.

Aceste cerințe trebuie să funcționeze simultan.

Organismul nu poate rezolva problema spunând:

**„păstrez totul pentru continuitate.”**

Dar nici:

**„șterg orice conversație în care apare ceva sensibil.”**

Este necesară o fiziologie intermediară.

---

# 10. Ce există deja — CSL Security Model

`CSL-027 — Security Model Specification` cere, între altele:

- trust boundaries;
- least privilege;
- explicit capability grants;
- audit events pentru operații sensibile;
- threat model documentat și versionat;
- aprobarea prin governance a excepțiilor de securitate.

Aceste principii sunt relevante pentru R-03.

---

# 11. Limitele de încredere

Organismul nu trebuie să considere toate organele și toate interfețele la fel de sigure.

Trebuie să existe limite între:

- sursă;
- captură;
- persistență;
- memorie;
- AI;
- dashboard;
- integrări;
- export;
- loguri;
- utilizatori;
- servicii externe.

Faptul că o informație poate intra într-un organ nu înseamnă că toate celelalte organe trebuie să o poată vedea.

---

# 12. Principiul privilegiului minim

Un organ trebuie să primească numai accesul necesar funcției sale.

Exemplu conceptual:

un organ care construiește rezumatul unei sesiuni poate avea nevoie să știe că autentificarea GitHub a funcționat.

Nu rezultă că are nevoie de valoarea tokenului GitHub.

---

# 13. Accesul trebuie să fie explicit

Accesul la informații sensibile nu trebuie să apară accidental prin simplul fapt că două organe folosesc aceeași bază de date sau același fișier.

Accesul trebuie să fie justificabil și controlabil.

---

# 14. Operațiile sensibile trebuie să lase urme

CSL introduce și principiul auditabilității operațiilor sensibile.

Pentru organism, aceasta produce o distincție importantă:

**secretul nu trebuie expus, dar operația asupra secretului poate necesita o urmă verificabilă.**

Exemplu:

organismul poate păstra:

`GitHub credential rotated`

fără să păstreze credentialul propriu-zis în jurnalul experienței.

---

# 15. Ce există deja — Identity and Authentication

`CANON-061 — Identity and Authentication Specification` definește principii precum:

- User Ownership;
- Least Privilege;
- Privacy by Design;
- Zero Trust;
- Secure by Default;
- No Hidden Permissions;
- Auditable Decisions.

Acestea sunt direct relevante pentru viitoarea fiziologie R-03.

---

# 16. Parolele

CANON-061 spune că parolele:

- nu trebuie păstrate în plain text;
- trebuie protejate prin mecanisme moderne de hashing;
- trebuie să suporte procese controlate de recuperare și rotație.

Pentru Persistent Experience rezultă un hotar puternic:

**experiența nu trebuie să transforme parola brută într-o amintire.**

---

# 17. API Keys

CANON-061 spune că API Keys nu trebuie să își expună secretul după creare.

Persistent Experience nu trebuie să anuleze această protecție prin capturarea ulterioară a valorii într-un transcript, raport sau rezumat.

---

# 18. Sesiunile

Sesiunile autentificate pot conține:

- Session ID;
- Refresh Token;
- client metadata;
- identitate;
- timp;
- context de acces.

Nu toate aceste elemente au aceeași sensibilitate.

R-03 trebuie să permită clasificarea lor separată.

---

# 19. Privacy by Design

CANON-061 afirmă:

**Privacy by Design.**

De asemenea, afirmă că trebuie procesată numai informația necesară funcționării platformei.

Acest principiu limitează tentația unui organism epistemic de a păstra informație numai pentru că tehnic poate.

---

# 20. Prima concluzie a auditului

AI-Toolkit nu pornește de la zero.

Strămoșii organismului conțin deja:

- secret management;
- neexpunerea secretelor;
- privacy by design;
- least privilege;
- zero trust;
- auditabilitate;
- controlul accesului;
- protecția parolelor;
- protecția API keys;
- separarea identităților.

Problema este că aceste reguli nu sunt încă reunite într-o fiziologie completă pentru Persistent Experience.

---

# 21. Ce lipsește

Nu este încă demonstrată o politică unificată care să răspundă pentru fiecare fragment de experiență:

1. este sigur de păstrat?
2. trebuie mascat?
3. trebuie exclus?
4. trebuie criptat?
5. cine îl poate vedea?
6. cât timp poate exista?
7. poate fi reamintit AI-ului?
8. poate fi exportat?
9. poate apărea într-un raport?
10. poate fi șters?
11. cine poate autoriza ștergerea?
12. trebuie păstrată dovada că a existat fără conținutul său?

---

# 22. Experiența trebuie să poată avea intimitate

R-03 introduce conceptul candidat:

**Experience Privacy Boundary**

Acesta reprezintă hotarul dintre:

- experiența trăită;
- experiența păstrată;
- experiența vizibilă;
- experiența reamintibilă;
- experiența exportabilă.

Acestea nu trebuie tratate ca fiind automat identice.

---

# 23. A trăi nu înseamnă a copia integral

Dacă terminalul primește temporar un token, organismul a trăit un eveniment în care tokenul a fost utilizat.

Dar fidelitatea experienței nu cere neapărat păstrarea valorii tokenului.

Organismul poate păstra evenimentul:

**„credentialul a fost furnizat și folosit”**

fără valoarea credentialului.

---

# 24. A proteja nu înseamnă a falsifica

Redactarea trebuie să păstreze adevărul structural.

Exemplu:

Original temporar:

`Authorization: Bearer <SECRET>`

Experiență protejată:

`Authorization credential present [REDACTED]`

Organismul știe că un credential a existat.

Nu păstrează valoarea lui în stratul obișnuit al experienței.

---

# 25. Clase candidate de sensibilitate

Auditul identifică necesitatea unor clase de sensibilitate.

Nu le declară încă normative.

Clase candidate:

- PUBLIC;
- INTERNAL;
- PRIVATE;
- SENSITIVE;
- SECRET;
- HIGHLY RESTRICTED.

Numele finale necesită reconciliere și eventual decizie umană.

---

# 26. PUBLIC

Material care poate fi expus fără restricții speciale.

Exemple posibile:

- documentație publică;
- commit public;
- issue public;
- informații intenționat publicate.

Public nu înseamnă automat important.

---

# 27. INTERNAL

Material destinat funcționării interne a organismului, dar care nu reprezintă în mod necesar un secret.

Exemple:

- stare internă;
- raționamente operaționale persistabile conform politicii;
- metadate interne;
- diagnostice.

Necesită o definiție ulterioară precisă.

---

# 28. PRIVATE

Material legitim pentru proprietar sau pentru un spațiu privat, dar care nu trebuie expus public.

Exemple posibile:

- conversații private;
- preferințe;
- proiecte private;
- decizii personale de lucru.

---

# 29. SENSITIVE

Material a cărui expunere poate produce prejudicii, pierderi, încălcarea intimității sau probleme operaționale.

Exemple:

- date personale;
- anumite informații de identitate;
- configurații sensibile;
- informații despre terți.

---

# 30. SECRET

Material care nu trebuie să apară în experiența obișnuită în formă brută.

Exemple:

- passwords;
- API secret values;
- access tokens;
- private keys;
- webhook secrets.

---

# 31. HIGHLY RESTRICTED

Auditul păstrează această clasă numai ca ipoteză de proiectare.

Ar putea fi necesară pentru informații cu restricții speciale.

Nu este acceptată prin acest audit.

---

# 32. Clasificarea nu trebuie să fie doar semantică

Organismul nu trebuie să se bazeze exclusiv pe AI pentru a „ghici” dacă ceva este secret.

Trebuie să poată utiliza și semnale deterministe.

Exemple:

- numele variabilei;
- tipul credentialului;
- proveniența;
- formatul cunoscut;
- clasificarea explicită;
- politica sursei.

---

# 33. Detectarea secretelor

Un viitor mecanism poate detecta tipare precum:

- password fields;
- authorization headers;
- bearer tokens;
- API keys;
- private key blocks;
- secret environment variables;
- credential files.

Acest audit nu implementează detectorul.

---

# 34. Detectarea nu este infailibilă

Nici reguli deterministe, nici AI-ul nu pot garanta identificarea perfectă a tuturor informațiilor sensibile.

Prin urmare, arhitectura trebuie să presupună posibilitatea:

- false positive;
- false negative;
- clasificare incompletă;
- informație necunoscută.

---

# 35. Protecție înainte de persistență

Principiu candidat:

**Atunci când este posibil, informația evident secretă trebuie protejată înainte să intre în depozitul persistent obișnuit al experienței.**

Este mai sigur să nu depozitezi secretul decât să îl depozitezi și să speri că nimeni nu îl va vedea.

---

# 36. Redactarea

Redactarea înseamnă înlocuirea valorii sensibile cu o reprezentare sigură.

Exemple:

`[REDACTED:TOKEN]`

`[REDACTED:PASSWORD]`

`[REDACTED:PRIVATE_KEY]`

Reprezentarea finală trebuie standardizată ulterior.

---

# 37. Excluderea

Unele informații pot necesita excludere completă dintr-un anumit strat.

Exemplu candidat:

valoarea brută a unei parole nu trebuie să intre în Persistent Experience.

Evenimentul utilizării parolei poate fi păstrat fără valoare.

---

# 38. Protecția prin referință

În anumite cazuri, experiența poate păstra o referință către un sistem securizat fără să copieze conținutul.

Exemplu conceptual:

`credential_ref: runtime-secret://github/main`

în loc de valoarea secretă.

Schema este numai ilustrativă.

---

# 39. Criptarea

Unele informații sensibile pot necesita persistență reală pentru funcționare.

În asemenea situații, criptarea poate fi necesară.

Dar:

**criptarea nu transformă automat o informație într-o experiență sigură.**

Trebuie controlate și:

- cheile;
- accesul;
- decriptarea;
- logurile;
- exporturile;
- backupurile.

---

# 40. Accesul

R-03 trebuie să răspundă nu numai:

**„păstrăm?”**

ci și:

**„cine vede?”**

Accesul poate depinde de:

- Human Authority;
- identity;
- role;
- workspace;
- organ;
- purpose;
- environment.

---

# 41. Omul și propriile informații

Principiu candidat:

**proprietarul trebuie să aibă control semnificativ asupra informației private care îl privește, în limitele obligațiilor tehnice, de securitate și legale aplicabile.**

Detaliile nu sunt încă reconciliate.

---

# 42. Informațiile despre alte persoane

Persistent Experience poate primi informații despre persoane care nu sunt proprietarul organismului.

Aceste informații nu trebuie tratate automat ca proprietatea nelimitată a organismului.

R-03 trebuie să distingă:

- informația despre owner;
- informația despre colaboratori;
- informația despre clienți;
- informația despre terți;
- informația publică;
- informația furnizată sub așteptare de confidențialitate.

---

# 43. Conversațiile Human–AI

R-01 a stabilit importanța conversației ca sursă de experiență.

R-03 introduce limita:

**faptul că omul spune ceva AI-ului nu trebuie interpretat automat ca permisiune universală de publicare, export sau expunere către alte organe.**

Captura și permisiunea de utilizare nu sunt automat același lucru.

---

# 44. Terminalul

Terminalul este o sursă cu risc ridicat deoarece poate conține:

- environment variables;
- tokens;
- URLs semnate;
- credentials;
- output de autentificare;
- configurații;
- date din fișiere private.

Captura terminalului necesită filtrare specială.

---

# 45. Git

Git este istorie persistentă.

Un secret introdus accidental într-un commit poate supraviețui chiar dacă este eliminat din versiunea curentă.

Persistent Experience nu trebuie să trateze existența într-un commit drept dovadă că informația este sigură pentru reamintire.

---

# 46. GitHub

GitHub poate conține:

- repository public;
- repository privat;
- issues;
- PRs;
- Actions;
- logs;
- secrets metadata;
- utilizatori;
- organizații.

Politica de experiență trebuie să respecte limitele sursei și ale identității.

---

# 47. Dashboard

Dashboard-ul poate deveni o suprafață de expunere.

Un secret protejat corect în storage poate deveni compromis dacă dashboard-ul îl afișează.

Prin urmare:

**persistența sigură și prezentarea sigură sunt probleme distincte.**

---

# 48. AI Partners

Viitorii parteneri AI nu trebuie să primească automat acces la întreaga experiență persistentă.

Accesul lor trebuie să fie limitat de:

- scop;
- identitate;
- permisiune;
- sensibilitate;
- necesitate.

---

# 49. Furnizorii AI externi

Transmiterea unui fragment către un furnizor AI extern este o formă de ieșire din organism.

Prin urmare, înainte de transmitere trebuie să existe posibilitatea de:

- filtrare;
- minimizare;
- redactare;
- autorizare;
- audit.

Politica exactă necesită reconciliere ulterioară.

---

# 50. Reamintirea

O informație poate fi legitim păstrată, dar neeligibilă pentru reamintire automată.

Exemplu:

o informație privată poate exista în storage protejat fără să fie introdusă automat în fiecare context AI.

---

# 51. Exportul

Exportul trebuie tratat separat de citirea internă.

Organismul poate permite utilizarea internă a unui material fără să permită exportarea lui într-un raport sau document public.

---

# 52. Rapoartele

Rapoartele sunt o suprafață importantă de risc.

Un raport trebuie să poată spune:

- secret detected;
- credential missing;
- authentication failed;

fără să publice valoarea secretului.

---

# 53. Logurile

Logurile sunt experiență operațională, dar pot deveni o sursă de scurgere.

Principiu candidat:

**logurile nu trebuie să devină un canal secundar prin care protecțiile secretelor sunt ocolite.**

---

# 54. Erorile

Mesajele de eroare pot conține accidental:

- request payload;
- headers;
- filesystem paths;
- environment;
- credentials;
- personal data.

Error capture trebuie să respecte R-03.

---

# 55. Debugging

Debugging-ul cere uneori informație suplimentară.

Dar „debug mode” nu trebuie să însemne:

**dezactivează intimitatea organismului.**

Accesul suplimentar trebuie să fie controlat și auditabil.

---

# 56. Backupurile

Ștergerea din storage activ nu garantează ștergerea din backup.

O politică matură trebuie să definească relația dintre:

- active storage;
- archive;
- backup;
- immutable evidence;
- deletion.

Acest audit nu stabilește încă politica finală.

---

# 57. Ștergerea

R-02 a stabilit că ștergerea este o decizie epistemic importantă.

R-03 adaugă:

**uneori protecția intimității poate cere ștergere.**

Prin urmare există o tensiune reală între:

- continuitate;
- auditabilitate;
- dreptul/obligația de eliminare;
- integritatea istoriei.

Aceasta nu trebuie ascunsă.

---

# 58. Ștergerea conținutului și păstrarea evenimentului

O soluție conceptuală posibilă este separarea:

**conținutului**

de

**dovezii că evenimentul a existat.**

Exemplu:

conținutul sensibil poate fi eliminat, dar organismul poate păstra:

`Sensitive material deleted by authorized decision at T`

fără materialul eliminat.

Aceasta este o direcție candidat, nu încă o regulă finală.

---

# 59. Dreptul de a uita și memoria organismului

O viitoare politică trebuie să reconcilieze eventualele obligații de ștergere cu necesitatea de audit.

Organismul nu poate presupune că „memorie permanentă” este întotdeauna legal sau legitim.

---

# 60. Autoritatea AI

AI-ul poate ajuta la:

- detectare;
- clasificare;
- recomandare;
- redactare;
- semnalarea riscului.

Dar AI-ul nu trebuie să primească implicit autoritate nelimitată de a:

- publica;
- declasifica;
- exporta;
- dezvălui;
- șterge definitiv;

material sensibil.

---

# 61. Autoritatea umană

Deciziile majore de politică trebuie să rămână sub Human Authority.

Aceasta include cel puțin definirea principiilor care guvernează:

- sensibilitatea;
- retenția;
- accesul;
- ștergerea;
- excepțiile;
- declasificarea.

---

# 62. Protecția implicită

Principiu candidat:

**când organismul are motive puternice să creadă că o valoare este secretă, comportamentul implicit trebuie să fie protecția, nu expunerea.**

---

# 63. Incertitudinea

Dacă organismul nu știe dacă o informație este sensibilă, nu trebuie să aleagă automat expunerea maximă.

Poate fi necesară o stare:

**sensitivity uncertain**

care cere tratament conservator până la clarificare.

---

# 64. False positives

Protecția excesivă poate ascunde informații utile.

De aceea omul trebuie să poată contesta o clasificare greșită.

---

# 65. False negatives

O informație sensibilă poate scăpa detectorului.

Prin urmare sistemul trebuie să permită:

- corectare ulterioară;
- redactare retroactivă unde este posibil;
- revocarea credentialului;
- investigarea expunerii;
- auditarea incidentului.

---

# 66. Incidentul de intimitate

Organismul trebuie să poată recunoaște un eveniment de tip:

**privacy/security incident**

fără să reproducă necontrolat tocmai materialul compromis.

---

# 67. Proveniența

Pentru o informație sensibilă poate conta:

- de unde a venit;
- cine a furnizat-o;
- în ce context;
- cu ce permisiune;
- pentru ce scop.

Proveniența trebuie păstrată fără a deveni ea însăși o scurgere.

---

# 68. Scopul utilizării

Accesul la experiență nu trebuie justificat numai prin:

**„organismul o are.”**

Poate fi necesar și:

**„organul are nevoie de ea pentru această funcție.”**

---

# 69. Minimizarea

Principiu candidat:

**un organ trebuie să primească cea mai mică porțiune de informație suficientă pentru funcția sa.**

Aceasta extinde least privilege de la acțiuni la informație.

---

# 70. Separarea stocării de prezentare

Trebuie separate conceptual:

- ce există;
- ce poate fi citit;
- ce poate fi reamintit;
- ce poate fi afișat;
- ce poate fi exportat.

Un singur câmp `stored=true` nu este suficient pentru fiziologia matură.

---

# 71. Separarea identității de conținut

Uneori organismul poate avea nevoie de eveniment fără identificarea completă a persoanei.

Pot fi necesare tehnici precum:

- pseudonymization;
- minimization;
- selective redaction.

Politica finală nu este încă stabilită.

---

# 72. Integritatea după redactare

Redactarea nu trebuie să producă o istorie falsă.

Organismul trebuie să poată distinge:

- valoare absentă;
- valoare necunoscută;
- valoare necolectată;
- valoare eliminată;
- valoare redactată;
- valoare inaccesibilă.

Aceste stări nu sunt semantic identice.

---

# 73. Explicabilitatea protecției

Când o informație este ascunsă, sistemul trebuie să poată explica, în limite sigure:

- că protecția există;
- ce clasă de regulă a produs-o;
- cine/ce politică a autorizat-o;
- dacă poate fi contestată.

---

# 74. Fără permisiuni ascunse

În acord cu principiile Identity Architecture:

**organismul nu trebuie să aibă permisiuni ascunse asupra intimității omului.**

Dacă un organ poate accesa material sensibil, acest fapt trebuie să fie justificabil.

---

# 75. Fără memorii secrete ale AI-ului

Principiu candidat:

**AI-ul nu trebuie să construiască o memorie paralelă neinspectabilă care ocolește regulile Persistent Experience.**

Dacă informația este persistentă și utilizată de organism, existența și regimul ei trebuie să fie guvernabile.

---

# 76. Relația cu R-01

R-01 stabilește conversația Human–AI ca sursă importantă de experiență.

R-03 limitează această captură:

**capturarea dialogului nu autorizează capturarea neprotejată a secretelor.**

---

# 77. Relația cu R-02

R-02 spune că experiența importantă trebuie păstrată.

R-03 adaugă:

**importanța nu anulează intimitatea.**

O informație poate fi simultan:

- foarte importantă;
- foarte sensibilă.

Organismul trebuie să poată respecta ambele adevăruri.

---

# 78. Relația cu viitoarea Memorie

Materialul sensibil nu trebuie promovat automat în memoria activă.

Memory trebuie să moștenească restricțiile experienței din care derivă.

---

# 79. Relația cu Knowledge

Transformarea unei experiențe sensibile în Knowledge nu trebuie să spele restricțiile de securitate.

Derivarea nu produce automat declasificare.

---

# 80. Relația cu Canon

Canonul nu trebuie să conțină accidental secrete numai pentru că acestea au apărut în dovezile care au condus la o decizie.

Canonul poate păstra regula fără valoarea secretă.

---

# 81. Moștenirea restricțiilor

Principiu candidat:

**o reprezentare derivată trebuie să moștenească restricțiile relevante ale sursei, cu excepția cazului în care există un proces explicit și autorizat de declasificare.**

---

# 82. Declasificarea

Organismul poate avea nevoie de un proces prin care materialul anterior sensibil devine mai puțin restricționat.

Această schimbare nu trebuie făcută implicit de AI.

---

# 83. Reclasificarea

Sensibilitatea se poate schimba.

Exemplu:

un token revocat nu mai oferă acces, dar istoricul lui poate rămâne sensibil din alte motive.

Prin urmare, expirarea unui secret nu înseamnă automat că valoarea devine publică.

---

# 84. Protecția trebuie să supraviețuiască transformărilor

Restricțiile trebuie considerate atunci când experiența este:

- rezumată;
- indexată;
- căutată;
- reamintită;
- transformată;
- exportată;
- folosită de AI;
- convertită în evidence;
- convertită în knowledge.

---

# 85. Problema copiilor derivate

Dacă un secret este redactat în sursa principală, dar rămâne într-un index, cache sau raport, protecția este incompletă.

R-03 trebuie să considere întregul traseu al informației.

---

# 86. Nevoia unui registru al protecției

Organismul matur poate necesita o evidență a regulilor aplicate materialului sensibil.

Aceasta ar putea include conceptual:

- classification;
- protection action;
- authority;
- timestamp;
- source;
- derived artifacts;
- retention status.

Schema finală nu este definită aici.

---

# 87. Nevoia unei fiziologii de urgență

Dacă un secret real intră accidental în Persistent Experience, organismul trebuie să poată reacționa.

Un viitor răspuns poate include:

1. detectare;
2. izolare;
3. oprirea propagării;
4. redactare;
5. identificarea copiilor;
6. notificarea omului;
7. revocarea credentialului unde este necesar;
8. auditarea incidentului.

Acest audit nu implementează mecanismul.

---

# 88. Ce NU trebuie făcut

R-03 nu trebuie implementat ca:

**„AI-ul decide ce este privat și ascunde ce vrea.”**

Nici ca:

**„păstrăm absolut tot pentru că memoria trebuie să fie perfectă.”**

Nici ca:

**„ștergem orice pare sensibil și pierdem istoria.”**

Este necesar un echilibru controlat și explicabil.

---

# 89. Concluzia principală R-03

Persistent Experience are nevoie de un **hotar de intimitate și protecție** propriu.

Acest hotar trebuie să permită organismului să păstreze adevărul experienței fără să transforme experiența într-un depozit necontrolat de secrete și date private.

Organismul trebuie să poată spune simultan:

**„acest eveniment a existat”**

și

**„această parte a lui nu poate fi expusă.”**

---

# 90. Principii propuse autorității umane

Auditul formulează următoarele principii pentru decizia omului.

Acestea NU sunt acceptate automat prin existența documentului.

---

# 91. Principiul 1 — Importanța nu anulează intimitatea

O experiență poate fi importantă și totuși sensibilă.

Importanța nu autorizează expunerea.

---

# 92. Principiul 2 — Secretele brute nu devin amintiri obișnuite

Parolele, tokenurile, private keys și valori similare nu trebuie păstrate în forma brută în Persistent Experience obișnuit.

---

# 93. Principiul 3 — Evenimentul poate supraviețui fără secret

Organismul trebuie să poată păstra faptul că un secret a fost utilizat fără să păstreze valoarea secretului.

---

# 94. Principiul 4 — Protecția trebuie aplicată cât mai devreme

Când informația este evident secretă, protecția trebuie aplicată înainte de persistența obișnuită, când acest lucru este tehnic posibil.

---

# 95. Principiul 5 — AI-ul nu este autoritatea finală asupra intimității

AI-ul poate detecta și recomanda.

Politicile majore și excepțiile rămân guvernate de autoritatea umană.

---

# 96. Principiul 6 — Accesul urmează necesitatea

Un organ primește numai informația necesară funcției sale.

Faptul că organismul posedă o informație nu înseamnă că fiecare organ o poate vedea.

---

# 97. Principiul 7 — Păstrarea și vizibilitatea sunt diferite

O informație poate fi păstrată fără să fie automat:

- reamintită;
- afișată;
- exportată;
- transmisă unui AI extern.

---

# 98. Principiul 8 — Restricțiile se moștenesc

Rezumatul, memoria, knowledge și alte reprezentări derivate trebuie să respecte restricțiile relevante ale sursei.

---

# 99. Principiul 9 — Redactarea păstrează adevărul structural

Când conținutul sensibil este eliminat sau mascat, organismul trebuie să poată păstra faptul că acel conținut a existat, fără a inventa o istorie falsă.

---

# 100. Principiul 10 — Ștergerea sensibilă trebuie să fie controlată

Ștergerea materialului sensibil trebuie să fie autorizată și, unde este legitim și sigur, auditabilă fără reproducerea materialului șters.

---

# 101. Principiul 11 — Intimitatea se aplică și copiilor

Protecția trebuie să considere:

- indexuri;
- cache;
- rapoarte;
- backupuri;
- rezumate;
- exporturi;
- alte artefacte derivate.

---

# 102. Principiul 12 — Omul poate contesta clasificarea

Omul trebuie să poată corecta atât clasificarea prea permisivă, cât și clasificarea excesiv de restrictivă.

---

# 103. Principiul 13 — Incertitudinea favorizează protecția

Când există un risc rezonabil ca informația să fie sensibilă și clasificarea nu este încă sigură, organismul trebuie să evite expunerea prematură.

---

# 104. Principiul 14 — Debugging-ul nu suspendă intimitatea

Modurile de diagnostic și debugging trebuie să respecte protecțiile de bază.

---

# 105. Principiul 15 — Furnizorii externi sunt o frontieră

Transmiterea experienței către un AI, API sau serviciu extern trebuie tratată ca ieșire dintr-o limită de încredere.

---

# 106. Principiul 16 — Nu există memorie paralelă necontrolată

Niciun organ AI nu trebuie să mențină intenționat o persistență ascunsă care ocolește guvernarea Persistent Experience.

---

# 107. Principiul 17 — Proprietarul trebuie să aibă control semnificativ

În limitele securității, obligațiilor tehnice și cerințelor legale aplicabile, proprietarul trebuie să poată înțelege și controla modul în care informația sa privată este păstrată și utilizată.

---

# 108. Principiul 18 — Informația despre terți necesită protecție

Faptul că organismul primește informație despre altă persoană nu îi acordă automat drept nelimitat de utilizare sau expunere.

---

# 109. Principiul 19 — Expirarea nu înseamnă publicare

Un token expirat, o parolă veche sau un secret revocat nu devine automat informație publică.

---

# 110. Principiul 20 — Operația poate fi auditată fără secret

Organismul trebuie să poată păstra dovezi despre operații sensibile fără să reproducă valorile protejate.

---

# 111. Principiul 21 — Protecția trebuie să fie explicabilă

Organismul trebuie să poată explica de ce un material este protejat, fără să dezvăluie tocmai conținutul protejat.

---

# 112. Principiul 22 — Privacy by Design

Protecția intimității trebuie să facă parte din fiziologia organismului, nu să fie adăugată numai după apariția incidentelor.

---

# 113. Întrebări pentru autoritatea umană

Autoritatea umană trebuie să decidă dacă acceptă următoarele 22 de principii:

1. Importanța nu anulează intimitatea.
2. Secretele brute nu devin amintiri obișnuite.
3. Evenimentul poate supraviețui fără secret.
4. Protecția trebuie aplicată cât mai devreme.
5. AI-ul nu este autoritatea finală asupra intimității.
6. Accesul urmează necesitatea.
7. Păstrarea și vizibilitatea sunt diferite.
8. Restricțiile se moștenesc.
9. Redactarea păstrează adevărul structural.
10. Ștergerea sensibilă trebuie să fie controlată.
11. Intimitatea se aplică și copiilor.
12. Omul poate contesta clasificarea.
13. Incertitudinea favorizează protecția.
14. Debugging-ul nu suspendă intimitatea.
15. Furnizorii externi sunt o frontieră.
16. Nu există memorie paralelă necontrolată.
17. Proprietarul trebuie să aibă control semnificativ.
18. Informația despre terți necesită protecție.
19. Expirarea nu înseamnă publicare.
20. Operația poate fi auditată fără secret.
21. Protecția trebuie să fie explicabilă.
22. Privacy by Design.

Fiecare poate fi:

- ACCEPTAT;
- MODIFICAT;
- RESPINS.

---

# 114. Ce rămâne nerezolvat chiar după acceptarea principiilor

Acceptarea principiilor nu va defini automat:

- schema exactă de clasificare;
- algoritmul de detectare;
- formatul redactării;
- mecanismul de criptare;
- retention periods;
- politica backupurilor;
- procedura juridică de ștergere;
- rolurile exacte;
- permisiunile exacte;
- mecanismul de declasificare;
- politica pentru furnizorii AI;
- implementarea software.

Acestea trebuie proiectate și validate separat.

---

# 115. Starea implementării

Auditul NU demonstrează existența unei implementări mature R-03.

Există organe ancestrale relevante, inclusiv Secret Manager și reguli de securitate/identitate.

Dar nu este demonstrat un sistem unificat care aplică fiziologia R-03 întregului traseu Persistent Experience.

---

# 116. Starea Canonului

Acest document este:

**RESEARCH / RECONCILIATION EVIDENCE**

Nu este automat Canon.

El citește și compară reguli existente și formulează principii candidate pentru decizia autorității umane.

---

# 117. Relația cu implementarea viitoare

Implementarea trebuie să vină după reconcilierea principiilor.

Ordinea sănătoasă este:

**experiență observată**

→ **audit**

→ **reconciliere**

→ **decizie umană**

→ **contract**

→ **implementare**

→ **teste**

→ **dovezi**

→ **acceptare de producție**

---

# 118. Declarația finală a auditului

R-03 identifică o nevoie fundamentală a organismului epistemic matur:

**intimitatea.**

Organismul trebuie să poată avea trecut fără să își expună toate secretele.

Trebuie să poată păstra adevărul unui eveniment fără să transforme parola, tokenul, cheia privată sau informația intimă într-o amintire liber circulantă.

Trebuie să știe că unele părți ale propriei experiențe au limite.

Iar aceste limite nu trebuie controlate în secret de AI.

Ele trebuie să fie:

- explicabile;
- auditabile;
- guvernabile;
- contestabile;
- compatibile cu autoritatea umană.

R-03 este, prin urmare, nu doar securitate tehnică.

Este **intimitatea organismului**.

---

END OF R-03 — INTIMITATEA ORGANISMULUI — CE ARE VOIE SĂ PĂSTREZE ȘI CE TREBUIE SĂ PROTEJEZE