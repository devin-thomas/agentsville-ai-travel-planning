# AgentsVille AI Travel Planning Agent

This is my cleaned-up portfolio version of an AI travel-planning agent project. The original version came from a guided notebook assignment, but I refactored the presentation here to emphasize the AI engineering ideas behind the work: structured outputs, tool design, mocked APIs, eval gates, and ReAct-style itinerary revision.

I am intentionally treating this repository as a portfolio case study, not as a polished commercial travel product. The value is in the engineering pattern: taking an LLM workflow that could easily become loose prompt soup and making it more testable, inspectable, and maintainable.

## What I wanted to demonstrate

- **Schema-first LLM development**: using Pydantic models so generated itineraries can be parsed and validated instead of trusted as free-form text.
- **Grounded generation**: building the itinerary from traveler preferences, destination data, mocked weather, and mocked activity records.
- **LLM-as-judge evaluation**: checking whether activities are compatible with weather using constrained output labels.
- **Tool-use design**: writing clear Python docstrings that double as tool descriptions for an agent.
- **ReAct-style revision**: forcing the revision agent through a THINK -> ACTION -> OBSERVATION loop instead of letting it jump straight to a final answer.
- **Eval-gated final output**: requiring the agent to run validation before calling the final-answer tool.
- **Secret hygiene**: removing the course-issued API key from the public notebook and reading model-provider settings from environment variables.

## What this repo is and is not

This repo is a **portfolio adaptation** of the project. It keeps the most important engineering artifacts visible and readable.

It is **not** a full production travel-planning app. The activity and weather APIs are mocked, and the notebook is meant to demonstrate agent architecture rather than provide real travel recommendations.

It is also not a verbatim copy of the original course submission. Some assignment-specific scaffolding, run outputs, and course-only credentials were intentionally removed so the public version is easier to review.

## Project structure

```text
.
├── agentsville_ai_travel_planning.ipynb  # Clean portfolio notebook
├── project_lib.py                        # Lightweight mocked API helpers
├── requirements.txt                      # Python dependencies
├── Dockerfile                            # Optional reproducible Jupyter environment
├── .dockerignore                         # Docker build cleanup
├── .env.example                          # Local environment template
├── .gitignore                            # Python/Jupyter ignore rules
└── README.md                             # Project overview
```

## Agent workflow

1. Parse vacation data into a validated `VacationInfo` object.
2. Pull mocked weather and activity data for each trip date.
3. Generate a structured itinerary that conforms to the `TravelPlan` Pydantic schema.
4. Evaluate the itinerary for budget, date coverage, activity validity, traveler-interest alignment, and weather compatibility.
5. Revise the itinerary with a ReAct-style agent when user feedback requires changes.
6. Run evals again before returning the final revised itinerary.

## Core AI engineering patterns

### Structured output validation

The notebook uses Pydantic models to make LLM output machine-checkable instead of relying on free-form text.

```python
class VacationInfo(BaseModel):
    travelers: List[Traveler]
    destination: str
    date_of_arrival: datetime.date
    date_of_departure: datetime.date
    budget: int
```

### Weather-aware LLM evaluation

The weather compatibility prompt is intentionally strict. It asks for reasoning, but the final answer must be one of two machine-readable labels:

```text
IS_COMPATIBLE
IS_INCOMPATIBLE
```

That makes the evaluator usable inside a normal Python validation function.

### Tool design

The activity lookup tool uses a production-style docstring so an LLM can understand when and how to call it.

```python
def get_activities_by_date_tool(date: str, city: str) -> List[dict]:
    """Fetch and validate available activities for a given city and date.

    Args:
        date: Activity date in `YYYY-MM-DD` format.
        city: City where activities should be searched.

    Returns:
        A list of dictionaries representing validated activities.
    """
```

### ReAct revision loop

The revision agent is prompted to use a strict cycle:

```text
THOUGHT -> ACTION -> OBSERVATION
```

The agent must call tools using valid JSON and must run evaluation before returning the final itinerary.

## Running locally with Python

Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in your local model-provider settings:

```bash
cp .env.example .env
```

Then run:

```bash
jupyter notebook agentsville_ai_travel_planning.ipynb
```

## Running with Docker

Docker is optional, but it makes the notebook easier to run consistently because reviewers do not need to manage a local Python or Jupyter setup.

Build the image:

```bash
docker build -t agentsville-ai-travel-planning .
```

Run Jupyter:

```bash
docker run --rm -p 8888:8888 --env-file .env agentsville-ai-travel-planning
```

Then open the Jupyter URL printed in the terminal.

## Security note

No real credential is committed to this repository. The notebook reads provider settings from environment variables.

## Reflection

The most important lesson from this project was that agentic AI work needs more than a clever prompt. The maintainable version comes from putting guardrails around the model: typed schemas, narrow tool contracts, exact output formats, and evals that decide whether an answer is acceptable.

That is the part I want this repo to communicate: I can build AI workflows that are structured enough for software engineering, not just demos that work once in a notebook.
