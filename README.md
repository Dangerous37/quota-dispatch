# Quota Dispatch

Replay a burst of jobs against independent tenant rate limits. Inspect the exact dispatch sequence and wait time before rolling out a queue configuration.

## Run locally

Use Python 3.12. The project uses the standard library. From the repository root:

```sh
python cli.py example.json
python -m unittest -v
```

The included example is synthetic. Pass a different UTF-8 JSON file to inspect your own input. The command prints JSON to stdout. Invalid input returns status 2 and an explanation on stderr. See [CONTRACT.md](CONTRACT.md) for input fields and interpretation.

## Operational limits

Discrete capacity planning simulator. No live worker, clock drift, distributed leases or sliding-window quota semantics. The simulator jumps across idle periods.

## Resumen en español

Simula cuotas distintas por cliente y cuantifica la espera que introduce una ráfaga de trabajos.
