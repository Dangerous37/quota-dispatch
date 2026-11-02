import json
import subprocess
import sys
import unittest
from pathlib import Path

from engine import evaluate


def example():
    return json.loads(Path(__file__).with_name("example.json").read_text(encoding="utf-8"))


class AcceptanceTests(unittest.TestCase):
    def test_example_cli(self):
        proc = subprocess.run([sys.executable, "cli.py", "example.json"], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(json.loads(proc.stdout), evaluate(example()))

    def test_quota_fairness_and_recovery(self):
        rows = evaluate(example())
        self.assertEqual([(r["tenant"],r["tick"]) for r in rows], [("a",0),("b",1),("b",2),("a",5),("b",6)])
        self.assertEqual(len({r["id"] for r in rows}), 5)

    def test_idle_jump_and_invalid_quota(self):
        data = example()
        data["jobs"] = [{"id":"later","arrival":10**9,"tenant":"a"}]
        self.assertEqual(evaluate(data)[0]["wait"], 0)
        data["quotas"]["a"] = 0
        with self.assertRaises(ValueError):
            evaluate(data)
