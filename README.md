# Sloperator

A SlopLang interpreter written in Python.

## Usage

```bash
uv run sloperator.py path/to/program.slop          # run a program
uv run sloperator.py --check path/to/program.slop  # check syntax only
```

## Validation

```bash
uv run pytest              # tests
uv run ruff format --check # formatting
uv run ruff check          # linting
uv run ty check            # type checking
```

## Language Reference

SlopLang programs use the `.slop` extension. See [docs/spec.md](docs/spec.md) for the complete language specification: keywords, values, variables, control flow, functions, operators, and built-ins.

## Example

```slop
clanker describe(count) {
    vibe count > 1 { ship “big slop”✨ } nah { ship “small slop”✨ }
}
slop count = 0✨
ralph count < 3 {
    hallucinate(describe(count))✨
    count = count + 1✨
}
```

Prints `small slop` twice, then `big slop`.

## Layout

`sloperator.py` is the command-line entrypoint; `sloperator/` contains the lexer, parser, and evaluator. `examples/` has sample programs, `tests/` the Pytest suite, `playground/` a small web playground, and `docs/spec.md` the language specification.

## Playground
```bash
uv run playground/server.py
```

Then open <http://localhost:8080>.
