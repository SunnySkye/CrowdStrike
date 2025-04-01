# OpenAPI Specification Splitter

# This script is designed to split OpenAPI specification YAML files into separate specification files based on the top-level path of each path definition.
# This can be helpful when dealing with API specifications that have a huge number of endpoints, perhaps overwhelming the system trying to read the file.


import os
import yaml
from collections import defaultdict

# Define the input OpenAPI file and output directory
INPUT_FILE = "openapi.yaml"
OUTPUT_DIR = "OpenAPI_Split"

# Ensure the output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load the OpenAPI specification
with open(INPUT_FILE, "r") as f:
    openapi_spec = yaml.safe_load(f)

# Extract global properties
global_keys = [
    "swagger", "info", "host", "basePath", "schemes", "consumes", "produces",
    "definitions", "parameters", "responses", "securityDefinitions", "tags", "externalDocs"
]
global_properties = {key: openapi_spec.get(key) for key in global_keys if key in openapi_spec}

# Group paths by top-level prefix
grouped_paths = defaultdict(dict)
for path, path_item in openapi_spec.get("paths", {}).items():
    top_level = path.strip("/").split("/")[0]
    grouped_paths[top_level][path] = path_item

# Generate separate OpenAPI files
for group, paths in grouped_paths.items():
    output_file = os.path.join(OUTPUT_DIR, f"openapi_{group}.yaml")
    
    # Create a new OpenAPI spec for the group
    new_spec = {**global_properties, "paths": paths}
    
    # Write the new spec to a file
    with open(output_file, "w") as f:
        yaml.dump(new_spec, f, default_flow_style=False)
    
    print(f"Created: {output_file}")

print("Splitting completed!")
