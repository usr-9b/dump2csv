# dump2data
extract data from .sql dumps to .csv files

-----

## Usage
### CLI

```bash
python dump2data.py -i <path_to_dump>
```

-----

## Flags
  * **`-i, --input`**: path to your `.sql` file!
  * **`--seperator`**: csv separator. Default is `,`.
  * **`-t, --tables`**: list of tables you want to extract, e.g., `-t users,orders,products`.
  * **`-od, --outputdir`**: dir to save the csv files. Default is `./`.
  * **`-op, --outputprefix`**: add a prefix to the output filenames, like `-op dbname_`.