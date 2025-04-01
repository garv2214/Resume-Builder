import re
import argparse

class Resume:
    def __init__(self, automated=False):
        self.personal_info = {}
        self.education = []
        self.work_experience = []
        self.skills = []

        self.email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        self.phone_pattern = r'^\+?1?\d{9,15}$'
        self.name_pattern = r'^[A-Za-z\s\'-]{2,50}$'
        self.date_pattern = r'^(0[1-9]|1[0-2])/\d{4}$'
        self.year_pattern = r'^\d{4}$'
        self.gpa_pattern = r'^[0-4](\.[0-9]{1,2})?$'

        self.automated = automated
        self.sample_data = {
            'personal_info': {
                'name': 'John Doe',
                'email': 'john.doe@email.com',
                'phone': '+911234567890',
                'address': '123 Main St, City, State 12345',
                'linkedin': 'https://linkedin.com/in/johndoe',
                'website': 'https://johndoe.com'
            },
            'education': [
                {
                    'degree': 'Bachelor of Science in Computer Science',
                    'institution': 'University of Technology',
                    'year': '2023',
                    'gpa': '3.8',
                    'honors': 'Magna Cum Laude'
                }
            ],
            'work_experience': [
                {
                    'company': 'Tech Corp',
                    'position': 'Software Engineer',
                    'start_date': '01/2022',
                    'end_date': 'Present',
                    'location': 'San Francisco, CA',
                    'description': [
                        'Developed full-stack applications using Python and React',
                        'Improved system performance by 40%',
                        'Led a team of 3 junior developers'
                    ]
                }
            ],
            'skills': ['Python', 'JavaScript', 'React', 'SQL', 'Git', 'AWS']
        }

        # Add specific error messages
        self.error_messages = {
            'name': {
                'pattern': "Name must be 2-50 characters long and contain only letters, spaces, hyphens, and apostrophes",
                'required': "Name is required"
            },
            'email': {
                'pattern': "Invalid email format. Please use format: example@domain.com",
                'required': "Email address is required"
            },
            'phone': {
                'pattern': "Phone number must contain 9-15 digits, optionally starting with '+'",
                'required': "Phone number is required"
            },
            'degree': {
                'pattern': "Degree must be 2-100 characters long and contain only letters, spaces, and parentheses",
                'required': "Degree information is required"
            },
            'institution': {
                'pattern': "Institution name must be 2-100 characters and contain only letters, spaces, hyphens, and ampersands",
                'required': "Institution name is required"
            },
            'year': {
                'pattern': "Year must be in YYYY format",
                'required': "Graduation year is required"
            },
            'gpa': {
                'pattern': "GPA must be between 0.0 and 4.0",
                'required': False
            },
            'company': {
                'pattern': "Company name must be 2-100 characters and contain only letters, numbers, spaces, and basic punctuation",
                'required': "Company name is required"
            },
            'position': {
                'pattern': "Position must be 2-100 characters and contain only letters, numbers, spaces, and basic punctuation",
                'required': "Position title is required"
            },
            'date': {
                'pattern': "Date must be in MM/YYYY format (e.g., 09/2023) or 'Present'",
                'required': "Date is required"
            }
        }

    def validate_input(self, field_name, prompt, required=True, pattern=None):
        """
        Enhanced input validation with specific error handling
        """
        if self.automated:
            return self.get_sample_data(prompt)
        
        while True:
            try:
                value = input(prompt).strip()
                
                # Check if required
                if not value and required:
                    if field_name in self.error_messages:
                        raise ValueError(self.error_messages[field_name]['required'])
                    raise ValueError("This field is required")
                
                # Skip pattern validation if field is optional and empty
                if not value and not required:
                    return value
                
                # Validate pattern if provided
                if pattern and not re.match(pattern, value):
                    if field_name in self.error_messages:
                        raise ValueError(self.error_messages[field_name]['pattern'])
                    raise ValueError("Invalid format")
                
                return value
                
            except ValueError as e:
                print(f"Error: {str(e)}")
            except Exception as e:
                print(f"An unexpected error occurred: {str(e)}")

    def get_sample_data(self, prompt):
        # Map prompts to sample data
        prompt_lower = prompt.lower()
        if 'name' in prompt_lower:
            return self.sample_data['personal_info']['name']
        elif 'email' in prompt_lower:
            return self.sample_data['personal_info']['email']
        # Add more mappings as needed
        return 'Sample Data'

    def add_personal_info(self):
        if self.automated:
            self.personal_info = self.sample_data['personal_info']
            return
            
        print("\n=== Personal Information ===")
        try:
            self.personal_info['name'] = self.validate_input(
                'name',
                "Full Name: ",
                pattern=self.name_pattern
            )
            self.personal_info['email'] = self.validate_input(
                'email',
                "Email: ",
                pattern=self.email_pattern
            )
            self.personal_info['phone'] = self.validate_input(
                'phone',
                "Phone: ",
                pattern=self.phone_pattern
            )
            self.personal_info['address'] = self.validate_input("Address: ")
            self.personal_info['linkedin'] = self.validate_input(
                "LinkedIn URL (optional): ",
                required=False,
                pattern=r'^https?://([a-zA-Z0-9-]+\.)?linkedin\.com/.*$',
                error_msg="Please enter a valid LinkedIn URL"
            )
            self.personal_info['website'] = self.validate_input(
                "Personal Website (optional): ",
                required=False,
                pattern=r'^https?://[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+.*$',
                error_msg="Please enter a valid URL"
            )
        except Exception as e:
            print(f"Error in personal information: {str(e)}")
            raise

    def add_education(self):
        if self.automated:
            for edu in self.sample_data['education']:
                entry = f"{edu['degree']} - {edu['institution']} ({edu['year']})"
                if edu['gpa']:
                    entry += f" | GPA: {edu['gpa']}"
                self.education.append(entry)
            return
            
        print("\n=== Education Details ===")
        try:
            education_entry = {
                'degree': self.validate_input(
                    'degree',
                    "Degree (e.g., Bachelor of Science): ",
                    pattern=r'^[A-Za-z\s\(\)]{2,100}$'
                ),
                'institution': self.validate_input(
                    'institution',
                    "Institution: ",
                    pattern=r'^[A-Za-z\s\'\-\&]{2,100}$'
                ),
                'year': self.validate_input(
                    "Year of Graduation: ",
                    pattern=self.year_pattern,
                    error_msg="Please enter a valid year (YYYY)"
                ),
                'gpa': self.validate_input(
                    "GPA (optional): ",
                    required=False,
                    pattern=self.gpa_pattern,
                    error_msg="Please enter a valid GPA between 0.0 and 4.0"
                ),
                'honors': self.validate_input(
                    "Honors/Awards (optional): ",
                    required=False
                )
            }

            entry = f"{education_entry['degree']} - {education_entry['institution']} ({education_entry['year']})"
            if education_entry['gpa']:
                entry += f" | GPA: {education_entry['gpa']}"
            self.education.append(entry)
        except Exception as e:
            print(f"Error in education entry: {str(e)}")
            raise

    def add_work_experience(self):
        if self.automated:
            for exp in self.sample_data['work_experience']:
                entry = (f"{exp['position']} at {exp['company']}\n"
                        f"{exp['start_date']} - {exp['end_date']}")
                if exp['description']:
                    entry += "\n" + "\n".join(f"• {item}" for item in exp['description'])
                self.work_experience.append(entry)
            return
        print("\n=== Work Experience ===")
        experience = {
            'company': self.validate_input(
                "Company: ",
                pattern=r'^[A-Za-z0-9\s\'\-\&\.]{2,100}$',
                error_msg="Please enter a valid company name"
            ),
            'position': self.validate_input(
                "Position: ",
                pattern=r'^[A-Za-z0-9\s\'\-\&]{2,100}$',
                error_msg="Please enter a valid position title"
            ),
            'start_date': self.validate_input(
                "Start Date (MM/YYYY): ",
                pattern=self.date_pattern,
                error_msg="Please use MM/YYYY format (e.g., 09/2023)"
            ),
            'end_date': self.validate_input(
                "End Date (MM/YYYY or 'Present'): ",
                pattern=r'^(0[1-9]|1[0-2])/\d{4}|Present$',
                error_msg="Please use MM/YYYY format or 'Present'"
            ),
            'location': self.validate_input(
                "Location (City, State/Country): ",
                required=False,
                pattern=r'^[A-Za-z\s\'\-\,]{2,100}$',
                error_msg="Please enter a valid location"
            ),
            'description': []
        }
        
        print("Enter job responsibilities (one per line, press Enter twice to finish):")
        while True:
            responsibility = input("- ").strip()
            if not responsibility:
                break
            experience['description'].append(responsibility)


        entry = (f"{experience['position']} at {experience['company']}\n"
                f"{experience['start_date']} - {experience['end_date']}")
        if experience['description']:
            entry += "\n" + "\n".join(f"• {item}" for item in experience['description'])
        self.work_experience.append(entry)

    def add_skills(self):
        if self.automated:
            self.skills = self.sample_data['skills']
            return
        print("\n=== Skills ===")
        print("Enter skills (comma-separated, minimum 1 skill):")
        while True:
            skills_input = self.validate_input("Skills: ")
            skills_list = [skill.strip() for skill in skills_input.split(',') if skill.strip()]
            if not skills_list:
                print("Please enter at least one skill.")
                continue
            self.skills = skills_list
            break

    def generate_resume(self):
        resume = f"""
{self.personal_info['name']}
{self.personal_info['email']} | {self.personal_info['phone']}
{self.personal_info['address']}
{self.personal_info['college']}

Education:
{'-' * 50}
"""
        for edu in self.education:
            resume += f"{edu}\n"

        resume += f"""
Work Experience:
{'-' * 50}
"""
        for exp in self.work_experience:
            resume += f"{exp}\n\n"

        resume += f"""
Skills:
{'-' * 50}
{', '.join(self.skills)}
"""
        return resume

def main():
    parser = argparse.ArgumentParser(description='Resume Generator')
    parser.add_argument('--automated', action='store_true', help='Use sample data to generate resume')
    args = parser.parse_args()

    try:
        resume = Resume(automated=args.automated)
        resume.add_personal_info()
        
        if not args.automated:
            while True:
                try:
                    resume.add_education()
                    if input("Add another education entry? (y/n): ").lower() != 'y':
                        break
                except Exception as e:
                    print(f"Error adding education entry: {str(e)}")
                    if input("Would you like to try again? (y/n): ").lower() != 'y':
                        break

            while True:
                try:
                    resume.add_work_experience()
                    if input("Add another work experience entry? (y/n): ").lower() != 'y':
                        break
                except Exception as e:
                    print(f"Error adding work experience: {str(e)}")
                    if input("Would you like to try again? (y/n): ").lower() != 'y':
                        break
        else:
            resume.add_education()
            resume.add_work_experience()

        resume.add_skills()

        print("\nGenerating Resume...\n")
        print(resume.generate_resume())
        
    except KeyboardInterrupt:
        print("\nResume generation cancelled by user.")
    except Exception as e:
        print(f"\nAn error occurred while generating the resume: {str(e)}")

if __name__ == "__main__":
    main()