from pyparsing import Regex, Group, OneOrMore

def format_chat_template(input_text):
    user_start = "{{#user}}"
    user_end = "{{/user}}"
    assistant_start = "{{#assistant}}"
    assistant_end = "{{/assistant}}"
    gen_command = "{{gen"
    write_command = "{{gen 'write'}}"

    # Define parsing patterns
    gen_expression = Group(gen_command + Regex(r"[^}]+") + "}}")
    text_expression = Regex(r"[^{}]+")

    # Combine patterns
    combined_expression = OneOrMore(gen_expression | text_expression)

    # Parse the input text
    parsed_data = combined_expression.parseString(input_text)
    # Initialize template parts
    template_parts = []

    gen_present = False
    # Process parsed data
    for item in parsed_data:
        if item[0].startswith(gen_command):
            # Wrap gen commands with assistant tags
            template_parts.append(assistant_start + " ".join(item) + assistant_end)
            gen_present = True
        else:
            # Wrap text segments with user tags
            gen_present = False
            template_parts.append(user_start + item + user_end)

    # Add assistant write command if not present
    if not gen_present:
        template_parts.append(assistant_start + write_command + assistant_end)

    formatted_template = " ".join(template_parts)

    return formatted_template


# Testing the function with different inputs
input_text1 = "how are things going, tell me about Delhi"
formatted_template1 = format_chat_template(input_text1)
print(formatted_template1)

input_text2 = "Tweak this proverb to apply to model instructions instead. Where there is no guidance{{gen 'rewrite'}}"
formatted_template2 = format_chat_template(input_text2)
print(formatted_template2)

input_text3 = "How is today's weather?{{gen 'write'}}How was yesterdays?"
formatted_template3 = format_chat_template(input_text3)
print(formatted_template3)
