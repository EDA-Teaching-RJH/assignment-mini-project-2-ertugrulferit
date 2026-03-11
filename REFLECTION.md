# Developer Journal: Mechanical Part Inventory & Sustainability Tracker

## Project Overview
For this assignment, I wanted to build something that actually felt useful for a mechanical engineer. I decided to create a Sustainability Tracker that doesn't just list parts but calculates their real-world physical mass and carbon impact. I’ve connected the features of this app to the key concepts we covered in Lectures 7 through 9.

## Connecting to the Course Materials

### Lecture 7: Objects and Classes
Early on, I realized that just using basic lists or dictionaries wouldn't work for a complex inventory. Following Lecture 7, I moved everything into a MechanicalPart class. This made my life much easier because it allowed me to keep the physics logic (like the density or mass math) inside the object itself. It made the code much cleaner and stopped me from having to rewrite the same math over and over in different parts of the app.

### Lecture 8: Inheritance (The Standard vs. Custom Problem)
One of the biggest challenges I faced was how to handle different categories of parts. I was inspired by the SDS example from class where we saw Undergraduate inheriting from Student, so I applied that same logic here. I created StandardPart and CustomComponent as subclasses.

* I gave the Standard parts a shelf location because they are off-the-shelf items.
* I gave the Custom parts a "Lead Time" attribute because they have to be manufactured from scratch.

This evidenced my understanding of Lecture 8 inheritance—it let me reuse the "Parent" code while giving the "Child" classes their own unique data.

### Lecture 9: Defensive Programming and Testing
Honestly, the testing phase from Lecture 9 was the most annoying but also the most helpful part of the process. I wrote a test_app.py script to try and "break" my own work. I used assertRaises to make sure that if I accidentally entered a part without a name, the system would stop me. This "Defensive Programming" is something I really focused on to make the registry feel professional and maintainable.

## My Working Process and Obstacles

### The "Cowsay" Environment Issue
I initially wanted to use the cowsay library like the lecturer did in the demo, but I kept getting a ModuleNotFoundError in my Codespace. Instead, I decided to put my own ASCII Crane. I’m actually glad this happened because it forced me to keep the project standard library only, so it will run on any computer without needing extra setup.

### The Unit Debate (mm3 vs m3)
I spent a lot of time debating whether to use mm3 or m3. While most CAD software uses millimeters, I chose to stay with m3 for the final version. My reasoning was that the CO2 and Density formulas we use in engineering are almost always based on meters. It kept the math simple and reduced the chance of huge decimal errors in the final sustainability report.

## Final Thoughts
Looking back at my Git history, I can see how the project grew from a simple script to a full-fledged system upon my fear of the code being too short. It is still a little bit shorter than your example, but I think that I have demonstrated everything clearly, and efficiently. Using the if __name__ == __main__: guard was a final touch I added to make sure my tests could run without the main menu popping up every time. It’s been a steep learning curve, but I’m proud that the final code is modular, tested, and actually works!