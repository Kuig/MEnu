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

The result is then printed in the console or on the Gui.

## How to use

## Hackability

## Dependencies

## How to deploy
