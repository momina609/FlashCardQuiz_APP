### 📦 IMPORTS
import tkinter as tk  #GUI library to create graphical user interface
from tkinter import messagebox,simpledialog
import json # data handling library to store and load data in json format
import random # utility library for random search
import spacy #  AI / NLP Library
import os    # system utility library

#🧠 this loads  AI spaCy's English language model used to understand and compare answers with NLP.
nlp=spacy.load("en_core_web_sm")

# 💾 flashcard storage functions
FLASHCARD_FILE="flashcards.json"

#Load saved flashcards
def load_flashcards():
    if os.path.exists(FLASHCARD_FILE):
        with open(FLASHCARD_FILE,"r") as f:
            return json.load(f)
    return[]
    
#Save flashcards
def save_flashcards(cards):
    with open(FLASHCARD_FILE,"w") as f:
        json.dump(cards,f,indent=2)
    
#🤖 AI LOGIC — NLP-based Answer Comparison
# AI algorithm! 💡.It converts both answers into spaCy documents and compares their semantic similarity.
#Returns True if similarity > 75%
def is_similar(ans1,ans2):
    doc1=nlp(ans1.lower())
    doc2=nlp(ans2.lower())
    return doc1.similarity(doc2)>0.75

#🧱 MAIN APP CLASS — GUI + Logic
class FlashcardApp:
   def __init__(self, root):
        self.root = root
        self.root.title("🌟 Smart Flashcard Quiz by Momina")
        self.root.geometry("550x450")
        self.root.configure(bg="#f9f5ff")

        self.flashcards = load_flashcards()
        self.score = 0
        self.total = 0
        self.current_card = None

        self.setup_ui()

   def setup_ui(self):
        title = tk.Label(self.root, text="🌸 AI-Powered Flashcard Trainer 🌸",
                         font=("Comic Sans MS", 18, "bold"), fg="#6c3483", bg="#f9f5ff")
        title.pack(pady=10)

        self.question_label = tk.Label(self.root, text="✨ Press 'Start Quiz' to begin your learning journey!",
                                       font=("Verdana", 12), fg="#5a5a5a", bg="#f9f5ff", wraplength=480)
        self.question_label.pack(pady=10)

        btn_frame = tk.Frame(self.root, bg="#f9f5ff")
        btn_frame.pack(pady=15)

        btn_style = {"font": ("Helvetica", 11, "bold"), "bg": "#dcd6f7", "fg": "#3e206d", "width": 20, "height": 2}

        tk.Button(btn_frame, text="➕ Add New Flashcard", command=self.add_flashcard, **btn_style).grid(row=0, column=0, padx=10, pady=5)
        tk.Button(btn_frame, text="🚀 Start Quiz", command=self.start_quiz, **btn_style).grid(row=0, column=1, padx=10, pady=5)
        tk.Button(btn_frame, text="📊 Show My Score", command=self.show_score, **btn_style).grid(row=1, column=0, padx=10, pady=5)
        tk.Button(btn_frame, text="➡️ Next Flashcard", command=self.ask_question, **btn_style).grid(row=1, column=1, padx=10, pady=5)

        self.status_label = tk.Label(self.root, text="💡 Progress: 0 / 0", font=("Verdana", 10), bg="#f9f5ff", fg="#6c3483")
        self.status_label.pack(pady=10)


# 📝 ADD FLASHCARD
   def add_flashcard(self):
        question = simpledialog.askstring("Add Flashcard", "Enter the question:")
        answer = simpledialog.askstring("Add Flashcard", "Enter the answer:")
        if question and answer:
            self.flashcards.append({"question": question, "answer": answer, "score": 0})
            save_flashcards(self.flashcards)
            messagebox.showinfo("Success", "✅ Flashcard added!")
# start quiz
   def start_quiz(self):
        if not self.flashcards:
            messagebox.showwarning("No Cards", "⚠️ Please add flashcards first.")
            return
        self.score = 0
        self.total = 0
        self.ask_question()

# ❓ ASK QUESTION
   def ask_question(self):
        if not self.flashcards:
            return
        self.current_card = random.choice(sorted(self.flashcards, key=lambda x: x['score']))
        q = self.current_card['question']
        self.question_label.config(text=f"❓ Q: {q}")
        user_ans = simpledialog.askstring("Quiz", f"Q: {q}")
        if user_ans:
            correct = is_similar(user_ans, self.current_card['answer'])
            self.total += 1
            if correct:
                self.score += 1
                self.current_card['score'] += 1
                messagebox.showinfo("Correct!", "✅ Well done!")
            else:
                self.current_card['score'] += 2
                messagebox.showinfo("Incorrect", f"❌ Correct answer was:\n{self.current_card['answer']}")
            save_flashcards(self.flashcards)
            self.status_label.config(text=f"Score: {self.score} / {self.total}")

# 🧮 SHOW SCORE
   def show_score(self):
       messagebox.showinfo("Your Score", f"🎯 Score: {self.score} out of {self.total}")

#▶️ RUN THE APP
if __name__ == "__main__":
    root = tk.Tk()
    app = FlashcardApp(root)
    root.mainloop()




