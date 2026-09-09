import os
import argparse

from dotenv import load_dotenv
from openai import OpenAI

from prompts import system_prompt
from call_function import available_functions
from call_function import call_function

def main() -> None:
    parser = argparse.ArgumentParser(description="AI Code Assistant")
    parser.add_argument("user_prompt", type=str, help="Prompt to send to the LLM")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY environment variable not set")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]
    for _ in range(20):
        is_done = generate_content(client, messages, args)
        if is_done:
            break
    else:
        print("Maximum iterations reached without a final response.")



def generate_content(client: OpenAI, messages: list, args: argparse.Namespace) -> None:
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        temperature=0,
        tools=available_functions
    )
    if not response.usage:
        raise RuntimeError("API response appears to be malformed")

    if args.verbose:
        print("User prompt:", args.user_prompt)
        print("Prompt tokens:", response.usage.prompt_tokens)
        print("Response tokens:", response.usage.completion_tokens)
    
    message = response.choices[0].message
    messages.append(message)
    if message.tool_calls:
        print("Function calls:")
        for tool in message.tool_calls:
            if tool.type != "function":
                continue
            result_message = call_function(tool, args.verbose)
            messages.append(result_message)
            if not result_message["content"]:
                raise RuntimeError("Function call returned empty content")

            if args.verbose:
                print(f"-> {result_message['content']}")
        return False
    else:
        print("Response:")
        print(message.content)
        return True


if __name__ == "__main__":
    main()
