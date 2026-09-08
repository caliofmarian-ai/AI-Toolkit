# BEGIN FUSION-02 CSL/UEM COLLECTION BOUNDARY
# This root-level file is an executable historical diagnostic, not a pytest
# test. It remains manually runnable and is excluded only from collection.
collect_ignore = globals().get("collect_ignore", [])
if "test_csl_semantic.py" not in collect_ignore:
    collect_ignore.append("test_csl_semantic.py")
# END FUSION-02 CSL/UEM COLLECTION BOUNDARY
