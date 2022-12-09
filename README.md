# SMART Implementation Prototype
Prototype implementation of Sequential Multiple Assignment Randomized Trials (SMART)

#### TODO
* ~store answers~
* ~input validation [DONE until validating custom questions]~
* ~store subject's progress / config in db~
  * ~log in~
  * ~log out~
* ~incorporate subject ID? => keep from retaking survey (integration REDCap?)~
* adding questions
  * only 1 primary question?
  * likert scale, text box
  * change labels on likert scale (keep scale point same)
* server-side validation
  * if user messes with values in vignette
  * authenticate REDCap token (account for false studies)
* keep from breaking (invalid study id, etc)
* show amazon code after survey
* add randomization table (to keep track of randomizations in case we lose tree)?
* UI
  * fix misclick
  * refresh entering num levels
* efficiency