# pnml_from_place
This project is aiming at using place information generates Petri Net (under the PNML standard, and visualized by ProM). <br></br>
The original idea is from prof Wil van der Aalst's paper. Using place's input and output information define a Petri Net. This project is the implementation. You could only provide places, the rest of transition, arc will be auto generated. <br></br>
And, ProM is no need for position information, so this project has no function about position <br></br>
Such a place array likes <br></br>
```
places = [{'input': ['a'], 'output': ['b']}, {'input': ['a','b'], 'output': ['c']},
{'input': ['c'], 'output': ['d']}, {'input': ['b'], 'output': ['d']}]
```
It will generate a string for pnml. And put it into ProM will looks like below<br></br>
<img align="right" src=https://raw.githubusercontent.com/FrankBGao/pnml_from_place/master/example.JPG >
The usage of this project is showed as below
```
pnml_string = gain_pnml('example',places)
pnml_file = open('example.pnml', 'w')
pnml_file.write(pnml_string)
