Git Bash command to get lines of code  
`git ls-files | grep -P ".*(py|css)" | xargs wc -l`