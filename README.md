# Radiography
Codes relating to x-ray radiography post processing algorithms


# How to get started
Begin by downloading the python script and the folder of example files

```git
git clone https://github.com/shahaniRG/Radiography.git
```

Install dependencies as needed.

# Using the code
Run the code in bash (or anaconda prompt) 

``` bash
python process_radiography_pchao.py path/to/example_data
```

# Help
To play with the different processing parameters, please see -h for details by running
```bash
python process_radiography_pchao.py -h

```

e.g.
```bash
python process_radiography_pchao.py path/to/example_data -vv --start 1000 --end 2000 --inc 5 --medfilt 2
```

## Continious vs Sequential
Adding the flags:
``` 
--type c
--type s
```
- Continous will use the **first** frame as the background that will be divided by the remaining frames.
- Sequential will use the **previous** frame as the background that will be divided by the remaininng frames.

Specify the number of frames bewteen sequential with the increment frames flag
```
--inc number_of_frames_to_increment
```


