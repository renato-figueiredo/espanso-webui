"""Testes do núcleo (emissor YAML + importador Beeftext). Rode: python3 -m unittest -v"""
import importlib.machinery
import importlib.util
import json
import random
import unittest
from pathlib import Path

import yaml

_p = Path(__file__).resolve().parent.parent / "espanso-webui"
_spec = importlib.util.spec_from_loader("ewui", importlib.machinery.SourceFileLoader("ewui", str(_p)))
ewui = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ewui)


class DumpYaml(unittest.TestCase):
    def roundtrip(self, text):
        d = {"global_vars": [{"name": "g", "type": "echo", "params": {"echo": text}}],
             "matches": [{"trigger": text or "t", "label": text, "replace": text,
                          "vars": [{"name": "x", "type": "echo", "params": {"echo": text}}]}]}
        self.assertEqual(yaml.safe_load(ewui.dump_yaml(d)), d, repr(text))

    def test_casos_chatos(self):
        for c in ["", "a", "-nome", "true", "12", "  x", "x ", "a: b", "# c", "{{v}}", "$|$", "é à",
                  "a\nb", "a\nb\n", "a\n\nb", "\ta\nb", "a\nb\n\n", "\nb", "x\r\ny", "'q'", '"d"',
                  "- x", "2024-01-01", "0x1F", "1_000", "null", "~", "a\n", "\n"]:
            self.roundtrip(c)

    def test_fuzz(self):
        rnd = random.Random(1)
        alphabet = "ab \n\t:#-'\"{}$|é\r\\"
        for _ in range(1500):
            self.roundtrip("".join(rnd.choice(alphabet) for _ in range(rnd.randint(0, 12))))

    def test_multilinha_usa_bloco(self):
        out = ewui.dump_yaml({"matches": [{"trigger": "-x", "replace": "a\nb"}]})
        self.assertIn("replace: |-", out)


class Beeftext(unittest.TestCase):
    SAMPLE = {"combos": [
        {"keyword": "-login", "snippet": "user#{key:tab}#{combo:-pw}#{cursor}", "description": "Login"},
        {"keyword": "-dt", "snippet": "#{dateTime:dd/MM/yyyy}", "name": "Data"},
        {"keyword": "-in", "snippet": "x #{input:nome}", "enabled": False},
        {"keyword": "-clip", "snippet": "[#{clipboard}]"},
    ], "groups": []}

    def test_conversao(self):
        m, warns = ewui.import_beeftext(json.dumps(self.SAMPLE))
        by = {x["trigger"]: x for x in m}
        self.assertEqual(by["-login"]["replace"], "user\t{{combo}}$|$")
        self.assertEqual(by["-login"]["force_mode"], "keys")
        self.assertEqual(by["-login"]["vars"][0], {"name": "combo", "type": "match", "params": {"trigger": "-pw"}})
        self.assertEqual(by["-dt"]["vars"][0]["params"]["format"], "%d/%m/%Y")
        self.assertEqual(by["-in"]["replace"], "x $|$")
        self.assertEqual(by["-clip"]["vars"][0]["type"], "clipboard")
        self.assertEqual(len(warns), 2)

    def test_json_invalido(self):
        with self.assertRaises(ValueError):
            ewui.import_beeftext('{"foo": 1}')


if __name__ == "__main__":
    unittest.main()
