# DFS
Finding the best Daily Fantasy Sports lineup by solving a multivariate optimization problem from a collection of player metadata scraped from Draft Kings and other fantasy sports providers. 

Gather required packages 
```python
pip install -r requirements.txt
``` 
Run
```python
python main.py <filepath> <bool> <teams>
```  

	- <filepath> has the path to the csv that holds the salary data. 
    	- Ex. DKSalaries.csv
	
	- <bool> controls team array 
    	- Ex. bool = True --> remove players belonging to "teams" array, 
		      bool = False --> include every player
	
	- <teams> is the array of team abbreviations whose players you want to remove
	
		- Ex. ["GB", "CHI", "HOU", "NO", "DEN", "OAK"] 

