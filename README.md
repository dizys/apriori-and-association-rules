# Frequent Item Set and Association Rule Generator

Basic algorithm implementation to identify frequent item sets and mine association rules. Including Apriori.

## Apriori

### Help

```bash
$ python src/apriori.py --help
Usage: python apriori.py FILENAME [OUTPUT_FILENAME] [SUPPORT_THRESHOLD]

FILENAME             File path for data input
OUTPUT_FILENAME      File path for output (default "apriori_output.txt")
SUPPORT_THRESHOLD    Support threshold when generating frequent set (default "0.5")
```

### Example

```bash
$ python src/apriori.py sample/data_set.dat out/apriori_output.txt 0.5 
```

## Association Rule

Uses the output of Apriori as its input.

### Help

```bash
$ python src/association_rule.py --help
Usage: python association_rule.py FILENAME [OUTPUT_FILENAME] [CONF_THRESHOLD]

FILENAME          File path for data input
OUTPUT_FILENAME   File path for output (default "association_rule_output.txt")
CONF_THRESHOLD    Confidence threshold when generating rules (default "0.4")
```

### Example

```bash
$ python src/association_rule.py out/apriori_output.txt out/association_rule_output.txt 0.4 
```

## License

MIT, see the [LICENSE](/LICENSE) file for details.