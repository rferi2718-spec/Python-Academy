from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.storage.jsonstore import JsonStore

Window.clearcolor = (0.04, 0.06, 0.08, 1)

store = JsonStore("progress.json")

lessons = [
    ("Lesson 1", "Introduction to Python",
     "Python is a programming language."),

    ("Lesson 2", "Print",
     "print('Hello World')"),

    ("Lesson 3", "Variables",
     "name = 'Alex'\nage = 15"),

    ("Lesson 4", "Data Types",
     "int, float, str, bool"),

    ("Lesson 5", "Input",
     "name = input('Your name: ')"),

    ("Lesson 6", "Operators",
     "+, -, *, /"),

    ("Lesson 7", "Conditions",
     "if age >= 18:\n    print('Adult')"),

    ("Lesson 8", "Else and Elif",
     "if / elif / else"),

    ("Lesson 9", "Loops",
     "for i in range(5):\n    print(i)"),

    ("Lesson 10", "While",
     "while x < 5:\n    x += 1"),

    ("Lesson 11", "Lists",
     "numbers = [1, 2, 3]"),

    ("Lesson 12", "Tuples",
     "data = (1, 2, 3)"),

    ("Lesson 13", "Dictionaries",
     "person = {'name': 'Alex'}"),

    ("Lesson 14", "Functions",
     "def hello():\n    print('Hello')"),

    ("Lesson 15", "Final Project",
     "Create your own Python project.")
]


class Academy(App):

    def build(self):
        self.root = BoxLayout(
            orientation="vertical",
            padding=15,
            spacing=10
        )

        title = Label(
            text="[b]PYTHON ACADEMY[/b]",
            markup=True,
            font_size=28,
            size_hint_y=None,
            height=70
        )

        self.root.add_widget(title)

        self.content = BoxLayout(
            orientation="vertical",
            spacing=10
        )

        scroll = ScrollView()
        scroll.add_widget(self.content)

        self.root.add_widget(scroll)

        self.show_home()

        return self.root

    def clear_content(self):
        self.content.clear_widgets()

    def show_home(self):
        self.clear_content()

        self.content.add_widget(Label(
            text="Learn Python Step by Step",
            font_size=20,
            size_hint_y=None,
            height=60
        ))

        for index, lesson in enumerate(lessons):
            button = Button(
                text=f"{lesson[0]} - {lesson[1]}",
                size_hint_y=None,
                height=55
            )

            button.bind(
                on_press=lambda btn, i=index: self.show_lesson(i)
            )

            self.content.add_widget(button)

        self.content.add_widget(Button(
            text="Take Final Quiz",
            size_hint_y=None,
            height=60,
            on_press=lambda btn: self.show_quiz()
        ))

    def show_lesson(self, index):
        self.clear_content()

        lesson = lessons[index]

        self.content.add_widget(Label(
            text=lesson[1],
            font_size=24,
            size_hint_y=None,
            height=70
        ))

        self.content.add_widget(Label(
            text=lesson[2],
            font_size=20,
            size_hint_y=None,
            height=150
        ))

        self.content.add_widget(Button(
            text="Mark as Completed",
            size_hint_y=None,
            height=60,
            on_press=lambda btn: self.complete_lesson(index)
        ))

        self.content.add_widget(Button(
            text="Back to Lessons",
            size_hint_y=None,
            height=60,
            on_press=lambda btn: self.show_home()
        ))

    def complete_lesson(self, index):
        completed = []

        if store.exists("progress"):
            completed = store.get("progress")["completed"]

        if index not in completed:
            completed.append(index)

        store.put("progress", completed=completed)

        self.show_home()

    def show_quiz(self):
        self.clear_content()

        questions = [
            ("Which command displays text?", ["print", "input", "if"], 0),
            ("Which symbol assigns a value?", ["==", "=", "!="], 1),
            ("Which keyword starts a function?", ["loop", "def", "for"], 1)
        ]

        self.quiz_index = 0
        self.quiz_score = 0
        self.questions = questions

        self.next_question()

    def next_question(self):
        self.clear_content()

        if self.quiz_index >= len(self.questions):
            self.content.add_widget(Label(
                text=f"Quiz Finished!\nScore: {self.quiz_score}/3",
                font_size=25
            ))

            self.content.add_widget(Button(
                text="Back to Home",
                on_press=lambda btn: self.show_home()
            ))

            return

        question, options, answer = self.questions[self.quiz_index]

        self.content.add_widget(Label(
            text=question,
            font_size=22
        ))

        for i, option in enumerate(options):
            button = Button(
                text=option,
                size_hint_y=None,
                height=60
            )

            button.bind(
                on_press=lambda btn, choice=i: self.check_answer(choice)
            )

            self.content.add_widget(button)

    def check_answer(self, choice):
        if choice == self.questions[self.quiz_index][2]:
            self.quiz_score += 1

        self.quiz_index += 1
        self.next_question()


if __name__ == "__main__":
    Academy().run()
