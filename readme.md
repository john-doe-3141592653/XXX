--- XXX: xxxxxxx xxxxxxxxxx xxxxxxxxx ---
===============================

The purpose of XXX is to generate random test cases from a template file describing the data model. XXX provides a command line interface. When launched, type "help" in the prompt to get a list of the available commands.
Type "help <command_name>" to get specific info on a command.


Requirements:
-----------
 * Python 3.6
Packages:
 * Numpy 1.18.4
 * z3-solver 4.8.8.0

Installation:
-----------
 follow the video or use the transcript after installing python 3.6
 
 
 Typical usage: 
-----------
 (more details in the [video]([XXX/XXX_tutorial_x265.mp4 at master · john-doe-3141592653/XXX · GitHub](https://github.com/john-doe-3141592653/XXX/blob/master/XXX_tutorial_x265.mp4)))
 

```
cd path/XXX/src
python3 Xxx.py         %launch XXX
display all            %visualize the settings
parse_template         %parse the template
generate               %generate test cases
cat ../experiment/test_case_0/test_case_0.test_case %visualize the result
```

Contents of the repository:
-----------

 1. src: the source code and the default settings
 2. templates : The template format specification (DTD and BNF) and a set of
 templates, including:
 	* the running example of the ISSTA paper (oz_reduced_paper.template)
 	* the complete Oz example (oz_complete.template)
 	* the tax payer example (tax_payer_paper.template)
 	* and many more
 3. a demonstration video
 4. the transcript of the video
 5. the link to the paper results
 
 
This software is released under CeCILL-B license (similar to BSD, without copyleft) 
with Copyright 2019.
 ______
 
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

