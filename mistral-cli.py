import argparse
import requests
import json
import os

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "YOUR_MISTRAL_API_KEY")
MISTRAL_API_BASE_URL = "https://api.mistral.ai/v1/chat/completions"

# Dynamically fetch available models from Mistral API
def get_available_models():
    try:
        # Assuming Mistral API has a models endpoint (adjust URL if needed)
        models_url = "https://api.mistral.ai/v1/models"  # Example endpoint
        headers = {
            "Authorization": f"Bearer {MISTRAL_API_KEY}"
        }
        response = requests.get(models_url, headers=headers)
        response.raise_for_status()
        models_data = response.json()
        
        # Extract model names from response (adjust based on actual API response structure)
        available_models = [model["id"] for model in models_data.get("data", [])]
        return available_models
    except Exception as e:
        print(f"Error fetching models from API: {e}")
        # Fallback to hardcoded list if API call fails
        return [
            "mistral-tiny",
            "devstral-latest",
            "devstral-medium-latest",
            "devstral-2512",
            "labs-mistral-small-creative"
        ]

AVAILABLE_MODELS = get_available_models()
DEFAULT_MODEL = AVAILABLE_MODELS[0]

def call_mistral_api(prompt, model=DEFAULT_MODEL):
    if MISTRAL_API_KEY == "YOUR_MISTRAL_API_KEY":
        print("Error: MISTRAL_API_KEY not set. Please set the environment variable or update the script.")
        return None

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {MISTRAL_API_KEY}"
    }

    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 1000
    }

    try:
        response = requests.post(MISTRAL_API_BASE_URL, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        response_json = response.json()

        if response_json and response_json.get("choices"):
            return response_json["choices"][0]["message"]["content"]
        else:
            print(f"Error: Unexpected API response structure: {response_json}")
            return None
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        print(f"Response content: {e.response.text}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON response: {response.text}")
        return None

def run_non_interactive_mode(prompt, model):
    print(f"Sending prompt to Mistral AI (Model: {model}):\n---")
    print(prompt)
    print("---\n")

    response_text = call_mistral_api(prompt, model)

    if response_text:
        print("\nMistral AI Response:\n---")
        print(response_text)
        print("---")
    else:
        print("Failed to get a response from Mistral AI.")

def run_interactive_mode(model):
    print(f"Starting interactive mode with Mistral AI (Model: {model}).")
    print("Type 'exit' or 'quit' to end the session.")
    print("--------------------------------------------------")

    while True:
        try:
            user_input = input("You: ").strip()
            if user_input.lower() in ["exit", "quit"]:
                print("Exiting interactive session. Goodbye!")
                break
            if not user_input:
                continue

            response_text = call_mistral_api(user_input, model)

            if response_text:
                print(f"Mistral: {response_text}\n")
            else:
                print("Mistral: Sorry, I couldn't get a response. Please try again.")

        except KeyboardInterrupt:
            print("\nExiting interactive session. Goodbye!")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Interact with the Mistral AI API in interactive or non-interactive mode."
    )
    parser.add_argument(
        "-p", "--prompt",
        type=str,
        help="Prompt for non-interactive mode. If provided, runs in non-interactive mode."
    )
    parser.add_argument(
        "-m", "--model",
        type=str,
        default=DEFAULT_MODEL,
        help=f"Specify the Mistral model to use (e.g., 'mistral-tiny', 'mistral-small', 'mistral-medium'). Default: {DEFAULT_MODEL}"
    )
    parser.add_argument(
        "-l", "--list",
        action="store_true",
        help="List available models and exit"
    )
    parser.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="Run in interactive chat mode. Overrides --prompt if both are provided."
    )

    args = parser.parse_args()

    if args.list:
        print("Available models:")
        for model in AVAILABLE_MODELS:
            print(f" - {model}")
        exit(0)
    elif args.interactive:
        run_interactive_mode(args.model)
    elif args.prompt:
        run_non_interactive_mode(args.prompt, args.model)
    else:
        print("No prompt provided and interactive mode not selected.")
        print("Usage examples:")
        print("  Non-interactive: python your_script_name.py -p 'Tell me a short story.' -m mistral-small")
        print("  Interactive: python your_script_name.py -i -m mistral-medium")
        print("  You can also set the API key as an environment variable: export MISTRAL_API_KEY='YOUR_KEY'")