# mistral-cli

-------------

This Python script provides a command-line interface (CLI) to interact with the Mistral AI API. It supports both non-interactive (single prompt) and interactive (chat) modes.

## Features

- Non-Interactive Mode: Send a single prompt to the Mistral AI API and get a response.

- Interactive Mode: Engage in a continuous chat session with the Mistral AI model.

- Model Selection: Easily specify which Mistral model to use (e.g., mistral-tiny, mistral-small, mistral-medium).

- API Key Management: Supports setting the API key via an environment variable for security and convenience.

## Prerequisites

### Mistral API Key

You need an API key from Mistral AI. If you don't have one, please refer to the Mistral AI documentation for instructions on how to obtain it.

`export MISTRAL_API_KEY=<YOUR_API_KEY>`

Before running the script, ensure you have the following installed:

    Python 3.6+

    requests library

You can install the requests library using pip:

    pip install requests --user

Or you can create a Python VirtualEnv for this:

    python -m venv .venv
    source .venv/bin/activate
    pip install requests --user

## Setup

Navigate to the directory where you saved `mistral-cli.py` in your terminal.
Non-Interactive Mode

Use the `-p` or `--prompt` flag to provide a single prompt. The script will print the AI's response and then exit.

    python mistral-cli.py -p "What is the capital of New York?"

You can also specify a different [Mistral Model](https://docs.mistral.ai/getting-started/models/models_overview/) using the -m or --model flag:

    python mistral-cli.py -p "Write a haiku about Ghost of Tsushima." -m mistral-small

Interactive Mode

Use the `-i` or `--interactive` flag to start a continuous chat session.

    python mistral-cli.py -i

You can also specify a different Mistral model for the interactive session:

    python mistral-cli.py -i -m mistral-tiny

Once in interactive mode, type your message at the You: prompt and press Enter. The AI's response will be displayed. To exit the interactive session, type exit or quit and press Enter.

Help

To see all available command-line arguments, use the --help flag:

    python mistral-cli.py --help

## Error Handling

The script includes basic error handling for API calls, such as network issues, HTTP errors, and unexpected API responses. If you encounter an "Error: MISTRAL_API_KEY not set" message, please ensure you have correctly set your API key as described in the "Set Your API Key" section.

## Customization

You can modify the DEFAULT_MODEL, temperature, and max_tokens variables within the mistral_cli.py script to adjust the behavior of the API calls.

**DEFAULT_MODEL**: Change the default model used if not specified via the command line.

**temperature**: Controls the randomness of the output. Lower values produce more deterministic results, while higher values lead to more diverse and creative outputs.

**max_tokens**: Sets the maximum number of tokens (words/characters) the AI can generate in its response.

## Author: Alex Mendes

<https://alexolinux.com>
