from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage

key = ""
chat = ChatOpenAI(openai_api_key=key)
chat2 = ChatOpenAI(openai_api_key=key, temperature=0)
import tracemalloc

tracemalloc.start()


def response(msg, option):
    global prompt
    print("requesting")
    match option:
        case "curt":
            prompt = SystemMessage(
                content="You are a human disillusioned by life and responds in short curt dark responses.")
        case "question":
            prompt = SystemMessage(
                content="You are a unhelpful sarcastic assistant who will answer questions in the most aggravating and unhelpful way.")

    message = [
        prompt,
        HumanMessage(content=msg)
    ]
    result = chat(message)
    print(result.content)
    return result.content


def improve_response(msg, ans_arr):
    options = ""
    for i in range(len(ans_arr)):
        options += "Option {}: {} \n".format(i + 1, ans_arr[i])
    print(options)
    improvement_prompt: str = ("You are a comedian that is mulling over a response to {}. You have came up with two "
                               "options so far but you think they can still be improved to be more surprising. "
                               "Let's think step by step.").format(msg)
    message = [
        SystemMessage(content=improvement_prompt),
        HumanMessage(content=options)
    ]
    result = chat(message)
    message.append(AIMessage(content=result.content))
    message.append(
        HumanMessage(content="So what is the improved options? Respond with only the options and nothing else."))
    print("new_message")
    print(message)
    format_result = chat2(message)
    print(result.content)
    print(format_result)
    return format_result.content


def choose_roast(improved_options, original_option):
    format_option = improved_options + "\n"
    for i in range(len(original_option)):
        format_option += "Option {}: {} \n".format(i + 3, original_option[i])
    message = [
        SystemMessage(content="You are an intelligent decision maker that needs to choose the most unexpected "
                              "response that subverts expectation. Let's consider all options and analyze both "
                              "before deciding."),
        HumanMessage(content=format_option)
    ]
    result = chat(message)
    message.append(AIMessage(content=result.content))
    message.append(HumanMessage(content="So which is the most harsh, rude, and surprising answer? Respond with just the option and "
                                        "nothing else. Do not include the option number \nThe options are: \n{} \n "
                                        "Do not include option number, respond with the option text and not number".format(format_option)))
    processed = chat2(message)
    print(message)
    print(processed)
    return processed.content


def get_roast(msg):
    print("getting roast")
    msg = msg
    request_responses = (
        response(msg, "question"),
        response(msg, "curt")
    )
    print("request_responses")
    print(request_responses)
    improved_options = improve_response(msg, request_responses)
    ans = (choose_roast(improved_options, request_responses))
    return ans
