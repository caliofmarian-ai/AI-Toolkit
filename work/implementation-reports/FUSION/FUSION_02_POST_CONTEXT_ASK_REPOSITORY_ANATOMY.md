# FUSION-02 — Post-Context ask_repository Anatomy

- Generated: 2026-08-22T19:38:38.872133+00:00
- Commit inspected: `03d5645a26362ed5f627b61ab3a8f943d8234b71`
- Mutation performed: NO
- Railway mutation performed: NO

## Proven position

- Historical organism recovery: PASS
- ConversationContextReconstructor.build: PASS
- Historical Experience continuity reaches context: PASS
- Preserved raw sources reconstructed: 3
- Failed human turn already preserved: YES
- Failed human turn must not be duplicated: YES

## ask_repository boundary

- Function starts at line: 200
- Function ends at line: 539

## Post-context physiology

    399:                 journey=journey_state,
    406:         # Bind the current Journey when the session is owned by the
    407:         # persistent AISessionEngine. Synthetic/test-double sessions may
    409:         persisted_session = self.sessions.get(
    410:             session["id"]
    411:         )
    412:
    413:         if persisted_session:
    414:             session = self.sessions.bind_journey(
    415:                 session["id"],
    416:                 journey_state.to_dict(),
    417:             )
    418:
    419:         reconstructed_context = self.conversation_context.build(
    420:             session["id"],
    421:             partner_identity={
    422:                 "provider": provider_id or session.get(
    423:                     "selected_provider", ""
    424:                 ),
    425:                 "model": model or session.get(
    426:                     "selected_model", ""
    427:                 ),
    428:             },
    429:         )
    430:
    431:         provider_cognitive_context = dict(
    432:             reconstructed_context
    433:         )
    434:         provider_cognitive_context[
    435:             "working_context"
    436:         ] = working_context_data
    437:
    438:         if read_navigation is not None:
    439:             provider_cognitive_context[
    440:                 "read_navigation"
    441:             ] = read_navigation
    442:
    443:         _fusion02_log_context_anatomy(
    444:             provider_cognitive_context
    445:         )
    446:
    447:         use_cognitive_working_context = getattr(
    448:             self.pipeline,
    449:             "use_cognitive_working_context",
    450:             None,
    451:         )
    452:
    453:         if callable(use_cognitive_working_context):
    454:             use_cognitive_working_context(
    455:                 working_context
    456:             )
    457:
    458:         try:
    459:             result = self.pipeline.run(
    460:                 prompt,
    461:                 settings,
    462:                 provider_id=provider_id,
    463:                 model=model,
    464:                 context_override=provider_cognitive_context,
    465:             )
    466:         except Exception as exc:
    467:             persisted_session = self.sessions.get(
    468:                 session["id"]
    469:             )
    470:
    471:             if persisted_session:
    472:                 self.sessions.mark_journey_interruption(
    473:                     session["id"],
    474:                     reason=(
    475:                         "provider-failure:"
    476:                         + type(exc).__name__
    477:                     ),
    478:                 )
    479:
    480:             raise
    481:
    482:         session = self.sessions.append_interaction(
    483:             session["id"],
    484:             effective_question,
    485:             result["answer"],
    486:             result["usage"],
    487:         )
    488:
    489:         ai_sequence = len(
    490:             session.get("raw_sources", [])
    491:         ) + 1
    492:
    493:         ai_source = self.conversation_experience.raw_source(
    494:             session=session,
    495:             experience=experience,
    496:             actor="AI",
    497:             content=result["answer"],
    498:             sequence=ai_sequence,
    499:             provider=result["provider"],
    500:             model=result["model"],
    501:         )
    502:
    503:         session = self.sessions.append_raw_source(
    504:             session["id"],
    505:             ai_source,
    506:         )
    507:
    508:         return {
    509:             "session_id": session["id"],
    510:             "experience_id": str(experience.experience_id),
    511:             "question": effective_question,
    512:             "answer": result["answer"],
    513:             "provider": result["provider"],
    514:             "model": result["model"],
    515:             "usage": result["usage"],
    516:             "raw_source_count": len(
    517:                 session.get("raw_sources", [])
    518:             ),
    519:             "information_need": cognitive_coordination[
    520:                 "information_need"
    521:             ],
    522:             "journey": journey_state.to_dict(),
    523:             "search_navigation": search_navigation,
    524:             "read_navigation": read_navigation,
    525:             "working_context": working_context_data,
    526:             "context": provider_cognitive_context,
    527:             "context_schema": provider_cognitive_context.get(
    528:                 "schema"
    529:             ),
    530:             "epistemic_status": {
    531:                 "conversation_is_raw_source": True,
    532:                 "conversation_is_evidence": False,
    533:                 "conversation_is_canon": False,
    534:                 "automatic_sedimentation": False,
    535:                 "retrieval_confers_authority": False,
    536:                 "human_authority_preserved": True,
    537:                 "unknown_is_valid": True,
    538:             },
    539:         }

## Purpose

Determine the exact remaining execution path after ConversationContextReconstructor.build before another real AI Partner message is allowed.

## Conservation

- No production code changed.
- No session changed.
- No Experience changed.
- No AI Partner message sent.
- No raw source created.
