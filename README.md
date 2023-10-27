# War and Peace Categorization Program

This program reads a large text file "War and Peace" by Tolstoy and two text files with word lists, one for "war-terms" and one for "peace-terms". The program categorizes the chapters of the book as war-related or peace-related based on the density of war and peace terms in each chapter.

## Notes

This program was created for a functional programming course at the FH Technikum Wien. The program was created using functional programming paradigms.

## Input Requirements

The program requires the following inputs:

- A large text file "War and Peace" by Tolstoy
- Two text files with word lists, one for "war-terms" and one for "peace-terms"

## Output

The program outputs the categorization of the chapters of the book as war-related or peace-related based on the density of war and peace terms in each chapter.

## Algorithm

The program categorizes the chapters as war-related or peace-related by counting the occurrences of war and peace terms in each chapter and calculating their relative density. If the density of war terms is higher than the peace density, the chapter is characterized as a war chapter.

## How to Run

To run the program, follow these steps:

1. Install [Python](https://www.python.org/downloads/) (version 3.6 or higher)
2. Clone this repository to your local machine
3. Navigate to the repository directory in your terminal or command prompt
4. Run the following command: `python main.py`

Note: The program assumes that the input files are located in the `in` folder.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


