# dump2data
cli ультилита для парсинга данных из `.sql` дампов в `.csv`

-----

## Использование
### CLI

```bash
python dump2data.py -i <path_to_dump> -od <output_dir>
```

-----

## Flags
  * **`-i, --input`**: путь до `.sql` дампа
  * **`--seperator`**: разделитель .csv, по умолчанию: `,`.
  * **`-t, --tables`**: сохранить только определенные таблицы, пример: `-t users,orders,products`.
  * **`-od, --outputdir`**: путь куда сохранять .csv файлы `./`.
  * **`-op, --outputprefix`**: добавить префикс к файлам `-op dbname_`.