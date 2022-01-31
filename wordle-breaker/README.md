# Game Helpers

## Wordle Helper
Not much Fancy but gets the work done. Slight raw and interactive, Will show you suggestions for your next move,
```buildoutcfg
## Input format and conditions
1. ith possible character(C), its guarantee of occurring there(P)
2. If ith character(C) is 0, it means not sure about this position
3. If for any ith position C is given but P is given as 0, it means, I know C will occur but not sure if it occurs in this position
4. If for any ith position C is given but P is given as 1, it means, I know C will definitely occur in this position
5. If for any ith position C is given but P is given 2, it means, I know C will never occur in this string
6. Length of input is always 10  length
```

```buildoutcfg

Ex: P1A2K0E0R0:
- P will occur in 1st position, A will not occur in this string, K E R will occur in some position in this string

```

### Official Game Link
- [Wordle](https://www.powerlanguage.co.uk/wordle/)

### Resources
- [https://github.com/first20hours/google-10000-english](https://github.com/first20hours/google-10000-english)
- [https://word.tips/five-letter-words/](https://word.tips/five-letter-words/)

## Nerdle Helper
Not much Fancy but gets the work done. Slight raw and interactive, Will show you suggestions for your next move,
```buildoutcfg
## Input format and conditions
1. ith possible character(C), its guarantee of occurring there(P)
2. If ith character(C) is X, it means not sure about this position
3. If for any ith position C is given but P is given as 0, it means, I know C will occur but not sure if it occurs in this position
4. If for any ith position C is given but P is given as 1, it means, I know C will definitely occur in this position
5. If for any ith position C is given but P is given 2, it means, I know C will never occur in this string
6. Length of input is always 16  length
```

```buildoutcfg

Ex: 5162-14102=11162:
- 5 will occur in 1st position
- 6 will never occur in this solution 
- '-' will occur in 3rd position
- 4 will occur in 4th position 
- 0 will never occur in this solution 
- '=' will occur in 6th position 
- 1 will occur in 7th position
- 6 will never occur in this solution
```
### Solution Logic
```buildoutcfg
- Uses backtrack generation 
- Postfix conversion, mathematical string evaluation
- Simple Constraint matching with positional occur/maps, will occur somewhere/domain knowledge and will never occur/invalid characters
```

### Official Game Link
- [Nerdle](https://nerdlegame.com/)