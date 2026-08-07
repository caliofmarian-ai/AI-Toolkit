#!/usr/bin/env bash
set -euo pipefail

cd /home/runner/work/AI-Toolkit/AI-Toolkit

PYTHONPATH=lib python3 - <<'PY'
import json
import unittest
from pathlib import Path

from python.ai_platform import AIPlatformService
from python.dashboard.service import EngineeringDashboardService


class AIPlatformTests(unittest.TestCase):
    def setUp(self):
        self.repo = Path('.').resolve()
        self.ai = AIPlatformService(repository_root=str(self.repo), workspace_root=str(self.repo.parent))

    def test_provider_registry_and_model_manager(self):
        control = self.ai.control_center()
        providers = {item['id'] for item in control['providers']}
        expected = {
            'openai',
            'anthropic',
            'google-gemini',
            'github-models',
            'ollama',
            'azure-openai',
            'openrouter',
            'custom',
        }
        self.assertTrue(expected.issubset(providers))
        self.assertIn('engineering_model', control['model_manager']['role_models'])

    def test_settings_and_connection_testing_mask_secrets(self):
        self.ai.configure_provider('openai', api_key='sk-test-secret-123456', timeout_seconds=30, retries=3, rate_limit_per_minute=42)
        settings_path = self.repo / '.ai' / 'platform' / 'ai_settings.json'
        raw = settings_path.read_text(encoding='utf-8')
        self.assertNotIn('sk-test-secret-123456', raw)

        control = self.ai.control_center()
        openai = next(item for item in control['providers'] if item['id'] == 'openai')
        self.assertEqual(openai['status'], 'configured')

        test_result = self.ai.test_connection('openai')
        self.assertIn('status', test_result)
        self.assertIn('last_response_time', test_result)
        self.assertIn(test_result['health_status'], {'healthy', 'degraded'})

    def test_context_builder_session_and_pipeline(self):
        response = self.ai.ask_repository('Explain this architecture.')
        self.assertTrue(response['answer'])
        self.assertTrue(response['session_id'])
        self.assertIn('input_tokens', response['usage'])

        sessions = self.ai.sessions.list_sessions()
        self.assertTrue(any(item['id'] == response['session_id'] for item in sessions))

    def test_prompt_library_and_usage_monitoring(self):
        self.ai.ask_repository('', prompt_name='next_steps')
        usage = self.ai.usage_summary()
        self.assertGreaterEqual(usage['total']['requests'], 1)
        self.assertIn('success_rate', usage['total'])

        prompts = self.ai.control_center()['prompt_library']
        self.assertIn('Engineering', prompts)

    def test_dashboard_integration(self):
        service = EngineeringDashboardService(repository_root='.', workspace_root='..')
        payload = service.build(refresh=True)
        self.assertIn('ai_control_center', payload)
        self.assertIn('providers', payload['ai_control_center'])

        ai_page = service.render_ai_control_center(payload)
        repository_page = service.render_repository(payload, question='What should be implemented next?')
        self.assertIn('AI Control Center', ai_page)
        self.assertIn('Repository-aware Engineering Chat', repository_page)


if __name__ == '__main__':
    unittest.main(verbosity=2)
PY
