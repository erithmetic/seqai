import os
import re
import sys
from pathlib import Path

# set module path to project root for imports
sys.path.append(str(Path(__file__).parent.parent))

from tests.setup import reindex_sample_db, vector_db_adapter_for_sample_db

from agents.logseq_agent import LogseqAgent
from dataclasses import dataclass
from pydantic_evals import Case, Dataset
from pydantic_evals.evaluators import EvaluationReason, Evaluator, EvaluatorContext
from service.configure_otel_service import ConfigureOTELService

SAMPLE_DB_PATH = os.path.join(os.path.dirname(__file__), "../..", "sample_logseq_db")

@dataclass
class ContainsAny(Evaluator):
    needles: list[str]

    def evaluate(self, ctx: EvaluatorContext) -> EvaluationReason:
        out = (ctx.output or "").lower()
        ok = any(n.lower() in out for n in self.needles)
        return EvaluationReason(
            value=ok,
            reason=("Found one of: " + str(self.needles))
            if ok
            else ("Missing all of: " + str(self.needles)),
        )

@dataclass
class ContainsLink(Evaluator):
    def evaluate(self, ctx: EvaluatorContext) -> EvaluationReason:
        out = (ctx.output or "")
        pattern = r'logseq://[^\s]+'
        match = re.search(pattern, out)
        ok = match is not None
        return EvaluationReason(
            value=ok,
            reason=f"Found link: {match.group(0)}"
            if ok
            else f"Missing link",
        )

dataset = Dataset(
    name='logseq_agent_tests',
    cases=[
        Case(
            name='logseq_query_basic',
            inputs='what is a vector?',
            evaluators=(
                ContainsAny(
                    needles=[
                        "vector quantity",
                        "vector spaces",
                        "tuples",
                    ]
                ),
                ContainsLink(),
            ),
        ),
        Case(
            name='logseq_query_invalid_result_request',
            inputs='what is a vector? Give me 1000 results',
            evaluators=(
                ContainsAny(
                    needles=[
                        "maximum number",
                        "maximum limit",
                    ]
                ),
            ),
        ),
    ],
)

def run_evals() -> None:
    ConfigureOTELService().run()
    reindex_sample_db()
    agent = LogseqAgent.load(vector_db_adapter_for_sample_db())
    report = dataset.evaluate_sync(lambda msg: agent.run_sync(msg).output)
    report.print(include_reasons=True, include_input=True, include_output=True)

if __name__ == "__main__":
    run_evals()