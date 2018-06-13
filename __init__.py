__version__ = "0.2.5"
__doc__ = " 
	fuctions you can use in mainpage of program :
		
	1. add todo: add new contents
	2. list todo: show contents with filter.
		      Also, you can manage categories here.
	3. modify todo: modify contents
	4. quit : quit the program.
	
	and special commands for more imformation:
		
	todolist --version: show which version is installed
	todolist --manual: show full manual with detailed imformation
"
__man__ = "

                   Open-Source-ToDo-List Manual
NAME	
	
	todo -- manage todo lists in CLI

SYNOPSIS
	
	'todolist' in the command line to run

DESCRIPTION
	
	The Open-Source-ToDo-List is schedule management tool for CLI environment  made of Python3 
	and uses SQLite3 data base
	
	In addition, this program has 5 data types.

	id : Index of data, automatically assigned by system.
	what : Name of task you want to record
	due : due date of task
	category : category of task
	finished : whether the task is finished or not, automatically assigned as false  
	 

	After running There are 4 main functions you can use.

	The things you can run by typing each number:
	
		1 : Add todo: Add new contents. Input what, due, category.
			      id and finished are automatically assigned.
		
		2 : List todo : Show the list of tasks with filter for each number.
				
				1.list_all : show all of contents
				2.list_finished : show only finished contents
				3.list_by_category : show contents which has category and sorted by category
				4.category edit
		2-4 : Category options
				
				1.add_category : add new category
				2.del_category : delete existing category
				3.list_category : show existing categories 
				4.return : go back to previous menu 
		
		3 : Modify todo :Modify the already recorded contents.
				 Can change its name, due date and category.
				Also can determine it’s finished or not.
				
				1.modify_contents : get id of data, and modify corresponding data's what and due.
				2.delete_todo : get id and delete the corresponding data
				3.mark_as_finished : get id and determine corresponding task is finished or not
				4.return : go back to previous menu
				
	
		4 : Quit: Quit, Close the Program

COMMANDS

	special commands offered for convenience

	 * todolist —-version : Show which version is installed 
	 
	 * todolist —-help : Show more information about program



HISTORY

	0.1.1 : May 23, 2018. First released test version
	0.2.0 : May 23, 2018. Minor bug fix
	0.2.6 : June 03, 2018 Major bug fix

BUGS

	No known bugs yet

License

		MIT License

	Copyright (c) 2018 Kang MinSeok

	Permission is hereby granted, free of charge, to any person obtaining a copy
	of this software and associated documentation files (the "Software"), to deal
	in the Software without restriction, including without limitation the rights
	to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
	copies of the Software, and to permit persons to whom the Software is
	furnished to do so, subject to the following conditions:

	The above copyright notice and this permission notice shall be included in all
	copies or substantial portions of the Software.

	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
	IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
	FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
	AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
	LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
	OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
	SOFTWARE.

"
