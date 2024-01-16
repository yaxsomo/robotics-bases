![Creative Commons License](https://i.creativecommons.org/l/by/4.0/88x31.png)

Robotics initiation class materials by Remi Fabre and Steve N'Guyen is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).

# Robotics initiation
From the a DC motor to a walking Hexapod, an introduction to robotics.
![Hexapod](hexapod.jpg)


## Notes

Some files are encrypted because they contain the solutions to some of the tasks. The passwords will be shared as we move forward in class.
Of course, I'll forget the passwords then. Note to myself: look for "Passwords for robotics initiation class" in my mail.

To decrypt:
```
qpdf --password=ASmartPassw0rd --decrypt directKinematicSolutionProtected.pdf directKinematicSolutionProtected.pdf
```

To encrypt:
```
qpdf --encrypt ASmartPassw0rd ASmartPassw0rd 256 -- directKinematicSolution.pdf directKinematicSolutionProtected.pdf
```