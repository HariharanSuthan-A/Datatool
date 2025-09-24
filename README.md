# datatool

Lightweight CSV data analyzer with REPL and plotting.

## Install

- Local editable install (dev):
```bash
python -m venv .venv && source .venv/bin/activate
pip install -e .
```

- From GitHub (replace with your repo URL):
```bash
pip install git+https://github.com/your-user/your-repo.git
```

## CLI
```bash
datatool --file data.csv --cmd "describe()"
datatool -f data.csv --repl
```

## Library
```python
from datatool import DataAnalyzer
analyzer = DataAnalyzer("data.csv")
print(analyzer.run("describe()"))
print(analyzer.run("scatter(age, salary)"))
```

## Commands
- head(), tail(n), info(), describe(), shape, columns, dtypes, missing()
- corr(), cov()
- mean(col), median(col), mode(col), std(col), var(col), sum(col)
- max(col), min(col), count(col), unique(col), nunique(col), value_counts(col)
- groupby(col, agg, target)
- filter(col, op, value)
- plot(col), hist(col), scatter(x, y), box(col), heatmap()
