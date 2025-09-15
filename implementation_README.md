A Python utility that reads a CSV file, applies a set of normalization rules, and writes the cleaned output to a new CSV file.  

## Features

- ✅ Convert **FullName** to uppercase  
- ✅ Zero-pad **ZIP codes** to 5 digits  
- ✅ Convert **Timestamp** from US/Pacific → US/Eastern in RFC3339 format  
- ✅ Convert **FooDuration** and **BarDuration** from `HH:MM:SS.MS` → total seconds  
- ✅ Replace **TotalDuration** with `FooDuration + BarDuration`  
- ✅ Ensure **Address** and **Notes** fields are valid UTF-8 (replace invalid chars with ` `)  
- ✅ Skip invalid rows and log warnings to `stderr`  

---

## Requirements

- Python **3.9+**
- Dependencies listed in `requirements.txt`:
  - `python-dateutil`
  - `tzdata` (needed for timezone support on Windows)

Install dependencies with:

bash
py -m pip install -r requirements.txt
`

---

## Usage

### 1. Clone / copy the project

bash
git clone https://github.com/Tomoti432/tom-oti-truss-interview-assessment.git

cd tom-oti-truss-interview-assessment


### 2. Run the tool

Using **stdin/stdout redirection**:

bash
py ./normalizer.py < ./sample.csv > ./output.csv


This will:

* Read `sample.csv`
* Normalize the rows
* Write the result to `output.csv`

### 3. Example

Input (`sample.csv`):

csv
Timestamp,Address,ZIP,FullName,FooDuration,BarDuration,TotalDuration,Notes
4/1/11 11:00:00 AM,123 4th St,94121,John Smith,1:23:32.123,1:32:33.123,0,Test


Output (`output.csv`):

csv
Timestamp,Address,ZIP,FullName,FooDuration,BarDuration,TotalDuration,Notes
2011-04-01T14:00:00-04:00,123 4th St,94121,JOHN SMITH,5012.123,5553.123,10565.246,Test


---

## Notes

* If your CSV headers differ (e.g. `Zip` vs `ZIP`), update the script or use the case-insensitive version.
* Invalid rows will be skipped and logged as warnings.

