# CSS-003 — Normative Language

Version: 1.0.0

Status: Draft

Classification: Canonical Standard

Standard Family: CSS

Identifier: CSS-003

Parent Standard: CSS-000_SPECIFICATION_MODEL

Owner: AI CTO

---

# Abstract

This specification defines the normative language used throughout the AI-Toolkit ecosystem.

Normative language establishes the formal meaning of engineering requirements and ensures that specifications are interpreted consistently by humans, AI systems and automated validation engines.

---

# 1. Purpose

The purpose of this specification is to define the official normative vocabulary used in every canonical specification.

Normative language removes ambiguity by assigning precise engineering meaning to specific requirement keywords.

---

# 2. Scope

This specification applies to every canonical standard, including:

- Governance
- Architecture
- CSS
- CDM
- CSL
- CANON
- Future AI-generated standard families

---

# 3. Fundamental Principles

Normative language shall be:

- deterministic
- unambiguous
- implementation-independent
- machine-readable
- human-readable
- verifiable
- auditable

---

# 4. Requirement Levels

Every engineering requirement shall belong to exactly one normative level.

Requirement levels are:

Mandatory

Prohibited

Recommended

Optional

Informative

---

# 5. Mandatory Requirements

The following keywords indicate mandatory requirements.

## MUST

Indicates an absolute engineering requirement.

Non-compliance is not permitted.

---

## SHALL

Equivalent to MUST.

Used primarily for formal engineering specifications.

---

## REQUIRED

Equivalent to MUST.

Used where readability is improved.

---

# 6. Prohibited Requirements

## MUST NOT

Indicates an absolute prohibition.

Implementations violating this requirement are non-conformant.

---

## SHALL NOT

Equivalent to MUST NOT.

---

# 7. Recommended Requirements

## SHOULD

Indicates a recommended engineering practice.

Alternative approaches may be acceptable when justified.

---

## RECOMMENDED

Equivalent to SHOULD.

---

# 8. Discouraged Requirements

## SHOULD NOT

Indicates that an action is discouraged.

Use requires explicit engineering justification.

---

## NOT RECOMMENDED

Equivalent to SHOULD NOT.

---

# 9. Optional Requirements

## MAY

Indicates optional behavior.

Implementations remain conformant whether or not the feature is implemented.

---

## OPTIONAL

Equivalent to MAY.

---

# 10. Lifecycle Keywords

The following lifecycle keywords may be used.

## DEPRECATED

The feature remains supported but should no longer be used in new implementations.

---

## OBSOLETE

The feature has been removed from the standard.

New implementations shall not depend upon it.

---

# 11. Implementation Keywords

## IMPLEMENTATION DEFINED

Behavior shall be documented by the implementation.

---

## IMPLEMENTATION SPECIFIC

Behavior may differ between implementations.

Differences shall be documented.

---

## UNDEFINED BEHAVIOR

The specification intentionally defines no required behavior.

Implementations shall not rely upon undefined behavior.

---

# 12. Informative Language

The following expressions are informative only.

Examples:

may consider

for example

typically

generally

in most cases

Informative statements never create engineering obligations.

---

# 13. Interpretation Rules

Normative keywords shall:

- retain identical meaning across every standard
- never be redefined by individual specifications
- remain independent of implementation technology

---

# 14. Validation Rules

Validation engines shall verify:

- correct keyword usage
- valid requirement classification
- absence of contradictory requirements
- consistent terminology

Improper use of normative keywords shall produce validation errors.

---

# 15. Writing Rules

Normative statements should:

- express exactly one requirement
- avoid compound obligations
- avoid ambiguity
- avoid subjective wording
- remain independently testable

---

# 16. Anti-patterns

The following are prohibited:

- redefining normative keywords
- mixing informative and normative language in a single requirement
- contradictory requirements
- ambiguous obligation levels
- hidden requirements

---

# 17. AI Interpretation

AI systems shall interpret normative keywords exactly as defined by this specification.

No AI implementation may infer stronger or weaker obligations than those explicitly expressed.

---

# 18. Relationship to Other Standards

CSS-000 defines the Canonical Specification Model.

CSS-001 defines the authoring process.

CSS-002 defines document presentation.

This specification defines the semantics of engineering requirements.

---

# 19. Conformance

A specification conforms to CSS-003 when:

- normative keywords are used correctly
- obligation levels are unambiguous
- every requirement is testable
- informative language is clearly distinguished
- no prohibited usage exists

---

# 20. Success Criteria

The Normative Language standard is successfully implemented when every engineering requirement throughout the AI-Toolkit ecosystem is interpreted consistently by humans, AI systems and automated validation engines.

---

# 21. Closing Statement

Normative language establishes the legal and engineering meaning of canonical specifications.

By standardizing requirement terminology, AI-Toolkit ensures deterministic interpretation, reliable validation and consistent implementation across the entire engineering ecosystem.