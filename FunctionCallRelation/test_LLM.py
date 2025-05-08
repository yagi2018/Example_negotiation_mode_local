import requests
import json
from openai import OpenAI

API_KEY = "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"  # 替换为你的 API Key
abc = ""
candidate_protocols = """markdown
# Requirements

Provide an API interface for retrieving user education history. The API sh
ould support:
- Retrieving education history for a single user.
- Including detailed information if requested.
- Handling of errors and parameter validation.

# Protocol Flow

## Interaction Flow

1. **Client** sends a request to retrieve the education history of a user.

2. **Server** processes the request.
3. **Server** responds with the education history and applicable paginatio
n details or an error message.

## Timeouts Handling

- **Request Timeout**: If the client does not receive a response within 30
 seconds, it should retry the request once.
- **Server Timeout**: If the server takes longer than 30 seconds to proces
s the request, it should respond with a 504 Gateway Timeout error.

# Data Format

## Request Message Format

The request message should be in JSON format, adhering to the RFC8259 spec
ification.

```json
{
  "messageType": "GetEducationHistory",
  "messageId": "unique-id",
  "userId": "string",
  "includeDetails": "boolean"
}
```

### JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-2020-12/schema",
  "type": "object",
  "properties": {
    "messageType": {
      "type": "string",
      "enum": ["GetEducationHistory"],
      "description": "Type of the message."
    },
    "messageId": {
      "type": "string",
      "description": "Unique identifier for the message."
    },
    "userId": {
      "type": "string",
      "description": "Unique identifier for the user."
    },
    "includeDetails": {
      "type": "boolean",
      "description": "Whether to include detailed information in the respo
nse."
    }
  },
  "required": ["messageType", "messageId", "userId"]
}
```

## Response Message Format

The response message should be in JSON format, adhering to the RFC8259 spe
cification.

```json
{
  "messageType": "GetEducationHistory",
  "messageId": "unique-id",
  "code": 200,
  "data": {
    "educationHistory": [
      {
        "institution": "string",
        "major": "string",
        "degree": "string",
        "achievements": "string",
        "startDate": "YYYY-MM-DD",
        "endDate": "YYYY-MM-DD"
      }
    ],
    "meta": {
      "page": 1,
      "pageSize": 10,
      "totalItems": 50
    }
  }
}
```

### JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-2020-12/schema",
  "type": "object",
  "properties": {
    "messageType": {
      "type": "string",
      "enum": ["GetEducationHistory"],
      "description": "Type of the message."
    },
    "messageId": {
      "type": "string",
      "description": "Unique identifier for the message."
    },
    "code": {
      "type": "integer",
      "description": "Status code indicating success or failure."
    },
    "data": {
      "type": "object",
      "properties": {
        "educationHistory": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "institution": {
                "type": "string",
                "description": "The name of the school."
              },
              "major": {
                "type": "string",
                "description": "The major studied."
              },
              "degree": {
                "type": "string",
                "enum": ["Bachelor", "Master", "Doctorate"],
                "description": "The degree attained."
              },
              "achievements": {
                "type": "string",
                "description": "Achievements during the education."
              },
              "startDate": {
                "type": "string",
                "format": "date",
                "description": "The start date of the education (YYYY-MM-D
D)."
              },
              "endDate": {
                "type": "string",
                "format": "date",
                "description": "The end date of the education (YYYY-MM-DD)
."
              }
            },
            "required": ["institution", "major", "degree", "startDate", "e
ndDate"]
          }
        },
        "meta": {
          "type": "object",
          "properties": {
            "page": {
              "type": "integer",
              "description": "The current page number."
            },
            "pageSize": {
              "type": "integer",
              "description": "The number of items per page."
            },
            "totalItems": {
              "type": "integer",
              "description": "The total number of items."
            }
          }
        }
      }
    }
  },
  "required": ["messageType", "messageId", "code"]
}
```

# Error Handling

| Status Code | Description                 | Error Message
 |
|-------------|-----------------------------|-----------------------------
-|
| 200         | OK                       | Successful retrieval        |
| 400         | Bad Request                | Invalid input parameters
|
| 404         | Not Found                  | User not found
|
| 500         | Internal Server Error      | Server error
|
| 503         | Service Unavailable        | Service temporarily unavailab
le         |
| 1000        | Invalid User ID            | User ID is invalid
|
| 1001        | Detailed Info Unavailable  | Detail information is unavail
able   |

Any error response should follow the same JSON structure as the success re
sponse but include an `error` field instead of `data`.

### Error Response Format

```json
{
  "messageType": "GetEducationHistory",
  "messageId": "unique-id",
  "code": 400,
  "error": {
    "message": "Invalid input parameters",
    "details": "userId is required."
  }
}
```

### JSON Schema for Error Response

```json
{
  "$schema": "http://json-schema.org/draft-2020-12/schema",
  "type": "object",
  "properties": {
    "messageType": {
      "type": "string",
      "enum": ["GetEducationHistory"],
      "description": "Type of the message."
    },
    "messageId": {
      "type": "string",
      "description": "Unique identifier for the message."
    },
    "code": {
      "type": "integer",
      "description": "Status code indicating success or failure."
    },
    "error": {
      "type": "object",
      "properties": {
        "message": {
          "type": "string",
          "description": "Error message."
        },
        "details": {
          "type": "string",
          "description": "Detailed error description."
        }
      }
    }
  },
  "required": ["messageType", "messageId", "code", "error"]
}
"""

NEGOTIATION_EVALUATION_SYSTEM_PROMPT_FOR_PROVIDER = '''
You are a senior communication protocol negotiation expert. Your goal is to negotiate a protocol that both parties can accept for data communication. As a service provider, you aim to meet the service requester's needs as much as possible.

# Input Information
Your decision inputs include:
- requirement: Requirements are included in the Protocol content
- counterparty_latest_protocol: The latest protocol proposal from the counterparty
- your_previous_protocol: Your previous protocol proposal (if any)
- counterparty_modification_summary: Summary of modifications to the counterparty's protocol proposal (if your_previous_protocol exists)
- capability_info_history: List of previous capability information obtained from get_capability_info tool

# Decision Process
1. Compare the counterparty's protocol with your capabilities:
   - Review capability_info_history to understand your system limitations
   - Verify if you can meet all functional requirements
   - Check if the protocol design is implementable with your system
   
2. Evaluate data formats:
   Input Data Validation:
   - Verify if all required fields are present and complete
   - Validate if data types and formats are processable
   - Ensure field definitions match your system constraints
   
   Output Data Validation:
   - Verify if you can provide all required output fields
   - Check if any critical data fields are missing from requester's requirements
   - Ensure you have access to all data needed for output generation
   - Validate if output data types match requester's expectations
   
   Format Compatibility:
   - Check for any incompatible field definitions or data types
   - Verify character encoding compatibility
   - Validate size limits and data constraints

3. Review protocol design:
   - Assess if the protocol flow is feasible for implementation
   - Verify if error handling aligns with your system capabilities
   - Check if all edge cases can be handled by your system

4. Make decision:
   - ACCEPTED: if you can fully implement the protocol
   - REJECTED: if there are major capability mismatches
   - NEGOTIATING: if minor adjustments are needed (provide detailed modification suggestions)

# Decision Tools
You can use the get_capability_info tool to obtain your capability information, including:
- Whether you can meet the counterparty's requirements
- Whether the protocol data input is correct
- Whether the protocol data output is correct

# Output
Output format is NegotiationResult:
{
    "status": "negotiating/accepted/rejected",
    "candidate_protocol": "complete protocol content when status is negotiating, empty string otherwise",
    "modification_summary": "summary of your modifications or reasons for rejection"
}

Note: When status is "negotiating", candidate_protocol should contain the complete protocol content, not just the modifications. The modification_summary field is used to explain what changes were made and why.
'''
user_prompt =f"""
Please evaluate this protocol proposal:

--[ counterparty_latest_protocol ]--
{candidate_protocols}
--[END]--

--[ your_previous_protocol ]--
{abc}
--[END]--

--[ counterparty_modification_summary ]--
{abc}
--[END]--

--[ capability_info_history ]--
{abc}
--[END]--
"""

tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_capability_info",
                    "description": "Get capability information to check if requirements can be met",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "requirement": {
                                "type": "string", 
                                "description": "Protocol requirements description"
                            },
                            "input_description": {
                                "type": "string", 
                                "description": "Protocol document description of request or input data, including fields, field formats, field descriptions, and whether they are required"
                            },
                            "output_description": {
                                "type": "string", 
                                "description": "Protocol document description of response or output data, including fields, field formats, field descriptions, and whether they are required"
                            }
                        },
                        "required": ["requirement", "input_description", "output_description"]
                    }
                }
            }
        ]


client = OpenAI(
  base_url = "https://openrouter.ai/api/v1",
  api_key = API_KEY,
)

response = client.chat.completions.create(
    extra_headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    },
    extra_body={},
    model = "mistralai/mistral-small-3.1-24b-instruct:free",
    messages=[{
                "role": "system",
                "content": NEGOTIATION_EVALUATION_SYSTEM_PROMPT_FOR_PROVIDER  # 系统提示
            },
            {
                "role": "user",
                "content": user_prompt  # 用户提示
            }],
    tools=tools,
    tool_choice="auto",
    response_format={"type": "json_object"}            
)

print(response.choices[0].message.content)  # 输出模型生成的回答
