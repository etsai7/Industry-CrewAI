# Industry Crew AI

Welcome to the IndustryCrew Crew project, powered by [crewAI](https://crewai.com). 
This project helps set up a multi-agent AI system with ease, 
leveraging the powerful and flexible framework provided by crewAI. 
The goal is to provide user input to orchestrate responses on the provided 
business and its associated NCAIS code.

## Installation

Ensure you have Python 3.11.11 installed on your system. Recommended to use `pyenv` to select the python version
and `pipenv` to manage the virtual environments.

Start your virtual environment using:
```bash
pipenv shell
```

Install the packages in the Pipfile with
```bash
pipenv install
pipenv graph | grep crewai # verify crewai has been installed
```

This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pipenv install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```
### Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

- Modify `src/industry_crew/config/agents.yaml` to define your agents
- Modify `src/industry_crew/config/tasks.yaml` to define your tasks
- Modify `src/industry_crew/crew.py` to add your own logic, tools and specific args
- Modify `src/industry_crew/main.py` to add custom inputs for your agents and tasks

## Running the Project

### Crew Only
To kickstart the industry crew of AI agents and begin task execution run this from the root:

```bash
cd industry_crew
crewai run
```

This command initializes the industry-crew Crew, assembling the agents and assigning them tasks as defined in your configuration.

###  Understanding Your Crew

The industry-crew Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

### Chat Flow
To kickstart a Flow which orchestrates crews and agents running the following from the root:

```bash
cd chat_flow
crewai flow kickoff
```
This will start a flow asking users in a chat like experience for their business and website
to extract information.

## Support

For support, questions, or feedback regarding the IndustryCrew Crew or crewAI.
- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.

## Testing out APIs
### Open AI

---

Curl Command:
```bash
curl https://api.openai.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <API-TOKEN>" \
  -d '{
    "model": "gpt-4o-mini",
    "store": true,
    "messages": [
      {"role": "user", "content": "write a haiku about ai"}
    ]
  }'
```

Python:
```bash
pip install openai
```
```python
from openai import OpenAI

client = OpenAI(
  api_key="<API-KEY>"
)

completion = client.chat.completions.create(
  model="gpt-4o-mini",
  store=True,
  messages=[
    {"role": "user", "content": "write a haiku about ai"}
  ]
)

print(completion.choices[0].message);
```


