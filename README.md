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
# Example Data, Continious and Sequential
e.g.
```bash
cd to/folder/like/GitHub/Radiography
python process_radiography_pchao.py example_data -vv --mode c --inc 5 --start 1000 --end 2000  --medfilt 2
python process_radiography_pchao.py example_data -vv --mode s --inc 5 --seq_fram 10 --start 1000 --end 2000  --medfilt 2
```

## Continious vs Sequential
Adding the flags:
``` 
--mode c
--mode s
```
- Continous will use the **first** frame as the background that will be divided by the remaining frames.

For example: 100 images, the resulting 99 images (not including the first image) will be f_n/f_1 for each nth image

- Sequential will use the **previous** frame (distance from current frame specified by --seq_frames flag) as the background that will be divided by the remaininng frames.

For example: 100 images, the resulting 90 images (not including the first 10 image) will be f_n/f_{n-10} for each nth image. In this case we are using a sequential increment of 10, use the --seq_frames flag to modify during processing.

Specify the number of frames bewteen sequential with the increment frames flag
```
--inc number_of_frames_to_increment
```


