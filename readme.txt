
	-----------------------------------------
	--- XXX: xxxxxxx xxxxxxxxxx xxxxxxxxx ---
	-----------------------------------------

Requirements: 
	Python		 	3.6
	packages:
	  - Numpy		1.18.4
	  - z3-solver	4.8.8.0

The purpose of XXX is to generate random test case from a template file describing 
the data model. XXX provides a command line interface. When launched, type "help" 
in the prompt to get a list of the available commands.
Type "help <command_name> to get specific info on a command.

Use the "display all" command to see the current settings. The "set" command can 
be used to change the settings.

Typical usage (more details in the video):
	- Step 0: cd path/XXX/src
	- Step 1: Launch XXX: python3 Xxx.py
	- Step 2: In XXX prompt: parse_template
	- Step 3: Find your test cases in the folder "experiment"

Contents of the repository:
	- src: the source code and the default settings
	- templates : The template format specification (DTD and BNF) and a set of
	  templates including:
		* the running example of the ISSRE paper (oz_reduced_paper.template)
		* the complete Oz example (oz_complete.template)
		* the tax payer example (tax_payer_paper.template)
		* and many more
	- a demonstration video
	- the transcript of the video

This software is released under CeCILL-B license (similar to BSD, without copyleft) 
with Copyright 2019.



		                 ______			
	        	        /     /\
		               /     /##\
		              /     /####\
	        	     /     /######\
		            /     /########\
		           /     /##########\
	        	  /     /#####/\#####\
		         /     /#####/++\#####\
		        /     /#####/++++\#####\
		       /     /#####/\+++++\#####\
		      /     /#####/  \+++++\#####\
		     /     /#####/    \+++++\#####\
		    /     /#####/      \+++++\#####\		
		   /     /#####/        \+++++\#####\
		  /     /#####/__________\+++++\#####\
		 /                        \+++++\#####\
		/__________________________\+++++\####/
		\+++++++++++++++++++++++++++++++++\##/
		 \+++++++++++++++++++++++++++++++++\/
		  ``````````````````````````````````

