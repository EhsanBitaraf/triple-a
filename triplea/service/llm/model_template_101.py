model_template_id = "T101"
model_name = "openbuddy-llama2-70B-v13.2-AWQ"
base_path = "http://localhost:5003/v1"
temperature = 0.7
frequency_penalty = 0
presence_penalty = 0
max_tokens = 3
top_p = 0.9
template = """Check the title and abstract of the article below and tell me if this article has anything to do with LLMs (Large Language Models) assessment methods? Your answer must be yes or no.
title: {title}
abstract : {abstract}
        """  # noqa: E501
