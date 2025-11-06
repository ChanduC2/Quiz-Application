import json
import random
from typing import List, Dict
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class Question:
    question: str
    options: List[str]
    correct_answer: int
    category: str
    difficulty: str

@dataclass
class QuizResult:
    score: int
    total: int
    percentage: float
    time_taken: str
    date: str

class QuizApp:
    def __init__(self):
        self.questions = self.load_default_questions()
        self.score = 0
        self.current_question = 0
        
    def load_default_questions(self) -> List[Question]:
        """Load default quiz questions"""
        return [
            Question(
                "What is the capital of France?",
                ["London", "Berlin", "Paris", "Madrid"],
                2,
                "Geography",
                "Easy"
            ),
            Question(
                "Which planet is known as the Red Planet?",
                ["Venus", "Mars", "Jupiter", "Saturn"],
                1,
                "Science",
                "Easy"
            ),
            Question(
                "Who wrote 'Romeo and Juliet'?",
                ["Charles Dickens", "William Shakespeare", "Jane Austen", "Mark Twain"],
                1,
                "Literature",
                "Medium"
            ),
            Question(
                "What is the largest ocean on Earth?",
                ["Atlantic Ocean", "Indian Ocean", "Arctic Ocean", "Pacific Ocean"],
                3,
                "Geography",
                "Easy"
            ),
            Question(
                "In what year did World War II end?",
                ["1943", "1944", "1945", "1946"],
                2,
                "History",
                "Medium"
            ),
            Question(
                "What is the speed of light?",
                ["299,792 km/s", "150,000 km/s", "500,000 km/s", "1,000,000 km/s"],
                0,
                "Science",
                "Hard"
            ),
            Question(
                "Which programming language is known for its use in web development?",
                ["Python", "JavaScript", "C++", "Java"],
                1,
                "Technology",
                "Medium"
            ),
            Question(
                "What is the smallest prime number?",
                ["0", "1", "2", "3"],
                2,
                "Mathematics",
                "Easy"
            ),
            Question(
                "Who painted the Mona Lisa?",
                ["Vincent van Gogh", "Pablo Picasso", "Leonardo da Vinci", "Michelangelo"],
                2,
                "Art",
                "Medium"
            ),
            Question(
                "What is the chemical symbol for gold?",
                ["Go", "Gd", "Au", "Ag"],
                2,
                "Science",
                "Medium"
            )
        ]
    
    def display_welcome(self):
        """Display welcome message"""
        print("\n" + "="*50)
        print("🎯 WELCOME TO THE QUIZ APPLICATION 🎯".center(50))
        print("="*50)
        print("\nTest your knowledge across various categories!")
        print(f"Total Questions: {len(self.questions)}\n")
    
    def display_question(self, question: Question, question_num: int):
        """Display a single question with options"""
        print("\n" + "-"*50)
        print(f"Question {question_num}/{len(self.questions)}")
        print(f"Category: {question.category} | Difficulty: {question.difficulty}")
        print("-"*50)
        print(f"\n{question.question}\n")
        
        for idx, option in enumerate(question.options, 1):
            print(f"{idx}. {option}")
        print()
    
    def get_user_answer(self, num_options: int) -> int:
        """Get and validate user input"""
        while True:
            try:
                answer = input("Your answer (enter option number): ").strip()
                answer = int(answer)
                if 1 <= answer <= num_options:
                    return answer - 1  # Convert to 0-indexed
                else:
                    print(f"Please enter a number between 1 and {num_options}")
            except ValueError:
                print("Invalid input! Please enter a number.")
            except KeyboardInterrupt:
                print("\n\nQuiz interrupted by user.")
                exit(0)
    
    def check_answer(self, user_answer: int, correct_answer: int) -> bool:
        """Check if the answer is correct"""
        if user_answer == correct_answer:
            print("\n✅ Correct! Well done!")
            return True
        else:
            print(f"\n❌ Wrong! The correct answer was option {correct_answer + 1}")
            return False
    
    def display_results(self, result: QuizResult):
        """Display final quiz results"""
        print("\n" + "="*50)
        print("📊 QUIZ RESULTS 📊".center(50))
        print("="*50)
        print(f"\nScore: {result.score}/{result.total}")
        print(f"Percentage: {result.percentage:.1f}%")
        print(f"Time: {result.time_taken}")
        print(f"Date: {result.date}")
        
        # Performance message
        if result.percentage >= 90:
            print("\n🌟 Outstanding! You're a quiz master!")
        elif result.percentage >= 70:
            print("\n👍 Great job! Keep it up!")
        elif result.percentage >= 50:
            print("\n📚 Good effort! Room for improvement.")
        else:
            print("\n💪 Keep practicing! You'll do better next time!")
        
        print("="*50 + "\n")
    
    def run_quiz(self, shuffle: bool = True):
        """Run the complete quiz"""
        self.display_welcome()
        
        # Option to shuffle questions
        questions = self.questions.copy()
        if shuffle:
            random.shuffle(questions)
        
        start_time = datetime.now()
        self.score = 0
        
        # Ask each question
        for idx, question in enumerate(questions, 1):
            self.display_question(question, idx)
            user_answer = self.get_user_answer(len(question.options))
            
            if self.check_answer(user_answer, question.correct_answer):
                self.score += 1
            
            input("\nPress Enter to continue...")
        
        # Calculate results
        end_time = datetime.now()
        time_taken = str(end_time - start_time).split('.')[0]
        
        result = QuizResult(
            score=self.score,
            total=len(questions),
            percentage=(self.score / len(questions)) * 100,
            time_taken=time_taken,
            date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        
        self.display_results(result)
        
        return result
    
    def practice_by_category(self):
        """Practice questions from a specific category"""
        categories = list(set(q.category for q in self.questions))
        
        print("\n📚 Available Categories:")
        for idx, cat in enumerate(categories, 1):
            count = sum(1 for q in self.questions if q.category == cat)
            print(f"{idx}. {cat} ({count} questions)")
        
        try:
            choice = int(input("\nSelect category (enter number): "))
            if 1 <= choice <= len(categories):
                selected_category = categories[choice - 1]
                filtered_questions = [q for q in self.questions if q.category == selected_category]
                
                # Temporarily replace questions
                original_questions = self.questions
                self.questions = filtered_questions
                self.run_quiz(shuffle=True)
                self.questions = original_questions
            else:
                print("Invalid choice!")
        except ValueError:
            print("Invalid input!")

def main():
    """Main function to run the quiz application"""
    quiz = QuizApp()
    
    while True:
        print("\n" + "="*50)
        print("MAIN MENU".center(50))
        print("="*50)
        print("\n1. Start Full Quiz")
        print("2. Practice by Category")
        print("3. Exit")
        
        try:
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == "1":
                quiz.run_quiz(shuffle=True)
            elif choice == "2":
                quiz.practice_by_category()
            elif choice == "3":
                print("\n👋 Thanks for playing! Goodbye!\n")
                break
            else:
                print("\n⚠️  Invalid choice! Please enter 1, 2, or 3.")
        except KeyboardInterrupt:
            print("\n\n👋 Thanks for playing! Goodbye!\n")
            break

if __name__ == "__main__":
    main()