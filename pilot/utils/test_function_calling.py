from pilot.const.function_calls import ARCHITECTURE
from pilot.utils.llm_connection import clean_json_response
from pilot.utils.function_calling import parse_agent_response, JsonPrompter


class TestFunctionCalling:
    def test_parse_agent_response_text(self):
        # Given
        response = {'text': 'Hello world!'}

        # When
        response = parse_agent_response(response, None)

        # Then
        assert response == 'Hello world!'

    def test_parse_agent_response_json(self):
        # Given
        response = {'text': '{"greeting": "Hello world!"}'}
        function_calls = {'definitions': [], 'functions': {}}

        # When
        response = parse_agent_response(response, function_calls)

        # Then
        assert response == {'greeting': 'Hello world!'}

    def test_parse_agent_response_json_markdown(self):
        # Given
        response = {'text': '```json\n{"greeting": "Hello world!"}\n```'}
        function_calls = {'definitions': [], 'functions': {}}

        # When
        response['text'] = clean_json_response(response['text'])
        response = parse_agent_response(response, function_calls)

        # Then
        assert response == {'greeting': 'Hello world!'}

    def test_parse_agent_response_markdown(self):
        # Given
        response = {'text': '```\n{"greeting": "Hello world!"}\n```'}
        function_calls = {'definitions': [], 'functions': {}}

        # When
        response['text'] = clean_json_response(response['text'])
        response = parse_agent_response(response, function_calls)

        # Then
        assert response == {'greeting': 'Hello world!'}

    def test_parse_agent_response_multiple_args(self):
        # Given
        response = {'text': '{"greeting": "Hello", "name": "John"}'}
        function_calls = {'definitions': [], 'functions': {}}

        # When
        response = parse_agent_response(response, function_calls)

        # Then
        assert response['greeting'] == 'Hello'
        assert response['name'] == 'John'


def test_json_prompter():
    # Given
    prompter = JsonPrompter()

    # When
    prompt = prompter.prompt('Create a web-based chat app', ARCHITECTURE['definitions'])  # , 'process_technologies')

    # Then
    assert prompt == '''Help choose the appropriate function to call to answer the user's question.
You must respond with ONLY the JSON object, with NO additional text or explanation.

Available functions:
- process_technologies - Print the list of technologies that are created.

Create a web-based chat app'''


def test_llama_json_prompter():
    # Given
    prompter = JsonPrompter(is_instruct=True)

    # When
    prompt = prompter.prompt('Create a web-based chat app', ARCHITECTURE['definitions'])  # , 'process_technologies')

    # Then
    assert prompt == '''[INST] <<SYS>>
Help choose the appropriate function to call to answer the user's question.
You must respond with ONLY the JSON object, with NO additional text or explanation.

Available functions:
- process_technologies - Print the list of technologies that are created.
<</SYS>>

Create a web-based chat app [/INST]'''


def test_json_prompter_named():
    # Given
    prompter = JsonPrompter()

    # When
    prompt = prompter.prompt('Create a web-based chat app', ARCHITECTURE['definitions'], 'process_technologies')

    # Then
    assert prompt == '''**IMPORTANT**
You must respond with ONLY the JSON object, with NO additional text or explanation.

Here is the schema for the expected JSON object:
```json
{
    "technologies": {
        "type": "array",
        "description": "List of technologies.",
        "items": {
            "type": "string",
            "description": "technology"
        }
    }
}
```

Create a web-based chat app'''


def test_llama_json_prompter_named():
    # Given
    prompter = JsonPrompter(is_instruct=True)

    # When
    prompt = prompter.prompt('Create a web-based chat app', ARCHITECTURE['definitions'], 'process_technologies')

    # Then
    assert prompt == '''[INST] <<SYS>>
**IMPORTANT**
You must respond with ONLY the JSON object, with NO additional text or explanation.

Here is the schema for the expected JSON object:
```json
{
    "technologies": {
        "type": "array",
        "description": "List of technologies.",
        "items": {
            "type": "string",
            "description": "technology"
        }
    }
}
```
<</SYS>>

Create a web-based chat app [/INST]'''
