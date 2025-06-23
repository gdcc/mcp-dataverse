# DRIFT Documentation

## InfraDID Class

### `__init__(self, DID_url)`
Initializes the InfraDID class with the given DID URL.

### `recognize_parameters(self, parameters)`
Replaces placeholders in the prompt with actual parameter values.

### `create_payload(self)`
Creates a JSON payload for the DID document.

### `register_tool(self, tool_name, tool_description, tool_parameters)`
Registers a tool with its name, description, and parameters.

### `register_dataset(self, dataset_name, dataset_description, dataset_parameters)`
Registers a dataset with its name, description, and parameters.

### `register_model(self, model_name, model_description, model_parameters)`
Registers a model with its name, description, and parameters.

### `register_prompt(self, prompt_name, prompt_description, prompt_provenance, variables)`
Registers a prompt with its name, description, provenance, and variables.

### `load_prompt(self, prompt_file)`
Loads a prompt from a file and recognizes parameters if a query is set.

### `get_prompt(self)`
Returns the current prompt.

### `set_session_id(self, session_id)`
Sets the session ID for the current instance.

### `set_model(self, model)`
Sets the model name for the current instance.

### `get_model(self)`
Returns the current model name.

### `set_compute_time(self, compute_time)`
Sets the compute time for the current instance.

### `set_confidence(self, confidence)`
Sets the confidence level for the current instance.

### `set_endpoint(self, endpoint)`
Sets the endpoint URL for the current instance.

### `get_endpoint(self)`
Returns the current endpoint URL.

### `set_source(self, source)`
Sets the source for the current instance.

### `create_did(self)`
Creates a DID by sending a POST request to the DID URL.

### `set_start_datetime(self)`
Sets the start datetime for the current instance.

### `set_end_datetime(self)`
Sets the end datetime for the current instance.

### `set_sparqlmuse(self, sparqlmuse_url)`
Sets the SPARQL Muse URL for the current instance.

### `get_compute_time(self)`
Calculates and returns the compute time.

### `set_prompt(self, prompt)`
Sets the prompt for the current instance.

### `get_did(self)`
Returns the created DID.

### `get_structured_result(self)`
Returns the structured result.

### `print_structured_result(self)`
Prints the structured result in a formatted JSON string.

### `set_structured_result(self, structured_result)`
Sets the structured result for the current instance.

## InfraModel Class

### `__init__(self, did=None, model_name=None, endpoint=None, readability_url=None)`
Initializes the InfraModel class with optional parameters for DID, model name, endpoint, and readability URL.

### `online_readability_content(self, url)`
Fetches readability content from the given URL.

### `get_readability_content(self)`
Returns the fetched readability content.

### `set_didinfo(self, didinfo)`
Sets the DID information for the current instance.

### `get_didinfo(self)`
Returns the DID information.

### `get_temp_did(self)`
Returns a temporary DID.

### `set_model(self, model_name, endpoint)`
Sets the model name and endpoint for the current instance.

### `set_prompt(self, prompt)`
Sets the prompt for the current instance.

### `get_prompt(self)`
Returns the current prompt.

### `set_provenance(self, provenance_chain=None, url=None)`
Sets the provenance chain and URL for the current instance.

### `get_provenance(self)`
Returns the provenance chain.

### `skolemize_graph(self, graph, base=None)`
Skolemizes the given RDF graph.

### `query_agent(self, prompt, model, readability_content=None, custom_content=None)`
Queries the agent with the given prompt and model, optionally using readability or custom content.

### `get_agent_result(self)`
Returns the result from the agent query.

### `query_ollama(self, prompt)`
Queries the Ollama model with the given prompt.

### `get_model(self)`
Returns the current model name.

### `get_primitives(self)`
Returns the registered primitives.

### `set_ontology(self, result)`
Sets the ontology based on the provided result.

### `get_ontology(self, q=False, uid=1)`
Generates and returns the ontology graph. 