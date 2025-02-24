from openai import OpenAI


def openai_response(
    # Model request
    user_content: str = None,
    system_content: str = None,
    # Model config
    api_key: str = "your_api_key",
    model_name: str = "gpt-4o-mini",
    max_tokens: int = 256,
    temperature: float = 0.0,
    top_p: float = 1.0,
    frequency_penalty: float = 0.0,
    presence_penalty: float = 0.0,
    n: int = 1,
    stop=None,
):
    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                # Assigned role for system
                {"role": "system", "content": system_content},
                # User request
                {"role": "user", "content": user_content},
            ],
            n=int(n),
            stop=stop,
            top_p=float(top_p),
            max_tokens=int(max_tokens),
            temperature=float(temperature),
            presence_penalty=float(presence_penalty),
            frequency_penalty=float(frequency_penalty),
        )
        output = response.choices[0].message.content
        tokens = response.usage

    except Exception as e:
        raise ValueError(f"Summary Error: {e}")

    return output, tokens
