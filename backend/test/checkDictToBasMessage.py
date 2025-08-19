from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    SystemMessage
)
from langchain.schema import (
    message_to_dict,
    messages_from_dict
)

# chat_history_dicts = [
#     { "type": "system", "data": { "content": "You are a helpful assistant." } },
#     { "type": "human", "data": { "content": "What is AI?" } },
#     { "type": "ai", "data": { "content": "AI is the simulation of human intelligence in machines." } }
# ]

chat_history_dicts = [{'type': 'system', 'data': {'content': 'You are a helpful assistant.', 'additional_kwargs': {}, 'response_metadata': {}, 'type': 'system', 'name': None, 'id': None}}, {'type': 'human', 'data': {'content': 'What is AI?', 'additional_kwargs': {}, 'response_metadata': {}, 'type': 'human', 'name': None, 'id': None, 'example': False}}, {'type': 'ai', 'data': {'content': 'AI is the simulation of human intelligence in machines.', 'additional_kwargs': {}, 'response_metadata': {}, 'type': 'ai', 'name': None, 'id': None, 'example': False, 'tool_calls': [], 'invalid_tool_calls': [], 'usage_metadata': None}}]

print(chat_history_dicts, '\n\n')

message_history = messages_from_dict(chat_history_dicts)

print(message_history, '\n')
print(type(message_history), '\n\n')


message_history_ = [ message_to_dict(m) for m in message_history]


print(message_history_, '\n')
print(type(message_history_))

print(chat_history_dicts[0]['data'])
print(chat_history_dicts[0]['data']['content'])
