from pathlib import Path


def test_t16_real_service_materializes_cognitive_working_context():
    source=Path(
        "lib/python/ai_platform/service.py"
    ).read_text(
        encoding="utf-8"
    )

    assert (
        "self.cognitive_coordinator.materialize_working_context("
        in source
    )

    assert (
        "provider_cognitive_context = dict("
        in source
    )

    assert (
        'provider_cognitive_context[\n'
        '            "working_context"\n'
        "        ] = working_context_data"
        in source
    )


def test_t16_real_service_supplies_cognitive_context_to_provider_pipeline():
    source=Path(
        "lib/python/ai_platform/service.py"
    ).read_text(
        encoding="utf-8"
    )

    assert (
        "context_override=provider_cognitive_context"
        in source
    )


def test_t16_real_service_does_not_call_legacy_context_builder():
    source=Path(
        "lib/python/ai_platform/service.py"
    ).read_text(
        encoding="utf-8"
    )

    assert "context_builder.build()" not in source
    assert "self.context_builder.build()" not in source


def test_t16_pipeline_retains_historical_legacy_compatibility():
    source=Path(
        "lib/python/ai_platform/pipeline.py"
    ).read_text(
        encoding="utf-8"
    )

    assert "self.context_builder.build()" in source

    assert (
        "context_override: Mapping[str, Any] | None = None"
        in source
    )


def test_t16_cognitive_pipeline_path_remains_available_and_governed():
    source=Path(
        "lib/python/ai_platform/pipeline.py"
    ).read_text(
        encoding="utf-8"
    )

    assert (
        "working_context: WorkingContext | None = None"
        in source
    )

    assert "effective_working_context" in source
    assert "ContextBudgetGovernor()" in source

    assert (
        "if effective_working_context is not None:"
        in source
    )


def test_t16_legacy_existence_does_not_make_it_real_service_default():
    service=Path(
        "lib/python/ai_platform/service.py"
    ).read_text(
        encoding="utf-8"
    )

    pipeline=Path(
        "lib/python/ai_platform/pipeline.py"
    ).read_text(
        encoding="utf-8"
    )

    # Compatibility physiology still exists.
    assert "self.context_builder.build()" in pipeline

    # But the organism's real service request explicitly supplies
    # reconstructed cognitive context to the provider pipeline.
    assert (
        "context_override=provider_cognitive_context"
        in service
    )

    assert (
        "materialize_working_context("
        in service
    )
