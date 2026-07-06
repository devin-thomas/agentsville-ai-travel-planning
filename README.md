# AgentsVille AI Travel Planning Agent

A portfolio-ready AI engineering project demonstrating how to build, validate, evaluate, and revise an agent-generated travel itinerary using structured outputs, mocked external APIs, Pydantic models, and a ReAct-style tool loop.

This project is designed to show practical AI engineering skills beyond prompt writing: schema design, tool interfaces, validation, evaluation gates, error handling, and iterative revision.

## What this demonstrates

- **Schema-first LLM development** using Pydantic models for validated structured outputs.
- **Grounded itinerary generation** from traveler preferences, destination data, daily weather, and available activity records.
- **LLM-as-judge evaluation** for weather compatibility with strict output labels.
- **Tool-use design** through clean docstrings that become callable tool descriptions.
- **ReAct-style agent revision** using a THINK -> ACTION -> OBSERVATION loop.
- **Evaluation-gated final output** where the revision agent must run validations before calling the final-answer tool.
- **Notebook-to-portfolio hygiene** with secrets removed and environment-variable based configuration.

## Project structure

```text
.
├── agentsville_ai_travel_planning.ipynb
├── project_lib.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
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

## Setup

Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in your local model-provider settings.

## Running the notebook

```bash
jupyter notebook agentsville_ai_travel_planning.ipynb
```

Run cells top-to-bottom. The mocked APIs in `project_lib.py` provide deterministic travel, activity, and weather data so the project can be reviewed without live third-party travel APIs.

## Security note

No real credential is committed to this repository. The notebook reads provider settings from environment variables.

## Portfolio framing

This project demonstrates how to make LLM behavior testable, inspectable, and maintainable through schemas, tools, evals, and constrained final outputs.
