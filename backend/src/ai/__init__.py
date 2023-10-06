import openai
import os
import requests

openai.api_type = "azure"

# Azure OpenAI on your own data is only supported by the 2023-08-01-preview API version
openai.api_version = "2023-08-01-preview"

# Azure OpenAI setup
openai.api_base = "https://nasa-sidekick-openai.openai.azure.com/" # Add your endpoint here
openai.api_key = os.environ["NASA_OPENAI_KEY"]
deployment_id = "nasa-ai-sidekick" # Add your deployment ID here
# Azure Cognitive Search setup
search_endpoint = "https://nasa-sidekick-search.search.windows.net"; # Add your Azure Cognitive Search endpoint here
search_key = os.environ["NASA_SEARCH_KEY"]; # Add your Azure Cognitive Search admin key here
search_index_name = "azureblob-index"; # Add your Azure Cognitive Search index name here

dev = False
github = True

if dev:
    openai.api_key = os.environ["NASA_OPENAI_KEY"]
if github:
    openai.api_key = os.getenv("NASA_OPENAI_KEY")
    
def setup_byod(deployment_id: str) -> None:
    """Sets up the OpenAI Python SDK to use your own data for the chat endpoint.

    :param deployment_id: The deployment ID for the model to use with your own data.

    To remove this configuration, simply set openai.requestssession to None.
    """

    class BringYourOwnDataAdapter(requests.adapters.HTTPAdapter):

        def send(self, request, **kwargs):
            request.url = f"{openai.api_base}/openai/deployments/{deployment_id}/extensions/chat/completions?api-version={openai.api_version}"
            return super().send(request, **kwargs)

    session = requests.Session()

    # Mount a custom adapter which will use the extensions endpoint for any call using the given `deployment_id`
    session.mount(
        prefix=f"{openai.api_base}/openai/deployments/{deployment_id}",
        adapter=BringYourOwnDataAdapter()
    )

    openai.requestssession = session

class AI:
    def __init__(self):
        self.api_key = openai.api_key
        self.temperature = 0.0
        self.max_tokens = 300
        self.top_p = 1.0
        self.frequency_penalty = 0.0
        self.presence_penalty = 0.0
        self.stop = ["\"\"\""]
    
    def sidekick_chat(self, user_request):
        
        setup_byod(deployment_id)
        completion = openai.ChatCompletion.create(
            messages=[{"role": "user", "content": user_request}],
            deployment_id=deployment_id,
            dataSources=[  # camelCase is intentional, as this is the format the API expects
                {
                    "type": "AzureCognitiveSearch",
                    "parameters": {
                        "endpoint": search_endpoint,
                        "key": search_key,
                        "indexName": search_index_name,
                    }
                }
            ]
        )
        
        return completion.choices[0].message.content