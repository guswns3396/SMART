# SMART Implementation Prototype
Prototype implementation of Sequential Multiple Assignment Randomized Trials (SMART)

#### TODO
* store answers
* ~input validation [DONE until validating custom questions]~
* ~store subject's progress / config in db~
* ~incorporate subject ID? => keep from retaking survey (integration REDCap?)~
* ask your own question
* only 1 primary question?
* server-side validation
* keep from breaking (invalid study id, etc)
* show amazon code after survey
* ~log in~
* ~log out~
* authenticate REDCap token (account for false studies)

make parse_param & make_tree staticmethods
call static methods to get lvls, root
store lvls, root, p, id in table

how to connect nodes (which contain scenario, qset, count) to answers??
* make tree through tables
* use level / question num & filter
  * alter get_vigentte_params

keep tree for count & questions/scenarios separate?
when user answers, just note the level & question
questions differ between levels, same within level