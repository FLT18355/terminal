" SPF syntax highlighting for Neovim
" Based on mcfunc.flt syntax

if exists("b:current_syntax")
  finish
endif

" Comments
syn match spfComment "^#.*$"

" Special commands
syn match spfDef "\*def("
syn match spfSleep "\*sleep("
syn match spfLoop "\*loop("
syn match spfFunction "^function "

" Variable references
syn match spfVarRef "\\\*{[^}]*}"

" Parentheses and brackets
syn match spfParen "[()]"
syn match spfBracket "[\[\]]"
syn match spfBrace "[{}]"

" Numbers
syn match spfNumber "\<\d\+\>"
syn match spfFloat "\<\d\+\.\d\+\>"

" Separators
syn match spfSemicolon ";"

" Minecraft commands
syn keyword spfCommand say execute playsound tp give effect particle title tellraw fill setblock clone summon kill gamemode weather time difficulty xp enchant clear replaceitem spreadplayers testfor testforblock testforblocks scoreboard tag team stopsound camera dialogue lesson code wb locate structure reload

" Highlighting
hi def link spfComment Comment
hi def link spfDef Keyword
hi def link spfSleep Keyword
hi def link spfLoop Keyword
hi def link spfFunction Keyword
hi def link spfVarRef Identifier
hi def link spfParen Delimiter
hi def link spfBracket Delimiter
hi def link spfBrace Delimiter
hi def link spfNumber Number
hi def link spfFloat Float
hi def link spfSemicolon Delimiter
hi def link spfCommand Statement

let b:current_syntax = "spf"
