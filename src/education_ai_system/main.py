# src/education_ai_system/main.py

from src.education_ai_system.crew import build_education_crew
from src.education_ai_system.embeddings.pinecone_manager import upsert_to_pinecone
from src.education_ai_system.data_processing.pdf_extractor import extract_text_and_tables
from src.education_ai_system.data_processing.text_chunker import split_text_into_chunks
from src.education_ai_system.data_processing.metadata_extractor import extract_metadata

import os
import json

def process_and_index_pdf(pdf_path):
    # Step 1: Extract text and tables
    text, tables = extract_text_and_tables(pdf_path)

    # Step 2: Chunk the extracted text
    chunks = split_text_into_chunks(text)

    # Step 3: Extract metadata and upsert embeddings
    metadata = [extract_metadata(chunk) for chunk in chunks]
    upsert_to_pinecone(chunks, metadata)

def run_and_save_crew_output(inputs):
    # Build the Crew and initiate shared context
    crew = build_education_crew()

    # Execute the crew tasks and retrieve results
    result = crew.kickoff(inputs=inputs)

    # Initialize shared context for subsequent tasks
    shared_context = {}

    # Extract and assign output from each task in sequence
    for task in crew.tasks:
        # Ensure the agent exists before accessing its role
        if task.agent and task.agent.role:
            # Access the result of the specific task by its agent's role
            task_result = getattr(result, task.agent.role.replace(" ", "_").lower(), None)

            if task_result is not None:
                # Update shared context with the agent's role and task result
                shared_context[task.agent.role] = task_result

                # Print task result for verification (optional)
                print(f"Output from {task.agent.role}:")
                print(task_result)
        else:
            print("Task agent or role is not defined.")

    return result

# Main function
# if __name__ == "__main__":
#     pdf_path = '/Users/libertyelectronics/Desktop/curriculum_builder/CB_Agent/data/pri1-3_civic (1).pdf'  # Update to actual file path
#     process_and_index_pdf(pdf_path)

#     # Sample user input
#     inputs = {'subject': 'CIVIC EDUCATION', 'grade_level': 'PRIMARY TWO', 'topic': 'OUR COMMUNITY'}

#     # Save inputs for later use in the conversion script
#     with open("user_inputs.json", "w") as f:
#         json.dump(inputs, f)

#     run_and_save_crew_output(inputs)