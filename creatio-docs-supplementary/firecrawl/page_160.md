<!-- Source: page_160 -->

[Skip to main content](https://academy.creatio.com/docs/8.x/no-code-customization/8.1/customization-tools/ai-tools/creatio-ai/intent-development-recommendations%20copy#__docusaurus_skipToContent_fallback)

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

This is documentation for Creatio **8.1**.

For up-to-date documentation, see the **[latest version](https://academy.creatio.com/docs/8.x/no-code-customization/customization-tools/recommendations/recommendations-on-app-creation)** (8.3).

Version: 8.1

On this page

Level: beginner

note

Creatio AI is available for beta testing in Creatio version 8.1.5 Quantum to a closed test group. The general public release of the feature is planned in the near future.

Development of a Creatio AI intent includes different steps. This article covers best practices on each of them. You can use these practices to get the most out of Creatio AI functionality.

In general, Creatio AI intent development consists of the following steps:

1. Define user needs. [Read more >>>](https://academy.creatio.com/docs/8.x/no-code-customization/8.1/customization-tools/ai-tools/creatio-ai/intent-development-recommendations%20copy#title-2536-1)
2. Design the intent. [Read more >>>](https://academy.creatio.com/docs/8.x/no-code-customization/8.1/customization-tools/ai-tools/creatio-ai/intent-development-recommendations%20copy#title-2536-3)
3. Develop actions. [Read more >>>](https://academy.creatio.com/docs/8.x/no-code-customization/8.1/customization-tools/ai-tools/creatio-ai/intent-development-recommendations%20copy#title-2536-9)
4. Test and refine the intent. [Read more >>>](https://academy.creatio.com/docs/8.x/no-code-customization/8.1/customization-tools/ai-tools/creatio-ai/intent-development-recommendations%20copy#title-2536-10)

## Step 1. Define user needs [​](https://academy.creatio.com/docs/8.x/no-code-customization/8.1/customization-tools/ai-tools/creatio-ai/intent-development-recommendations%20copy\#title-2536-1 "Direct link to Step 1. Define user needs")

The first step in developing a Creatio AI intent is to identify the challenges and repetitive tasks faced by Creatio users that Creatio AI can streamline. For example, consider these areas where Creatio AI's generative AI capabilities can offer significant value:

- **Data analysis and insights**. Users often struggle to extract meaningful insights from large datasets. Creatio AI scenarios can assist with tasks like identifying trends, generating reports, and summarizing key findings based on user requests.
- **Content creation and summarization**. Creatio AI can automate repetitive tasks like writing descriptions, generating emails, or summarizing documents based on user intent and relevant data points within Creatio.
- **Workflow design and automation**. Complex workflows can be time-consuming to build. Creatio AI scenarios can leverage user intent and data context to suggest appropriate actions or even generate basic workflow structures.
- **Personalized user assistance**. Leverage Creatio AI's ability to analyze user behavior and context to provide personalized suggestions and recommendations within the Creatio UI.
Identify opportunities for LLM Integration.

Once you identify user pain points, explore how you can leverage Creatio AI LLM (Large Language Model) capabilities to address them:

- **Utilize NLP (Natural language processing)**. Enable users to describe their needs and goals in natural language. The LLM can interpret these requests and translate them into actionable steps within the Creatio AI scenario.
- **Harness text generation**. Leverage the LLM's ability to generate text to automate tasks like writing reports, summarizing data points, or suggesting relevant information based on user intent and context.
- **Explore data analysis capabilities**. Utilize the LLM to analyze data sets within Creatio and generate insights, identify trends, or answer user questions based on the retrieved information.

## Step 2. Design the intent [​](https://academy.creatio.com/docs/8.x/no-code-customization/8.1/customization-tools/ai-tools/creatio-ai/intent-development-recommendations%20copy\#title-2536-3 "Direct link to Step 2. Design the intent")

For the intent to work correctly, you need to fill out several fields. View our recommendations on filling them out below.

### Name [​](https://academy.creatio.com/docs/8.x/no-code-customization/8.1/customization-tools/ai-tools/creatio-ai/intent-development-recommendations%20copy\#title-2536-4 "Direct link to Name")

A human-readable name for your intent. Must reflect the main goal of the intent, be short, and easy to read.

### Code [​](https://academy.creatio.com/docs/8.x/no-code-customization/8.1/customization-tools/ai-tools/creatio-ai/intent-development-recommendations%20copy\#title-2536-5 "Direct link to Code")

Creatio and the LLM use the code to execute the intent. Must start with a prefix, "Usr" out of the box.

### Description [​](https://academy.creatio.com/docs/8.x/no-code-customization/8.1/customization-tools/ai-tools/creatio-ai/intent-development-recommendations%20copy\#title-2536-6 "Direct link to Description")

A detailed plaintext description of what the intent does, when to use it, and how it behaves. The LLM uses this description to determine which intent to trigger, when, and for what purpose. The description is crucial for the correct operation of the intent and must contain a complete description of your intent.

### Status [​](https://academy.creatio.com/docs/8.x/no-code-customization/8.1/customization-tools/ai-tools/creatio-ai/intent-development-recommendations%20copy\#title-2536-7 "Direct link to Status")

Whether to trigger the intent. Available values:

- **Active**. An active intent, triggered for all users.
- **In development**. An intent in development. Triggered only for users that have access to the "CanDevelopCopilotIntents" ("CanDevelopCopilotIntents" code) system operation.
- **Deactivated** A deactivated intent. Not triggered.

### Prompt [​](https://academy.creatio.com/docs/8.x/no-code-customization/8.1/customization-tools/ai-tools/creatio-ai/intent-development-recommendations%20copy\#title-2536-8 "Direct link to Prompt")

The prompt serves as the initial instruction for the LLM, setting the stage for the entire intent. Here is how to craft an effective prompt:

- **Be specific and actionable**. The prompt must be specific enough to clearly articulate the user goal and provide sufficient context for the LLM and subsequent actions. It must clearly define what the user wants to achieve and include any relevant details.

- **Use actionable verbs**. Use strong action verbs that convey the desired action. This guides the LLM towards the appropriate course of action.

- **Include data and context**. If the intent requires access to specific data or operates within a particular context, incorporate that information into the prompt. This ensures the LLM has the necessary information to understand the user's request.

- **Be straightforward**. Clarify expectations. Provide direct and clear instructions and avoid vague wording.


|     |     |
| --- | --- |
| ❌ | Summarize the case description. |
| ✅ | Summarize the case in no more than 200 characters. Use 3 to 5 sentences. Use professional language without jargon. |

- **Structure the prompt**. Highlight parameters, action names, and important information using blocks like \[\], <>, "", etc.





```text
Open the email template by executing the action [Open Email Page] with <Subject>, <email text> in HTML format and <ID> of Contact or Account.
```

- **Use capital letters for emphasis**. You can highlight especially important information using capital letters. The LLM pays special attention to this text.

- **Give examples of what you expect from the model (few-shot prompting)**. Provide a couple of examples.





```text
The example response must be no longer than 150 characters. Here are the expected examples:
[Response #1] Total score: 17. Errors: Informal greeting, Repeatedly requested already provided client information.
[Response #2] Total score: 23. Errors: No follow-up on additional questions after 5 minutes.
```

- **Specify the steps required to complete a task**. Divide a large prompt into tasks that the LLM will perform.





```text
Your task is to create a summary of no more than 400 words based on the case to the support team. To generate the summary, follow these steps:
1.	Use the current user's context to retrieve the main information about the Case.
2.	Retrieve information about the case owner.
3.	Retrieve information about the case subject.
4.	Retrieve information about the case status.
5.	Generate the case summary. Use no more than 200 characters. Use a 3 to 5 sentence. Use professional language without jargon.
```

- **Describe the parameters of actions and their purposes**. If necessary, describe the parameters, their possible values, and properties in the prompt. This provides a more predictable result and more accurate intent handling.





```text
Execute the function [Check email settings] that has the following parameters:
<ContactID>: a unique ID of the Contact to whom the email can be sent (usually this ID is called Contact and is located on the page where the user is working).
<AccountID>: a unique ID of the account to whom the email can be sent (usually this ID is called Account and is located on the page where the user is working).
One of these parameters can be empty. In response, you will receive a signal indicating whether you can proceed and with which ID.
```

- **Use field names in objects**. The platform works with objects and object fields. If you use field names in the prompt, specify the field names in the object, especially if they differ from the field names on the page.


Learn more about writing effective prompts: [Strategy: write clear instructions (Official OpenAI documentation)](https://platform.openai.com/docs/guides/prompt-engineering/strategy-write-clear-instructions), [Best practices for prompt engineering with the OpenAI API (Official OpenAI documentation)](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-the-openai-api), [Prompting guide 101 (Official Google documentation)](https://services.google.com/fh/files/misc/gemini-for-google-workspace-prompting-guide-101.pdf).

## Step 3. Develop actions [​](https://academy.creatio.com/docs/8.x/no-code-customization/8.1/customization-tools/ai-tools/creatio-ai/intent-development-recommendations%20copy\#title-2536-9 "Direct link to Step 3. Develop actions")

Actions are the building blocks that translate the user's intent into concrete steps in Creatio. They represent the individual actions that Creatio AI needs to execute sequentially to achieve the desired outcome.

You can use actions to do the following:

- **Interact with the platform**: The main purpose of actions is interacting with Creatio, for example, opening a page, populating fields using data, obtaining information, starting a process, forecasting data, sending a request to a web service, etc.
- **Obtain additional context**: If you need to request data that the user does not see on the page, you can use a data retrieval action that returns data as outbound parameters.
- **Check platform data before proceeding**: If you need to verify whether further operations can be performed in Creatio, for example, check if a mailbox is configured, you can use an action for this purpose.

Here is how to define effective actions:

- **Break down the task**. Deconstruct the user goal into a series of smaller, more manageable actions. Aim for a granular level of detail, ensuring each action contributes directly to the overall objective.
- **Establish logical sequence**. Establish a clear and logical sequence for executing the goal actions. Consider any dependencies between actions and ensure they are addressed in the design. Some actions might need to be completed before others can be initiated.
- **Be comprehensive**. Ensure the set of goal actions comprehensively covers all the steps required to fulfill the user intent.

The success of Creatio AI actions hinges on clear and accurate descriptions, input, and output parameters for each action. This data acts as the bridge between the no-code creators defining the actions and the Creatio AI LLM responsible for executing them.

## Step 4. Test and refine the intent [​](https://academy.creatio.com/docs/8.x/no-code-customization/8.1/customization-tools/ai-tools/creatio-ai/intent-development-recommendations%20copy\#title-2536-10 "Direct link to Step 4. Test and refine the intent")

Testing and refinement are crucial steps in ensuring that your intents function as intended and deliver a seamless user experience. This iterative process lets you identify and address any potential issues before deploying the intent to users.

Follow these testing strategies:

- **Thorough Testing**. Rigorously test the intent using various user inputs and edge cases.
- **Focus areas**. Pay close attention to the accuracy of LLM outputs, the execution logic of goal actions, and the overall functionality of the intent.
- **User testing**. Involve potential users in the testing process to gather feedback on the clarity of the prompt, the ease of use, and the overall usefulness of the intent.

Refine your intent in the following ways based on testing:

- **Prompt adjustments**. Refine the prompt to improve clarity, address ambiguities, or provide more specific instructions.
- **Action optimization**. Review the actions to ensure they are executed in the correct sequence, handle potential errors gracefully, and produce the desired outcome.

Treat testing and refinement as an ongoing process. As user needs evolve and new features are introduced, revisit your intents and adjust them to maintain their effectiveness.

* * *

## See also [​](https://academy.creatio.com/docs/8.x/no-code-customization/8.1/customization-tools/ai-tools/creatio-ai/intent-development-recommendations%20copy\#see-also "Direct link to See also")

[Creatio AI overview](https://academy.creatio.com/documents?id=2528)

[Develop Creatio AI intents](https://academy.creatio.com/documents?id=2535)

[Data privacy in Creatio AI](https://academy.creatio.com/documents?id=2529)

[Strategy: write clear instructions (Official OpenAI documentation)](https://platform.openai.com/docs/guides/prompt-engineering/strategy-write-clear-instructions)

[Best practices for prompt engineering with the OpenAI API (Official OpenAI documentation)](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-the-openai-api)

[Prompting guide 101 (Official Google documentation)](https://services.google.com/fh/files/misc/gemini-for-google-workspace-prompting-guide-101.pdf)

- [Step 1. Define user needs](https://academy.creatio.com/docs/8.x/no-code-customization/8.1/customization-tools/ai-tools/creatio-ai/intent-development-recommendations%20copy#title-2536-1)
- [Step 2. Design the intent](https://academy.creatio.com/docs/8.x/no-code-customization/8.1/customization-tools/ai-tools/creatio-ai/intent-development-recommendations%20copy#title-2536-3)
  - [Name](https://academy.creatio.com/docs/8.x/no-code-customization/8.1/customization-tools/ai-tools/creatio-ai/intent-development-recommendations%20copy#title-2536-4)
  - [Code](https://academy.creatio.com/docs/8.x/no-code-customization/8.1/customization-tools/ai-tools/creatio-ai/intent-development-recommendations%20copy#title-2536-5)
  - [Description](https://academy.creatio.com/docs/8.x/no-code-customization/8.1/customization-tools/ai-tools/creatio-ai/intent-development-recommendations%20copy#title-2536-6)
  - [Status](https://academy.creatio.com/docs/8.x/no-code-customization/8.1/customization-tools/ai-tools/creatio-ai/intent-development-recommendations%20copy#title-2536-7)
  - [Prompt](https://academy.creatio.com/docs/8.x/no-code-customization/8.1/customization-tools/ai-tools/creatio-ai/intent-development-recommendations%20copy#title-2536-8)
- [Step 3. Develop actions](https://academy.creatio.com/docs/8.x/no-code-customization/8.1/customization-tools/ai-tools/creatio-ai/intent-development-recommendations%20copy#title-2536-9)
- [Step 4. Test and refine the intent](https://academy.creatio.com/docs/8.x/no-code-customization/8.1/customization-tools/ai-tools/creatio-ai/intent-development-recommendations%20copy#title-2536-10)
- [See also](https://academy.creatio.com/docs/8.x/no-code-customization/8.1/customization-tools/ai-tools/creatio-ai/intent-development-recommendations%20copy#see-also)