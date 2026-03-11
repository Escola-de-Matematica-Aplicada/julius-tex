Key capabilities
About this model
We introduce DeepSeek-V3.2 Speciale, a model that harmonizes high computational efficiency with superior reasoning and agent performance. Our approach is built upon three key technical breakthroughs.
Key model capabilities
DeepSeek Sparse Attention (DSA): We introduce DSA, an efficient attention mechanism that substantially reduces computational complexity while preserving model performance, specifically optimized for long-context scenarios.
Scalable Reinforcement Learning Framework: By implementing a robust RL protocol and scaling post-training compute, DeepSeek-V3.2 performs comparably to GPT-5. Notably, our high-compute variant, DeepSeek-V3.2-Speciale, surpasses GPT-5 and exhibits reasoning proficiency on par with Gemini-3.0-Pro.
Large-Scale Agentic Task Synthesis Pipeline: To integrate reasoning into tool-use scenarios, we developed a novel synthesis pipeline that systematically generates training data at scale. This facilitates scalable agentic post-training, improving compliance and generalization in complex interactive environments.
Use cases
See Responsible AI for additional considerations for responsible use.
Key use cases
The provider has not supplied this information.
Out of scope use cases
Microsoft and external researchers have found Deepseek V3.2 Speciale to be less aligned than other models -- meaning the model appears to have undergone less refinement designed to make its behavior and outputs more safe and appropriate for users -- resulting in (i) higher risks that the model will produce potentially harmful content and (ii) lower scores on safety and jailbreak benchmarks. We recommend customers use Azure AI Content Safety in conjunction with this model and conduct their own evaluations on production systems.
Pricing
Pricing is based on a number of factors, including deployment type and tokens used. See pricing details here.
Technical specs
The provider has not supplied this information.
Training cut-off date
The provider has not supplied this information.
Training time
The provider has not supplied this information.
Input formats
Text
Output formats
Text
Supported languages
The provider has not supplied this information.
Sample JSON response
The provider has not supplied this information.
Model architecture
The provider has not supplied this information.
Long context
The provider has not supplied this information.
Optimizing model performance
The provider has not supplied this information.
Additional assets
The provider has not supplied this information.
Training disclosure
Training, testing and validation
The provider has not supplied this information.
Distribution
Distribution channels
The provider has not supplied this information.
More information
Learn more: original model announcement
DeepSeek-V3.2 Speciale introduces significant updates to its chat template compared to prior versions. The primary changes involve a revised format for tool calling and the introduction of a "thinking with tools" capability.
To assist the community in understanding and adapting to this new template, we have provided a dedicated encoding folder, which contains Python scripts and test cases demonstrating how to encode messages in OpenAI-compatible format into input strings for the model and how to parse the model's text output.
Content filtering
When deployed via Microsoft Foundry, prompts and completions are passed through a default configuration of Azure AI Content Safety classification models to detect and prevent the output of harmful content. Learn more about Azure AI Content Safety. Configuration options for content filtering vary when you deploy a model for production in Microsoft Foundry; learn more.
