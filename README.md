# gorg
This project arose from frustrations with (and deep enthusiasm for) Emacs Org-Mode, which is a system I've been 
using for several years as a personal information manager.

Basic ideas: 
  - text-based information is stored in chunks
  - chunks are linked to each other arbitrarily, using a directed graph structure
  - this graph involves one or two fundamental link types, with the option to create others
  - this network of data chunks is stored serially, using YAML (a JSON persistence will also be implemented eventually)
  - editing this network amounts to manipulating a live data structure 
    - this is a key distinction from Org-Mode, in which every editing command is an operation on a formatted text file
  - this data structure is presented to the user through nestable, composable Interfaces
  - Interfaces consist of Gates, which are regions of a text buffer with a particular KeyMap attached to them
  - Interfaces can be specified in a config file in advance
  - KeyMaps simply pair key input sequences with commands
    - users can arbitrarily script new commands and reference them in KeyMap definitions, which are then referenced
    by Gate definitions, which are then referenced by Interface definitions, etc
    
I'm writing this in Python, because that's what I know.  It's probably not the best language for it - I tried for a while
in Elisp but eventually ran out of features.  I think a more advance Lisp would probably be ideal.
    
