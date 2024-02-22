# MEnu
A weekly menu planner (coming soon, just let me finish the readme first)

## Purpose
To provide a quick way to plan your meals without the need to spend cognitive resources on marginally important decisions. Possibly with a user interface helping those who don't speak computer science fluently.

## Features
- Available dishes and ingredients are listed in an Excel file that the user can freely edit (please don't edit cells **bold** text);
- Ingredients can be combined according to user-defined criteria (somehow... almost... kind of);
- For each ingredient the user can set properties like
  - Does Alice like this? / Does Bob like this? (names can be customised)
  - Is this for all seasons or the cold/warm season?
  - Is this better for lunch or dinner?
- Avoid repeating the same meal twice in a row;
- Avoid repeating peculiar dishes more than once a week;
- Avoid not having pizza at least once, but not more than once, because my mum told me that (actually, the fact that at least once a week is guaranteed is enforced by statistical means: pizza has its own category);
- The user can set for all meals of all weekdays if Alice or Bob are present (so to pick only dishes they like);
- It works with a Tkinter GUI, but also as a console command (just run it to generate a menù using the week number as seed);
- The source code is an obscene mix of English and Italian.

## How it works
There are some "meal types" (think of them as *curses*, or *meal classes*) stored in the first sheet of the Excel file, each composed of a combination of ingredient types (ingredients and their type are stored in the second sheet of the Excel file).

At startup, the random seed is set to the current week number of the year. Season (which is just *hot* or *cold*) is also initialised based on week number.
The first meal type of the week is picked at random, and then for all the remaining 13 meals, a new meal type is randomly selected avoiding repeating the same type twice in a row, and avoiding repeating the special type "pizza" more than once a week.

The actual meal is composed by picking ingredients at random based on the types requested by the picked meal type and considering some constraints, e.g. the season. To avoid repeating the same meal twice, some of its ingredients are removed from the available ingredients for the week.

The result is then printed in the console or on the GUI.

## How to use
First, you need to populate the Excel file with your favourite dishes/ingredients, then you just have to run the console version (that has default parameters) or the GUI version, which has quite self-explanatory parameters, so let's just dive into how the Excel file customization works.

The first sheet of the Excel file contains some meal types. A meal type consists of a collection of ingredient types (encoded as a string of single-char tokens) that need to be combined to produce the dish (sorry, one dish per meal).

You can use existing meal types, or create new ones. The ingredient type tokens can also be chosen at wish, they just have to match the tokens used in the second sheet of the Excel file (more on this later). Nevertheless consider that some tokens (such as t, p, u, z) have a special meaning: once an ingredient belonging to these types is consumed, it is removed from the available ingredients to avoid eating it again in the week.

The second sheet of the Excel file contains a list of ingredients. They have the following properties:
- name;
- ingredient type (single char);
- preferred season (-1: cold weather, 0: all year, 1: hot weather);
- preferred moment of the day (-1: lunch, 0: no preference, 1, dinner);
- Liked by person 1;
- Liked by person 2.

The last sheet contains some settings such as the names of persons 1 and 2, and a word that the user may want to show in the title bar of the GUI version.

## Hackability

## Dependencies

## How to deploy
