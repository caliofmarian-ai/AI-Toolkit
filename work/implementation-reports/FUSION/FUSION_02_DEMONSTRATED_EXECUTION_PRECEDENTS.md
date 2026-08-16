
## FUSION-02 — Evolved production contract vs stale test-double

Classification: DEMONSTRATED TEST-INFRASTRUCTURE CONTRACT PRECEDENT

Observed failure:

`AIPlatformService.ask_repository()` passed the newly supported
`context_override` keyword to `AIRequestPipeline.run()`.

The durable-conversation FUSION-02 test-double still represented the
older pipeline contract:

`_fake_result(prompt, settings, provider_id="", model="")`

and therefore raised:

`TypeError: _fake_result() got an unexpected keyword argument 'context_override'`

The local production contract was inspected before recovery and
demonstrated to support `context_override`.

Recovery:

Only the stale test-double was evolved to represent the real production
contract and to return the supplied reconstructed context.

Production context reconstruction was not removed or weakened merely to
satisfy an obsolete fake.

Epistemic classification:

This precedent is demonstrated execution/error evidence.
It is not Canon merely by being recorded here.
