# set module path to project root for imports
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from tests.setup import reindex_sample_db, vector_db_adapter_for_sample_db

from agents.logseq_agent import LogseqAgent, logseq_agent, query_logseq
from dataclasses import dataclass
from pydantic_evals import Case, Dataset
from pydantic_evals.evaluators import EvaluationReason, Evaluator, EvaluatorContext

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
            ),
        ),
    ],
)

def main(input: str) -> str:
    agent = LogseqAgent(vector_db_adapter_for_sample_db())
    blocks = agent.query_logseq(input, 5).blocks
    context = "\n\n---\n\n".join(block.content for block in blocks)
    prompt = f"""Use the CONTEXT to answer the USER. If the answer isn't in the context, say you don't know.

    CONTEXT:
    {context}

    USER:
    {input}
    """
    result = logseq_agent.run_sync(prompt)
    return result.output

def run_evals() -> None:
    reindex_sample_db()

    report = dataset.evaluate_sync(main)
    report.print(include_reasons=True, include_input=True, include_output=True)


if __name__ == "__main__":
    run_evals()