import re
from typing import Any, List, Optional

import matplotlib.pyplot as plt
import pandas as pd


class DataAnalyzer:
    def __init__(self, filepath: str):
        self.df = pd.read_csv(filepath)
        print("✅ Dataset loaded with columns:", list(self.df.columns))

    def _validate_columns(self, cols: List[str]) -> Optional[str]:
        for col in cols:
            if col and col not in self.df.columns:
                return f"❌ Column '{col}' not found."
        return None

    def help_text(self) -> str:
        return (
            "Available commands:\n"
            "- head(), tail(n), info(), describe(), shape, columns, dtypes, missing()\n"
            "- corr(), cov()\n"
            "- mean(col), median(col), mode(col), std(col), var(col), sum(col)\n"
            "- max(col), min(col), count(col), unique(col), nunique(col), value_counts(col)\n"
            "- groupby(col, agg, target)  e.g., groupby(department, mean, salary)\n"
            "- filter(col, op, value)     ops: ==, !=, >, <, >=, <=\n"
            "- plot(col), hist(col), scatter(x, y), box(col), heatmap()\n"
            "- help\n"
            "Examples: describe(), mean(age), scatter(age, salary), value_counts(department)"
        )

    def run(self, command: str) -> Any:
        command = command.strip()
        if not command:
            return "❌ Empty command"

        if command == "help":
            return self.help_text()

        match = re.match(r"(\w+)(?:\((.*)\))?$", command)
        if not match:
            return f"❌ Invalid command: {command}"

        func, argstr = match.groups()
        args = [] if argstr is None or argstr.strip() == "" else [a.strip() for a in argstr.split(",")]

        if func == "head":
            n = 5
            if args:
                try:
                    n = int(args[0])
                except ValueError:
                    return "❌ head(n) expects integer n"
            return self.df.head(n)
        if func == "tail":
            n = 5
            if args:
                try:
                    n = int(args[0])
                except ValueError:
                    return "❌ tail(n) expects integer n"
            return self.df.tail(n)
        if func == "info":
            import io
            buf = io.StringIO()
            self.df.info(buf=buf)
            return buf.getvalue()
        if func == "describe":
            return self.df.describe()
        if func == "shape":
            return self.df.shape
        if func == "columns":
            return list(self.df.columns)
        if func == "dtypes":
            return self.df.dtypes
        if func == "missing":
            return self.df.isna().sum()
        if func == "corr":
            return self.df.corr(numeric_only=True)
        if func == "cov":
            return self.df.cov(numeric_only=True)

        single_col_funcs = {
            "mean": lambda s: s.mean(),
            "median": lambda s: s.median(),
            "mode": lambda s: s.mode().tolist(),
            "std": lambda s: s.std(),
            "var": lambda s: s.var(),
            "sum": lambda s: s.sum(),
            "max": lambda s: s.max(),
            "min": lambda s: s.min(),
            "count": lambda s: s.count(),
            "unique": lambda s: s.unique(),
            "nunique": lambda s: s.nunique(),
            "value_counts": lambda s: s.value_counts(),
        }
        if func in single_col_funcs:
            if len(args) != 1:
                return f"❌ {func}(col) expects exactly one column"
            err = self._validate_columns([args[0]])
            if err:
                return err
            return single_col_funcs[func](self.df[args[0]])

        if func == "groupby":
            if len(args) != 3:
                return "❌ groupby(group_col, agg, target_col) required"
            group_col, agg, target_col = args
            err = self._validate_columns([group_col, target_col])
            if err:
                return err
            if agg not in {"mean", "sum", "min", "max", "count", "median", "std", "var"}:
                return "❌ Unsupported agg. Use mean,sum,min,max,count,median,std,var"
            return getattr(self.df.groupby(group_col)[target_col], agg)()

        if func == "filter":
            if len(args) != 3:
                return "❌ filter(col, op, value) required"
            col, op, value = args
            err = self._validate_columns([col])
            if err:
                return err
            series = self.df[col]
            try:
                value_coerced: Any = float(value) if series.dtype.kind in "biufc" else value
            except ValueError:
                value_coerced = value
            if op == "==":
                return self.df[series == value_coerced]
            if op == "!=":
                return self.df[series != value_coerced]
            if op == ">":
                return self.df[series > value_coerced]
            if op == "<":
                return self.df[series < value_coerced]
            if op == ">=":
                return self.df[series >= value_coerced]
            if op == "<=":
                return self.df[series <= value_coerced]
            return "❌ Unsupported operator. Use ==, !=, >, <, >=, <="

        if func == "plot":
            if len(args) != 1:
                return "❌ plot(col) expects one column"
            err = self._validate_columns([args[0]])
            if err:
                return err
            self.df[args[0]].plot()
            plt.title(f"Plot of {args[0]}")
            plt.xlabel(args[0])
            plt.tight_layout()
            plt.show()
            return f"📊 Plot displayed for {args[0]}"
        if func == "hist":
            if len(args) != 1:
                return "❌ hist(col) expects one column"
            err = self._validate_columns([args[0]])
            if err:
                return err
            self.df[args[0]].hist()
            plt.title(f"Histogram of {args[0]}")
            plt.xlabel(args[0])
            plt.tight_layout()
            plt.show()
            return f"📊 Histogram displayed for {args[0]}"
        if func == "scatter":
            if len(args) != 2:
                return "❌ scatter(x, y) expects two columns"
            err = self._validate_columns(args)
            if err:
                return err
            self.df.plot.scatter(x=args[0], y=args[1])
            plt.title(f"Scatter plot: {args[0]} vs {args[1]}")
            plt.tight_layout()
            plt.show()
            return f"📊 Scatter plot displayed for {args[0]} vs {args[1]}"
        if func == "box":
            if len(args) != 1:
                return "❌ box(col) expects one column"
            err = self._validate_columns([args[0]])
            if err:
                return err
            self.df[[args[0]]].plot.box()
            plt.title(f"Box plot of {args[0]}")
            plt.tight_layout()
            plt.show()
            return f"📊 Box plot displayed for {args[0]}"
        if func == "heatmap":
            corr = self.df.corr(numeric_only=True)
            import numpy as np
            fig, ax = plt.subplots(figsize=(6, 5))
            cax = ax.imshow(corr.values, cmap="viridis")
            ax.set_xticks(range(len(corr.columns)))
            ax.set_yticks(range(len(corr.index)))
            ax.set_xticklabels(corr.columns, rotation=90)
            ax.set_yticklabels(corr.index)
            fig.colorbar(cax)
            plt.title("Correlation heatmap")
            plt.tight_layout()
            plt.show()
            return "📊 Heatmap displayed"

        return f"❌ Function '{func}' not supported. Type 'help' for options."



