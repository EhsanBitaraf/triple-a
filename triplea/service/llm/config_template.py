# How to suppress OpenAI API warnings in Python
# https://stackoverflow.com/questions/71893613/how-to-suppress-openai-api-warnings-in-python
import logging
import os
import json
from pathlib import Path
from triplea.config.settings import SETTINGS
from triplea.service.click_logger import logger
from triplea.utils.general import print_pretty_dict


logging.getLogger().setLevel(logging.CRITICAL)




def convert_Prompt_text_to_template_json(prompt_string,
                           model_template_id= "ollama",
                           model_name= "llama3.2:3b-instruct-fp16",
                           base_path="http://localhost:11434/v1"):
   

   # Your original string
   original_string = """


### Instruction

Your task is to evaluate the title and abstract of the given article, then categorize it into one of the predefined groups below. Use the group descriptions as guidance and respond in JSON format. Ensure that the output includes the group ID, group name, and an optional explanation if necessary.

### Groups:

1. **Architecture and Modeling**  
   - Focused on the technical foundations of OpenEHR, including reference models, templates, and platform architecture.  
   - Subtopics: semantic modeling and computational methods.

2. **Implementation and Case Studies**  
   - Real-world applications, pilot studies, and lessons learned in OpenEHR implementations.  
   - Subcategories: *Challenges in Implementation* or *Regional/National Deployments*.

3. **Interoperability and Standards**  
   - Research on OpenEHR integration with standards like HL7 FHIR, SNOMED CT, or DICOM.  
   - Subcategories: *Data Exchange Frameworks* or *Semantic Interoperability*.

4. **Clinical Decision Support**  
   - Articles about OpenEHR's role in clinical decision-making, algorithms, and AI-driven applications.  
   - Subcategory: *AI/ML Integration*.

5. **Archetype Development and Management**  
   - Designing, validating, and managing archetypes/templates with clinical relevance.  
   - Subcategories: *Tooling for Archetype Design* or *Governance of Clinical Content*.

6. **Deployment and System Integration**  
   - Integration into healthcare infrastructures, including cloud-based and legacy systems.  
   - Subcategories: *Cloud-based Deployments*, *Legacy System Migration*, or *Security and Privacy*.

7. **Usability and User-Centered Design**  
   - Focus on stakeholder interactions, usability studies, and human factors in OpenEHR system adoption.

8. **Data Analytics and Research**  
   - Secondary use of OpenEHR data in research, analytics, or population health.  
   - Subcategories: *Big Data Applications* or *Epidemiological Studies*.

9. **Education and Capacity Building**  
   - Teaching and training OpenEHR practices for healthcare professionals and developers.

10. **Economic and Policy Implications**  
    - Cost-effectiveness studies and policy-level evaluations of OpenEHR adoption.

11. **Comparison with Alternative Frameworks**  
    - Contrasting OpenEHR with other EHR standards or exploring alternatives.

12. **Future Directions and Innovations**  
    - Speculative research, emerging technologies, or AI integrations in OpenEHR.

### Format:

Respond in the following JSON structure:
```json
{
  "groupID": 2,
  "group": "Implementation and Case Studies",
  "description": "Optional explanation if necessary"
}
```

---

### Input  
**Title**: {Title}  
**Abstract**: {Abstract}  


"""
   original_string = prompt_string
   # Create a dictionary with the 'template' field
   data = {"template": original_string}

   data = {
      "version" : "0.0.2",
      "stop_immediately": 0,
      "model_template_id": model_template_id,
      "model_name": model_name,
      "base_path": base_path,
      "temperature": 0.5,
      "frequency_penalty": 0,
      "presence_penalty": 0,
      "max_tokens": 512,
      "top_p": 0.9,
      "response_must_be_json": True,
      "template": original_string
   }

   # Convert the dictionary to a JSON string
   json_string = json.dumps(data)

   print_pretty_dict(data)
   print(json_string)
   with open(f"{model_template_id}.json",'w',encoding='utf8') as f:
      f.write(json_string)
   print(f"Template save in {model_template_id}.json")




def read_llm_template():
    if os.path.exists(SETTINGS.AAA_LLM_TEMPLATE_FILE) is False:
        # raise FileNotFoundError(f"File {SETTINGS.AAA_LLM_TEMPLATE_FILE} Not Found.")
        logger.WARNING("LLM template not found or not configured.")
        return None

    with open(SETTINGS.AAA_LLM_TEMPLATE_FILE, encoding="utf-8") as f:
        d = json.load(f)
    return d



def read_llm_template_from_file(llmtemplate_filename):
    # llmtemplate_dir = Path(os.path.dirname(SETTINGS.AAA_LLM_TEMPLATE_FILE))
    # llmtemplate = llmtemplate_dir / llmtemplate_filename
    llmtemplate = Path(llmtemplate_filename)
    if os.path.exists(llmtemplate):
        pass
        # print(f"The file {llmtemplate} exists")
    else:
        print(f"The file {llmtemplate} does not exist")
        exit()
    with open(llmtemplate, encoding='utf-8') as f:
        d = json.load(f)
    return d

