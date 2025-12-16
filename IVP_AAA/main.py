import os
import sys
import json
import cv2
import numpy as np
import importlib.util
from pathlib import Path
import google.generativeai as genai
from datetime import datetime
import base64
import io
from PIL import Image
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class IVPAnalyzer:
    def __init__(self):
        logger.info("Initializing IVP Analyzer...")
        self.analyser_data = self.load_analyser_data()
        self.current_analysis_id = len(self.analyser_data)
        self.ivp_modules_path = os.path.abspath("IVP_Modules")
        logger.info(f"Found {len(self.analyser_data)} existing analyses")
        logger.info(f"IVP modules path: {self.ivp_modules_path}")
        
        # Configure Gemini AI keys (prioritize built-in fallback first)
        fallback_key = "AIzaSyBLt-BtV2RXMeTIgo4Xqt_1RwmMV_usXzY"
        env_keys = [
            os.getenv('GOOGLE_API_KEY_1'),
            os.getenv('GOOGLE_API_KEY_2'),
            os.getenv('GOOGLE_API_KEY_3')
        ]
        # Keep only provided env keys
        env_keys = [k for k in env_keys if k]
        # Fallback first so we use it immediately if env keys are invalid
        self.api_keys = [fallback_key] + env_keys
        
        if not self.api_keys:
            raise ValueError("No Gemini API keys found")
        
        # Try to configure with the first available key
        self.current_key_index = 0
        self.configure_gemini()
        logger.info("IVP Analyzer initialized successfully")
    
    def configure_gemini(self):
        """Configure Gemini with current API key"""
        try:
            genai.configure(api_key=self.api_keys[self.current_key_index])
            self.model = genai.GenerativeModel('gemini-2.5-flash')
            logger.info(f"Gemini configured with key {self.current_key_index + 1}/{len(self.api_keys)}")
        except Exception as e:
            logger.error(f"Failed to configure Gemini with key {self.current_key_index + 1}: {e}")
            raise
    
    def try_next_gemini_key(self):
        """Try the next available Gemini API key"""
        if self.current_key_index < len(self.api_keys) - 1:
            self.current_key_index += 1
            logger.info(f"Trying next Gemini API key: {self.current_key_index + 1}/{len(self.api_keys)}")
            self.configure_gemini()
            return True
        else:
            logger.error("All Gemini API keys exhausted")
            return False
        
    def load_analyser_data(self):
        """Load existing analysis data from Analyser.json"""
        try:
            with open('Analyser.json', 'r') as f:
                data = f.read().strip()
                # Check if file is empty
                if not data:
                    logger.warning("Analyser.json is empty, returning empty list")
                    return []
                return json.loads(data)
        except FileNotFoundError:
            logger.info("Analyser.json not found, starting with empty list")
            return []
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing Analyser.json: {e}. File may be corrupted. Starting with empty list.")
            # Backup the corrupted file
            try:
                import shutil
                backup_path = 'Analyser.json.backup'
                shutil.copy2('Analyser.json', backup_path)
                logger.info(f"Backed up corrupted file to {backup_path}")
            except Exception as backup_error:
                logger.warning(f"Could not backup corrupted file: {backup_error}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error loading Analyser.json: {e}. Starting with empty list.")
            return []
    
    def save_analyser_data(self):
        """Save analysis data to Analyser.json"""
        try:
            # Ensure analyser_data is a list
            if not isinstance(self.analyser_data, list):
                logger.error(f"analyser_data is not a list (type: {type(self.analyser_data)}). Resetting to empty list.")
                self.analyser_data = []
            
            # Write to temporary file first, then rename (atomic write)
            temp_path = 'Analyser.json.tmp'
            with open(temp_path, 'w') as f:
                json.dump(self.analyser_data, f, indent=2)
            
            # Atomic rename (works on Windows too)
            if os.path.exists('Analyser.json'):
                os.replace(temp_path, 'Analyser.json')
            else:
                os.rename(temp_path, 'Analyser.json')
            
            logger.info(f"Successfully saved {len(self.analyser_data)} analysis entries to Analyser.json")
        except Exception as e:
            logger.error(f"Error saving analyser data: {e}")
            # Clean up temp file if it exists
            try:
                if os.path.exists('Analyser.json.tmp'):
                    os.remove('Analyser.json.tmp')
            except:
                pass
            raise
    
    def get_ivp_module_function(self, module_name):
        """Dynamically import and return IVP module function"""
        # Use absolute path to ensure we find the modules
        module_file = os.path.abspath(os.path.join(self.ivp_modules_path, f"{module_name}.py"))
        
        logger.debug(f"Looking for module: {module_file}")
        logger.debug(f"IVP modules path: {os.path.abspath(self.ivp_modules_path)}")
        logger.debug(f"Module exists: {os.path.exists(module_file)}")
        
        if not os.path.exists(module_file):
            logger.warning(f"Module file not found: {module_file}")
            # List files in IVP_Modules directory for debugging
            try:
                ivp_dir = os.path.abspath(self.ivp_modules_path)
                if os.path.exists(ivp_dir):
                    files = os.listdir(ivp_dir)
                    logger.debug(f"Files in IVP_Modules: {files}")
                else:
                    logger.error(f"IVP_Modules directory not found: {ivp_dir}")
            except Exception as e:
                logger.error(f"Error listing IVP_Modules directory: {e}")
            return None
            
        try:
            spec = importlib.util.spec_from_file_location(module_name, module_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Create a wrapper function that executes the module's main code
            def module_wrapper():
                # Execute the module's main code by simulating __name__ == "__main__"
                # Most IVP modules have their main logic in the if __name__ == "__main__" block
                try:
                    # First try to call process_image() function (our fixed version)
                    if hasattr(module, 'process_image'):
                        logger.debug(f"Calling process_image() from module {module_name}")
                        module.process_image()
                        return
                    
                    # Try to find and call a main function
                    function_names = [
                        'main',
                        'process_image',
                        'process'
                    ]
                    
                    for func_name in function_names:
                        if hasattr(module, func_name):
                            attr = getattr(module, func_name)
                            if callable(attr):
                                logger.debug(f"Calling function {func_name} from module {module_name}")
                                attr()
                                return
                    
                    # Try to find function based on module name (convert spaces and title case to function name)
                    # e.g., "Digital Image Representation" -> "digital_image_representation"
                    # Also try variations: remove "and", "the", etc.
                    base_name = module_name.lower().replace(' ', '_')
                    module_func_name_variants = [
                        base_name,  # "digital_image_representation" or "thresholding_and_intensity_slicing"
                        base_name.replace('_and_', '_'),  # "thresholding_intensity_slicing" (remove "and")
                        base_name.replace(' and ', '_'),  # handle space around "and"
                        base_name.replace(' and ', '_').replace('_and_', '_'),  # both
                    ]
                    # Remove duplicates while preserving order
                    seen = set()
                    unique_variants = []
                    for variant in module_func_name_variants:
                        if variant not in seen:
                            seen.add(variant)
                            unique_variants.append(variant)
                    module_func_name_variants = unique_variants
                    
                    for module_func_name in module_func_name_variants:
                        if hasattr(module, module_func_name):
                            attr = getattr(module, module_func_name)
                            if callable(attr):
                                logger.debug(f"Calling function {module_func_name} from module {module_name}")
                                attr()
                                return
                    
                    # Also try looking for any function in the module (most modules have one main function)
                    module_attrs = [attr for attr in dir(module) if not attr.startswith('_') and callable(getattr(module, attr))]
                    # Filter out standard library functions
                    module_attrs = [attr for attr in module_attrs if attr not in ['print', 'open', 'range', 'len', 'str', 'int', 'float', 'list', 'dict', 'tuple']]
                    if len(module_attrs) == 1:
                        # If there's exactly one function, it's probably the main one
                        func_name = module_attrs[0]
                        logger.debug(f"Found single function {func_name} in module {module_name}, calling it")
                        getattr(module, func_name)()
                        return
                    
                    # Execute the module's __main__ block
                    # Read the source and manually execute just the __main__ block
                    try:
                        with open(module_file, 'r', encoding='utf-8') as f:
                            source_lines = f.readlines()
                        
                        # Find the __main__ block and extract what it does
                        in_main_block = False
                        main_block_code = []
                        for i, line in enumerate(source_lines):
                            if 'if __name__' in line and "'__main__'" in line:
                                in_main_block = True
                                continue
                            if in_main_block:
                                # Check for indentation - if line starts with non-whitespace at same level as if, we're done
                                if line.strip() and not line.startswith((' ', '\t')) and not line.strip().startswith('#'):
                                    break
                                main_block_code.append(line)
                        
                        if main_block_code:
                            # Execute just the main block code
                            main_block_source = ''.join(main_block_code)
                            exec_namespace = module.__dict__.copy()
                            exec(main_block_source, exec_namespace)
                            # Update module with any new definitions
                            module.__dict__.update(exec_namespace)
                            logger.debug(f"Executed __main__ block code for module {module_name}")
                            return
                        else:
                            # Fallback: try to execute the whole file with __name__ set to '__main__'
                            logger.debug(f"Could not extract __main__ block, trying full execution")
                            with open(module_file, 'r', encoding='utf-8') as f:
                                source_code = f.read()
                            exec_namespace = module.__dict__.copy()
                            exec_namespace['__name__'] = '__main__'
                            compiled_code = compile(source_code, module_file, 'exec')
                            exec(compiled_code, exec_namespace)
                            module.__dict__.update({k: v for k, v in exec_namespace.items() if not k.startswith('__')})
                            logger.debug(f"Executed full module with __name__='__main__' for {module_name}")
                            return
                    except Exception as exec_error:
                        logger.error(f"Error executing __main__ block for {module_name}: {exec_error}")
                        raise
                    
                except Exception as e:
                    logger.error(f"Error executing module {module_name}: {e}")
                    import traceback
                    logger.error(traceback.format_exc())
                    raise
            
            return module_wrapper
                    
        except Exception as e:
            logger.error(f"Error loading module {module_name}: {e}")
            return None
    
    def process_image_with_ivp(self, image_path, topics):
        """Process image with selected IVP topics"""
        logger.info(f"Processing image: {image_path}")
        logger.info(f"Selected topics: {topics}")
        results = {}
        
        # Load image
        img = cv2.imread(image_path)
        if img is None:
            logger.error(f"Could not load image: {image_path}")
            return {"error": f"Could not load image: {image_path}"}
        
        logger.info(f"Image loaded successfully, shape: {img.shape}")
        
        # Create temporary directory for processing
        temp_dir = "temp_processing"
        try:
            os.makedirs(temp_dir, exist_ok=True)
            logger.info(f"Created temp directory: {temp_dir}")
        except Exception as e:
            logger.error(f"Failed to create temp directory: {e}")
            return {"error": f"Failed to create temp directory: {e}"}
        
        # Save image as 'image.jpg' for IVP modules
        temp_image_path = os.path.join(temp_dir, "image.jpg")
        try:
            cv2.imwrite(temp_image_path, img)
            logger.info(f"Saved image to temp path: {temp_image_path}")
        except Exception as e:
            logger.error(f"Failed to save image: {e}")
            return {"error": f"Failed to save image: {e}"}
        
        # Process with each selected topic
        for topic in topics:
            logger.info(f"Processing topic: {topic}")
            try:
                # Change to temp directory for processing
                original_cwd = os.getcwd()
                os.chdir(temp_dir)
                logger.debug(f"Changed to temp directory: {temp_dir}")
                
                # Get and execute IVP module
                ivp_function = self.get_ivp_module_function(topic)
                if ivp_function:
                    logger.info(f"Executing IVP module for: {topic}")
                    ivp_function()
                    
                    # Read output files if any
                    # List all files first for debugging
                    all_files = os.listdir('.')
                    logger.debug(f"All files in temp directory: {all_files}")
                    
                    output_files = [f for f in all_files if f.endswith(('.txt', '.jpg', '.png', '.jpeg', '.bmp')) and f != 'image.jpg']
                    logger.info(f"Found {len(output_files)} output files: {output_files}")
                    
                    # If no output files found, check if module wrote to a specific directory
                    if len(output_files) == 0:
                        logger.warning(f"No output files found in current directory after executing {topic}")
                        logger.debug(f"Current working directory: {os.getcwd()}")
                        # Check for common output directories
                        for output_dir in ['output', 'results', 'temp_processing']:
                            if os.path.exists(output_dir):
                                dir_files = [f for f in os.listdir(output_dir) if f.endswith(('.txt', '.jpg', '.png', '.jpeg', '.bmp'))]
                                if dir_files:
                                    logger.info(f"Found {len(dir_files)} output files in {output_dir}: {dir_files}")
                                    output_files = [os.path.join(output_dir, f) for f in dir_files]
                                    break
                    topic_results = []
                    
                    for output_file in output_files:
                        if output_file.endswith('.txt'):
                            with open(output_file, 'r') as f:
                                content = f.read()
                                topic_results.append(content)
                                logger.debug(f"Read text output: {output_file} ({len(content)} chars)")
                        else:
                            # For image outputs, convert to base64
                            with open(output_file, 'rb') as f:
                                img_data = f.read()
                                img_b64 = base64.b64encode(img_data).decode()
                                topic_results.append(f"Image output: {img_b64}")
                                logger.debug(f"Read image output: {output_file} ({len(img_data)} bytes)")
                    
                    results[topic] = topic_results
                    logger.info(f"Successfully processed topic: {topic}")
                else:
                    logger.warning(f"Module not found for topic: {topic}")
                    results[topic] = [f"Module {topic} not found or not executable"]
                
                # Clean up temp files
                for f in os.listdir('.'):
                    if f != 'image.jpg':
                        try:
                            os.remove(f)
                            logger.debug(f"Removed temp file: {f}")
                        except Exception as e:
                            logger.warning(f"Failed to remove temp file {f}: {e}")
                
                # Return to original directory
                os.chdir(original_cwd)
                logger.debug(f"Returned to original directory: {original_cwd}")
                
            except Exception as e:
                logger.error(f"Error processing topic {topic}: {str(e)}")
                results[topic] = [f"Error processing {topic}: {str(e)}"]
                try:
                    os.chdir(original_cwd)
                except:
                    pass
        
        # Clean up temp directory
        import shutil
        try:
            shutil.rmtree(temp_dir)
            logger.info(f"Cleaned up temp directory: {temp_dir}")
        except FileNotFoundError:
            logger.debug("Temp directory already cleaned up")
        except Exception as e:
            logger.warning(f"Failed to clean up temp directory: {e}")
        
        logger.info(f"Image processing completed. Results: {len(results)} topics processed")
        return results
    
    def analyze_with_gemini(self, image_path, ivp_results):
        """Use Gemini AI to analyze the processed image results with key fallback"""
        logger.info(f"Analyzing with Gemini: {os.path.basename(image_path)}")
        
        # Prepare prompt for Gemini
        prompt = f"""
        As a professional photographer analyzer, please analyze the following image processing results and determine if this image is GOOD or BAD for photography.
        
        Image: {os.path.basename(image_path)}
        
        Processing Results:
        {json.dumps(ivp_results, indent=2)}
        
        Please provide:
        1. Classification: GOOD or BAD
        2. Brief reasoning (one line explaining why)
        
        Format your response as:
        Classification: [GOOD/BAD]
        Reasoning: [Your one-line explanation]
        """
        
        logger.debug(f"Gemini prompt prepared, length: {len(prompt)} chars")
        
        # Try with current key, fallback to next keys if needed
        max_retries = len(self.api_keys)
        for attempt in range(max_retries):
            try:
                response = self.model.generate_content(prompt)
                response_text = response.text
                logger.info(f"Gemini response received: {len(response_text)} chars")
                
                # Parse response
                lines = response_text.strip().split('\n')
                classification = "BAD"  # Default
                reasoning = "Unable to analyze"
                
                for line in lines:
                    if line.startswith("Classification:"):
                        classification = line.split(":", 1)[1].strip().upper()
                    elif line.startswith("Reasoning:"):
                        reasoning = line.split(":", 1)[1].strip()
                
                logger.info(f"Gemini analysis result: {classification} - {reasoning}")
                return {
                    "classification": classification,
                    "reasoning": reasoning
                }
                
            except Exception as e:
                logger.error(f"Gemini analysis failed with key {self.current_key_index + 1}: {str(e)}")
                
                # Try next key if available
                if attempt < max_retries - 1:
                    if self.try_next_gemini_key():
                        logger.info(f"Retrying with next API key...")
                        continue
                    else:
                        break
                else:
                    logger.error("All Gemini API keys exhausted")
                    return {
                        "classification": "BAD",
                        "reasoning": f"Analysis error: All API keys failed"
                    }
        
        return {
            "classification": "BAD",
            "reasoning": "Analysis error: Unable to connect to Gemini"
        }
    
    def process_folder(self, media_type, topics, folder_path):
        """Process all images/videos in a folder"""
        logger.info(f"Starting folder processing: {media_type} from {folder_path}")
        logger.info(f"Selected topics: {topics}")
        
        if not os.path.exists(folder_path):
            logger.error(f"Folder path does not exist: {folder_path}")
            return {"error": "Folder path does not exist"}
        
        # Get all media files
        if media_type == "image":
            extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif']
        else:
            extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv']
        
        logger.info(f"Looking for files with extensions: {extensions}")
        media_files = []
        for file in os.listdir(folder_path):
            if any(file.lower().endswith(ext) for ext in extensions):
                media_files.append(os.path.join(folder_path, file))
        
        logger.info(f"Found {len(media_files)} {media_type} files")
        if not media_files:
            logger.error(f"No {media_type} files found in folder")
            return {"error": f"No {media_type} files found in folder"}
        
        # Initialize analysis data
        analysis_data = {
            "selected": media_type,
            "topics_selected": topics,
            "folder_path": folder_path,
            "output": {
                "good_images": [],
                "bad_images": []
            },
            "summary": ""
        }
        
        good_count = 0
        bad_count = 0
        
        # Process each media file
        for i, media_file in enumerate(media_files):
            logger.info(f"Processing {i+1}/{len(media_files)}: {os.path.basename(media_file)}")
            # Don't print progress to stdout as it interferes with JSON output
            
            # Process with IVP modules
            logger.info(f"Starting IVP processing for: {os.path.basename(media_file)}")
            ivp_results = self.process_image_with_ivp(media_file, topics)
            
            # Analyze with Gemini
            logger.info(f"Starting Gemini analysis for: {os.path.basename(media_file)}")
            gemini_analysis = self.analyze_with_gemini(media_file, ivp_results)
            
            # Store results
            image_data = {
                "image_number": i + 1,
                "image_name": os.path.basename(media_file),
                "image_path": media_file,
                "reason": gemini_analysis["reasoning"]
            }
            
            if gemini_analysis["classification"] == "GOOD":
                analysis_data["output"]["good_images"].append(image_data)
                good_count += 1
                logger.info(f"Image classified as GOOD: {os.path.basename(media_file)}")
            else:
                analysis_data["output"]["bad_images"].append(image_data)
                bad_count += 1
                logger.info(f"Image classified as BAD: {os.path.basename(media_file)}")
        
        # Generate summary
        quality_score = (good_count/len(media_files)*100) if len(media_files) > 0 else 0
        summary = f"""
        Analysis Summary for {media_type.title()}s in {os.path.basename(folder_path)}:
        
        Total {media_type}s processed: {len(media_files)}
        Good {media_type}s: {good_count}
        Bad {media_type}s: {bad_count}
        
        Quality Score: {quality_score:.1f}%
        
        The analysis was performed using {len(topics)} IVP topics: {', '.join(topics)}.
        """
        
        analysis_data["summary"] = summary.strip()
        logger.info(f"Analysis completed: {good_count} good, {bad_count} bad, {quality_score:.1f}% quality")
        
        # Save to analyser data
        logger.info(f"Before save: analyser_data contains {len(self.analyser_data)} entries")
        self.analyser_data.append(analysis_data)
        logger.info(f"After append: analyser_data contains {len(self.analyser_data)} entries")
        
        # Validate before saving
        if not isinstance(self.analyser_data, list):
            logger.error(f"analyser_data is not a list before saving! Type: {type(self.analyser_data)}")
            logger.error(f"Resetting analyser_data. Current value: {self.analyser_data}")
            self.analyser_data = [analysis_data]  # At least save current analysis
        
        if len(self.analyser_data) == 0:
            logger.warning("analyser_data is empty before saving! This should not happen.")
            self.analyser_data = [analysis_data]  # At least save current analysis
        
        self.save_analyser_data()
        logger.info(f"Analysis data saved successfully. Total entries in file: {len(self.analyser_data)}")
        
        return analysis_data
    
    def get_analysis_summary(self):
        """Get summary of all analyses"""
        if not self.analyser_data:
            return "No analyses performed yet."
        
        summary = f"Total Analyses: {len(self.analyser_data)}\n\n"
        
        for i, analysis in enumerate(self.analyser_data):
            good_count = len(analysis["output"]["good_images"])
            bad_count = len(analysis["output"]["bad_images"])
            total = good_count + bad_count
            
            summary += f"Analysis {i+1}:\n"
            summary += f"  Type: {analysis['selected']}\n"
            summary += f"  Folder: {os.path.basename(analysis['folder_path'])}\n"
            summary += f"  Results: {good_count} good, {bad_count} bad\n"
            summary += f"  Quality: {(good_count/total*100):.1f}%\n\n"
        
        return summary

def main():
    """Main function to handle command line arguments"""
    if len(sys.argv) < 4:
        # Output error as JSON
        error_result = {"error": "Usage: python main.py <media_type> <topics_json> <folder_path>"}
        print(json.dumps(error_result))
        return
    
    media_type = sys.argv[1]
    topics = json.loads(sys.argv[2])
    folder_path = sys.argv[3]
    
    try:
        analyzer = IVPAnalyzer()
        result = analyzer.process_folder(media_type, topics, folder_path)
        
        # Output result as JSON only
        print(json.dumps(result, indent=2))
    except Exception as e:
        # Output error as JSON
        error_result = {"error": f"Analysis failed: {str(e)}"}
        print(json.dumps(error_result))

if __name__ == "__main__":
    main()
