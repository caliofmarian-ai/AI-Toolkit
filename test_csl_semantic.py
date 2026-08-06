from python.engineering_engine.compiler import EngineeringCompiler

compiler = EngineeringCompiler()
result = compiler.compile("docs/canonical", run_generators=False)

print("=" * 80)
print("CSL SEMANTIC COMPILATION TEST")
print("=" * 80)

print("\nSTATISTICS")
for k, v in result.stats.items():
    print(f"{k}: {v}")

print("\nVALIDATION RESULTS")
print("Validation objects:", len(result.validation_results))

for i, validation in enumerate(result.validation_results[:10], 1):
    print("-" * 60)
    print("Validation", i)
    print("Type:", type(validation).__name__)

    for attr in dir(validation):
        if attr.startswith("_"):
            continue
        try:
            value = getattr(validation, attr)
            if callable(value):
                continue
            print(f"{attr}: {value}")
        except Exception:
            pass

print("\nUEM STATISTICS")
print(result.uem.statistics())

print("\nDOCUMENT LOOKUP")

for doc in [
    "CANON-001",
    "CANON-010",
    "CANON-032",
    "CANON-067"
]:
    print("-" * 40)
    print(doc)

    obj = result.uem.get_object(doc)

    if obj is None:
        print("NOT FOUND")
    else:
        print("Name:", obj.name)
        print("Version:", obj.version)
        print("Status:", obj.status)
        print("Source:", obj.source_document)

print("\nRELATIONSHIP COUNTS")

rels = result.uem.all_relationships()

print("Relationships:", len(rels))

contains = {}

for rel in rels:
    key = rel.relation_type.name
    contains[key] = contains.get(key, 0) + 1

for k, v in sorted(contains.items()):
    print(k, "=", v)

print("\n" + "=" * 80)
print("SEMANTIC TEST FINISHED")
print("=" * 80)
