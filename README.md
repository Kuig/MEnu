# MEnu

A weekly menu planner (coming soon, just let me finish the readme first)

## Purpose

To provide a quick way to plan your meals without the need to spend cognitive resources on marginally important decisions. Possibly with a user interface helping those who don't speak computer science fluently.

## Features

- Available dishes and ingredients are listed in an Excel file that the user can freely edit;
- Ingredients can be combined according to user-defined criteria (somehow... almost... kind of);
- For each ingredient the user can set properties like
  - Does Alice like this? / Does Bob like this? (names can be customised)
  - Is this for all seasons or the cold/warm season?
  - Is this better for lunch or dinner?
- Avoid repeating the same meal twice in a row;
- Avoid repeating peculiar dishes more than once a week;
- Having pizza at least once per week, but not more than once, because the doctor told me (actually, the fact that "at least once a week is guaranteed" is enforced by statistical means: pizza has its own category and there aren't many categories);
- The user can set for all meals of all weekdays if Alice or Bob are present (so to pick only dishes they like);
- It works with a Tkinter GUI, but also as a console command (just run it to generate a menu using the week number as seed);
- The source code is an obscene mix of English and Italian.

## How it works
There are some "meal types" (think of them as *courses*, or *meal classes*) stored in the first sheet of the Excel file, each composed of a combination of ingredient types (ingredients and their type are stored in the second sheet of the Excel file).

At startup, the random seed is set to the current week number. Season (which is just *hot* or *cold*) is also initialised based on week number.
The first meal type of the week is picked at random, and then for all the remaining 13 meals, a new meal type is randomly selected avoiding repeating the same type twice in a row, and avoiding repeating the special type "pizza" more than once a week.

The actual meal is composed by picking ingredients at random based on the types defined in the picked meal type and considering some constraints, e.g. the season. To avoid repeating the same meal twice, some of its ingredients are removed from the available ingredients for the week.

The result is then printed in the console or on the GUI.

## How to use

First, you need to populate the Excel file with your favourite dishes/ingredients, then you just have to run the console version (that has default parameters) or the GUI version (which has quite self-explanatory parameters), so let's just dive into how the Excel file customization works.

The first sheet of the Excel file contains some meal types. A meal type consists of a collection of ingredient types (encoded as a string of single-char tokens) that need to be combined to produce a dish (sorry, one dish per meal).

You can use existing meal types, or create new ones. The ingredient type tokens can also be chosen at wish, they just have to match the tokens used in the second sheet of the Excel file (more on this later). Nevertheless consider that some tokens (such as t, p, u, z) have a special meaning: once an ingredient belonging to these types is consumed, it is removed from the available ingredients to avoid eating it again in the week. I will add a list of special tokens in the third sheet (the *settings* one) in the future, but for now enjoy the sick pleasure of hard-coded stuff.

The second sheet of the Excel file contains a list of ingredients. They have the following properties:
- name;
- ingredient type (single char);
- preferred season (-1: cold weather, 0: all year, 1: hot weather);
- preferred moment of the day (-1: lunch, 0: no preference, 1, dinner);
- Liked by person 0;
- Liked by person 1.

The last sheet contains some settings such as the names of persons 0 and 1, and a word that the user may want to show in the title bar of the GUI version.

Note that cells with **bold** text are not meant to be edited manually, while all the others can be freely modified, deleted or added.

Finally, note that the Excel file has some comments and conditional formatting to help you interpret the content.

## Hackability

The proposed architecture is highly hackable just by editing the Excel file:
- You can use the special case of pizza also for things that are not a pizza, such as "going to the restaurant" or "a thin disc of bread covered with tomato, mozzarella and pineapple". (JK, I'm not offended by pineapple on pizza);
- If you are not interested in having the "liked by person #" you can use those two fields to further characterize the ingredients (e.g. *proteins* and *carbohydrates*) and create weekly patterns based on that.
- You can use meal types with a fined degree of categorization in order to increase menu entropy/variety.

## Dependencies

This Python code requires Numpy, Pandas and PIL.

## How to deploy

Just keep all three files in the same directory. The Excel file should be named `Menu.xlsx`, but you can change this in the source code.

If you want to compile the standalone executable you need [PyInstaller](https://pyinstaller.org/en/stable/); once you installed it, just run

    pyinstaller Menu_gui.py --noconsole --onefile

Once you have the executable (which will be huge, due to obvious reasons), just keep it in the same directory as the Excel file.
