# To-Do-Widget

This is a multithreaded Windows 10 desktop widget that functions similar to a to-do list. It uses a
sqlite database as a backend to store all the tasks and corresponding due dates. On the day of the 
due date provided by any task, the program sends a desktop notification to the user, reminding them 
that the task is due.

## Installation

The only requirement needed is the **win10toast** python library.

```bash
pip install win10toast
```

## Usage

To use the widget, simply download the **widget.py** file. Then open your command prompt/powershell
and traverse to the file location of **widget.py**. Then run using the following command in your terminal

```python
pythonw.exe widget.py
```

## License
[MIT](https://choosealicense.com/licenses/mit/)