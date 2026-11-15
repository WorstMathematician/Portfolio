# Spark Execution Study

A PySpark lab project exploring how Spark plans and executes DataFrame workloads. The notebook demonstrates lazy evaluation, partitioning, narrow and wide transformations, shuffle boundaries, execution plans, Jobs/Stages/Tasks, caching, and practical optimization choices.

## What the notebook shows

- A lazy DataFrame transformation chain and the action that triggers execution
- Partition counts and balanced record distribution across four partitions
- A physical plan with `Exchange hashpartitioning`, indicating a shuffle boundary
- Spark UI observations: two `grouped.show()` executions produced job pairs 3/4 and 15/16 in the same reused job group
- A caching comparison with five million matching records; the repeated cached count was slightly faster in this run
- Recommendations focused on early filtering/projection, avoiding large driver collections, checking exchanges, and caching reused data

## Run

Open `Spark_Lab4.ipynb` in Jupyter with PySpark installed. Runtime measurements and Spark job IDs are environment-specific; the notebook retains the recorded run outputs for context.

## Public-copy notes

This copy removes embedded Spark UI screenshots and replaces the local Spark UI URL. The original screenshots include local machine or temporary notebook paths, so they are not included in this public version. Assignment handout material and the PDF export are also omitted; use the notebook as the project artifact and regenerate a PDF from it if needed.
