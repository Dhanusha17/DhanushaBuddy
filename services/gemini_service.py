import os
import json
import streamlit as st
from google import genai
from google.genai import errors
from google.genai import types
from dotenv import load_dotenv, find_dotenv

# Force explicit loading of the exact .env file in the current working directory
dotenv_path = find_dotenv('.env')
load_dotenv(dotenv_path)

from utils.prompts import (
    LEARN_CONCEPTS_SYSTEM_INSTRUCTION, 
    LEARN_CONCEPTS_USER_TEMPLATE,
    AI_CHAT_SYSTEM_INSTRUCTION,
    CODING_GENERATOR_SYSTEM_INSTRUCTION,
    CODING_GENERATOR_USER_TEMPLATE,
    CODING_EVALUATOR_SYSTEM_INSTRUCTION,
    CODING_EVALUATOR_USER_TEMPLATE,
    APTITUDE_QUIZ_SYSTEM_INSTRUCTION,
    APTITUDE_QUIZ_USER_TEMPLATE,
    HR_SETUP_SYSTEM_INSTRUCTION,
    HR_SETUP_USER_TEMPLATE,
    HR_EVALUATE_SYSTEM_INSTRUCTION,
    HR_EVALUATE_USER_TEMPLATE,
    HR_REPORT_SYSTEM_INSTRUCTION,
    HR_REPORT_USER_TEMPLATE
)

class GeminiService:
    """
    Service class responsible for communicating with Google's Gemini models using the google-genai SDK.
    Handles configuration, exception control, and response parsing.
    """
    def __init__(self):
        self.api_key = self._resolve_api_key()
        self.client = None
        self.model_name = "gemini-2.5-flash"
        
        if self.api_key:
            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception:
                pass

    def _resolve_api_key(self) -> str:
        """
        Resolves the Gemini API Key from environment variables (local) or Streamlit secrets (production).
        """
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            try:
                if "GEMINI_API_KEY" in st.secrets:
                    api_key = st.secrets["GEMINI_API_KEY"]
            except Exception:
                pass
        return api_key

    def is_configured(self) -> bool:
        """
        Returns True if the GenAI client was successfully initialized.
        """
        return self.client is not None
        
    def _handle_api_error(self, e: Exception) -> str:
        """Helper to parse API Errors according to strict requirements"""
        error_msg = str(e).lower()
        if "api_key_invalid" in error_msg or "api key not valid" in error_msg or "api key" in error_msg or "400" in error_msg or "403" in error_msg:
            return "Invalid Gemini API key."
        return f"Gemini API Error: {str(e)}"

    def get_concept_explanation(self, subject: str, topic: str) -> dict:
        if not self.is_configured():
            return {"error": "Gemini API key not found. Please configure your .env file."}

        try:
            user_prompt = LEARN_CONCEPTS_USER_TEMPLATE.format(subject=subject, topic=topic)
            config = types.GenerateContentConfig(
                system_instruction=LEARN_CONCEPTS_SYSTEM_INSTRUCTION,
                response_mime_type="application/json",
                temperature=0.2
            )
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=user_prompt,
                config=config
            )
            parsed_data = json.loads(response.text)
            return parsed_data
            
        except errors.APIError as e:
            return {"error": self._handle_api_error(e)}
        except json.JSONDecodeError:
            return {"error": "Failed to parse the explanation content. Please try generating the concept again."}
        except Exception as e:
            return {"error": f"An unexpected error occurred: {str(e)}"}

    def get_chat_response(self, messages: list, system_instruction: str = None) -> str:
        if not self.is_configured():
            return "Gemini API key not found. Please configure your .env file."

        try:
            contents = []
            for msg in messages:
                role = "user" if msg["role"] == "user" else "model"
                contents.append(
                    types.Content(
                        role=role,
                        parts=[types.Part.from_text(text=msg["content"])]
                    )
                )
            
            config = types.GenerateContentConfig(
                system_instruction=system_instruction or AI_CHAT_SYSTEM_INSTRUCTION,
                temperature=0.7
            )
            
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=contents,
                config=config
            )
            return response.text
            
        except errors.APIError as e:
            return self._handle_api_error(e)
        except Exception as e:
            return f"An unexpected error occurred during chat generation: {str(e)}"

    def generate_coding_problem(self, language: str, difficulty: str) -> dict:
        if not self.is_configured():
            return {"error": "Gemini API key not found. Please configure your .env file."}

        try:
            user_prompt = CODING_GENERATOR_USER_TEMPLATE.format(language=language, difficulty=difficulty)
            config = types.GenerateContentConfig(
                system_instruction=CODING_GENERATOR_SYSTEM_INSTRUCTION,
                response_mime_type="application/json",
                temperature=0.7
            )
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=user_prompt,
                config=config
            )
            parsed_data = json.loads(response.text)
            return parsed_data
            
        except errors.APIError as e:
            return {"error": self._handle_api_error(e)}
        except json.JSONDecodeError:
            return {"error": "Failed to parse the generated coding challenge. Please try creating a new problem."}
        except Exception as e:
            return {"error": f"An unexpected error occurred: {str(e)}"}

    def evaluate_coding_solution(self, problem: dict, language: str, code: str) -> dict:
        if not self.is_configured():
            return {"error": "Gemini API key not found. Please configure your .env file."}

        try:
            user_prompt = CODING_EVALUATOR_USER_TEMPLATE.format(
                title=problem.get("title", ""),
                problem_statement=problem.get("problem_statement", ""),
                language=language,
                code=code
            )
            config = types.GenerateContentConfig(
                system_instruction=CODING_EVALUATOR_SYSTEM_INSTRUCTION,
                response_mime_type="application/json",
                temperature=0.2
            )
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=user_prompt,
                config=config
            )
            parsed_data = json.loads(response.text)
            return parsed_data
            
        except errors.APIError as e:
            return {"error": self._handle_api_error(e)}
        except json.JSONDecodeError:
            return {"error": "Failed to parse the evaluation report. Please submit your code again."}
        except Exception as e:
            return {"error": f"An unexpected error occurred: {str(e)}"}

    def generate_aptitude_quiz(self, category: str, difficulty: str) -> list:
        if not self.is_configured():
            return [{"error": "Gemini API key not found. Please configure your .env file."}]

        try:
            user_prompt = APTITUDE_QUIZ_USER_TEMPLATE.format(category=category, difficulty=difficulty)
            config = types.GenerateContentConfig(
                system_instruction=APTITUDE_QUIZ_SYSTEM_INSTRUCTION,
                response_mime_type="application/json",
                temperature=0.7
            )
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=user_prompt,
                config=config
            )
            parsed_data = json.loads(response.text)
            return parsed_data
            
        except errors.APIError as e:
            return [{"error": self._handle_api_error(e)}]
        except json.JSONDecodeError:
            return [{"error": "Failed to parse the generated quiz. Please try generating again."}]
        except Exception as e:
            return [{"error": f"An unexpected error occurred: {str(e)}"}]

    def setup_hr_interview(self, category: str, difficulty: str) -> dict:
        if not self.is_configured():
            return {"error": "Gemini API key not found. Please configure your .env file."}

        try:
            user_prompt = HR_SETUP_USER_TEMPLATE.format(category=category, difficulty=difficulty)
            config = types.GenerateContentConfig(
                system_instruction=HR_SETUP_SYSTEM_INSTRUCTION,
                response_mime_type="application/json",
                temperature=0.7
            )
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=user_prompt,
                config=config
            )
            parsed_data = json.loads(response.text)
            return parsed_data
            
        except errors.APIError as e:
            return {"error": self._handle_api_error(e)}
        except json.JSONDecodeError:
            return {"error": "Failed to parse the first question."}
        except Exception as e:
            return {"error": f"An unexpected error occurred: {str(e)}"}

    def evaluate_hr_answer(self, category: str, difficulty: str, question_number: int, total_questions: int, question: str, answer: str) -> dict:
        if not self.is_configured():
            return {"error": "Gemini API key not found. Please configure your .env file."}

        try:
            user_prompt = HR_EVALUATE_USER_TEMPLATE.format(
                category=category, 
                difficulty=difficulty,
                question_number=question_number,
                total_questions=total_questions,
                question=question,
                answer=answer
            )
            config = types.GenerateContentConfig(
                system_instruction=HR_EVALUATE_SYSTEM_INSTRUCTION,
                response_mime_type="application/json",
                temperature=0.7
            )
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=user_prompt,
                config=config
            )
            parsed_data = json.loads(response.text)
            return parsed_data
            
        except errors.APIError as e:
            return {"error": self._handle_api_error(e)}
        except json.JSONDecodeError:
            return {"error": "Failed to parse the evaluation."}
        except Exception as e:
            return {"error": f"An unexpected error occurred: {str(e)}"}

    def generate_hr_report(self, category: str, difficulty: str, history: list) -> dict:
        if not self.is_configured():
            return {"error": "Gemini API key not found. Please configure your .env file."}

        try:
            history_text = "\n\n".join([
                f"Q{i+1}: {item['question']}\nA{i+1}: {item['answer']}\nEval: {item.get('evaluation', {}).get('strengths', '')} / {item.get('evaluation', {}).get('areas_for_improvement', '')}"
                for i, item in enumerate(history)
            ])
            user_prompt = HR_REPORT_USER_TEMPLATE.format(
                category=category, 
                difficulty=difficulty,
                history=history_text
            )
            config = types.GenerateContentConfig(
                system_instruction=HR_REPORT_SYSTEM_INSTRUCTION,
                response_mime_type="application/json",
                temperature=0.7
            )
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=user_prompt,
                config=config
            )
            parsed_data = json.loads(response.text)
            return parsed_data
            
        except errors.APIError as e:
            return {"error": self._handle_api_error(e)}
        except json.JSONDecodeError:
            return {"error": "Failed to parse the final report."}
        except Exception as e:
            return {"error": f"An unexpected error occurred: {str(e)}"}
