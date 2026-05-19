# type:ignore
from pathlib import Path

import click
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

CODE_NAMES = {
    "N801": "Class name should use CapWords convention",
    "N802": "Function name should be lowercase",
    "N803": "Argument name should be lowercase",
    "N806": "Variable in function should be lowercase",
    "N815": "Variable in class scope should not be mixedCase",
    "N816": "Variable in global scope should not be mixedCase",
}


@click.command()
@click.option(
    "-o",
    "--output",
    type=click.Path(writable=True, dir_okay=False, path_type=Path),
    default=None,
    help="Output file (defaults to <INPUT>.pdf)",
)
@click.argument(
    "input",
    type=click.Path(exists=True, readable=True, dir_okay=False, path_type=Path),
)
def main(
    output: Path | None,
    input: Path,
) -> None:
    output = output or input.with_suffix(".pdf")

    df = pd.read_csv(
        input,
        dtype={
            "id": str,
            "code": str,
        },
    )

    df = df[df["code"] != "invalid-syntax"]
    df["name"] = df["code"].map(lambda x: CODE_NAMES.get(x, f"Unknown code ({x})"))
    summary = df.groupby(["id", "name"]).size().reset_index(name="count")

    plt.figure(figsize=(5.5, 3.25))
    sns.set_theme(style="whitegrid", context="paper")
    sns.ecdfplot(data=summary, x="count", hue="name", palette="Dark2")
    plt.ylabel("Proportion of Projects (F(x))")
    plt.xlabel("Violation Count per Project (x)")
    sns.move_legend(
        plt.gca(),
        "lower right",
        title="Code",
        # fontsize="x-small",  # Scales based on your context (paper)
        # title_fontsize="small",
        # frameon=True,
    )
    plt.tight_layout()
    plt.savefig(output.with_name(f"{output.stem}_ecdf{output.suffix}"))
    plt.close()


if __name__ == "__main__":
    main()
