Action Space

| ID | Action | Argument | Description | 
|----|--------|----------|-------------|
| 1  | Add command composiiton | int location, int option | add stuff like &, ; \|\| | 
| 2  | Add comment | int location | Add a comment operator # | 
| 3  | Add (,) | int location, int option | Adds a ( ,) |
| 4  | Add {,} | int location, int option | Adds a { ,} |
| 5  | Add [,] | int location, int option | Adds a [ ,] |
| 6  | Add :, $  | int location, int option | Adds a : |
| 7  | Include a new command | int location, int option | add one of the commands 
 
Can maybe include block comments hack as well: 
```bash
: << "COMMENT" 
this is a multline
block
comment 
COMMENT
echo "HeHeHeHe"
# Normal Comment
```

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
