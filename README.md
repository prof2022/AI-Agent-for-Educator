# Curriculum Builder AI System

## Overview
The **Curriculum Builder AI System** is an AI-powered educational tool designed to assist educators in generating structured schemes of work, lesson plans, and lesson notes based on **Nigerian academic standards**. This system leverages **machine learning** and **natural language processing (NLP)** to ensure content is relevant, well-structured, and aligned with curriculum requirements.

## Features
### AI-Driven Curriculum Development
- **Scheme of Work Generation**: Creates structured outlines for academic terms and subjects.
- **Lesson Plan Creation**: Develops detailed lesson plans based on syllabus requirements.
- **Lesson Notes Generation**: Produces well-detailed lesson notes for effective teaching.

### Intelligent Content Retrieval
- **Pinecone for Vector Search**: Efficiently retrieves relevant academic materials using vector similarity search.
- **Exa API for Web Search**: Fetches contextual web data to supplement generated content with real-world examples.
- **Metadata Extraction**: Gathers additional insights to enhance lesson relevance and engagement.

### Customization and Localization
- **Tailored for Nigerian Curriculum**: Ensures alignment with Nigerian **Ministry of Education** standards.
- **Subject & Grade-Level Adaptability**: Generates materials for different subjects and educational levels.
- **Cultural Relevance**: Incorporates local examples and contexts for better student comprehension.

## Technologies Used
- **Machine Learning & NLP**: Enhances content generation and structuring.
- **Pinecone**: Provides vector similarity search for optimized data retrieval.
- **Exa API**: Enables real-time web search for supplementary academic content.
- **Python**: Core programming language for development.
- **dotenv**: Manages environment variables securely.

## Installation
### Prerequisites
1. Python 3.8+
2. `pip` (Python package manager)
3. API keys for Pinecone and Exa API

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/curriculum-builder-ai.git
   cd curriculum-builder-ai
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   - Create a `.env` file in the root directory.
   - Add the following variables:
     ```env
     PINECONE_API_KEY=your_pinecone_api_key
     EXA_API_KEY=your_exa_api_key
     ```
4. Run the project:
   ```bash
   python main.py
   ```

## Usage
### Example Commands
1. **Generate a Scheme of Work**:
   ```text
   Create a scheme of work for Junior Secondary School Mathematics, Term 1.
   ```
2. **Generate a Lesson Plan**:
   ```text
   Generate a lesson plan for Basic Science, Topic: Photosynthesis, Grade: Primary 6.
   ```
3. **Create Lesson Notes**:
   ```text
   Provide lesson notes on "The Water Cycle" for Senior Secondary School Geography.
   ```

## File Structure
```
.
├── main.py                        # Entry point for the application
├── src/
│   ├── curriculum_builder/
│   │   ├── main_system.py          # Multi-agent system coordination
│   │   ├── modules/
│   │   │   ├── scheme_generator.py
│   │   │   ├── lesson_plan_generator.py
│   │   │   ├── lesson_notes_generator.py
│   │   │   ├── content_retrieval.py
│   │   │   └── metadata_extractor.py
│   │   └── config.json              # Configuration settings
├── tests/
│   └── test_modules.py              # Unit tests for modules
├── requirements.txt                 # Python dependencies
├── .env                             # Environment variables
└── README.md                        # Project documentation
```

## Testing
Run unit tests to validate functionality:
```bash
python -m unittest discover tests/
```

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature/fix.
3. Submit a pull request with a clear description of changes.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Future Enhancements
- **Integration with LMS**: Connect the system with learning management platforms.
- **Multi-language Support**: Expand capabilities for regional languages.
- **AI-Powered Assessment Generator**: Generate quizzes and tests based on generated content.
